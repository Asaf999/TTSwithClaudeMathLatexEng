#!/usr/bin/env python3
"""
Base Vocabulary Classes
======================

Simplified base classes for domain vocabularies that inherit from the enhanced base.
"""

from typing import Dict, List, Tuple, Union, Callable
import re
import logging
from abc import ABC, abstractmethod
from enum import Enum

from .base import BaseDomainVocabulary, BaseDomainProcessor, BaseDomainContext

logger = logging.getLogger(__name__)


class SimpleDomainVocabulary(BaseDomainVocabulary):
    """Simplified domain vocabulary that handles common patterns"""
    
    def __init__(self):
        self.terms = {}  # Will be populated by subclass
        self.patterns = []  # Will be populated by subclass
        super().__init__()
    
    def _build_vocabulary(self) -> None:
        """Build vocabulary from terms dictionary"""
        self.vocabulary = self.terms.copy()
    
    def _build_patterns(self) -> None:
        """Build patterns - should be overridden by subclasses"""
        pass


class SimpleDomainProcessor(BaseDomainProcessor):
    """Simplified domain processor with common functionality"""
    
    def __init__(self):
        self.context = None  # Will be set by subclass
        self.special_rules = {}  # Will be set by subclass
        super().__init__()
    
    def _create_context_patterns(self) -> Dict[Any, List[str]]:
        """Default empty context patterns"""
        return {}
    
    def detect_subcontext(self, text: str) -> Any:
        """Default context detection"""
        return self.context if hasattr(self, 'context') else BaseDomainContext.GENERAL
    
    def _apply_special_rules(self, text: str) -> str:
        """Default no special rules"""
        return text
    
    def process(self, text: str) -> str:
        """Simplified process that returns string instead of ProcessedExpression"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        if hasattr(self.context, 'value'):
            logger.debug(f"{self.__class__.__name__} subcontext: {self.context.value}")
        
        # Pre-process
        text = self._preprocess(text)
        
        # Apply vocabulary
        text = self._apply_vocabulary(text)
        
        # Apply special rules
        text = self._apply_special_rules(text)
        
        # Post-process
        text = self._postprocess(text)
        
        return text
    
    def get_context_info(self) -> Dict[str, Any]:
        """Get information about current processing context"""
        domain_name = self.__class__.__name__.replace('Processor', '').lower()
        return {
            'domain': domain_name,
            'subcontext': getattr(self.context, 'value', str(self.context)) if self.context else 'general',
            'vocabulary_size': len(self.vocabulary.terms) if hasattr(self.vocabulary, 'terms') else 0,
            'pattern_count': len(self.vocabulary.patterns) if hasattr(self.vocabulary, 'patterns') else 0,
        }