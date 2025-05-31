# MathSpeak Clean Architecture Implementation Guide

## Overview

This guide documents the Clean Architecture implementation for MathSpeak, a mathematical text-to-speech system. The new architecture maintains 100% backward compatibility while providing better maintainability, testability, and extensibility.

## Architecture Layers

### 1. Domain Layer (`mathspeak_clean/domain/`)
The innermost layer containing business logic with no external dependencies.

```
domain/
├── entities/           # Core business entities
│   ├── expression.py   # MathExpression entity
│   └── pattern.py      # MathPattern entity
├── interfaces/         # Abstract interfaces
│   └── pattern_repository.py
└── services/           # Domain services
    └── pattern_processor.py
```

**Key Components:**
- `MathExpression`: Core entity representing a LaTeX expression
- `MathPattern`: Entity for pattern matching rules
- `PatternProcessorService`: Core business logic for pattern processing

### 2. Application Layer (`mathspeak_clean/application/`)
Contains use cases that orchestrate domain logic.

```
application/
├── use_cases/          # Application use cases
│   └── process_expression.py
├── interfaces/         # Application-specific interfaces
└── dto/               # Data transfer objects
```

**Key Components:**
- `ProcessExpressionUseCase`: Orchestrates expression processing
- Request/Response DTOs for use case communication

### 3. Infrastructure Layer (`mathspeak_clean/infrastructure/`)
External concerns like databases, caching, and configuration.

```
infrastructure/
├── persistence/        # Data storage implementations
│   ├── memory_pattern_repository.py
│   └── lru_cache.py
├── config/            # Configuration management
│   └── settings.py
├── logging/           # Structured logging
│   └── logger.py
└── container.py       # Dependency injection
```

**Key Components:**
- `LRUCache`: High-performance caching implementation
- `Settings`: Comprehensive configuration management
- `Container`: Dependency injection container

### 4. Adapters Layer (`mathspeak_clean/adapters/`)
Adapters for integrating with legacy code and external systems.

```
adapters/
└── legacy_pattern_adapter.py  # Legacy patterns_v2.py compatibility
```

### 5. Presentation Layer (`mathspeak_clean/presentation/`)
User interfaces (API, CLI).

```
presentation/
├── api/               # REST API
│   └── app.py        # FastAPI application
└── cli/              # Command-line interface
```

## Key Design Patterns

### 1. Dependency Injection
All dependencies are injected through constructors:

```python
class ProcessExpressionUseCase:
    def __init__(
        self,
        pattern_processor: PatternProcessorService,
        cache: Optional[Cache] = None,
    ) -> None:
        self.pattern_processor = pattern_processor
        self.cache = cache
```

### 2. Repository Pattern
Abstract data access through interfaces:

```python
class PatternRepository(ABC):
    @abstractmethod
    def add(self, pattern: MathPattern) -> None:
        pass
    
    @abstractmethod
    def get_all(self) -> List[MathPattern]:
        pass
```

### 3. Use Case Pattern
Encapsulate business operations:

```python
@dataclass
class ProcessExpressionRequest:
    latex: LaTeXExpression
    audience_level: AudienceLevel

class ProcessExpressionUseCase:
    def execute(self, request: ProcessExpressionRequest) -> ProcessExpressionResponse:
        # Orchestrate domain logic
```

### 4. Adapter Pattern
Bridge between old and new code:

```python
class LegacyPatternAdapter:
    def process_legacy(self, latex: str) -> str:
        # Use legacy patterns_v2.py
```

## Type System

Comprehensive type hints throughout:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Cache(Protocol):
    def get(self, key: str) -> Optional[Any]: ...
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None: ...
```

## Error Handling

Hierarchical exception system:

```
MathSpeakError (base)
├── DomainError
│   ├── ValidationError
│   └── PatternError
├── ApplicationError
│   └── UseCaseError
└── InfrastructureError
    ├── TTSError
    ├── CacheError
    └── ConfigurationError
```

## Configuration Management

Environment-based configuration with validation:

```python
# From environment variables
MATHSPEAK_AUDIENCE_LEVEL=undergraduate
MATHSPEAK_CACHE_ENABLED=true
MATHSPEAK_LOG_LEVEL=INFO

# Or from JSON file
{
  "default_audience_level": "undergraduate",
  "cache_enabled": true,
  "cache_ttl": 3600
}
```

## Logging

Structured JSON logging with context:

```python
logger.info(
    "Processing expression",
    extra={
        "expression": latex,
        "complexity": complexity_score,
        "processing_time": duration,
    }
)
```

## Testing Strategy

### Unit Tests
Test individual components in isolation:

```python
def test_math_expression_validation():
    with pytest.raises(ValidationError):
        MathExpression("")  # Empty expression
```

### Integration Tests
Test component interactions:

```python
def test_process_expression_use_case():
    # Set up dependencies
    repository = MemoryPatternRepository()
    processor = PatternProcessorService(repository)
    use_case = ProcessExpressionUseCase(processor)
    
    # Test use case
    request = ProcessExpressionRequest("\\frac{1}{2}")
    response = use_case.execute(request)
    assert response.result.speech == "1 over 2"
```

### Devil Tests Compatibility
Ensure 100% backward compatibility:

```python
# All 150 devil tests must pass
assert passed == 150  # ✓
```

## Migration Guide

### Using Legacy Patterns
The system automatically loads legacy patterns:

```python
adapter = LegacyPatternAdapter()
adapter.initialize()  # Loads patterns from patterns_v2.py
```

### Gradual Migration
1. Start using clean architecture for new features
2. Gradually migrate existing code
3. Legacy adapter ensures compatibility

### API Migration
Old API calls continue to work:

```python
# Old way (still works)
from mathspeak.core.patterns_v2 import process_math_to_speech
result = process_math_to_speech("\\frac{1}{2}")

# New way (recommended)
container = get_container()
use_case = container.get(ProcessExpressionUseCase)
response = use_case.execute(ProcessExpressionRequest("\\frac{1}{2}"))
```

## Development Workflow

### 1. Setting Up Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run linting
flake8 mathspeak_clean/

# Run type checking
mypy mathspeak_clean/

# Format code
black mathspeak_clean/
```

### 2. Adding New Patterns
```python
# Create pattern entity
pattern = MathPattern(
    pattern=r"\\newcommand\{([^}]+)\}",
    replacement=r"new command \1",
    priority=PRIORITY_HIGH,
    domain=PatternDomain.GENERAL,
)

# Add to repository
repository.add(pattern)
```

### 3. Adding New Use Cases
1. Create request/response DTOs
2. Implement use case class
3. Register in container
4. Add API endpoint

## Performance Considerations

### Caching
- LRU cache with configurable size
- TTL-based expiration
- Cache hit rates tracked

### Pattern Matching
- Patterns sorted by priority
- Domain-specific filtering
- Compiled regex patterns

### Memory Management
- Singleton services
- Lazy initialization
- Proper cleanup

## Security

### Input Validation
- Expression length limits
- LaTeX syntax validation
- Balanced delimiters check

### Configuration
- Environment variable validation
- Type checking
- Range validation

## Future Enhancements

### Short-term
1. Add file-based pattern repository
2. Implement pattern hot-reloading
3. Add prometheus metrics

### Medium-term
1. Database pattern storage
2. Pattern versioning
3. A/B testing framework

### Long-term
1. Machine learning integration
2. Multi-language support
3. Plugin system

## Conclusion

The Clean Architecture implementation provides:
- ✅ 100% backward compatibility
- ✅ Better maintainability
- ✅ Comprehensive testing
- ✅ Type safety
- ✅ Dependency injection
- ✅ Structured logging
- ✅ Configuration management
- ✅ Error handling

All while maintaining the original 100% success rate on devil tests!