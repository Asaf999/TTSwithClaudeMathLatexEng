#!/usr/bin/env python3
"""
MathSpeak Anki Integration
==========================

Integrate MathSpeak with Anki for audio-enhanced mathematical flashcards.
"""

import json
import sqlite3
import zipfile
import tempfile
import asyncio
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import hashlib
import shutil

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager


class AnkiMathSpeakIntegration:
    """Integrate MathSpeak with Anki cards"""
    
    def __init__(self, anki_collection_path: Optional[str] = None, 
                 prefer_offline: bool = False):
        """
        Initialize Anki integration
        
        Args:
            anki_collection_path: Path to collection.anki2 file
            prefer_offline: Use offline TTS engines
        """
        self.collection_path = self._find_anki_collection(anki_collection_path)
        self.media_dir = self.collection_path.parent / "collection.media"
        
        # Initialize MathSpeak
        self.voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=self.voice_manager,
            enable_caching=True,
            prefer_offline_tts=prefer_offline
        )
        
        # Audio settings
        self.audio_format = "mp3"
        self.audio_prefix = "mathspeak_"
        
    def _find_anki_collection(self, custom_path: Optional[str] = None) -> Path:
        """Find Anki collection.anki2 file"""
        if custom_path:
            path = Path(custom_path)
            if path.exists():
                return path
            else:
                raise FileNotFoundError(f"Anki collection not found at: {custom_path}")
        
        # Common Anki paths
        possible_paths = [
            # Linux
            Path.home() / ".local/share/Anki2/User 1/collection.anki2",
            # macOS
            Path.home() / "Library/Application Support/Anki2/User 1/collection.anki2",
            # Windows
            Path.home() / "AppData/Roaming/Anki2/User 1/collection.anki2",
        ]
        
        for path in possible_paths:
            if path.exists():
                print(f"Found Anki collection at: {path}")
                return path
        
        raise FileNotFoundError(
            "Could not find Anki collection. Please specify the path manually."
        )
    
    def extract_math_from_cards(self, deck_name: Optional[str] = None,
                               tag_filter: Optional[str] = None) -> List[Dict]:
        """
        Extract mathematical expressions from Anki cards
        
        Args:
            deck_name: Filter by deck name
            tag_filter: Filter by tag (e.g., "math", "calculus")
            
        Returns:
            List of cards with math expressions
        """
        conn = sqlite3.connect(self.collection_path)
        cursor = conn.cursor()
        
        # Get cards with notes
        query = """
        SELECT n.id, n.flds, n.tags, c.did, d.name
        FROM notes n
        JOIN cards c ON c.nid = n.id
        JOIN decks d ON c.did = d.id
        WHERE 1=1
        """
        
        params = []
        
        if deck_name:
            query += " AND d.name LIKE ?"
            params.append(f"%{deck_name}%")
        
        if tag_filter:
            query += " AND n.tags LIKE ?"
            params.append(f"%{tag_filter}%")
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cards_with_math = []
        
        # LaTeX pattern matchers
        latex_patterns = [
            r'\$([^$]+)\$',  # Inline math $...$
            r'\$\$([^$]+)\$\$',  # Display math $$...$$
            r'\\\[([^\]]+)\\\]',  # Display math \[...\]
            r'\\\(([^\)]+)\\\)',  # Inline math \(...\)
            r'\[latex\]([^\[]+)\[/latex\]',  # Anki LaTeX tags
        ]
        
        for note_id, fields, tags, deck_id, deck_name in results:
            # Parse fields (front and back of card)
            field_list = fields.split('\x1f')
            
            for i, field in enumerate(field_list):
                # Find all math expressions in field
                math_expressions = []
                
                for pattern in latex_patterns:
                    matches = re.findall(pattern, field, re.DOTALL)
                    math_expressions.extend(matches)
                
                if math_expressions:
                    cards_with_math.append({
                        'note_id': note_id,
                        'deck_name': deck_name,
                        'tags': tags,
                        'field_index': i,
                        'field_content': field,
                        'math_expressions': math_expressions,
                        'original_field': field
                    })
        
        conn.close()
        print(f"Found {len(cards_with_math)} fields with mathematical expressions")
        return cards_with_math
    
    async def generate_audio_for_card(self, card: Dict, 
                                     output_dir: Optional[Path] = None) -> List[str]:
        """
        Generate audio files for mathematical expressions in a card
        
        Args:
            card: Card dictionary from extract_math_from_cards
            output_dir: Directory to save audio files (default: Anki media)
            
        Returns:
            List of generated audio filenames
        """
        if output_dir is None:
            output_dir = self.media_dir
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        audio_files = []
        
        for i, expr in enumerate(card['math_expressions']):
            # Generate unique filename based on expression
            expr_hash = hashlib.md5(expr.encode()).hexdigest()[:8]
            audio_filename = f"{self.audio_prefix}{card['note_id']}_{i}_{expr_hash}.{self.audio_format}"
            audio_path = output_dir / audio_filename
            
            # Skip if already exists
            if audio_path.exists():
                print(f"Audio already exists: {audio_filename}")
                audio_files.append(audio_filename)
                continue
            
            try:
                # Process expression
                result = self.engine.process_latex(expr)
                
                # Generate audio
                success = await self.engine.speak_expression(
                    result, 
                    output_file=str(audio_path)
                )
                
                if success:
                    print(f"Generated audio: {audio_filename}")
                    audio_files.append(audio_filename)
                else:
                    print(f"Failed to generate audio for: {expr}")
                    
            except Exception as e:
                print(f"Error processing expression '{expr}': {e}")
        
        return audio_files
    
    def update_card_with_audio(self, card: Dict, audio_files: List[str], 
                              auto_play: bool = True) -> str:
        """
        Update card field to include audio playback
        
        Args:
            card: Card dictionary
            audio_files: List of audio filenames
            auto_play: Automatically play audio when card is shown
            
        Returns:
            Updated field content
        """
        field_content = card['original_field']
        
        # Create audio tags
        audio_tags = []
        for audio_file in audio_files:
            if auto_play:
                # Auto-playing audio tag
                audio_tag = f'[sound:{audio_file}]'
            else:
                # Clickable play button
                audio_tag = f'<a href="#" onclick="playSound(\'{audio_file}\'); return false;">🔊</a>'
            audio_tags.append(audio_tag)
        
        # Strategy 1: Add audio after each math expression
        updated_content = field_content
        
        # Replace each math expression with expression + audio
        for i, expr in enumerate(card['math_expressions']):
            if i < len(audio_tags):
                # Find the math expression in original format
                for pattern in [
                    f'${expr}$',
                    f'$${expr}$$',
                    f'\\[{expr}\\]',
                    f'\\({expr}\\)',
                    f'[latex]{expr}[/latex]'
                ]:
                    if pattern in updated_content:
                        replacement = f"{pattern} {audio_tags[i]}"
                        updated_content = updated_content.replace(pattern, replacement, 1)
                        break
        
        # Strategy 2: Add all audio at the end if not inserted inline
        remaining_audio = [tag for tag in audio_tags if tag not in updated_content]
        if remaining_audio:
            audio_section = '<div class="mathspeak-audio">' + ' '.join(remaining_audio) + '</div>'
            updated_content += '\n' + audio_section
        
        return updated_content
    
    def batch_process_deck(self, deck_name: str, 
                          tag_filter: Optional[str] = None,
                          auto_update: bool = False,
                          backup_first: bool = True) -> Dict[str, any]:
        """
        Process an entire deck and add audio to all math cards
        
        Args:
            deck_name: Name of deck to process
            tag_filter: Optional tag filter
            auto_update: Automatically update Anki database
            backup_first: Create backup before modifying
            
        Returns:
            Processing statistics
        """
        stats = {
            'cards_processed': 0,
            'audio_generated': 0,
            'errors': 0,
            'skipped': 0
        }
        
        # Create backup if requested
        if backup_first and auto_update:
            backup_path = self.create_backup()
            print(f"Created backup: {backup_path}")
        
        # Extract cards with math
        cards = self.extract_math_from_cards(deck_name, tag_filter)
        
        if not cards:
            print("No cards with mathematical expressions found")
            return stats
        
        # Process each card
        async def process_all():
            for card in cards:
                print(f"\nProcessing card {card['note_id']} from {card['deck_name']}")
                
                try:
                    # Generate audio
                    audio_files = await self.generate_audio_for_card(card)
                    
                    if audio_files:
                        stats['audio_generated'] += len(audio_files)
                        
                        # Update card if requested
                        if auto_update:
                            updated_content = self.update_card_with_audio(card, audio_files)
                            self.update_anki_database(card['note_id'], 
                                                    card['field_index'], 
                                                    updated_content)
                    else:
                        stats['skipped'] += 1
                    
                    stats['cards_processed'] += 1
                    
                except Exception as e:
                    print(f"Error processing card: {e}")
                    stats['errors'] += 1
        
        # Run async processing
        asyncio.run(process_all())
        
        return stats
    
    def update_anki_database(self, note_id: int, field_index: int, 
                           new_content: str) -> None:
        """Update Anki database with new field content"""
        conn = sqlite3.connect(self.collection_path)
        cursor = conn.cursor()
        
        # Get current fields
        cursor.execute("SELECT flds FROM notes WHERE id = ?", (note_id,))
        result = cursor.fetchone()
        
        if result:
            fields = result[0].split('\x1f')
            fields[field_index] = new_content
            new_fields = '\x1f'.join(fields)
            
            # Update note
            cursor.execute("UPDATE notes SET flds = ?, mod = ? WHERE id = ?",
                         (new_fields, int(Path.ctime()), note_id))
            conn.commit()
            print(f"Updated note {note_id}")
        
        conn.close()
    
    def create_backup(self) -> Path:
        """Create backup of Anki collection"""
        backup_dir = self.collection_path.parent / "MathSpeak_Backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = Path.ctime()
        backup_name = f"collection_backup_{timestamp}.anki2"
        backup_path = backup_dir / backup_name
        
        shutil.copy2(self.collection_path, backup_path)
        return backup_path
    
    def export_audio_package(self, deck_name: str, output_file: str) -> None:
        """
        Export audio files for a deck as a package
        
        Args:
            deck_name: Deck to export audio for
            output_file: Output zip file path
        """
        cards = self.extract_math_from_cards(deck_name)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            audio_files = []
            
            # Generate all audio
            async def generate_all():
                for card in cards:
                    files = await self.generate_audio_for_card(card, temp_path)
                    audio_files.extend(files)
            
            asyncio.run(generate_all())
            
            # Create manifest
            manifest = {
                'deck_name': deck_name,
                'total_cards': len(cards),
                'audio_files': audio_files,
                'mathspeak_version': '1.0.0'
            }
            
            manifest_path = temp_path / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Create zip
            with zipfile.ZipFile(output_file, 'w') as zf:
                zf.write(manifest_path, "manifest.json")
                for audio_file in audio_files:
                    audio_path = temp_path / audio_file
                    if audio_path.exists():
                        zf.write(audio_path, audio_file)
            
            print(f"Exported {len(audio_files)} audio files to {output_file}")


def main():
    """CLI interface for Anki integration"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MathSpeak Anki Integration - Add audio to math flashcards"
    )
    
    parser.add_argument(
        'action',
        choices=['scan', 'process', 'export'],
        help='Action to perform'
    )
    
    parser.add_argument(
        '--collection',
        help='Path to collection.anki2 file'
    )
    
    parser.add_argument(
        '--deck',
        help='Deck name to process'
    )
    
    parser.add_argument(
        '--tag',
        help='Filter by tag'
    )
    
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Use offline TTS engines'
    )
    
    parser.add_argument(
        '--auto-update',
        action='store_true',
        help='Automatically update Anki cards'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip backup creation'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for export'
    )
    
    args = parser.parse_args()
    
    # Initialize integration
    try:
        integration = AnkiMathSpeakIntegration(
            anki_collection_path=args.collection,
            prefer_offline=args.offline
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease specify your Anki collection path with --collection")
        print("Common locations:")
        print("  Linux: ~/.local/share/Anki2/User 1/collection.anki2")
        print("  macOS: ~/Library/Application Support/Anki2/User 1/collection.anki2")
        print("  Windows: %APPDATA%/Anki2/User 1/collection.anki2")
        return
    
    # Execute action
    if args.action == 'scan':
        # Scan for math expressions
        cards = integration.extract_math_from_cards(args.deck, args.tag)
        
        print(f"\nFound {len(cards)} fields with math expressions")
        
        # Show sample
        for card in cards[:5]:
            print(f"\nDeck: {card['deck_name']}")
            print(f"Tags: {card['tags']}")
            print(f"Math expressions: {len(card['math_expressions'])}")
            for expr in card['math_expressions'][:2]:
                print(f"  - {expr[:50]}...")
    
    elif args.action == 'process':
        # Process deck
        if not args.deck:
            print("Error: --deck required for processing")
            return
        
        stats = integration.batch_process_deck(
            deck_name=args.deck,
            tag_filter=args.tag,
            auto_update=args.auto_update,
            backup_first=not args.no_backup
        )
        
        print("\nProcessing complete!")
        print(f"Cards processed: {stats['cards_processed']}")
        print(f"Audio files generated: {stats['audio_generated']}")
        print(f"Errors: {stats['errors']}")
        print(f"Skipped: {stats['skipped']}")
        
        if not args.auto_update:
            print("\nNote: Cards were not updated. Use --auto-update to modify Anki database.")
    
    elif args.action == 'export':
        # Export audio package
        if not args.deck:
            print("Error: --deck required for export")
            return
        
        output_file = args.output or f"{args.deck}_mathspeak_audio.zip"
        integration.export_audio_package(args.deck, output_file)


if __name__ == "__main__":
    main()