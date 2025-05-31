"""Domain service for pattern processing."""

import logging
import time
from typing import List, Optional, Tuple

from mathspeak_clean.domain.entities.expression import MathExpression
from mathspeak_clean.domain.entities.pattern import MathPattern
from mathspeak_clean.domain.interfaces.pattern_repository import PatternRepository
from mathspeak_clean.shared.constants import (
    DEFAULT_PATTERN_TIMEOUT,
    PRIORITY_CRITICAL,
    PatternDomain,
)
from mathspeak_clean.shared.exceptions import PatternMatchError, ProcessingError, TimeoutError
from mathspeak_clean.shared.types import PatternMatch, SpeechText

logger = logging.getLogger(__name__)


class PatternProcessorService:
    """Domain service for processing mathematical patterns.
    
    This service encapsulates the core business logic for converting
    mathematical expressions to speech using pattern matching.
    """
    
    def __init__(
        self,
        pattern_repository: PatternRepository,
        timeout: float = DEFAULT_PATTERN_TIMEOUT,
    ) -> None:
        """Initialize pattern processor service.
        
        Args:
            pattern_repository: Repository for pattern storage
            timeout: Maximum processing time in seconds
        """
        self.pattern_repository = pattern_repository
        self.timeout = timeout
        self._pattern_cache: Optional[List[MathPattern]] = None
    
    def process_expression(self, expression: MathExpression) -> SpeechText:
        """Process mathematical expression to speech text.
        
        Args:
            expression: Mathematical expression to process
            
        Returns:
            Speech text representation
            
        Raises:
            ProcessingError: If processing fails
            TimeoutError: If processing times out
        """
        start_time = time.time()
        
        # Get relevant patterns
        patterns = self._get_relevant_patterns(expression)
        
        # Apply patterns in priority order
        result = expression.latex
        applied_patterns: List[PatternMatch] = []
        
        for pattern in patterns:
            if time.time() - start_time > self.timeout:
                raise TimeoutError("pattern_processing", self.timeout)
            
            try:
                matches_before = pattern.count_matches(result)
                if matches_before > 0:
                    new_result = pattern.apply(result)
                    
                    if new_result != result:
                        # Pattern was successfully applied
                        applied_patterns.append(
                            PatternMatch(
                                pattern=pattern.pattern,
                                replacement=pattern.replacement,
                                position=(0, len(result)),  # Simplified for now
                                priority=pattern.priority,
                                domain=pattern.domain.value,
                            )
                        )
                        result = new_result
                        
                        logger.debug(
                            f"Applied pattern '{pattern.description or pattern.pattern}' "
                            f"({matches_before} matches)"
                        )
                        
            except Exception as e:
                logger.warning(f"Error applying pattern {pattern}: {e}")
                # Continue with other patterns
        
        # Post-process the result
        result = self._post_process(result, expression.audience_level)
        
        # Validate result
        if not result or result == expression.latex:
            raise ProcessingError(
                expression.latex,
                "pattern_processing",
                "No patterns matched the expression"
            )
        
        return result
    
    def _get_relevant_patterns(self, expression: MathExpression) -> List[MathPattern]:
        """Get patterns relevant to the expression.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Sorted list of relevant patterns
        """
        if self._pattern_cache is None:
            self._refresh_pattern_cache()
        
        patterns = self._pattern_cache or []
        
        # Filter patterns based on expression content and complexity
        relevant_patterns = []
        
        # Always include critical patterns
        critical_patterns = [
            p for p in patterns
            if p.priority >= PRIORITY_CRITICAL
        ]
        relevant_patterns.extend(critical_patterns)
        
        # Add domain-specific patterns based on expression content
        domains_to_check = self._detect_domains(expression)
        for domain in domains_to_check:
            domain_patterns = [
                p for p in patterns
                if p.domain == domain and p not in relevant_patterns
            ]
            relevant_patterns.extend(domain_patterns)
        
        # Add general patterns
        general_patterns = [
            p for p in patterns
            if p.domain == PatternDomain.GENERAL and p not in relevant_patterns
        ]
        relevant_patterns.extend(general_patterns)
        
        # Sort by priority (highest first)
        relevant_patterns.sort(key=lambda p: p.priority, reverse=True)
        
        return relevant_patterns
    
    def _detect_domains(self, expression: MathExpression) -> List[PatternDomain]:
        """Detect mathematical domains present in expression.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            List of detected domains
        """
        domains = []
        
        # Domain detection based on keywords and commands
        domain_indicators = {
            PatternDomain.CALCULUS: [
                "int", "integral", "derivative", "partial", "nabla",
                "lim", "limit", "dx", "dy", "dt"
            ],
            PatternDomain.LINEAR_ALGEBRA: [
                "matrix", "pmatrix", "bmatrix", "vmatrix", "det",
                "determinant", "transpose", "inverse", "eigenvalue"
            ],
            PatternDomain.STATISTICS: [
                "sum", "prod", "mean", "variance", "std", "probability",
                "expect", "var", "cov", "corr"
            ],
            PatternDomain.SET_THEORY: [
                "cup", "cap", "subset", "superset", "in", "notin",
                "emptyset", "setminus", "complement"
            ],
            PatternDomain.LOGIC: [
                "forall", "exists", "land", "lor", "neg", "implies",
                "iff", "therefore", "because"
            ],
            PatternDomain.NUMBER_THEORY: [
                "mod", "gcd", "lcm", "prime", "divides", "coprime"
            ],
            PatternDomain.COMPLEX_ANALYSIS: [
                "complex", "imag", "real", "conjugate", "arg", "abs"
            ],
        }
        
        for domain, keywords in domain_indicators.items():
            if expression.contains_domain(keywords):
                domains.append(domain)
        
        # Always include general domain as fallback
        domains.append(PatternDomain.GENERAL)
        
        return domains
    
    def _post_process(self, text: str, audience_level: str) -> str:
        """Post-process the speech text.
        
        Args:
            text: Raw speech text
            audience_level: Target audience level
            
        Returns:
            Post-processed speech text
        """
        # Remove extra spaces
        text = " ".join(text.split())
        
        # Apply audience-specific adjustments
        if audience_level in ["elementary", "high_school"]:
            # Simplify language for younger audiences
            text = text.replace("with respect to", "by")
            text = text.replace("such that", "where")
            text = text.replace("for all", "for every")
        
        # Fix common speech issues
        text = text.replace(" .", ".")
        text = text.replace(" ,", ",")
        text = text.replace("  ", " ")
        
        # Ensure proper capitalization
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text.strip()
    
    def _refresh_pattern_cache(self) -> None:
        """Refresh the pattern cache from repository."""
        try:
            self._pattern_cache = self.pattern_repository.get_all()
            logger.info(f"Loaded {len(self._pattern_cache)} patterns into cache")
        except Exception as e:
            logger.error(f"Failed to load patterns: {e}")
            self._pattern_cache = []
    
    def add_pattern(self, pattern: MathPattern) -> None:
        """Add a new pattern.
        
        Args:
            pattern: Pattern to add
        """
        self.pattern_repository.add(pattern)
        self._refresh_pattern_cache()
    
    def get_pattern_statistics(self) -> dict:
        """Get statistics about patterns.
        
        Returns:
            Dictionary with pattern statistics
        """
        if self._pattern_cache is None:
            self._refresh_pattern_cache()
        
        patterns = self._pattern_cache or []
        
        stats = {
            "total_patterns": len(patterns),
            "patterns_by_domain": {},
            "patterns_by_priority": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "default": 0,
            },
            "average_complexity": 0,
        }
        
        # Count by domain
        for domain in PatternDomain:
            count = sum(1 for p in patterns if p.domain == domain)
            if count > 0:
                stats["patterns_by_domain"][domain.value] = count
        
        # Count by priority
        for pattern in patterns:
            if pattern.priority >= 1000:
                stats["patterns_by_priority"]["critical"] += 1
            elif pattern.priority >= 750:
                stats["patterns_by_priority"]["high"] += 1
            elif pattern.priority >= 500:
                stats["patterns_by_priority"]["medium"] += 1
            elif pattern.priority >= 250:
                stats["patterns_by_priority"]["low"] += 1
            else:
                stats["patterns_by_priority"]["default"] += 1
        
        # Calculate average complexity
        if patterns:
            total_complexity = sum(p.complexity_score for p in patterns)
            stats["average_complexity"] = total_complexity / len(patterns)
        
        return stats