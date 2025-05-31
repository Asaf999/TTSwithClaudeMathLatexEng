"""Adapter for legacy patterns_v2.py compatibility."""

import logging
from typing import Any, List, Optional

from mathspeak_clean.domain.entities.expression import MathExpression
from mathspeak_clean.domain.entities.pattern import MathPattern
from mathspeak_clean.domain.interfaces.pattern_repository import PatternRepository
from mathspeak_clean.infrastructure.persistence.memory_pattern_repository import (
    MemoryPatternRepository,
)
from mathspeak_clean.shared.constants import (
    PRIORITY_CRITICAL,
    PRIORITY_DEFAULT,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PatternDomain,
)
from mathspeak_clean.shared.types import LaTeXExpression, SpeechText

logger = logging.getLogger(__name__)


class LegacyPatternAdapter:
    """Adapter to use legacy patterns_v2.py with new architecture.
    
    This adapter allows gradual migration from the old monolithic
    patterns_v2.py to the new clean architecture.
    """
    
    def __init__(self) -> None:
        """Initialize adapter with legacy module."""
        self._legacy_module = None
        self._pattern_repository: PatternRepository = MemoryPatternRepository()
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the adapter by loading legacy patterns."""
        if self._initialized:
            return
        
        try:
            # Import legacy module
            from mathspeak.core import patterns_v2
            self._legacy_module = patterns_v2
            
            # Extract patterns from legacy module
            self._extract_legacy_patterns()
            
            self._initialized = True
            logger.info("Legacy pattern adapter initialized successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import legacy patterns_v2: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize legacy adapter: {e}")
            raise
    
    def process_legacy(
        self,
        latex: LaTeXExpression,
        audience_level: str = "undergraduate"
    ) -> SpeechText:
        """Process expression using legacy module directly.
        
        Args:
            latex: LaTeX expression
            audience_level: Target audience
            
        Returns:
            Speech text
        """
        if not self._initialized:
            self.initialize()
        
        if self._legacy_module is None:
            raise RuntimeError("Legacy module not loaded")
        
        # Convert audience level to legacy format
        legacy_level = self._convert_audience_level(audience_level)
        
        # Call legacy function
        return self._legacy_module.process_math_to_speech(latex, legacy_level)
    
    def get_pattern_repository(self) -> PatternRepository:
        """Get pattern repository with extracted patterns.
        
        Returns:
            Pattern repository
        """
        if not self._initialized:
            self.initialize()
        
        return self._pattern_repository
    
    def _extract_legacy_patterns(self) -> None:
        """Extract patterns from legacy module."""
        if self._legacy_module is None:
            return
        
        # Common pattern categories in legacy code
        pattern_categories = {
            # High priority patterns
            "matrix_patterns": (PatternDomain.LINEAR_ALGEBRA, PRIORITY_HIGH),
            "integral_patterns": (PatternDomain.CALCULUS, PRIORITY_HIGH),
            "derivative_patterns": (PatternDomain.CALCULUS, PRIORITY_HIGH),
            "limit_patterns": (PatternDomain.CALCULUS, PRIORITY_HIGH),
            "sum_patterns": (PatternDomain.CALCULUS, PRIORITY_MEDIUM),
            
            # Medium priority patterns
            "fraction_patterns": (PatternDomain.GENERAL, PRIORITY_MEDIUM),
            "greek_patterns": (PatternDomain.GENERAL, PRIORITY_MEDIUM),
            "function_patterns": (PatternDomain.GENERAL, PRIORITY_MEDIUM),
            
            # Low priority patterns
            "symbol_patterns": (PatternDomain.GENERAL, PRIORITY_LOW),
            "cleanup_patterns": (PatternDomain.GENERAL, PRIORITY_LOW),
        }
        
        patterns_added = 0
        
        # Extract patterns from legacy module attributes
        for attr_name in dir(self._legacy_module):
            attr_value = getattr(self._legacy_module, attr_name)
            
            # Look for pattern lists
            if isinstance(attr_value, list) and attr_name.endswith("_patterns"):
                domain, priority = pattern_categories.get(
                    attr_name,
                    (PatternDomain.GENERAL, PRIORITY_DEFAULT)
                )
                
                for item in attr_value:
                    if isinstance(item, tuple) and len(item) >= 2:
                        pattern_str, replacement = item[0], item[1]
                        
                        try:
                            pattern = MathPattern(
                                pattern=pattern_str,
                                replacement=replacement,
                                priority=priority,
                                domain=domain,
                                description=f"Legacy pattern from {attr_name}",
                            )
                            self._pattern_repository.add(pattern)
                            patterns_added += 1
                            
                        except Exception as e:
                            logger.warning(
                                f"Failed to convert legacy pattern {pattern_str}: {e}"
                            )
        
        logger.info(f"Extracted {patterns_added} patterns from legacy module")
    
    def _convert_audience_level(self, level: str) -> Any:
        """Convert audience level to legacy format.
        
        Args:
            level: New audience level
            
        Returns:
            Legacy audience level
        """
        if self._legacy_module is None:
            return level
        
        # Try to get AudienceLevel enum from legacy module
        if hasattr(self._legacy_module, "AudienceLevel"):
            audience_enum = self._legacy_module.AudienceLevel
            
            # Map string to enum
            level_map = {
                "elementary": "ELEMENTARY",
                "high_school": "HIGH_SCHOOL",
                "undergraduate": "UNDERGRADUATE",
                "graduate": "GRADUATE",
                "research": "RESEARCH",
            }
            
            enum_name = level_map.get(level, "UNDERGRADUATE")
            if hasattr(audience_enum, enum_name):
                return getattr(audience_enum, enum_name)
        
        return level
    
    def migrate_pattern(self, pattern: MathPattern) -> bool:
        """Migrate a pattern to the new system.
        
        Args:
            pattern: Pattern to migrate
            
        Returns:
            True if migration successful
        """
        try:
            self._pattern_repository.add(pattern)
            return True
        except Exception as e:
            logger.error(f"Failed to migrate pattern {pattern}: {e}")
            return False
    
    def get_migration_status(self) -> dict:
        """Get migration status information.
        
        Returns:
            Dictionary with migration status
        """
        if not self._initialized:
            return {
                "initialized": False,
                "patterns_extracted": 0,
                "legacy_available": False,
            }
        
        stats = self._pattern_repository.count()
        
        return {
            "initialized": True,
            "patterns_extracted": stats,
            "legacy_available": self._legacy_module is not None,
            "pattern_domains": {
                domain.value: self._pattern_repository.count_by_domain(domain)
                for domain in PatternDomain
            },
        }