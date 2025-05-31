"""In-memory implementation of pattern repository."""

import uuid
from typing import Dict, List, Optional

from mathspeak_clean.domain.entities.pattern import MathPattern
from mathspeak_clean.domain.interfaces.pattern_repository import PatternRepository
from mathspeak_clean.shared.constants import PatternDomain
from mathspeak_clean.shared.types import PatternPriority


class MemoryPatternRepository(PatternRepository):
    """In-memory implementation of pattern repository.
    
    This implementation stores patterns in memory. Suitable for development
    and testing, but patterns are lost when the application restarts.
    """
    
    def __init__(self) -> None:
        """Initialize empty repository."""
        self._patterns: Dict[str, MathPattern] = {}
        self._domain_index: Dict[PatternDomain, List[str]] = {}
        self._priority_index: Dict[int, List[str]] = {}
    
    def add(self, pattern: MathPattern) -> None:
        """Add a pattern to the repository.
        
        Args:
            pattern: Pattern to add
            
        Raises:
            ValueError: If pattern already exists
        """
        # Generate unique ID
        pattern_id = str(uuid.uuid4())
        
        # Check for duplicate patterns
        for existing_id, existing_pattern in self._patterns.items():
            if (existing_pattern.pattern == pattern.pattern and
                existing_pattern.domain == pattern.domain):
                raise ValueError(
                    f"Pattern already exists with ID {existing_id}: {pattern.pattern}"
                )
        
        # Store pattern
        self._patterns[pattern_id] = pattern
        
        # Update domain index
        if pattern.domain not in self._domain_index:
            self._domain_index[pattern.domain] = []
        self._domain_index[pattern.domain].append(pattern_id)
        
        # Update priority index
        if pattern.priority not in self._priority_index:
            self._priority_index[pattern.priority] = []
        self._priority_index[pattern.priority].append(pattern_id)
    
    def get_by_id(self, pattern_id: str) -> Optional[MathPattern]:
        """Get pattern by ID.
        
        Args:
            pattern_id: Unique pattern identifier
            
        Returns:
            Pattern if found, None otherwise
        """
        return self._patterns.get(pattern_id)
    
    def get_by_domain(self, domain: PatternDomain) -> List[MathPattern]:
        """Get all patterns for a specific domain.
        
        Args:
            domain: Mathematical domain
            
        Returns:
            List of patterns for the domain
        """
        pattern_ids = self._domain_index.get(domain, [])
        return [self._patterns[pid] for pid in pattern_ids]
    
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
        patterns = []
        
        for priority, pattern_ids in self._priority_index.items():
            if priority >= min_priority:
                if max_priority is None or priority <= max_priority:
                    patterns.extend(self._patterns[pid] for pid in pattern_ids)
        
        # Sort by priority (highest first)
        patterns.sort(key=lambda p: p.priority, reverse=True)
        return patterns
    
    def get_all(self) -> List[MathPattern]:
        """Get all patterns.
        
        Returns:
            List of all patterns
        """
        patterns = list(self._patterns.values())
        # Sort by priority (highest first)
        patterns.sort(key=lambda p: p.priority, reverse=True)
        return patterns
    
    def update(self, pattern_id: str, pattern: MathPattern) -> None:
        """Update an existing pattern.
        
        Args:
            pattern_id: ID of pattern to update
            pattern: Updated pattern data
            
        Raises:
            ValueError: If pattern not found
        """
        if pattern_id not in self._patterns:
            raise ValueError(f"Pattern not found: {pattern_id}")
        
        old_pattern = self._patterns[pattern_id]
        
        # Update indices if domain or priority changed
        if old_pattern.domain != pattern.domain:
            # Remove from old domain index
            if old_pattern.domain in self._domain_index:
                self._domain_index[old_pattern.domain].remove(pattern_id)
            
            # Add to new domain index
            if pattern.domain not in self._domain_index:
                self._domain_index[pattern.domain] = []
            self._domain_index[pattern.domain].append(pattern_id)
        
        if old_pattern.priority != pattern.priority:
            # Remove from old priority index
            if old_pattern.priority in self._priority_index:
                self._priority_index[old_pattern.priority].remove(pattern_id)
            
            # Add to new priority index
            if pattern.priority not in self._priority_index:
                self._priority_index[pattern.priority] = []
            self._priority_index[pattern.priority].append(pattern_id)
        
        # Update pattern
        self._patterns[pattern_id] = pattern
    
    def delete(self, pattern_id: str) -> None:
        """Delete a pattern.
        
        Args:
            pattern_id: ID of pattern to delete
            
        Raises:
            ValueError: If pattern not found
        """
        if pattern_id not in self._patterns:
            raise ValueError(f"Pattern not found: {pattern_id}")
        
        pattern = self._patterns[pattern_id]
        
        # Remove from indices
        if pattern.domain in self._domain_index:
            self._domain_index[pattern.domain].remove(pattern_id)
        
        if pattern.priority in self._priority_index:
            self._priority_index[pattern.priority].remove(pattern_id)
        
        # Delete pattern
        del self._patterns[pattern_id]
    
    def count(self) -> int:
        """Count total number of patterns.
        
        Returns:
            Total pattern count
        """
        return len(self._patterns)
    
    def count_by_domain(self, domain: PatternDomain) -> int:
        """Count patterns in a specific domain.
        
        Args:
            domain: Mathematical domain
            
        Returns:
            Pattern count for the domain
        """
        return len(self._domain_index.get(domain, []))
    
    def search(self, query: str) -> List[MathPattern]:
        """Search patterns by text query.
        
        Args:
            query: Search query (searches pattern and description)
            
        Returns:
            List of matching patterns
        """
        query_lower = query.lower()
        matching_patterns = []
        
        for pattern in self._patterns.values():
            # Search in pattern regex
            if query_lower in pattern.pattern.lower():
                matching_patterns.append(pattern)
                continue
            
            # Search in replacement
            if query_lower in pattern.replacement.lower():
                matching_patterns.append(pattern)
                continue
            
            # Search in description
            if pattern.description and query_lower in pattern.description.lower():
                matching_patterns.append(pattern)
        
        # Sort by priority
        matching_patterns.sort(key=lambda p: p.priority, reverse=True)
        return matching_patterns
    
    def clear(self) -> None:
        """Clear all patterns from repository."""
        self._patterns.clear()
        self._domain_index.clear()
        self._priority_index.clear()