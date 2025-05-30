"""Unit tests for patterns base classes."""

import pytest
from unittest.mock import Mock
from core.patterns.base import (
    AudienceLevel,
    MathDomain,
    PatternRule,
    PatternHandler,
    DomainProcessor
)


class TestAudienceLevel:
    """Test AudienceLevel enum."""
    
    def test_audience_levels_exist(self):
        """Test all expected audience levels exist."""
        assert AudienceLevel.ELEMENTARY
        assert AudienceLevel.MIDDLE_SCHOOL
        assert AudienceLevel.HIGH_SCHOOL
        assert AudienceLevel.UNDERGRADUATE
        assert AudienceLevel.GRADUATE
        assert AudienceLevel.RESEARCH
    
    def test_audience_level_values(self):
        """Test audience level values are strings."""
        for level in AudienceLevel:
            assert isinstance(level.value, str)
            assert len(level.value) > 0


class TestMathDomain:
    """Test MathDomain enum."""
    
    def test_math_domains_exist(self):
        """Test all expected math domains exist."""
        assert MathDomain.ARITHMETIC
        assert MathDomain.ALGEBRA
        assert MathDomain.CALCULUS
        assert MathDomain.LINEAR_ALGEBRA
        assert MathDomain.STATISTICS
        assert MathDomain.LOGIC
        assert MathDomain.TOPOLOGY
    
    def test_domain_values(self):
        """Test domain values are strings."""
        for domain in MathDomain:
            assert isinstance(domain.value, str)
            assert len(domain.value) > 0


class TestPatternRule:
    """Test PatternRule class."""
    
    def test_pattern_rule_creation(self):
        """Test PatternRule can be created with required fields."""
        rule = PatternRule(
            pattern=r"\\frac\{(.+?)\}\{(.+?)\}",
            replacement="fraction {0} over {1}",
            priority=10,
            domain=MathDomain.ARITHMETIC,
            audience_level=AudienceLevel.HIGH_SCHOOL
        )
        
        assert rule.pattern == r"\\frac\{(.+?)\}\{(.+?)\}"
        assert rule.replacement == "fraction {0} over {1}"
        assert rule.priority == 10
        assert rule.domain == MathDomain.ARITHMETIC
        assert rule.audience_level == AudienceLevel.HIGH_SCHOOL
        assert rule.description == ""
        assert rule.examples == []
    
    def test_pattern_rule_with_optional_fields(self):
        """Test PatternRule with optional fields."""
        examples = ["\\frac{1}{2}", "\\frac{x}{y}"]
        rule = PatternRule(
            pattern=r"\\frac\{(.+?)\}\{(.+?)\}",
            replacement="fraction {0} over {1}",
            priority=10,
            domain=MathDomain.ARITHMETIC,
            audience_level=AudienceLevel.HIGH_SCHOOL,
            description="Fraction notation",
            examples=examples
        )
        
        assert rule.description == "Fraction notation"
        assert rule.examples == examples
    
    def test_pattern_rule_equality(self):
        """Test PatternRule equality comparison."""
        rule1 = PatternRule(
            pattern=r"\\frac\{(.+?)\}\{(.+?)\}",
            replacement="fraction {0} over {1}",
            priority=10,
            domain=MathDomain.ARITHMETIC,
            audience_level=AudienceLevel.HIGH_SCHOOL
        )
        
        rule2 = PatternRule(
            pattern=r"\\frac\{(.+?)\}\{(.+?)\}",
            replacement="fraction {0} over {1}",
            priority=10,
            domain=MathDomain.ARITHMETIC,
            audience_level=AudienceLevel.HIGH_SCHOOL
        )
        
        assert rule1 == rule2
    
    def test_pattern_rule_sorting(self):
        """Test PatternRule sorts by priority."""
        rule1 = PatternRule(
            pattern=r"pattern1",
            replacement="replacement1",
            priority=5,
            domain=MathDomain.ARITHMETIC,
            audience_level=AudienceLevel.HIGH_SCHOOL
        )
        
        rule2 = PatternRule(
            pattern=r"pattern2",
            replacement="replacement2",
            priority=10,
            domain=MathDomain.ARITHMETIC,
            audience_level=AudienceLevel.HIGH_SCHOOL
        )
        
        rules = [rule1, rule2]
        sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)
        
        assert sorted_rules[0] == rule2  # Higher priority first
        assert sorted_rules[1] == rule1


class TestPatternHandler:
    """Test PatternHandler abstract base class."""
    
    def test_cannot_instantiate_directly(self):
        """Test PatternHandler cannot be instantiated directly."""
        with pytest.raises(TypeError):
            PatternHandler()
    
    def test_concrete_implementation(self):
        """Test concrete implementation of PatternHandler."""
        class ConcreteHandler(PatternHandler):
            @property
            def domain(self):
                return MathDomain.ARITHMETIC
            
            @property
            def name(self):
                return "TestHandler"
            
            def get_patterns(self, audience_level=None):
                return [
                    PatternRule(
                        pattern=r"test",
                        replacement="TEST",
                        priority=1,
                        domain=self.domain,
                        audience_level=AudienceLevel.HIGH_SCHOOL
                    )
                ]
            
            def process_match(self, match, audience_level=None):
                return "processed"
        
        handler = ConcreteHandler()
        assert handler.domain == MathDomain.ARITHMETIC
        assert handler.name == "TestHandler"
        
        patterns = handler.get_patterns()
        assert len(patterns) == 1
        assert patterns[0].pattern == r"test"
        
        result = handler.process_match(Mock())
        assert result == "processed"
    
    def test_filter_patterns_by_audience(self):
        """Test filtering patterns by audience level."""
        class ConcreteHandler(PatternHandler):
            @property
            def domain(self):
                return MathDomain.ARITHMETIC
            
            @property
            def name(self):
                return "TestHandler"
            
            def get_patterns(self, audience_level=None):
                all_patterns = [
                    PatternRule(
                        pattern=r"basic",
                        replacement="BASIC",
                        priority=1,
                        domain=self.domain,
                        audience_level=AudienceLevel.ELEMENTARY
                    ),
                    PatternRule(
                        pattern=r"advanced",
                        replacement="ADVANCED",
                        priority=1,
                        domain=self.domain,
                        audience_level=AudienceLevel.GRADUATE
                    )
                ]
                
                if audience_level:
                    # Simple filtering logic for test
                    return [p for p in all_patterns if p.audience_level == audience_level]
                return all_patterns
            
            def process_match(self, match, audience_level=None):
                return "processed"
        
        handler = ConcreteHandler()
        
        # Get all patterns
        all_patterns = handler.get_patterns()
        assert len(all_patterns) == 2
        
        # Get elementary patterns only
        elementary_patterns = handler.get_patterns(AudienceLevel.ELEMENTARY)
        assert len(elementary_patterns) == 1
        assert elementary_patterns[0].pattern == r"basic"


class TestDomainProcessor:
    """Test DomainProcessor abstract base class."""
    
    def test_cannot_instantiate_directly(self):
        """Test DomainProcessor cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DomainProcessor()
    
    def test_concrete_implementation(self):
        """Test concrete implementation of DomainProcessor."""
        class ConcreteDomainProcessor(DomainProcessor):
            @property
            def domain(self):
                return MathDomain.ARITHMETIC
            
            @property
            def name(self):
                return "TestProcessor"
            
            def process(self, text, context=None):
                return f"processed: {text}"
            
            def can_handle(self, text):
                return "test" in text.lower()
        
        processor = ConcreteDomainProcessor()
        assert processor.domain == MathDomain.ARITHMETIC
        assert processor.name == "TestProcessor"
        
        # Test processing
        result = processor.process("test input")
        assert result == "processed: test input"
        
        # Test can_handle
        assert processor.can_handle("This is a test")
        assert not processor.can_handle("This is not")
    
    def test_processor_with_context(self):
        """Test processor that uses context."""
        class ContextAwareProcessor(DomainProcessor):
            @property
            def domain(self):
                return MathDomain.ARITHMETIC
            
            @property
            def name(self):
                return "ContextProcessor"
            
            def process(self, text, context=None):
                if context and context.get('verbose'):
                    return f"verbose: {text}"
                return f"simple: {text}"
            
            def can_handle(self, text):
                return True
        
        processor = ContextAwareProcessor()
        
        # Without context
        result = processor.process("test")
        assert result == "simple: test"
        
        # With context
        result = processor.process("test", {"verbose": True})
        assert result == "verbose: test"