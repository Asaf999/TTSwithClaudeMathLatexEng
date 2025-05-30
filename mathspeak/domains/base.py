#!/usr/bin/env python3
"""
Base Domain Processor
====================

Abstract base class for all mathematical domain processors.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Tuple, Callable, Optional, Any, Union
import re
import logging
from dataclasses import dataclass
from functools import lru_cache
import json
import os

from mathspeak.core.engine import ProcessedExpression


logger = logging.getLogger(__name__)


@dataclass
class DomainPattern:
    """A pattern for domain-specific processing"""
    pattern: Union[str, re.Pattern]
    replacement: Union[str, Callable]
    priority: int = 50
    description: str = ""
    
    def __post_init__(self):
        if isinstance(self.pattern, str):
            self.pattern = re.compile(self.pattern)


class BaseDomainContext(Enum):
    """Base class for domain contexts"""
    GENERAL = "general"


class BaseDomainVocabulary(ABC):
    """Abstract base class for domain vocabularies"""
    
    def __init__(self):
        self.vocabulary: Dict[str, Union[str, Callable]] = {}
        self.patterns: List[DomainPattern] = []
        self.compiled_patterns: List[Tuple[re.Pattern, Union[str, Callable]]] = []
        self._build_vocabulary()
        self._build_patterns()
        self._compile_patterns()
        self._unknown_commands_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'unknown_latex_commands.json'
        )
    
    @abstractmethod
    def _build_vocabulary(self) -> None:
        """Build the domain-specific vocabulary"""
        pass
    
    @abstractmethod
    def _build_patterns(self) -> None:
        """Build the domain-specific patterns"""
        pass
    
    def _compile_patterns(self) -> None:
        """Compile all patterns for efficiency"""
        # Sort by priority (higher first)
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
        
        # Build compiled patterns list
        self.compiled_patterns = []
        
        # Add vocabulary patterns
        for pattern, replacement in self.vocabulary.items():
            try:
                if r'\\' in pattern:
                    flexible_pattern = self._escape_for_both_backslashes(pattern)
                    self.compiled_patterns.append((re.compile(flexible_pattern), replacement))
                else:
                    self.compiled_patterns.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        # Add custom patterns
        for pattern_obj in self.patterns:
            self.compiled_patterns.append((pattern_obj.pattern, pattern_obj.replacement))
    
    def _escape_for_both_backslashes(self, pattern: str) -> str:
        """Create pattern that matches both single and double backslashes"""
        import re as regex
        
        def replace_command(match):
            cmd = match.group(0)
            if cmd.startswith(r'\\'):
                cmd_name = cmd[2:]
            else:
                return cmd
            
            return r'(?:\\\\|\\)' + regex.escape(cmd_name)
        
        pattern = regex.sub(r'\\\\[a-zA-Z]+', replace_command, pattern)
        return pattern
    
    @lru_cache(maxsize=1024)
    def apply_all_patterns(self, text: str) -> str:
        """Apply all patterns with caching for performance"""
        result = text
        
        # Sort patterns by length (longer patterns first) to avoid conflicts
        sorted_patterns = sorted(self.compiled_patterns,
                               key=lambda x: len(x[0].pattern) if hasattr(x[0], 'pattern') else 0,
                               reverse=True)
        
        # Track unknown commands
        unknown_commands = set()
        
        for pattern, replacement in sorted_patterns:
            try:
                if callable(replacement):
                    result = pattern.sub(replacement, result)
                else:
                    result = pattern.sub(replacement, result)
            except Exception as e:
                logger.warning(f"Pattern application failed: {e}")
        
        # Track any remaining LaTeX commands as unknown
        remaining_commands = re.findall(r'\\[a-zA-Z]+', result)
        for cmd in remaining_commands:
            unknown_commands.add(cmd)
        
        # Log unknown commands
        if unknown_commands:
            self._log_unknown_commands(unknown_commands)
        
        return result
    
    def _log_unknown_commands(self, commands: set) -> None:
        """Log unknown LaTeX commands for future improvement"""
        try:
            # Load existing unknown commands
            if os.path.exists(self._unknown_commands_file):
                with open(self._unknown_commands_file, 'r') as f:
                    unknown_data = json.load(f)
            else:
                unknown_data = {}
            
            # Update with new commands
            for cmd in commands:
                if cmd not in unknown_data:
                    unknown_data[cmd] = {
                        "count": 1,
                        "domain": self.__class__.__name__
                    }
                else:
                    unknown_data[cmd]["count"] += 1
            
            # Save back
            with open(self._unknown_commands_file, 'w') as f:
                json.dump(unknown_data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to log unknown commands: {e}")


class BaseDomainProcessor(ABC):
    """Abstract base class for domain processors"""
    
    def __init__(self):
        self.vocabulary = self._create_vocabulary()
        self.context_patterns = self._create_context_patterns()
        logger.info(f"{self.__class__.__name__} initialized")
    
    @abstractmethod
    def _create_vocabulary(self) -> BaseDomainVocabulary:
        """Create the domain vocabulary instance"""
        pass
    
    @abstractmethod
    def _create_context_patterns(self) -> Dict[Any, List[str]]:
        """Create patterns for context detection"""
        pass
    
    @abstractmethod
    def detect_subcontext(self, text: str) -> Any:
        """Detect the specific sub-context within this domain"""
        pass
    
    def process(self, text: str) -> ProcessedExpression:
        """Process text through the domain pipeline"""
        # Pre-process
        processed = self._preprocess(text)
        
        # Apply vocabulary
        processed = self._apply_vocabulary(processed)
        
        # Apply special rules
        processed = self._apply_special_rules(processed)
        
        # Post-process
        processed = self._postprocess(processed)
        
        # Create result
        return ProcessedExpression(
            original=text,
            processed=processed,
            context=self.__class__.__name__.replace('Processor', '').lower()
        )
    
    def _preprocess(self, text: str) -> str:
        """Pre-process text before vocabulary application"""
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply domain vocabulary to text"""
        return self.vocabulary.apply_all_patterns(text)
    
    @abstractmethod
    def _apply_special_rules(self, text: str) -> str:
        """Apply domain-specific special rules"""
        pass
    
    def _postprocess(self, text: str) -> str:
        """Post-process text after all transformations"""
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([,.;:!?])', r'\1', text)
        
        return text
    
    def _process_nested(self, content: str) -> str:
        """Process nested mathematical content safely"""
        if content is None:
            return ""
        content = content.strip()
        
        # Common replacements for nested content
        replacements = [
            (r'\\mathbb{R}', 'R'),
            (r'\\mathbb{C}', 'C'),
            (r'\\mathbb{Z}', 'Z'),
            (r'\\mathbb{Q}', 'Q'),
            (r'\\mathbb{N}', 'N'),
            (r'_([0-9])', r' sub \1'),
            (r'\^([0-9])', r' to the \1'),
            (r'\\infty', 'infinity'),
            (r'\\to', 'approaches'),
            (r'\\leq', 'less than or equal to'),
            (r'\\geq', 'greater than or equal to'),
            (r'\\neq', 'not equal to'),
            (r'\\approx', 'approximately'),
            (r'\\pm', 'plus or minus'),
            (r'\\times', 'times'),
            (r'\\cdot', 'dot'),
            (r'\\ldots', 'dot dot dot'),
            (r'\\alpha', 'alpha'),
            (r'\\beta', 'beta'),
            (r'\\gamma', 'gamma'),
            (r'\\delta', 'delta'),
            (r'\\epsilon', 'epsilon'),
            (r'\\theta', 'theta'),
            (r'\\lambda', 'lambda'),
            (r'\\mu', 'mu'),
            (r'\\sigma', 'sigma'),
            (r'\\pi', 'pi'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _number_name(self, n: str) -> str:
        """Convert number to word"""
        numbers = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
            '9': 'nine', '10': 'ten', '11': 'eleven', '12': 'twelve'
        }
        return numbers.get(n, n)
    
    def _ordinal(self, n: str) -> str:
        """Convert number to ordinal"""
        ordinals = {
            '0': 'zeroth', '1': 'first', '2': 'second', '3': 'third',
            '4': 'fourth', '5': 'fifth', '6': 'sixth', '7': 'seventh',
            '8': 'eighth', '9': 'ninth', '10': 'tenth', '11': 'eleventh',
            '12': 'twelfth', '13': 'thirteenth', '20': 'twentieth',
            '21': 'twenty-first', '22': 'twenty-second', '23': 'twenty-third'
        }
        if n in ordinals:
            return ordinals[n]
        if n.endswith('1') and not n.endswith('11'):
            return f"{n}st"
        elif n.endswith('2') and not n.endswith('12'):
            return f"{n}nd"
        elif n.endswith('3') and not n.endswith('13'):
            return f"{n}rd"
        else:
            return f"{n}th"