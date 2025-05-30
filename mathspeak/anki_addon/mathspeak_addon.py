# MathSpeak Anki Add-on
# Place this file in Anki's addons21 folder

"""
MathSpeak for Anki
==================

Adds MathSpeak audio generation directly to Anki's editor.
"""

import os
import sys
import json
import asyncio
import hashlib
from pathlib import Path
from typing import Optional

from aqt import mw, gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo, tooltip
from anki.hooks import addHook
from PyQt6.QtWidgets import QMenu, QAction

# Add MathSpeak to path (adjust path as needed)
MATHSPEAK_PATH = Path.home() / "MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak"
if MATHSPEAK_PATH.exists():
    sys.path.insert(0, str(MATHSPEAK_PATH.parent))

try:
    from mathspeak.core.engine import MathematicalTTSEngine
    from mathspeak.core.voice_manager import VoiceManager
    MATHSPEAK_AVAILABLE = True
except ImportError:
    MATHSPEAK_AVAILABLE = False
    showInfo("MathSpeak not found. Please install MathSpeak and update the path in the addon.")


class MathSpeakAddon:
    """MathSpeak integration for Anki"""
    
    def __init__(self):
        self.engine = None
        self.config = mw.addonManager.getConfig(__name__) or {}
        self.setup_engine()
        
    def setup_engine(self):
        """Initialize MathSpeak engine"""
        if not MATHSPEAK_AVAILABLE:
            return
            
        try:
            voice_manager = VoiceManager()
            self.engine = MathematicalTTSEngine(
                voice_manager=voice_manager,
                enable_caching=True,
                prefer_offline_tts=self.config.get('prefer_offline', False)
            )
        except Exception as e:
            showInfo(f"Failed to initialize MathSpeak: {str(e)}")
            self.engine = None
    
    def add_audio_to_field(self, editor: Editor, field_content: str) -> str:
        """Add MathSpeak audio to field"""
        if not self.engine:
            showInfo("MathSpeak engine not available")
            return field_content
        
        import re
        
        # Find LaTeX expressions
        patterns = [
            (r'\$([^$]+)\$', r'$\1$'),  # $...$
            (r'\$\$([^$]+)\$\$', r'$$\1$$'),  # $$...$$
            (r'\\\[([^\]]+)\\\]', r'\[\1\]'),  # \[...\]
            (r'\\\(([^\)]+)\\\)', r'\(\1\)'),  # \(...\)
            (r'\[latex\]([^\[]+)\[/latex\]', r'[latex]\1[/latex]'),  # [latex]...[/latex]
        ]
        
        modified_content = field_content
        audio_added = False
        
        for pattern, full_pattern in patterns:
            matches = re.finditer(pattern, field_content)
            
            for match in matches:
                expr = match.group(1)
                full_expr = match.group(0)
                
                try:
                    # Generate audio
                    audio_file = self.generate_audio_for_expression(
                        expr, 
                        editor.note.id if editor.note else None
                    )
                    
                    if audio_file:
                        # Add audio tag after expression
                        audio_tag = f" [sound:{audio_file}]"
                        
                        # Only add if not already present
                        if audio_tag not in modified_content:
                            modified_content = modified_content.replace(
                                full_expr,
                                full_expr + audio_tag,
                                1
                            )
                            audio_added = True
                            
                except Exception as e:
                    tooltip(f"Error processing expression: {str(e)}")
        
        if audio_added:
            tooltip("MathSpeak audio added!")
        else:
            tooltip("No new math expressions found to process")
            
        return modified_content
    
    def generate_audio_for_expression(self, expression: str, 
                                    note_id: Optional[int] = None) -> Optional[str]:
        """Generate audio file for math expression"""
        if not self.engine:
            return None
        
        # Create unique filename
        expr_hash = hashlib.md5(expression.encode()).hexdigest()[:8]
        note_suffix = f"_{note_id}" if note_id else ""
        filename = f"mathspeak{note_suffix}_{expr_hash}.mp3"
        
        # Full path in media folder
        media_dir = Path(mw.col.media.dir())
        audio_path = media_dir / filename
        
        # Skip if already exists
        if audio_path.exists():
            return filename
        
        # Generate audio synchronously (blocking)
        try:
            # Process expression
            result = self.engine.process_latex(expression)
            
            # Run async code in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            success = loop.run_until_complete(
                self.engine.speak_expression(result, output_file=str(audio_path))
            )
            
            loop.close()
            
            if success and audio_path.exists():
                # Register with Anki's media manager
                mw.col.media.add_file(str(audio_path))
                return filename
                
        except Exception as e:
            if audio_path.exists():
                audio_path.unlink()
            raise e
            
        return None
    
    def on_editor_button_clicked(self, editor: Editor):
        """Handle MathSpeak button click"""
        # Get current field content
        field_num = editor.currentField
        if field_num is None:
            tooltip("Please select a field first")
            return
        
        note = editor.note
        if not note:
            return
            
        field_content = note.fields[field_num]
        
        # Process field
        new_content = self.add_audio_to_field(editor, field_content)
        
        if new_content != field_content:
            # Update field
            note.fields[field_num] = new_content
            editor.loadNoteKeepingFocus()
    
    def add_editor_button(self, buttons, editor):
        """Add MathSpeak button to editor"""
        if not MATHSPEAK_AVAILABLE:
            return buttons
            
        button = editor.addButton(
            icon=None,  # Could add custom icon
            cmd="mathspeak",
            func=lambda e: self.on_editor_button_clicked(e),
            tip="Add MathSpeak audio to mathematical expressions (Alt+M)",
            keys="Alt+M",
            label="🔊"
        )
        
        buttons.append(button)
        return buttons
    
    def on_add_cards_menu(self, menu: QMenu, editor: Editor):
        """Add MathSpeak to context menu"""
        if not MATHSPEAK_AVAILABLE:
            return
            
        action = QAction("Add MathSpeak Audio", menu)
        action.triggered.connect(lambda: self.on_editor_button_clicked(editor))
        menu.addAction(action)
    
    def batch_process_current_deck(self):
        """Process all cards in current deck"""
        if not self.engine:
            showInfo("MathSpeak engine not available")
            return
        
        deck_id = mw.col.decks.selected()
        deck_name = mw.col.decks.name(deck_id)
        
        # Get cards in deck
        card_ids = mw.col.find_cards(f"deck:{deck_name}")
        
        if not card_ids:
            showInfo("No cards found in current deck")
            return
        
        processed = 0
        errors = 0
        
        mw.progress.start(max=len(card_ids), label="Processing cards with MathSpeak...")
        
        for i, cid in enumerate(card_ids):
            card = mw.col.get_card(cid)
            note = card.note()
            
            modified = False
            
            # Process each field
            for field_idx, field_content in enumerate(note.fields):
                try:
                    new_content = self.add_audio_to_field(None, field_content)
                    if new_content != field_content:
                        note.fields[field_idx] = new_content
                        modified = True
                except Exception as e:
                    errors += 1
            
            if modified:
                note.flush()
                processed += 1
            
            mw.progress.update(value=i)
            
            # Check if cancelled
            if mw.progress.want_cancel():
                break
        
        mw.progress.finish()
        
        showInfo(f"""MathSpeak Batch Processing Complete:
        
Cards processed: {processed}
Errors: {errors}
        
Audio files have been added to your cards.""")


# Global addon instance
addon = None


def setup_addon():
    """Initialize the addon"""
    global addon
    
    if MATHSPEAK_AVAILABLE:
        addon = MathSpeakAddon()
        
        # Add editor button
        gui_hooks.editor_did_init_buttons.append(addon.add_editor_button)
        
        # Add context menu
        gui_hooks.editor_will_show_context_menu.append(addon.on_add_cards_menu)
        
        # Add menu item for batch processing
        action = QAction("Process Current Deck with MathSpeak", mw)
        action.triggered.connect(addon.batch_process_current_deck)
        mw.form.menuTools.addAction(action)


# Initialize on Anki startup
setup_addon()