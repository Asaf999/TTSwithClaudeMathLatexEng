"""Pattern entity for mathematical expression matching."""

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Pattern

from mathspeak_clean.shared.constants import PRIORITY_DEFAULT, PatternDomain
from mathspeak_clean.shared.exceptions import PatternSyntaxError, ValidationError
from mathspeak_clean.shared.types import PatternPriority, PatternTransform


@dataclass
class MathPattern:
    """Mathematical pattern entity.
    
    Represents a pattern for matching and transforming mathematical expressions.
    """
    
    pattern: str
    replacement: str
    priority: PatternPriority = PRIORITY_DEFAULT
    domain: PatternDomain = PatternDomain.GENERAL
    description: Optional[str] = None
    flags: int = 0
    transform: Optional[PatternTransform] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    _compiled: Optional[Pattern[str]] = field(default=None, init=False)
    
    def __post_init__(self) -> None:
        """Compile and validate pattern after initialization."""
        self.validate()
        self._compile()
    
    def validate(self) -> None:
        """Validate the pattern.
        
        Raises:
            ValidationError: If pattern is invalid
            PatternSyntaxError: If regex syntax is invalid
        """
        if not self.pattern:
            raise ValidationError("pattern", "Pattern cannot be empty")
        
        if not self.replacement and not self.transform:
            raise ValidationError(
                "replacement",
                "Either replacement string or transform function must be provided"
            )
        
        if self.priority < 0:
            raise ValidationError(
                "priority",
                "Priority must be non-negative",
                self.priority
            )
        
        # Validate regex syntax
        try:
            re.compile(self.pattern, self.flags)
        except re.error as e:
            raise PatternSyntaxError(self.pattern, str(e))
    
    def _compile(self) -> None:
        """Compile the regex pattern."""
        try:
            self._compiled = re.compile(self.pattern, self.flags)
        except re.error as e:
            raise PatternSyntaxError(self.pattern, f"Failed to compile: {e}")
    
    @property
    def compiled(self) -> Pattern[str]:
        """Get compiled regex pattern.
        
        Returns:
            Compiled pattern
            
        Raises:
            RuntimeError: If pattern not compiled
        """
        if self._compiled is None:
            raise RuntimeError("Pattern not compiled")
        return self._compiled
    
    def match(self, text: str) -> Optional[re.Match[str]]:
        """Match pattern against text.
        
        Args:
            text: Text to match against
            
        Returns:
            Match object if pattern matches, None otherwise
        """
        return self.compiled.search(text)
    
    def find_all(self, text: str) -> list[re.Match[str]]:
        """Find all matches in text.
        
        Args:
            text: Text to search in
            
        Returns:
            List of match objects
        """
        return list(self.compiled.finditer(text))
    
    def apply(self, text: str) -> str:
        """Apply pattern transformation to text.
        
        Args:
            text: Text to transform
            
        Returns:
            Transformed text
        """
        if self.transform:
            # Use custom transform function
            matches = self.find_all(text)
            result = text
            
            # Apply transform in reverse order to preserve positions
            for match in reversed(matches):
                transformed = self.transform(match.group(0))
                result = result[:match.start()] + transformed + result[match.end():]
            
            return result
        else:
            # Use regex replacement
            return self.compiled.sub(self.replacement, text)
    
    def count_matches(self, text: str) -> int:
        """Count number of matches in text.
        
        Args:
            text: Text to search in
            
        Returns:
            Number of matches
        """
        return len(self.find_all(text))
    
    @property
    def is_simple(self) -> bool:
        """Check if pattern is a simple string replacement."""
        # Check if pattern contains regex metacharacters
        metacharacters = r".^$*+?{}[]|()\\"
        return not any(char in self.pattern for char in metacharacters)
    
    @property
    def complexity_score(self) -> int:
        """Calculate complexity score of the pattern.
        
        Returns:
            Complexity score (0-100)
        """
        score = 0
        
        # Regex metacharacters
        metacharacters = r".^$*+?{}[]|()\\"
        meta_count = sum(1 for char in self.pattern if char in metacharacters)
        score += min(meta_count * 5, 30)
        
        # Capturing groups
        group_count = self.pattern.count("(") - self.pattern.count("\\(")
        score += min(group_count * 10, 30)
        
        # Pattern length
        length_factor = min(len(self.pattern) // 10, 20)
        score += length_factor
        
        # Lookarounds
        if "(?=" in self.pattern or "(?!" in self.pattern:
            score += 10
        if "(?<=" in self.pattern or "(?<!" in self.pattern:
            score += 10
        
        return min(score, 100)
    
    def __str__(self) -> str:
        """String representation."""
        return f"MathPattern({self.pattern[:30]}{'...' if len(self.pattern) > 30 else ''} -> {self.replacement[:30]}{'...' if len(self.replacement) > 30 else ''})"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"MathPattern(pattern={self.pattern!r}, "
            f"replacement={self.replacement!r}, "
            f"priority={self.priority}, "
            f"domain={self.domain.value})"
        )
    
    def __lt__(self, other: "MathPattern") -> bool:
        """Compare patterns by priority (higher priority first)."""
        return self.priority > other.priority