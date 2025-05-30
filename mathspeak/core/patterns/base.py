#!/usr/bin/env python3
"""
Base Classes and Types for Mathematical Speech Patterns
=======================================================

This module defines the core abstractions and types used throughout
the pattern matching system.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# ===========================
# Context and Audience Levels
# ===========================

class AudienceLevel(Enum):
    """Audience sophistication levels"""
    HIGH_SCHOOL = "high_school"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    RESEARCH = "research"

class MathDomain(Enum):
    """Mathematical domains for pattern categorization"""
    BASIC_ARITHMETIC = "basic_arithmetic"
    ALGEBRA = "algebra"
    FUNCTIONS = "functions"
    CALCULUS = "calculus"
    LINEAR_ALGEBRA = "linear_algebra"
    SET_THEORY = "set_theory"
    PROBABILITY = "probability"
    NUMBER_THEORY = "number_theory"
    COMPLEX_ANALYSIS = "complex_analysis"
    TOPOLOGY = "topology"
    LOGIC = "logic"
    DISCRETE_MATH = "discrete_math"

@dataclass
class PatternRule:
    """A mathematical pattern with its natural speech replacement"""
    pattern: str  # Regex pattern
    replacement: Union[str, Callable]  # Natural speech or function
    domain: MathDomain
    description: str
    priority: int = 50
    audience_levels: List[AudienceLevel] = None
    
    def __post_init__(self):
        self.compiled = re.compile(self.pattern)
        if self.audience_levels is None:
            self.audience_levels = list(AudienceLevel)

# ===========================
# Abstract Base Classes
# ===========================

class PatternHandler(ABC):
    """Abstract base class for pattern handlers"""
    
    def __init__(self, domain: MathDomain):
        self.domain = domain
        self.patterns: List[PatternRule] = []
        self._init_patterns()
    
    @abstractmethod
    def _init_patterns(self):
        """Initialize patterns for this handler"""
        pass
    
    def process(self, text: str, audience: AudienceLevel = AudienceLevel.UNDERGRADUATE) -> str:
        """Process text with patterns appropriate for audience"""
        result = text
        
        # Filter patterns by audience level
        applicable_patterns = [
            p for p in self.patterns 
            if audience in p.audience_levels
        ]
        
        # Sort by priority (highest first)
        applicable_patterns.sort(key=lambda p: p.priority, reverse=True)
        
        for pattern_rule in applicable_patterns:
            try:
                if callable(pattern_rule.replacement):
                    # Custom function replacement
                    result = pattern_rule.compiled.sub(pattern_rule.replacement, result)
                else:
                    # Simple string replacement
                    result = pattern_rule.compiled.sub(pattern_rule.replacement, result)
            except Exception as e:
                logger.warning(f"Pattern application failed: {pattern_rule.description}: {e}")
        
        return result
    
    def get_patterns_for_audience(self, audience: AudienceLevel) -> List[PatternRule]:
        """Get patterns applicable for given audience level"""
        return [p for p in self.patterns if audience in p.audience_levels]

class DomainProcessor(ABC):
    """Abstract base class for domain-specific processors"""
    
    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.confidence_threshold = 0.3
        
    @abstractmethod
    def can_handle(self, expression: str) -> float:
        """Return confidence score (0.0-1.0) for handling this expression"""
        pass
    
    @abstractmethod
    def process(self, expression: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process expression and return natural speech"""
        pass
    
    def get_keywords(self) -> List[str]:
        """Return keywords that indicate this domain"""
        return []

# ===========================
# Utility Functions
# ===========================

def create_pattern_rule(
    pattern: str,
    replacement: Union[str, Callable],
    domain: MathDomain,
    description: str,
    priority: int = 50,
    audience_levels: Optional[List[AudienceLevel]] = None
) -> PatternRule:
    """Factory function for creating pattern rules"""
    return PatternRule(
        pattern=pattern,
        replacement=replacement,
        domain=domain,
        description=description,
        priority=priority,
        audience_levels=audience_levels
    )

def natural_speech_wrapper(replacement_func: Callable) -> Callable:
    """Decorator to wrap replacement functions with natural speech improvements"""
    def wrapper(match):
        result = replacement_func(match)
        # Add natural speech improvements here if needed
        return result
    return wrapper