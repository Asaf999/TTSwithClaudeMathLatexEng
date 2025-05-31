#!/usr/bin/env python3
"""Test clean architecture implementation against devil tests."""

import sys
import time
from typing import List, Tuple

# Add paths
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

# Import clean architecture components
from mathspeak_clean.domain.entities.expression import MathExpression
from mathspeak_clean.domain.entities.pattern import MathPattern
from mathspeak_clean.domain.services.pattern_processor import PatternProcessorService
from mathspeak_clean.infrastructure.persistence.memory_pattern_repository import (
    MemoryPatternRepository,
)
from mathspeak_clean.infrastructure.persistence.lru_cache import LRUCache
from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionUseCase,
    ProcessExpressionRequest,
)
from mathspeak_clean.adapters.legacy_pattern_adapter import LegacyPatternAdapter
from mathspeak_clean.shared.constants import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PatternDomain,
)

# Import devil tests
from test_devil_patterns import get_devil_test_cases


def setup_clean_architecture():
    """Set up clean architecture components with legacy patterns."""
    print("Setting up clean architecture...")
    
    # Initialize adapter
    adapter = LegacyPatternAdapter()
    adapter.initialize()
    
    # Get pattern repository with legacy patterns
    pattern_repository = adapter.get_pattern_repository()
    
    # Add some critical patterns for devil tests
    critical_patterns = [
        # Nested fractions
        MathPattern(
            pattern=r"\\frac\{([^{}]+)\}\{([^{}]+)\}",
            replacement=r"\1 over \2",
            priority=PRIORITY_HIGH,
            domain=PatternDomain.GENERAL,
            description="Basic fraction"
        ),
        
        # Square root
        MathPattern(
            pattern=r"\\sqrt\{([^{}]+)\}",
            replacement=r"square root of \1",
            priority=PRIORITY_HIGH,
            domain=PatternDomain.GENERAL,
            description="Square root"
        ),
        
        # Exponents
        MathPattern(
            pattern=r"\^{([^{}]+)}",
            replacement=r" to the \1",
            priority=PRIORITY_HIGH,
            domain=PatternDomain.GENERAL,
            description="Exponent"
        ),
        
        # Integrals
        MathPattern(
            pattern=r"\\int_\{([^{}]+)\}\^\{([^{}]+)\}",
            replacement=r"integral from \1 to \2",
            priority=PRIORITY_HIGH,
            domain=PatternDomain.CALCULUS,
            description="Definite integral"
        ),
        
        # Limits
        MathPattern(
            pattern=r"\\lim_\{([^{}]+)\\to([^{}]+)\}",
            replacement=r"limit as \1 approaches \2",
            priority=PRIORITY_HIGH,
            domain=PatternDomain.CALCULUS,
            description="Limit"
        ),
        
        # Summation
        MathPattern(
            pattern=r"\\sum_\{([^{}]+)\}\^\{([^{}]+)\}",
            replacement=r"sum from \1 to \2",
            priority=PRIORITY_HIGH,
            domain=PatternDomain.CALCULUS,
            description="Summation"
        ),
        
        # Greek letters
        MathPattern(
            pattern=r"\\alpha",
            replacement="alpha",
            priority=PRIORITY_MEDIUM,
            domain=PatternDomain.GENERAL,
            description="Greek alpha"
        ),
        
        # Cleanup backslashes
        MathPattern(
            pattern=r"\\\\",
            replacement=" ",
            priority=PRIORITY_CRITICAL,
            domain=PatternDomain.GENERAL,
            description="Remove double backslashes"
        ),
    ]
    
    # Add critical patterns
    for pattern in critical_patterns:
        try:
            pattern_repository.add(pattern)
        except ValueError:
            # Pattern already exists
            pass
    
    # Create services
    pattern_processor = PatternProcessorService(pattern_repository)
    cache = LRUCache(max_size=1000)
    
    # Create use case
    use_case = ProcessExpressionUseCase(pattern_processor, cache)
    
    return use_case, adapter


def test_clean_architecture_against_devils():
    """Test clean architecture against devil test cases."""
    # Set up architecture
    use_case, adapter = setup_clean_architecture()
    
    # Get devil test cases
    devil_tests = get_devil_test_cases()
    
    print(f"\nTesting {len(devil_tests)} devil cases with clean architecture...")
    print("=" * 80)
    
    passed = 0
    failed = 0
    errors = 0
    
    # Test subset of devil tests
    test_subset = devil_tests[:20]  # Test first 20 for now
    
    for i, (latex, expected) in enumerate(test_subset, 1):
        try:
            # Create request
            request = ProcessExpressionRequest(
                latex=latex,
                audience_level="undergraduate",
                use_cache=True
            )
            
            # Process with clean architecture
            start_time = time.time()
            response = use_case.execute(request)
            clean_result = response.result.speech
            processing_time = time.time() - start_time
            
            # Process with legacy for comparison
            legacy_result = adapter.process_legacy(latex)
            
            # Normalize for comparison
            clean_normalized = clean_result.strip().lower()
            expected_normalized = expected.strip().lower()
            legacy_normalized = legacy_result.strip().lower()
            
            # Check results
            clean_match = clean_normalized == expected_normalized
            legacy_match = legacy_normalized == expected_normalized
            
            if clean_match:
                passed += 1
                status = "✅ PASS"
            else:
                failed += 1
                status = "❌ FAIL"
            
            print(f"{status} Test {i:3d}: {latex[:50]}...")
            print(f"   Expected: {expected[:60]}...")
            print(f"   Clean:    {clean_result[:60]}... ({processing_time:.3f}s)")
            print(f"   Legacy:   {legacy_result[:60]}... (match: {legacy_match})")
            
            if response.result.cache_hit:
                print("   (from cache)")
            
            print()
            
        except Exception as e:
            errors += 1
            print(f"❌ ERROR Test {i}: {latex[:50]}...")
            print(f"   Error: {e}")
            print()
    
    # Print summary
    print("=" * 80)
    print("CLEAN ARCHITECTURE TEST SUMMARY")
    print("=" * 80)
    print(f"Total tests: {len(test_subset)}")
    print(f"Passed:      {passed} ({passed/len(test_subset)*100:.1f}%)")
    print(f"Failed:      {failed} ({failed/len(test_subset)*100:.1f}%)")
    print(f"Errors:      {errors} ({errors/len(test_subset)*100:.1f}%)")
    
    # Get cache stats
    cache_stats = use_case.cache.get_stats()
    print(f"\nCache stats: {cache_stats}")
    
    # Get pattern stats
    pattern_stats = use_case.pattern_processor.get_pattern_statistics()
    print(f"\nPattern stats: {pattern_stats}")
    
    return passed == len(test_subset)


if __name__ == "__main__":
    success = test_clean_architecture_against_devils()
    sys.exit(0 if success else 1)