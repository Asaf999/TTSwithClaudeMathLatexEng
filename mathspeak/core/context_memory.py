#!/usr/bin/env python3
"""
Context Memory System for Mathematical Text-to-Speech
====================================================

Enhanced context tracking that remembers defined symbols, tracks mathematical
structures, and maintains reading state across expressions.

This module enables the TTS system to:
- Remember previously defined symbols and their meanings
- Track mathematical structure (theorems, proofs, examples)
- Handle cross-references intelligently
- Maintain continuity across multiple expressions
- Provide context-aware pronunciation
"""

import re
import time
import logging
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict
from enum import Enum
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# ===========================
# Mathematical Structures
# ===========================

class StructureType(Enum):
    """Types of mathematical structures we track"""
    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    PROPOSITION = "proposition"
    COROLLARY = "corollary"
    PROOF = "proof"
    EXAMPLE = "example"
    REMARK = "remark"
    NOTATION = "notation"
    EQUATION = "equation"
    SECTION = "section"
    CHAPTER = "chapter"

@dataclass
class MathematicalStructure:
    """Represents a mathematical structure with metadata"""
    type: StructureType
    identifier: Optional[str]  # e.g., "Theorem 3.1", "Definition 2.5"
    label: Optional[str]  # LaTeX label for cross-references
    content: str
    timestamp: float = field(default_factory=time.time)
    parent: Optional['MathematicalStructure'] = None
    children: List['MathematicalStructure'] = field(default_factory=list)
    
    def get_full_identifier(self) -> str:
        """Get full identifier including parent context"""
        if self.identifier:
            if self.parent and self.parent.identifier:
                return f"{self.parent.identifier} - {self.identifier}"
            return self.identifier
        return f"Unnamed {self.type.value}"

@dataclass
class DefinedSymbol:
    """Represents a mathematical symbol with its definition"""
    symbol: str  # The LaTeX representation
    name: str  # Natural language name
    definition: str  # What it represents
    context: str  # Where it was defined
    timestamp: float = field(default_factory=time.time)
    usage_count: int = 0
    related_symbols: List[str] = field(default_factory=list)
    
    def increment_usage(self) -> None:
        """Track symbol usage"""
        self.usage_count += 1

# ===========================
# Memory Banks
# ===========================

class SymbolMemory:
    """Manages memory of defined mathematical symbols"""
    
    def __init__(self, max_symbols: int = 1000):
        self.symbols: Dict[str, DefinedSymbol] = OrderedDict()
        self.max_symbols = max_symbols
        self.symbol_aliases: Dict[str, str] = {}  # Maps aliases to canonical forms
        
        # Common symbol patterns
        self.symbol_patterns = [
            # Definition patterns
            (r'[Ll]et\s+(\$?\\?[a-zA-Z]+(?:_[a-zA-Z0-9]+)?\$?)\s*(?:=|:=|be|denote)',
             'explicit_definition'),
            (r'[Dd]efine\s+(\$?\\?[a-zA-Z]+(?:_[a-zA-Z0-9]+)?\$?)\s*(?:=|:=|as|to be)',
             'explicit_definition'),
            (r'(\$?\\?[a-zA-Z]+(?:_[a-zA-Z0-9]+)?\$?)\s*:=',
             'assignment_definition'),
            (r'[Ww]here\s+(\$?\\?[a-zA-Z]+(?:_[a-zA-Z0-9]+)?\$?)\s+(?:is|denotes|represents)',
             'clarification_definition'),
        ]
        
        # Compile patterns
        self.compiled_patterns = [
            (re.compile(pattern), def_type) 
            for pattern, def_type in self.symbol_patterns
        ]
    
    def define_symbol(self, 
                     symbol: str, 
                     name: str, 
                     definition: str,
                     context: str = "") -> None:
        """Define or update a mathematical symbol"""
        # Normalize symbol
        symbol = self._normalize_symbol(symbol)
        
        # Check if updating existing
        if symbol in self.symbols:
            logger.debug(f"Updating existing symbol: {symbol}")
            self.symbols[symbol].definition = definition
            self.symbols[symbol].timestamp = time.time()
        else:
            # Add new symbol
            self.symbols[symbol] = DefinedSymbol(
                symbol=symbol,
                name=name,
                definition=definition,
                context=context
            )
            
            # Manage memory limit
            if len(self.symbols) > self.max_symbols:
                # Remove oldest symbols
                oldest = list(self.symbols.keys())[:len(self.symbols) - self.max_symbols]
                for old_symbol in oldest:
                    del self.symbols[old_symbol]
    
    def recall_symbol(self, symbol: str) -> Optional[DefinedSymbol]:
        """Recall a previously defined symbol"""
        symbol = self._normalize_symbol(symbol)
        
        # Check direct match
        if symbol in self.symbols:
            self.symbols[symbol].increment_usage()
            return self.symbols[symbol]
        
        # Check aliases
        if symbol in self.symbol_aliases:
            canonical = self.symbol_aliases[symbol]
            if canonical in self.symbols:
                self.symbols[canonical].increment_usage()
                return self.symbols[canonical]
        
        return None
    
    def extract_definitions(self, text: str) -> List[Tuple[str, str]]:
        """Extract symbol definitions from text"""
        definitions = []
        
        for pattern, def_type in self.compiled_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                symbol = match.group(1).strip()
                # Extract definition context
                start = match.end()
                end = min(start + 100, len(text))
                definition_context = text[start:end].split('.')[0]
                definitions.append((symbol, definition_context))
        
        return definitions
    
    def _normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol representation"""
        # Remove $ signs
        symbol = symbol.strip('$')
        # Ensure backslash for LaTeX commands
        if symbol.startswith('\\'):
            return symbol
        elif symbol in ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 
                       'lambda', 'mu', 'pi', 'sigma', 'omega']:
            return f"\\{symbol}"
        return symbol
    
    def add_alias(self, alias: str, canonical: str) -> None:
        """Add an alias for a symbol"""
        alias = self._normalize_symbol(alias)
        canonical = self._normalize_symbol(canonical)
        self.symbol_aliases[alias] = canonical
    
    def get_usage_stats(self) -> Dict[str, int]:
        """Get symbol usage statistics"""
        return {
            symbol: data.usage_count 
            for symbol, data in self.symbols.items()
            if data.usage_count > 0
        }

class StructureMemory:
    """Manages memory of mathematical structures"""
    
    def __init__(self):
        self.structures: List[MathematicalStructure] = []
        self.structure_index: Dict[str, MathematicalStructure] = {}
        self.label_index: Dict[str, MathematicalStructure] = {}
        self.current_structure: Optional[MathematicalStructure] = None
        self.structure_stack: List[MathematicalStructure] = []
        
        # Patterns for structure detection
        self.structure_patterns = {
            StructureType.THEOREM: r'[Tt]heorem\s*(\d+(?:\.\d+)*)?',
            StructureType.LEMMA: r'[Ll]emma\s*(\d+(?:\.\d+)*)?',
            StructureType.PROPOSITION: r'[Pp]roposition\s*(\d+(?:\.\d+)*)?',
            StructureType.COROLLARY: r'[Cc]orollary\s*(\d+(?:\.\d+)*)?',
            StructureType.DEFINITION: r'[Dd]efinition\s*(\d+(?:\.\d+)*)?',
            StructureType.EXAMPLE: r'[Ee]xample\s*(\d+(?:\.\d+)*)?',
            StructureType.PROOF: r'[Pp]roof\b',
            StructureType.REMARK: r'[Rr]emark\s*(\d+(?:\.\d+)*)?',
        }
        
        # Compile patterns
        self.compiled_patterns = {
            struct_type: re.compile(pattern)
            for struct_type, pattern in self.structure_patterns.items()
        }
    
    def begin_structure(self, 
                       struct_type: StructureType,
                       identifier: Optional[str] = None,
                       label: Optional[str] = None) -> MathematicalStructure:
        """Begin a new mathematical structure"""
        structure = MathematicalStructure(
            type=struct_type,
            identifier=identifier,
            label=label,
            content="",
            parent=self.current_structure
        )
        
        # Add to parent if exists
        if self.current_structure:
            self.current_structure.children.append(structure)
        
        # Update indices
        self.structures.append(structure)
        if identifier:
            self.structure_index[identifier] = structure
        if label:
            self.label_index[label] = structure
        
        # Update current context
        self.structure_stack.append(structure)
        self.current_structure = structure
        
        logger.debug(f"Began structure: {struct_type.value} {identifier or ''}")
        return structure
    
    def end_structure(self) -> Optional[MathematicalStructure]:
        """End current mathematical structure"""
        if not self.structure_stack:
            return None
        
        completed = self.structure_stack.pop()
        self.current_structure = self.structure_stack[-1] if self.structure_stack else None
        
        logger.debug(f"Ended structure: {completed.get_full_identifier()}")
        return completed
    
    def detect_structures(self, text: str) -> List[Tuple[StructureType, Optional[str]]]:
        """Detect mathematical structures in text"""
        detected = []
        
        for struct_type, pattern in self.compiled_patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                identifier = None
                if match.lastindex and match.group(1):
                    identifier = f"{struct_type.value.capitalize()} {match.group(1)}"
                detected.append((struct_type, identifier))
        
        return detected
    
    def resolve_reference(self, reference: str) -> Optional[MathematicalStructure]:
        """Resolve a cross-reference to a structure"""
        # Check direct identifier match
        if reference in self.structure_index:
            return self.structure_index[reference]
        
        # Check label match
        if reference in self.label_index:
            return self.label_index[reference]
        
        # Try fuzzy matching
        reference_lower = reference.lower()
        for identifier, structure in self.structure_index.items():
            if reference_lower in identifier.lower():
                return structure
        
        return None
    
    def get_current_context(self) -> str:
        """Get description of current structural context"""
        if not self.current_structure:
            return "main text"
        
        context_parts = []
        for structure in self.structure_stack:
            context_parts.append(structure.get_full_identifier())
        
        return " within ".join(context_parts)

# ===========================
# Cross-Reference Handler
# ===========================

class CrossReferenceHandler:
    """Handles mathematical cross-references"""
    
    def __init__(self, structure_memory: StructureMemory):
        self.structure_memory = structure_memory
        
        # Reference patterns
        self.ref_patterns = [
            (r'[Ss]ee\s+([Tt]heorem|[Ll]emma|[Pp]roposition)\s*(\d+(?:\.\d+)*)',
             'see_reference'),
            (r'[Bb]y\s+([Tt]heorem|[Ll]emma|[Pp]roposition)\s*(\d+(?:\.\d+)*)',
             'by_reference'),
            (r'[Ff]rom\s+([Tt]heorem|[Ll]emma|[Pp]roposition)\s*(\d+(?:\.\d+)*)',
             'from_reference'),
            (r'[Ii]n\s+([Tt]heorem|[Ll]emma|[Pp]roposition)\s*(\d+(?:\.\d+)*)',
             'in_reference'),
            (r'\\ref\{([^}]+)\}', 'latex_ref'),
            (r'\\eqref\{([^}]+)\}', 'latex_eqref'),
            (r'\\cite\{([^}]+)\}', 'latex_cite'),
            (r'[Ee]quation\s*\((\d+(?:\.\d+)*)\)', 'equation_ref'),
        ]
        
        # Compile patterns
        self.compiled_patterns = [
            (re.compile(pattern), ref_type)
            for pattern, ref_type in self.ref_patterns
        ]
    
    def process_references(self, text: str) -> str:
        """Process cross-references in text"""
        processed = text
        
        for pattern, ref_type in self.compiled_patterns:
            processed = pattern.sub(
                lambda m: self._expand_reference(m, ref_type),
                processed
            )
        
        return processed
    
    def _expand_reference(self, match: re.Match, ref_type: str) -> str:
        """Expand a cross-reference match"""
        if ref_type in ['see_reference', 'by_reference', 'from_reference', 'in_reference']:
            struct_type = match.group(1)
            number = match.group(2)
            reference = f"{struct_type} {number}"
            
            # Try to resolve
            structure = self.structure_memory.resolve_reference(reference)
            if structure:
                return f"{match.group(0)} (which states: {structure.content[:50]}...)"
            return match.group(0)
        
        elif ref_type == 'latex_ref':
            label = match.group(1)
            structure = self.structure_memory.resolve_reference(label)
            if structure:
                return structure.identifier or f"the {structure.type.value}"
            return f"reference {label}"
        
        elif ref_type == 'latex_eqref':
            label = match.group(1)
            return f"equation ({label})"
        
        elif ref_type == 'equation_ref':
            return match.group(0)  # Keep as is
        
        return match.group(0)

# ===========================
# Main Context Memory System
# ===========================

class ContextMemory:
    """Main context memory system integrating all components"""
    
    def __init__(self, 
                 config_path: Optional[Path] = None,
                 persist_symbols: bool = True):
        # Initialize memory components
        self.symbol_memory = SymbolMemory()
        self.structure_memory = StructureMemory()
        self.reference_handler = CrossReferenceHandler(self.structure_memory)
        
        # Reading state
        self.reading_state = {
            'position': 'beginning',  # beginning, middle, end
            'expressions_read': 0,
            'last_expression': None,
            'session_start': time.time(),
        }
        
        # Configuration
        self.persist_symbols = persist_symbols
        self.config_path = config_path or Path.home() / ".mathspeak" / "context_memory.json"
        
        # Load persisted data
        if self.persist_symbols:
            self._load_persisted_data()
        
        logger.info("Context memory system initialized")
    
    def process_expression(self, expression: str, processed_text: str) -> Dict[str, Any]:
        """Process an expression and update context memory"""
        # Update reading state
        self.reading_state['expressions_read'] += 1
        self.reading_state['last_expression'] = expression
        
        # Extract and store symbol definitions
        definitions = self.symbol_memory.extract_definitions(expression)
        for symbol, definition in definitions:
            self.symbol_memory.define_symbol(
                symbol=symbol,
                name=f"symbol {symbol}",
                definition=definition,
                context=self.structure_memory.get_current_context()
            )
        
        # Detect and track structures
        structures = self.structure_memory.detect_structures(expression)
        for struct_type, identifier in structures:
            if struct_type == StructureType.PROOF:
                # Check if ending a proof
                if "Q.E.D" in expression or "∎" in expression or "□" in expression:
                    self.structure_memory.end_structure()
                else:
                    self.structure_memory.begin_structure(struct_type, identifier)
            else:
                self.structure_memory.begin_structure(struct_type, identifier)
        
        # Process cross-references
        enhanced_text = self.reference_handler.process_references(processed_text)
        
        # Build context info
        context_info = {
            'current_structure': self.structure_memory.get_current_context(),
            'defined_symbols': len(self.symbol_memory.symbols),
            'active_structures': len(self.structure_memory.structure_stack),
            'references_found': enhanced_text != processed_text,
            'reading_position': self._determine_reading_position(),
        }
        
        return {
            'enhanced_text': enhanced_text,
            'context_info': context_info,
            'new_definitions': definitions,
        }
    
    def enhance_with_context(self, text: str) -> str:
        """Enhance text with remembered context"""
        enhanced = text
        
        # Replace symbols with their definitions when first used
        for symbol, data in self.symbol_memory.symbols.items():
            if data.usage_count == 0:
                # First use - add definition
                pattern = re.escape(symbol)
                replacement = f"{symbol} (which we defined as {data.definition})"
                enhanced = re.sub(pattern, replacement, enhanced, count=1)
        
        # Add context for structures
        if self.structure_memory.current_structure:
            context = self.structure_memory.get_current_context()
            if "proof" in context.lower() and "beginning" in self.reading_state['position']:
                enhanced = f"We are now in the {context}. " + enhanced
        
        # Process cross-references
        enhanced = self.reference_handler.process_references(enhanced)
        
        return enhanced
    
    def get_symbol_reminder(self, symbol: str) -> Optional[str]:
        """Get a reminder about a previously defined symbol"""
        symbol_data = self.symbol_memory.recall_symbol(symbol)
        if symbol_data:
            if symbol_data.usage_count > 5:
                return f"{symbol}"  # Well-known, no reminder needed
            else:
                return f"{symbol}, which is {symbol_data.definition}"
        return None
    
    def _determine_reading_position(self) -> str:
        """Determine current reading position"""
        expressions = self.reading_state['expressions_read']
        
        if expressions <= 2:
            return 'beginning'
        elif self.structure_memory.current_structure and \
             self.structure_memory.current_structure.type == StructureType.PROOF:
            # Check for proof end markers
            if self.reading_state['last_expression']:
                if any(marker in self.reading_state['last_expression'] 
                       for marker in ['Q.E.D', '∎', '□']):
                    return 'end'
            return 'middle'
        else:
            return 'middle'
    
    def _load_persisted_data(self) -> None:
        """Load persisted symbol definitions"""
        if not self.config_path.exists():
            return
        
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                
            # Restore symbols
            for symbol_data in data.get('symbols', []):
                self.symbol_memory.symbols[symbol_data['symbol']] = DefinedSymbol(
                    symbol=symbol_data['symbol'],
                    name=symbol_data['name'],
                    definition=symbol_data['definition'],
                    context=symbol_data.get('context', ''),
                    usage_count=symbol_data.get('usage_count', 0)
                )
            
            logger.info(f"Loaded {len(self.symbol_memory.symbols)} persisted symbols")
            
        except Exception as e:
            logger.error(f"Failed to load persisted data: {e}")
    
    def save_persisted_data(self) -> None:
        """Save symbol definitions for future sessions"""
        if not self.persist_symbols:
            return
        
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare data
            data = {
                'symbols': [
                    {
                        'symbol': symbol,
                        'name': symbol_data.name,
                        'definition': symbol_data.definition,
                        'context': symbol_data.context,
                        'usage_count': symbol_data.usage_count,
                    }
                    for symbol, symbol_data in self.symbol_memory.symbols.items()
                    if symbol_data.usage_count > 0  # Only save used symbols
                ],
                'saved_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            # Save
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(data['symbols'])} symbols to persistent storage")
            
        except Exception as e:
            logger.error(f"Failed to save persisted data: {e}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        return {
            'expressions_processed': self.reading_state['expressions_read'],
            'symbols_defined': len(self.symbol_memory.symbols),
            'structures_tracked': len(self.structure_memory.structures),
            'current_context': self.structure_memory.get_current_context(),
            'symbol_usage_stats': self.symbol_memory.get_usage_stats(),
            'session_duration': time.time() - self.reading_state['session_start'],
        }
    
    def reset_session(self) -> None:
        """Reset session state while keeping learned symbols"""
        self.structure_memory = StructureMemory()
        self.reference_handler = CrossReferenceHandler(self.structure_memory)
        self.reading_state = {
            'position': 'beginning',
            'expressions_read': 0,
            'last_expression': None,
            'session_start': time.time(),
        }
        logger.info("Session state reset")

# ===========================
# Testing Functions
# ===========================

def test_context_memory():
    """Test context memory functionality"""
    memory = ContextMemory(persist_symbols=False)
    
    test_expressions = [
        "Let $X$ be a topological space and $\\tau$ be its topology.",
        "Definition 3.1. A space $X$ is compact if every open cover has a finite subcover.",
        "Theorem 3.2. Every closed subset of a compact space is compact.",
        "Proof. Let $F \\subseteq X$ be closed where $X$ is compact.",
        "By Theorem 3.2, we know that $F$ is compact.",
        "Q.E.D.",
    ]
    
    print("Testing Context Memory System")
    print("=" * 60)
    
    for i, expr in enumerate(test_expressions, 1):
        print(f"\nExpression {i}: {expr}")
        result = memory.process_expression(expr, expr)
        
        print(f"Context: {result['context_info']['current_structure']}")
        print(f"Symbols defined: {result['context_info']['defined_symbols']}")
        if result['new_definitions']:
            print(f"New definitions: {result['new_definitions']}")
        print(f"Enhanced: {result['enhanced_text'][:100]}...")
    
    print("\nSession Summary:")
    summary = memory.get_session_summary()
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    test_context_memory()