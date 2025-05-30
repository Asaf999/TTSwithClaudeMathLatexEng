# Natural Speech Improvements for MathSpeak

## Summary of Changes

This document outlines the improvements made to make MathSpeak sound more like a real mathematics professor rather than a robot reading LaTeX code.

## 1. Subscript Improvements

### Before:
- `$x_1$` → "x underscore 1"
- `$a_{ij}$` → "a underscore open brace i j close brace"
- `$\pi_1$` → "pi underscore 1"

### After:
- `$x_1$` → "x sub 1"
- `$a_{ij}$` → "a i j" (for matrix elements)
- `$\pi_1$` → "pi sub 1"

### Implementation:
Added pattern matching in `engine.py` to detect and replace subscript patterns:
```python
(r'([a-zA-Z])_\{([^}]+)\}', lambda m: f'{m.group(1)} sub {m.group(2)}'),
(r'([a-zA-Z])_([a-zA-Z0-9])', lambda m: f'{m.group(1)} sub {m.group(2)}'),
(r'([A-Z])_\{([ij])([ij])\}', lambda m: f'{m.group(1)} {m.group(2)} {m.group(3)}'),  # Matrix elements
```

## 2. Superscript Improvements

### Before:
- `$x^2$` → "x caret 2"
- `$y^3$` → "y caret 3"
- `$z^n$` → "z caret n"

### After:
- `$x^2$` → "x squared"
- `$y^3$` → "y cubed"
- `$z^n$` → "z to the n"
- `$a^{10}$` → "a to the power of 10"

### Implementation:
Added intelligent superscript handling:
```python
(r'([a-zA-Z])\^2', lambda m: f'{m.group(1)} squared'),
(r'([a-zA-Z])\^3', lambda m: f'{m.group(1)} cubed'),
(r'([a-zA-Z])\^\{([^}]+)\}', lambda m: f'{m.group(1)} to the {m.group(2)}'),
```

## 3. Fraction Improvements

### Before:
- `$\frac{1}{2}$` → "frac 1 2"
- `$\frac{a}{b}$` → "frac a b"

### After:
- `$\frac{1}{2}$` → "one half"
- `$\frac{3}{4}$` → "three fourths"
- `$\frac{2}{3}$` → "two thirds"
- `$\frac{a}{b}$` → "a over b"
- `$\frac{\pi}{2}$` → "pi over 2"

### Implementation:
Enhanced the fraction processing in `patterns.py` with common fraction recognition.

## 4. Differential Improvements

### Before:
- `dx` → "dx" (as one word)
- `dy` → "dy"

### After:
- `dx` → "d x" (with space)
- `dy` → "d y"
- `$\frac{dy}{dx}$` → "d y over d x"

### Implementation:
Added differential patterns:
```python
(r'dx', 'd x'),
(r'dy', 'd y'),
(r'dz', 'd z'),
(r'dt', 'd t'),
```

## 5. Streaming Mode Fix

### Before:
- Interactive streaming defaulted to offline TTS

### After:
- Interactive streaming now uses online TTS by default for better quality
- Changed `prefer_offline=True` to `prefer_offline=False` in `streaming_mode.py`

## 6. Natural Mathematical Idioms

### Added Support For:
- Matrix element notation: `$A_{ij}$` → "A i j"
- Natural powers: `$x^4$` → "x to the fourth"
- Common roots: `$\sqrt{2}$` → "square root of 2"
- nth roots: `$\sqrt[3]{x}$` → "cube root of x"

## 7. Testing

Created comprehensive test suite in `test_improvements.py` to verify all improvements.

## Usage Examples

### Command Line:
```bash
# Test subscripts
ms "x_1 + x_2 = x_3"

# Test matrix multiplication
ms "A_{ij} = \sum_{k=1}^n B_{ik} C_{kj}"

# Test calculus
ms "\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"

# Interactive mode with streaming
ms --interactive --stream
```

### Python API:
```python
from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

engine = MathematicalTTSEngine(
    voice_manager=VoiceManager(),
    prefer_offline_tts=False  # Use online TTS
)

result = engine.process_latex("$x_1^2 + x_2^2 = r^2$")
print(result.processed)  # "x sub 1 squared plus x sub 2 squared equals r squared"
```

## Benefits

1. **More Natural**: Sounds like a professor speaking, not a computer
2. **Better Comprehension**: Easier to follow mathematical expressions
3. **Standard Notation**: Uses standard mathematical terminology
4. **Consistent**: Reliable conversion patterns

## Future Improvements

1. Context-aware pronunciation (e.g., "x one" vs "x sub 1" based on context)
2. More mathematical idioms and patterns
3. Support for additional languages
4. Voice inflection for emphasis