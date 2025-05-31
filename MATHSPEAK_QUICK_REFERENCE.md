# MathSpeak Quick Reference Card

## Installation
```bash
pip install -r requirements.txt
pip install -e .
```

## Basic Commands
```bash
# Text output
ms "$x^2 + y^2 = r^2$"

# Audio playback
ms -a "$E = mc^2$"

# Save to file
ms -o output.mp3 "$\int_0^1 x^2 dx$"

# Interactive mode
ms -i

# Streaming mode
ms -s
```

## Common Options
| Flag | Description | Example |
|------|-------------|---------|
| `-t` | Text only | `ms -t "$\pi$"` |
| `-a` | Play audio | `ms -a "$\sqrt{2}$"` |
| `-o` | Output file | `ms -o file.mp3 "expr"` |
| `-v` | Voice | `ms -v en-GB-LibbyNeural "expr"` |
| `-r` | Rate | `ms -r 0.8 "expr"` |
| `-b` | Batch | `ms -b input.txt` |
| `--offline` | Offline mode | `ms --offline "expr"` |

## Python Usage
```python
from mathspeak import MathSpeak

# Initialize
ms = MathSpeak()

# Text output
text = ms.speak("$\\frac{a}{b}$")

# Audio output
audio = ms.speak_audio("$\\sum_{i=1}^n i$")

# Batch processing
results = ms.batch_speak(["$x^2$", "$y^3$"])
```

## REST API
```bash
# Start server
python mathspeak_server.py

# Generate audio
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"expression": "$x^2$"}' \
  -o output.mp3

# Get text only
curl -X POST http://localhost:8000/speak/text \
  -H "Content-Type: application/json" \
  -d '{"expression": "$\\pi r^2$"}'
```

## Docker
```bash
# Run container
docker run -p 8000:8000 mathspeak

# With options
docker run -p 8000:8000 \
  -e MS_ENGINE=offline \
  -v $(pwd)/cache:/app/cache \
  mathspeak
```

## Common LaTeX Examples

### Basic Math
| LaTeX | Speech |
|-------|--------|
| `$x^2$` | "x squared" |
| `$x_i$` | "x sub i" |
| `$\frac{a}{b}$` | "a over b" |
| `$\sqrt{x}$` | "square root of x" |
| `$\sqrt[3]{x}$` | "cube root of x" |

### Calculus
| LaTeX | Speech |
|-------|--------|
| `$\frac{d}{dx}$` | "d by d x" |
| `$\frac{\partial f}{\partial x}$` | "partial f by partial x" |
| `$\int_a^b f(x)dx$` | "integral from a to b of f of x d x" |
| `$\lim_{x \to 0}$` | "limit as x approaches 0" |

### Greek Letters
| LaTeX | Speech |
|-------|--------|
| `$\alpha$` | "alpha" |
| `$\beta$` | "beta" |
| `$\gamma$` | "gamma" |
| `$\Delta$` | "capital delta" |
| `$\pi$` | "pi" |

### Operators
| LaTeX | Speech |
|-------|--------|
| `$\sum$` | "sum" |
| `$\prod$` | "product" |
| `$\cup$` | "union" |
| `$\cap$` | "intersection" |
| `$\in$` | "in" |

## Troubleshooting

### No Audio?
```bash
ms --test-audio
ms --list-voices
ms --offline "test"
```

### Performance Issues?
```bash
export MS_CACHE_ENABLED=true
ms --cache-stats
ms --warm-cache expressions.txt
```

### Errors?
```bash
ms --debug "$expression$"
ms --validate "$expression$"
export MS_LOG_LEVEL=DEBUG
```

## Environment Variables
```bash
export MS_ENGINE=edge           # or offline
export MS_DEFAULT_VOICE=en-US-AriaNeural
export MS_CACHE_ENABLED=true
export MS_CACHE_SIZE=10000
export MS_LOG_LEVEL=INFO
```

## Support
- User Guide: `MATHSPEAK_USER_GUIDE.md`
- Examples: `mathspeak/docs/examples/`
- API Docs: `mathspeak/docs/api_reference.md`

---
Version 1.0.0 | Quick Reference Card