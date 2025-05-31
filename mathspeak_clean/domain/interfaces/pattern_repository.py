"""Pattern repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from mathspeak_clean.domain.entities.pattern import MathPattern
from mathspeak_clean.shared.constants import PatternDomain
from mathspeak_clean.shared.types import PatternPriority


class PatternRepository(ABC):
    """Abstract pattern repository interface.
    
    This interface defines the contract for pattern storage and retrieval.
    Implementations can use different storage mechanisms (memory, file, database).
    """
    
    @abstractmethod
    def add(self, pattern: MathPattern) -> None:
        """Add a pattern to the repository.
        
        Args:
            pattern: Pattern to add
            
        Raises:
            ValueError: If pattern already exists
        """
        pass
    
    @abstractmethod
    def get_by_id(self, pattern_id: str) -> Optional[MathPattern]:
        """Get pattern by ID.
        
        Args:
            pattern_id: Unique pattern identifier
            
        Returns:
            Pattern if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_by_domain(self, domain: PatternDomain) -> List[MathPattern]:
        """Get all patterns for a specific domain.
        
        Args:
            domain: Mathematical domain
            
        Returns:
            List of patterns for the domain
        """
        pass
    
    @abstractmethod
    def get_by_priority_range(
        self,
        min_priority: PatternPriority,
        max_priority: Optional[PatternPriority] = None,
    ) -> List[MathPattern]:
        """Get patterns within a priority range.
        
        Args:
            min_priority: Minimum priority (inclusive)
            max_priority: Maximum priority (inclusive), None for no upper bound
            
        Returns:
            List of patterns within the range
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[MathPattern]:
        """Get all patterns.
        
        Returns:
            List of all patterns
        """
        pass
    
    @abstractmethod
    def update(self, pattern_id: str, pattern: MathPattern) -> None:
        """Update an existing pattern.
        
        Args:
            pattern_id: ID of pattern to update
            pattern: Updated pattern data
            
        Raises:
            ValueError: If pattern not found
        """
        pass
    
    @abstractmethod
    def delete(self, pattern_id: str) -> None:
        """Delete a pattern.
        
        Args:
            pattern_id: ID of pattern to delete
            
        Raises:
            ValueError: If pattern not found
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total number of patterns.
        
        Returns:
            Total pattern count
        """
        pass
    
    @abstractmethod
    def count_by_domain(self, domain: PatternDomain) -> int:
        """Count patterns in a specific domain.
        
        Args:
            domain: Mathematical domain
            
        Returns:
            Pattern count for the domain
        """
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[MathPattern]:
        """Search patterns by text query.
        
        Args:
            query: Search query (searches pattern and description)
            
        Returns:
            List of matching patterns
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all patterns from repository."""
        pass