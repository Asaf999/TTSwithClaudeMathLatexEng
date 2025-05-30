# MathSpeak API Reference

## Overview

MathSpeak is a comprehensive mathematical text-to-speech system that converts LaTeX mathematical expressions into natural spoken language. The system supports multiple TTS engines, voice roles, and audience levels.

## Core Classes

### MathematicalTTSEngine

The main engine class that orchestrates mathematical text processing and speech generation.

```python
from core.engine import MathematicalTTSEngine
from core.patterns_v2 import AudienceLevel

engine = MathematicalTTSEngine()
```

#### Methods

##### `process_latex(latex_input: str, audience_level: AudienceLevel = AudienceLevel.UNDERGRADUATE) -> ProcessedExpression`

Process LaTeX mathematical expressions into natural language.

**Parameters:**
- `latex_input` (str): LaTeX mathematical expression
- `audience_level` (AudienceLevel): Target audience complexity level

**Returns:**
- `ProcessedExpression`: Object containing processed text, metadata, and performance metrics

**Example:**
```python
result = engine.process_latex(r"$\int_0^1 x^2 dx = \frac{1}{3}$")
print(result.processed)  # "the integral from 0 to 1 of x squared dx equals one third"
```

##### `async speak_expression(latex_input: str, output_file: str = None, ...) -> bool`

Generate speech from LaTeX expressions with professor-quality narration.

**Parameters:**
- `latex_input` (str): LaTeX mathematical expression
- `output_file` (str, optional): Output audio file path
- `voice_role` (str, optional): Voice role to use
- `engine_name` (str, optional): Specific TTS engine
- `audience_level` (AudienceLevel): Target audience level
- `progress` (optional): Progress callback object

**Returns:**
- `bool`: True if speech generation was successful

**Example:**
```python
success = await engine.speak_expression(
    r"$\lim_{x \to 0} \frac{\sin x}{x} = 1$",
    output_file="limit_theorem.mp3",
    audience_level=AudienceLevel.UNDERGRADUATE
)
```

### TTSEngineManager

Manages multiple TTS engines with automatic fallback.

```python
from core.tts_engines import TTSEngineManager

tts_manager = TTSEngineManager()
```

#### Methods

##### `async synthesize(text: str, output_file: str, ...) -> bool`

Synthesize speech using available engines with fallback.

**Parameters:**
- `text` (str): Text to convert to speech
- `output_file` (str): Output audio file path
- `voice` (str, optional): Voice to use
- `rate` (str, optional): Speech rate
- `engine_name` (str, optional): Specific engine to use

**Returns:**
- `bool`: True if synthesis was successful

**Example:**
```python
success = await tts_manager.synthesize(
    "Hello world",
    "output.mp3",
    voice="en-US-AriaNeural",
    rate="+10%"
)
```

##### `async generate_speech(text: str, output_file: str, ...) -> bool`

Alias for `synthesize()` for backward compatibility.

##### `async generate_speech_batch(texts: List[str], output_files: List[str], ...) -> List[bool]`

Generate speech for multiple texts concurrently.

**Parameters:**
- `texts` (List[str]): List of texts to convert
- `output_files` (List[str]): List of output file paths
- `voice` (str, optional): Voice for all texts
- `rate` (str, optional): Speech rate for all texts
- `engine_name` (str, optional): Engine to use
- `max_concurrent` (int): Maximum concurrent operations (default: 3)

**Returns:**
- `List[bool]`: Success flags for each text

**Example:**
```python
texts = ["First equation", "Second equation", "Third equation"]
files = ["eq1.mp3", "eq2.mp3", "eq3.mp3"]
results = await tts_manager.generate_speech_batch(texts, files)
```

### VoiceManager

Manages multi-voice orchestration with intelligent voice switching.

```python
from core.voice_manager import VoiceManager, VoiceRole

voice_manager = VoiceManager()
```

#### Voice Roles

- `VoiceRole.PROFESSOR`: Main mathematical narrator
- `VoiceRole.ASSISTANT`: Secondary explanations
- `VoiceRole.STUDENT`: Questions and clarifications
- `VoiceRole.NARRATOR`: General narration
- `VoiceRole.EMPHASIS`: Important concepts
- `VoiceRole.EXAMPLE`: Example demonstrations
- `VoiceRole.DEFINITION`: Definition explanations

## Pattern Processing

### PatternHandler (Abstract Base Class)

Base class for domain-specific pattern handlers.

```python
from core.patterns.base import PatternHandler, PatternRule, MathDomain

class CustomHandler(PatternHandler):
    @property
    def domain(self):
        return MathDomain.CUSTOM
    
    @property
    def name(self):
        return "CustomHandler"
    
    def get_patterns(self, audience_level=None):
        return [
            PatternRule(
                pattern=r"\\custom\{(.+?)\}",
                replacement="custom {0}",
                priority=10,
                domain=self.domain,
                audience_level=audience_level
            )
        ]
    
    def process_match(self, match, audience_level=None):
        return self.get_patterns()[0].replacement.format(match.group(1))
```

### Available Handlers

#### ArithmeticHandler
- **Domain:** Basic arithmetic operations
- **Patterns:** Fractions, percentages, basic operations
- **File:** `core/patterns/arithmetic.py`

#### AlgebraHandler
- **Domain:** Algebraic expressions
- **Patterns:** Polynomials, equations, functions
- **File:** `core/patterns/algebra.py`

#### CalculusHandler
- **Domain:** Calculus operations
- **Patterns:** Derivatives, integrals, limits, series
- **File:** `core/patterns/calculus.py`

## Configuration

### AudienceLevel

Defines the complexity level of mathematical explanations.

```python
from core.patterns_v2 import AudienceLevel

# Available levels
AudienceLevel.ELEMENTARY      # Elementary school
AudienceLevel.MIDDLE_SCHOOL   # Middle school
AudienceLevel.HIGH_SCHOOL     # High school
AudienceLevel.UNDERGRADUATE   # University undergraduate
AudienceLevel.GRADUATE        # Graduate level
AudienceLevel.RESEARCH        # Research level
```

### Engine Configuration

Configure TTS engines and their priorities:

```python
# Configure specific engine
engine = MathematicalTTSEngine()
await engine.speak_expression(
    latex_input,
    engine_name="edge_tts",  # or "gtts", "pyttsx3", "espeak"
    voice="en-US-AriaNeural"
)
```

## Utilities

### Audio Player

```python
from utils.audio_player import AudioPlayer

player = AudioPlayer()
await player.play("output.mp3")
```

### Cache Management

```python
from utils.cache import ExpressionCache

cache = ExpressionCache(max_size=1000)
result = cache.get(latex_expression)
if not result:
    result = process_expression(latex_expression)
    cache.set(latex_expression, result)
```

### Progress Tracking

```python
from utils.progress import ProgressTracker

progress = ProgressTracker("Processing mathematics")
result = await engine.speak_expression(
    latex_input,
    progress=progress
)
```

## Error Handling

### Common Exceptions

```python
from core.engine import MathProcessingError, TTSError

try:
    result = engine.process_latex(invalid_latex)
except MathProcessingError as e:
    print(f"Math processing failed: {e}")
except TTSError as e:
    print(f"TTS generation failed: {e}")
```

### Logging

```python
import logging

# Configure logging for MathSpeak
logging.getLogger('mathspeak').setLevel(logging.INFO)
```

## Advanced Usage

### Custom Domain Processors

```python
from domains.base import DomainProcessor
from core.patterns.base import MathDomain

class CustomDomainProcessor(DomainProcessor):
    @property
    def domain(self):
        return MathDomain.CUSTOM
    
    @property
    def name(self):
        return "Custom Domain"
    
    def process(self, text, context=None):
        # Custom processing logic
        return processed_text
    
    def can_handle(self, text):
        return "custom_keyword" in text.lower()

# Register the processor
engine.register_domain_processor(CustomDomainProcessor())
```

### Batch Processing

```python
# Process multiple expressions
expressions = [
    r"$f(x) = x^2$",
    r"$\int f(x) dx$",
    r"$\lim_{x \to \infty} f(x)$"
]

# Generate all speech files concurrently
output_files = [f"expr_{i}.mp3" for i in range(len(expressions))]
results = await tts_manager.generate_speech_batch(
    expressions, 
    output_files,
    max_concurrent=3
)
```

### Performance Monitoring

```python
# Get performance report
report = engine.get_performance_report()
print(f"Cache hit rate: {report['metrics']['cache_hit_rate']:.2%}")
print(f"Tokens per second: {report['metrics']['tokens_per_second']:.1f}")
print(f"Unknown commands: {report['metrics']['unknown_commands']}")
```

## Integration Examples

### Anki Integration

```python
from anki_integration import MathSpeakAnki

anki = MathSpeakAnki()
success = await anki.process_card_with_math(
    card_id="12345",
    generate_audio=True
)
```

### CLI Usage

```bash
# Command line interface
python -m mathspeak --input "formula.tex" --output "speech.mp3" --voice "professor"

# Batch processing
python -m mathspeak --batch --input-dir "formulas/" --output-dir "audio/"
```

## Testing

### Unit Testing

```python
import pytest
from tests_organized.unit.core.test_engine import TestMathematicalTTSEngine

# Run specific test
pytest tests_organized/unit/core/test_engine.py::TestMathematicalTTSEngine::test_latex_processing
```

### Integration Testing

```python
# Run integration tests
pytest tests_organized/integration/ -v

# Run performance tests
pytest tests_organized/performance/ -v --benchmark-only
```

## Best Practices

1. **Always use async/await** for TTS operations
2. **Handle exceptions** properly for robust applications
3. **Use appropriate audience levels** for your target users
4. **Cache results** for repeated expressions
5. **Monitor performance** with the built-in metrics
6. **Test edge cases** with mathematical expressions
7. **Use batch processing** for multiple expressions
8. **Configure logging** for debugging and monitoring

## Version Compatibility

- Python 3.8+
- AsyncIO support required
- Optional dependencies for specific TTS engines
- Cross-platform compatibility (Windows, macOS, Linux)

---

For more examples and advanced usage, see the `/examples` directory and integration tests.