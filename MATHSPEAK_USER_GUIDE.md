# MathSpeak Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Basic Usage](#basic-usage)
5. [Advanced Features](#advanced-features)
6. [API Reference](#api-reference)
7. [Docker Deployment](#docker-deployment)
8. [Configuration](#configuration)
9. [Mathematical Domain Support](#mathematical-domain-support)
10. [Troubleshooting](#troubleshooting)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)

## 1. Introduction

MathSpeak is a powerful Text-to-Speech (TTS) system specifically designed for mathematical expressions. It converts LaTeX mathematical notation into natural, understandable speech, making mathematics accessible to visually impaired users, students, and educators.

### Key Features
- **LaTeX Support**: Full LaTeX mathematical notation support
- **Natural Speech**: Contextual pronunciation for clarity
- **Multiple TTS Engines**: EdgeTTS (online) and espeak-ng (offline)
- **Real-time Streaming**: Process math as you type
- **REST API**: Easy integration with applications
- **Security**: Built-in protection against malicious LaTeX
- **Caching**: High-performance expression caching

## 2. Installation

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 1GB free disk space
- Internet connection (for EdgeTTS) or espeak-ng (for offline)

### Installation Methods

#### Method 1: Python Package (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/mathspeak.git
cd mathspeak

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install MathSpeak
pip install -e .
```

#### Method 2: Docker
```bash
# Pull the image
docker pull mathspeak:latest

# Or build locally
docker build -t mathspeak .
```

#### Method 3: System-wide Installation
```bash
# Install globally
sudo pip install -r requirements.txt
sudo python setup.py install

# Create command shortcut (Linux/Mac)
./mathspeak/setup_ms_shortcut.sh
```

### Offline TTS Setup
For offline operation without internet:
```bash
# Install espeak-ng
python mathspeak/install_offline_tts.py

# Install offline dependencies
pip install -r mathspeak/requirements-offline.txt
```

## 3. Quick Start

### Basic Command Line Usage
```bash
# Simple expression
ms "The integral is $\int_0^1 x^2 dx$"

# With audio output
ms -a "The integral is $\int_0^1 x^2 dx$"

# Save to file
ms -o output.mp3 "The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$"
```

### Python API Usage
```python
from mathspeak import MathSpeak

# Initialize
mathspeak = MathSpeak()

# Convert to speech text
text = mathspeak.speak("$E = mc^2$")
print(text)  # Output: "E equals m c squared"

# Generate audio
audio_data = mathspeak.speak_audio("$\sum_{i=1}^n i = \frac{n(n+1)}{2}$")
```

## 4. Basic Usage

### Command Line Interface

#### Basic Commands
```bash
# Text output only
ms -t "expression"

# Audio playback
ms -a "expression"

# Save to file
ms -o filename.mp3 "expression"

# Batch processing
ms -b input.txt -o output_dir/

# Streaming mode
ms -s
```

#### Options
- `-t, --text`: Text output only
- `-a, --audio`: Play audio immediately
- `-o, --output`: Save audio to file
- `-v, --voice`: Select voice (en-US-AriaNeural, etc.)
- `-r, --rate`: Speech rate (0.5-2.0)
- `-b, --batch`: Process multiple expressions
- `-s, --stream`: Interactive streaming mode
- `--offline`: Use offline TTS engine

### Processing LaTeX Files
```bash
# Process entire LaTeX document
ms -f document.tex -o audio/

# Extract and speak equations only
ms -f document.tex --equations-only
```

### Interactive Mode
```bash
# Start interactive session
ms -i

# Commands in interactive mode:
> $\frac{d}{dx} \sin(x) = \cos(x)$
> voice en-GB-LibbyNeural
> rate 0.8
> save derivative.mp3 $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$
> quit
```

## 5. Advanced Features

### Real-time Streaming
```python
from mathspeak.streaming import RealTimeProcessor

processor = RealTimeProcessor()

# Process chunks of text
async for audio_chunk in processor.process_stream(text_chunks):
    play_audio(audio_chunk)
```

### Batch Processing
```python
from mathspeak import MathSpeak

ms = MathSpeak()

expressions = [
    "$x^2 + y^2 = r^2$",
    "$e^{i\pi} + 1 = 0$",
    "$\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}$"
]

# Process all at once
results = ms.batch_speak(expressions)
```

### Custom Voice Profiles
```python
# Professor style
ms = MathSpeak(style="professor")

# Student-friendly style
ms = MathSpeak(style="student")

# Custom configuration
ms = MathSpeak(
    voice="en-US-JennyNeural",
    rate=0.9,
    pitch=1.1,
    emphasis="strong"
)
```

### Context-Aware Processing
```python
# Provide context for better pronunciation
ms.speak("In topology, $X$ is compact", context="topology")

# Educational context
ms.speak("$\sin^2(x)$", context="trigonometry", level="high_school")
```

## 6. API Reference

### REST API Endpoints

Start the API server:
```bash
# Development
python mathspeak_server.py

# Production
uvicorn mathspeak.api.server:app --host 0.0.0.0 --port 8000
```

#### POST /speak
Generate audio from LaTeX expression:
```bash
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "$\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}$",
    "voice": "en-US-AriaNeural",
    "rate": 1.0
  }' \
  --output integral.mp3
```

#### POST /speak/text
Get text representation only:
```bash
curl -X POST http://localhost:8000/speak/text \
  -H "Content-Type: application/json" \
  -d '{"expression": "$\\sum_{i=1}^n i$"}'
```

Response:
```json
{
  "text": "sum from i equals 1 to n of i",
  "processing_time": 0.005
}
```

#### POST /speak/stream
Stream audio in real-time:
```bash
curl -X POST http://localhost:8000/speak/stream \
  -H "Content-Type: application/json" \
  -d '{"expression": "long expression..."}' \
  --output stream.mp3
```

#### POST /batch
Process multiple expressions:
```bash
curl -X POST http://localhost:8000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "expressions": [
      "$a^2 + b^2 = c^2$",
      "$F = ma$"
    ]
  }'
```

#### WebSocket /ws
Real-time bidirectional communication:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    expression: "$\\frac{dy}{dx}$",
    stream: true
  }));
};

ws.onmessage = (event) => {
  const audio = event.data;
  playAudio(audio);
};
```

## 7. Docker Deployment

### Basic Docker Usage
```bash
# Run with default settings
docker run -p 8000:8000 mathspeak

# With custom configuration
docker run -p 8000:8000 \
  -e MS_ENGINE=offline \
  -e MS_CACHE_SIZE=5000 \
  -v $(pwd)/cache:/app/cache \
  mathspeak
```

### Docker Compose
```yaml
version: '3.8'
services:
  mathspeak:
    image: mathspeak:latest
    ports:
      - "8000:8000"
    environment:
      - MS_ENGINE=edge
      - MS_DEFAULT_VOICE=en-US-AriaNeural
      - MS_CACHE_ENABLED=true
    volumes:
      - ./cache:/app/cache
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - mathspeak
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mathspeak
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mathspeak
  template:
    metadata:
      labels:
        app: mathspeak
    spec:
      containers:
      - name: mathspeak
        image: mathspeak:latest
        ports:
        - containerPort: 8000
        env:
        - name: MS_ENGINE
          value: "edge"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

## 8. Configuration

### Configuration File
Create `~/.mathspeak/config.json`:
```json
{
  "engine": "edge",
  "default_voice": "en-US-AriaNeural",
  "default_rate": 1.0,
  "cache": {
    "enabled": true,
    "size": 10000,
    "ttl": 86400,
    "persist": true
  },
  "security": {
    "max_expression_length": 10000,
    "timeout": 5.0,
    "blacklist_commands": true
  },
  "advanced": {
    "parallel_processing": true,
    "max_workers": 4,
    "stream_chunk_size": 1024
  }
}
```

### Environment Variables
```bash
# TTS Engine
export MS_ENGINE=edge  # or offline

# Default voice
export MS_DEFAULT_VOICE=en-US-JennyNeural

# Cache settings
export MS_CACHE_ENABLED=true
export MS_CACHE_SIZE=10000
export MS_CACHE_DIR=/var/cache/mathspeak

# Security
export MS_SECURITY_ENABLED=true
export MS_MAX_EXPRESSION_LENGTH=10000

# Performance
export MS_PARALLEL_WORKERS=4
export MS_STREAM_BUFFER_SIZE=4096
```

### Voice Configuration

#### Available Voices (EdgeTTS)
- **US English**: en-US-AriaNeural, en-US-JennyNeural, en-US-GuyNeural
- **UK English**: en-GB-LibbyNeural, en-GB-RyanNeural
- **Australian**: en-AU-NatashaNeural, en-AU-WilliamNeural
- **Canadian**: en-CA-ClaraNeural, en-CA-LiamNeural

#### Voice Customization
```python
# Configure voice parameters
ms = MathSpeak(
    voice_config={
        "name": "en-US-AriaNeural",
        "rate": 0.9,        # 0.5-2.0
        "pitch": 1.0,       # 0.5-2.0
        "volume": 1.0,      # 0.0-1.0
        "emphasis": "moderate",  # none, moderate, strong
        "breaks": {
            "sentence": 500,   # ms
            "comma": 300,      # ms
            "equation": 400    # ms
        }
    }
)
```

## 9. Mathematical Domain Support

### Supported Mathematical Areas

#### Basic Mathematics
```latex
# Arithmetic
$2 + 3 \times 4$           → "2 plus 3 times 4"
$\frac{3}{4}$              → "3 over 4"
$\sqrt{16}$                → "square root of 16"
$\sqrt[3]{8}$              → "cube root of 8"
```

#### Algebra
```latex
# Equations
$x^2 + 5x + 6 = 0$         → "x squared plus 5 x plus 6 equals 0"
$|x - 3| < 5$              → "absolute value of x minus 3 is less than 5"

# Polynomials
$(x + 1)^3$                → "open parenthesis x plus 1 close parenthesis cubed"
$x^{n+1}$                  → "x to the power of n plus 1"
```

#### Calculus
```latex
# Derivatives
$\frac{d}{dx} f(x)$        → "d by d x of f of x"
$f'(x)$                    → "f prime of x"
$\frac{\partial f}{\partial x}$ → "partial f by partial x"

# Integrals
$\int_0^1 x^2 dx$          → "integral from 0 to 1 of x squared d x"
$\oint_C f(z) dz$          → "contour integral over C of f of z d z"

# Limits
$\lim_{x \to 0} \frac{\sin x}{x}$ → "limit as x approaches 0 of sine x over x"
```

#### Linear Algebra
```latex
# Matrices
$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ → "2 by 2 matrix with entries a, b, c, d"

# Vectors
$\vec{v} = \langle 1, 2, 3 \rangle$ → "vector v equals 1, 2, 3"
$\vec{a} \cdot \vec{b}$    → "vector a dot vector b"
$\vec{a} \times \vec{b}$   → "vector a cross vector b"
```

#### Advanced Mathematics
```latex
# Set Theory
$A \cup B$                 → "A union B"
$A \cap B$                 → "A intersection B"
$x \in \mathbb{R}$         → "x in the real numbers"

# Logic
$p \implies q$             → "p implies q"
$\forall x \in X$          → "for all x in X"
$\exists y : P(y)$         → "there exists y such that P of y"

# Topology
$\mathcal{O}$              → "script O"
$X \cong Y$                → "X is homeomorphic to Y"
```

### Custom Commands
Add custom LaTeX commands in `~/.mathspeak/custom_commands.json`:
```json
{
  "\\Z": "the integers",
  "\\prob": "probability of",
  "\\E": "expected value of",
  "\\var": "variance of"
}
```

## 10. Troubleshooting

### Common Issues

#### Issue: No Audio Output
```bash
# Check TTS engine
ms --test-audio

# Verify voice installation
ms --list-voices

# Use offline engine
ms --offline "test expression"
```

#### Issue: LaTeX Parsing Errors
```bash
# Validate LaTeX
ms --validate "$your expression$"

# Show detailed errors
ms --debug "$expression$"

# Check for unsupported commands
ms --check-commands "$expression$"
```

#### Issue: Slow Performance
```bash
# Enable caching
export MS_CACHE_ENABLED=true

# Pre-warm cache
ms --warm-cache common_expressions.txt

# Check cache statistics
ms --cache-stats
```

#### Issue: Memory Usage
```bash
# Limit cache size
export MS_CACHE_SIZE=1000

# Clear cache
ms --clear-cache

# Monitor memory
ms --monitor
```

### Debug Mode
```bash
# Enable debug logging
export MS_LOG_LEVEL=DEBUG

# Run with debug output
ms --debug "$expression$"

# Save debug log
ms --debug "$expression$" 2> debug.log
```

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Invalid LaTeX syntax" | Malformed expression | Check brackets and commands |
| "Security violation" | Dangerous commands detected | Remove file I/O commands |
| "Expression too long" | Exceeds length limit | Split into smaller parts |
| "Unknown command" | Unsupported LaTeX | Add to custom commands |
| "TTS engine error" | Audio generation failed | Check internet/engine |

## 11. Performance Optimization

### Caching Strategy
```python
# Pre-warm cache with common expressions
from mathspeak import MathSpeak

ms = MathSpeak()
common_expressions = [
    "$x^2$", "$\sqrt{x}$", "$\frac{a}{b}$",
    "$\sin(x)$", "$\cos(x)$", "$e^x$"
]
ms.warm_cache(common_expressions)
```

### Batch Processing
```python
# Process many expressions efficiently
expressions = load_expressions("math_problems.txt")
results = ms.batch_speak(expressions, parallel=True, workers=4)
```

### Connection Pooling
```python
# Reuse TTS connections
ms = MathSpeak(
    connection_pool_size=10,
    connection_timeout=30
)
```

### Memory Management
```python
# Configure memory limits
ms = MathSpeak(
    cache_size=5000,          # Max cached expressions
    cache_memory_limit="1GB",  # Max memory for cache
    auto_cleanup=True         # Remove old entries
)
```

## 12. Security Considerations

### Input Validation
MathSpeak automatically validates all input for:
- Dangerous LaTeX commands (file I/O, shell execution)
- Expansion bombs (recursive macros)
- Resource exhaustion (deeply nested expressions)
- Length limits (prevents DoS)

### Safe Mode
```python
# Maximum security
ms = MathSpeak(security_mode="strict")

# Custom security rules
ms = MathSpeak(
    security_config={
        "max_length": 5000,
        "max_depth": 50,
        "timeout": 3.0,
        "blacklist": ["\\input", "\\write"],
        "whitelist": ["\\frac", "\\sqrt"]
    }
)
```

### API Security
```nginx
# Rate limiting in nginx.conf
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20;
    proxy_pass http://mathspeak:8000;
}
```

### Docker Security
```dockerfile
# Run as non-root user
USER mathspeak:mathspeak

# Read-only filesystem
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /app/cache \
  mathspeak
```

## Appendix A: LaTeX Command Reference

### Frequently Used Commands
| LaTeX | Speech | Category |
|-------|--------|----------|
| `\frac{a}{b}` | "a over b" | Fractions |
| `\sqrt{x}` | "square root of x" | Roots |
| `x^2` | "x squared" | Exponents |
| `x_i` | "x sub i" | Subscripts |
| `\sum` | "sum" | Operators |
| `\int` | "integral" | Calculus |
| `\infty` | "infinity" | Symbols |
| `\alpha` | "alpha" | Greek |

### Complete Command List
See `/mathspeak/docs/latex_commands.md` for full reference.

## Appendix B: Integration Examples

### Python Application
```python
from mathspeak import MathSpeak

class MathTeachingApp:
    def __init__(self):
        self.ms = MathSpeak(style="teacher")
    
    def explain_equation(self, latex):
        # Generate explanation
        speech = self.ms.speak(latex, context="explanation")
        
        # Play audio
        audio = self.ms.speak_audio(latex)
        play_audio(audio)
        
        return speech
```

### Web Application
```javascript
// JavaScript client
class MathSpeakClient {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
    }
    
    async speakMath(expression) {
        const response = await fetch(`${this.apiUrl}/speak`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({expression})
        });
        
        const audioBlob = await response.blob();
        const audio = new Audio(URL.createObjectURL(audioBlob));
        audio.play();
    }
}
```

### Anki Integration
```python
# Install in Anki
# Tools -> Add-ons -> Install from file -> mathspeak_addon.ankiaddon

# Usage in cards
# Front: {{Equation}}
# Back: {{MathSpeak:Equation}}
```

## Appendix C: Troubleshooting Checklist

1. **Installation Issues**
   - [ ] Python version 3.8+?
   - [ ] All dependencies installed?
   - [ ] Correct virtual environment?

2. **Audio Issues**
   - [ ] TTS engine installed?
   - [ ] Internet connection (for EdgeTTS)?
   - [ ] Audio device working?

3. **Performance Issues**
   - [ ] Cache enabled?
   - [ ] Sufficient memory?
   - [ ] CPU not overloaded?

4. **API Issues**
   - [ ] Server running?
   - [ ] Correct port?
   - [ ] Firewall rules?

## Support

- **Documentation**: `/mathspeak/docs/`
- **Examples**: `/mathspeak/docs/examples/`
- **Issues**: GitHub Issues
- **Email**: support@mathspeak.ai

---

**Version**: 1.0.0  
**Last Updated**: May 31, 2025