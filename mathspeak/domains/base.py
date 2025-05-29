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
        self._build_vocabulary()
        self._build_patterns()
        self._compile_patterns()
    
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
    
    def _escape_for_both_backslashes(self, pattern: str) -> str:
        """Create pattern that matches both single and double backslashes"""
        # Replace \\ with \\{1,2} to match one or two backslashes
        pattern = pattern.replace('\\\\', '\\\\{1,2}')
        return pattern
    
    def apply_vocabulary(self, text: str) -> str:
        """Apply vocabulary replacements to text"""
        result = text
        
        # Apply direct replacements
        for term, replacement in self.vocabulary.items():
            if isinstance(replacement, str):
                # Make pattern flexible for backslashes
                flexible_term = self._escape_for_both_backslashes(term)
                pattern = re.compile(r'\b' + flexible_term + r'\b')
                result = pattern.sub(replacement, result)
            elif callable(replacement):
                # Lambda functions for dynamic replacements
                pattern = re.compile(term)
                result = pattern.sub(replacement, result)
        
        return result
    
    def apply_patterns(self, text: str) -> str:
        """Apply pattern-based replacements to text"""
        result = text
        
        for pattern_obj in self.patterns:
            if isinstance(pattern_obj.replacement, str):
                result = pattern_obj.pattern.sub(pattern_obj.replacement, result)
            elif callable(pattern_obj.replacement):
                result = pattern_obj.pattern.sub(pattern_obj.replacement, result)
        
        return result


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
        result = self.vocabulary.apply_vocabulary(text)
        result = self.vocabulary.apply_patterns(result)
        return result
    
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
    
    def _process_nested(self, text: str, depth: int = 0) -> str:
        """Process nested structures"""
        if depth > 5:  # Prevent infinite recursion
            return text
        
        # This can be overridden in subclasses for specific handling
        return text