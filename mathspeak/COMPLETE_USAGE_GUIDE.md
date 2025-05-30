# MathSpeak Complete Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [CLI Usage](#cli-usage)
4. [Python API](#python-api)
5. [Mathematical Notation Guide](#mathematical-notation-guide)
6. [Tips and Tricks](#tips-and-tricks)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)
10. [Integration Examples](#integration-examples)

---

## Quick Start

### Basic Usage
```bash
# Simple expression
python mathspeak.py "x^2 + y^2 = r^2"

# Complex integral
python mathspeak.py "\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"

# Save to file
python mathspeak.py "\pi_1(S^1) \cong \mathbb{Z}" --save

# Interactive mode
python mathspeak.py --interactive
```

### Installation in One Line
```bash
pip install -r requirements.txt && python install_offline_tts.py
```

---

## Installation

### Standard Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/mathspeak.git
cd mathspeak

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install offline TTS support (optional but recommended)
python install_offline_tts.py
```

### Minimal Installation (Online TTS only)
```bash
pip install edge-tts numpy
```

### Full Installation (All features)
```bash
pip install -r requirements_full.txt
```

### System Dependencies

**Linux:**
```bash
# For offline TTS
sudo apt-get install espeak-ng libespeak-ng-dev

# For audio playback
sudo apt-get install mpv  # or mplayer, aplay
```

**macOS:**
```bash
# Uses built-in say command and afplay
# No additional dependencies needed
```

**Windows:**
```bash
# Uses built-in SAPI
# Install pygame for better audio playback
pip install pygame
```

---

## CLI Usage

### Basic Syntax
```bash
python mathspeak.py [expression] [options]
```

### All CLI Options

#### Input Options
```bash
# Direct expression
python mathspeak.py "e^{i\pi} + 1 = 0"

# From file
python mathspeak.py --file lecture_notes.tex

# Interactive mode
python mathspeak.py --interactive

# Batch processing
python mathspeak.py --batch expressions.txt --batch-output ./output/
```

#### Output Options
```bash
# Save with auto-generated filename
python mathspeak.py "x^2" --save

# Save to specific file
python mathspeak.py "x^2" --output my_audio.mp3

# Batch output directory
python mathspeak.py --batch input.txt --batch-output ./audio_files/
```

#### Voice Options
```bash
# Change voice role
python mathspeak.py "theorem" --voice theorem
python mathspeak.py "definition" --voice definition

# Available voices: narrator, theorem, definition, example, proof, remark

# Adjust speed
python mathspeak.py "fast math" --speed 1.5
python mathspeak.py "slow math" --speed 0.8
```

#### Processing Options
```bash
# Force mathematical context
python mathspeak.py "\pi_1" --context topology
python mathspeak.py "\oint" --context complex_analysis

# Disable features
python mathspeak.py "x^2" --no-commentary
python mathspeak.py "x^2" --no-cache

# Use offline TTS engines
python mathspeak.py "x^2" --offline
```

#### Information Options
```bash
# Run test expressions
python mathspeak.py --test basic
python mathspeak.py --test topology
python mathspeak.py --test all

# Show performance statistics
python mathspeak.py "complex expression" --stats

# Enable debug logging
python mathspeak.py "x^2" --debug

# Version information
python mathspeak.py --version
```

### Examples with Output

```bash
# Example 1: Basic quadratic
$ python mathspeak.py "x^2 + 2x + 1 = 0"
🔄 Processing expression: x^2 + 2x + 1 = 0
📝 Natural speech: x squared plus 2 x plus 1 equals 0
🎯 Mathematical context: algebra
⏱️  Processing time: 0.042s
🔊 Generating speech...

# Example 2: Complex analysis with context
$ python mathspeak.py "\oint_\gamma f(z)dz" --context complex_analysis
🔄 Processing expression: \oint_\gamma f(z)dz
📝 Natural speech: the contour integral over gamma of f of z d z
🎯 Mathematical context: complex_analysis
⏱️  Processing time: 0.038s
🔊 Generating speech...

# Example 3: Save with statistics
$ python mathspeak.py "\sum_{n=1}^\infty \frac{1}{n^2}" --save --stats
🔄 Processing expression: \sum_{n=1}^\infty \frac{1}{n^2}
📝 Natural speech: the sum from n equals 1 to infinity of 1 over n squared
🎯 Mathematical context: real_analysis
⏱️  Processing time: 0.051s
🔊 Generating speech...
✅ Audio saved to: mathspeak_20250530_120000.mp3

📊 Performance Report:
Metrics:
  tokens_per_second: 156.32
  cache_hit_rate: 0.00
  total_processing_time: 0.051
```

---

## Python API

### Basic API Usage

```python
from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

# Initialize
voice_manager = VoiceManager()
engine = MathematicalTTSEngine(voice_manager=voice_manager)

# Process LaTeX
result = engine.process_latex("\\int_0^1 x^2 dx")
print(f"Natural speech: {result.processed}")
print(f"Context: {result.context}")

# Generate speech
import asyncio
asyncio.run(engine.speak_expression(result, "output.mp3"))
```

### Advanced API Features

```python
# Force specific context
from mathspeak.core.engine import MathematicalContext

result = engine.process_latex(
    "\\pi_1(X)", 
    force_context=MathematicalContext.TOPOLOGY
)

# Custom voice configuration
voice_manager.set_voice_for_role(VoiceRole.THEOREM, "en-US-AriaNeural")

# Batch processing
expressions = [
    "x^2 + y^2 = r^2",
    "e^{i\\pi} + 1 = 0",
    "\\nabla \\times \\vec{F} = 0"
]

for expr in expressions:
    result = engine.process_latex(expr)
    await engine.speak_expression(result, f"output_{i}.mp3")

# Performance monitoring
report = engine.get_performance_report()
print(f"Cache hit rate: {report['metrics']['cache_hit_rate']}")
```

### Context Management

```python
# Available contexts
from mathspeak.core.engine import MathematicalContext

contexts = [
    MathematicalContext.GENERAL,
    MathematicalContext.ALGEBRA,
    MathematicalContext.CALCULUS,
    MathematicalContext.TOPOLOGY,
    MathematicalContext.COMPLEX_ANALYSIS,
    MathematicalContext.REAL_ANALYSIS,
    MathematicalContext.NUMBER_THEORY,
    MathematicalContext.LINEAR_ALGEBRA,
    MathematicalContext.ABSTRACT_ALGEBRA,
    MathematicalContext.DIFFERENTIAL_GEOMETRY,
    MathematicalContext.PROBABILITY,
    MathematicalContext.STATISTICS
]

# Context affects pronunciation
expr = "\\pi"
for ctx in [MathematicalContext.GENERAL, MathematicalContext.COMPLEX_ANALYSIS]:
    result = engine.process_latex(expr, force_context=ctx)
    print(f"{ctx}: {result.processed}")
```

### Custom Domain Processors

```python
from mathspeak.domains.base import BaseDomainProcessor

class MyCustomProcessor(BaseDomainProcessor):
    def process(self, expression: str) -> str:
        # Custom processing logic
        return self.apply_rules(expression, custom_rules)
    
    @property
    def patterns(self):
        return {
            r'\\mycmd\{([^}]+)\}': r'my command of \1',
        }

# Register processor
engine.domain_processors[MathematicalContext.CUSTOM] = MyCustomProcessor()
```

---

## Mathematical Notation Guide

### Basic Arithmetic
```latex
# Addition/Subtraction
a + b           → "a plus b"
a - b           → "a minus b"
a \pm b         → "a plus or minus b"

# Multiplication/Division
a \cdot b       → "a times b"
a \times b      → "a times b"
\frac{a}{b}     → "a over b"
a/b             → "a divided by b"

# Powers and Roots
x^2             → "x squared"
x^3             → "x cubed"
x^n             → "x to the n"
\sqrt{x}        → "square root of x"
\sqrt[3]{x}     → "cube root of x"
```

### Greek Letters
```latex
\alpha          → "alpha"
\beta           → "beta"
\gamma          → "gamma"
\delta          → "delta"
\epsilon        → "epsilon"
\theta          → "theta"
\pi             → "pi"
\sigma          → "sigma"
\omega          → "omega"

# Variants
\varepsilon     → "varepsilon"
\varphi         → "varphi"
```

### Calculus
```latex
# Derivatives
\frac{d}{dx}    → "d by d x"
\frac{df}{dx}   → "d f by d x"
f'(x)           → "f prime of x"
f''(x)          → "f double prime of x"
\partial f      → "partial f"

# Integrals
\int f dx       → "integral of f d x"
\int_a^b        → "integral from a to b"
\oint           → "contour integral"
\iint           → "double integral"

# Limits
\lim_{x \to a}  → "limit as x approaches a"
\lim_{x \to \infty} → "limit as x approaches infinity"
```

### Set Theory
```latex
\in             → "in"
\notin          → "not in"
\subset         → "subset of"
\subseteq       → "subset or equal to"
\cup            → "union"
\cap            → "intersection"
\emptyset       → "empty set"
\mathbb{R}      → "the real numbers"
\mathbb{Z}      → "the integers"
\mathbb{N}      → "the natural numbers"
```

### Logic
```latex
\forall         → "for all"
\exists         → "there exists"
\nexists        → "there does not exist"
\implies        → "implies"
\iff            → "if and only if"
\land           → "and"
\lor            → "or"
\neg            → "not"
```

### Linear Algebra
```latex
\vec{v}         → "vector v"
\mathbf{A}      → "matrix A"
\det(A)         → "determinant of A"
A^T             → "A transpose"
A^{-1}          → "A inverse"
\langle u,v \rangle → "inner product of u and v"
||v||           → "norm of v"
```

### Special Functions
```latex
\sin x          → "sine x"
\cos x          → "cosine x"
\tan x          → "tangent x"
\ln x           → "natural log of x"
\log x          → "log x"
\exp x          → "exponential of x"
e^x             → "e to the x"
```

### Advanced Notation

#### Topology
```latex
\pi_1(X)        → "the fundamental group of X"
H_n(X)          → "the n-th homology group of X"
\overline{A}    → "the closure of A"
\partial A      → "the boundary of A"
int(A)          → "the interior of A"
```

#### Complex Analysis
```latex
\Re(z)          → "real part of z"
\Im(z)          → "imaginary part of z"
|z|             → "modulus of z"
\arg(z)         → "argument of z"
\bar{z}         → "z conjugate"
```

#### Abstract Algebra
```latex
G/H             → "G mod H"
\ker(f)         → "kernel of f"
\text{im}(f)    → "image of f"
[G:H]           → "the index of H in G"
\cong           → "isomorphic to"
```

---

## Tips and Tricks

### Getting Natural Speech

1. **Use standard notation**: MathSpeak recognizes common patterns
   ```latex
   # Good
   \int_0^1 x^2 dx
   
   # Less natural
   \int\limits_{0}^{1} x^{2} \, dx
   ```

2. **Add context with text**:
   ```latex
   \text{Let } f(x) = x^2 \text{ where } x \in \mathbb{R}
   ```

3. **Break complex expressions**:
   ```latex
   # Instead of one long expression
   \frac{d}{dx}\left[\int_0^x e^{-t^2} dt\right] = e^{-x^2}
   
   # Break it up
   F(x) = \int_0^x e^{-t^2} dt
   \frac{dF}{dx} = e^{-x^2}
   ```

### Context Hints

Add contextual hints to improve pronunciation:

```latex
# Topology context
\pi_1(S^1) \cong \mathbb{Z}  # fundamental group

# Number theory context  
p \equiv 3 \pmod{4}  # prime congruence

# Analysis context
\epsilon > 0  # epsilon-delta proof
```

### Voice Selection Strategy

- **Narrator**: General explanations, main content
- **Theorem**: Important results, theorems
- **Definition**: New terms, formal definitions
- **Example**: Concrete examples, calculations
- **Proof**: Proof steps, logical arguments
- **Remark**: Side notes, observations

### Batch Processing Tips

Create a well-formatted input file:
```text
# expressions.txt
# Basic algebra
x^2 + 2x + 1 = (x+1)^2

# Calculus
\int_0^1 x^2 dx = \frac{1}{3}

# Topology
\pi_1(S^1) \cong \mathbb{Z}
```

Process with:
```bash
python mathspeak.py --batch expressions.txt --batch-output ./lectures/
```

---

## Performance Optimization

### 1. Enable Caching (Default)
```python
# Caching is enabled by default
engine = MathematicalTTSEngine(enable_caching=True)

# Check cache performance
report = engine.get_performance_report()
print(f"Cache hit rate: {report['cache']['hit_rate']}")
```

### 2. Use Offline TTS for Speed
```bash
# Offline TTS is faster but lower quality
python mathspeak.py "expression" --offline
```

### 3. Batch Processing
```python
# Process multiple expressions efficiently
async def batch_process(expressions):
    tasks = []
    for i, expr in enumerate(expressions):
        result = engine.process_latex(expr)
        task = engine.speak_expression(result, f"output_{i}.mp3")
        tasks.append(task)
    
    await asyncio.gather(*tasks)
```

### 4. Preprocess Common Expressions
```python
# Warm up cache with common expressions
common_expressions = [
    "x^2", "\\int", "\\sum", "\\frac{a}{b}",
    "\\pi", "\\infty", "\\partial"
]

for expr in common_expressions:
    engine.process_latex(expr)
```

### 5. Memory Management
```python
# Clear cache periodically for long-running processes
engine.clear_cache()

# Set cache size limit
engine.max_cache_size = 1000
```

---

## Troubleshooting

### Common Issues

#### No Audio Output
```bash
# Check audio dependencies
python -c "import pygame; pygame.mixer.init()"

# Try different audio backend
python mathspeak.py "test" --debug

# Linux: Install audio player
sudo apt-get install mpv
```

#### Slow Performance
```bash
# Use offline TTS
python mathspeak.py "expression" --offline

# Disable commentary
python mathspeak.py "expression" --no-commentary

# Check cache is working
python mathspeak.py "expression" --stats
```

#### Unknown LaTeX Commands
```python
# Check what commands are unknown
result = engine.process_latex("\\mycommand{x}")
print(f"Unknown: {result.unknown_commands}")

# Add custom patterns
engine.natural_converter.add_pattern(
    r'\\mycommand\{([^}]+)\}',
    r'my command of \1'
)
```

#### Installation Issues

**Linux:**
```bash
# Missing espeak-ng
sudo apt-get update
sudo apt-get install espeak-ng libespeak-ng-dev

# Python.h missing
sudo apt-get install python3-dev
```

**macOS:**
```bash
# Use homebrew for dependencies
brew install espeak-ng

# Permission issues
pip install --user -r requirements.txt
```

**Windows:**
```bash
# Use conda for complex dependencies
conda install -c conda-forge pyttsx3

# Or use WSL for Linux compatibility
```

### Debug Mode

Enable detailed logging:
```bash
python mathspeak.py "expression" --debug

# Or in Python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Profiling

```python
import cProfile
import pstats

# Profile expression processing
profiler = cProfile.Profile()
profiler.enable()

for _ in range(100):
    engine.process_latex("\\int_0^1 x^2 dx")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

---

## Advanced Usage

### Custom TTS Integration

```python
from mathspeak.core.tts_engines import BaseTTSEngine

class MyCustomTTS(BaseTTSEngine):
    def __init__(self):
        self.name = "custom"
        
    async def generate_speech(self, text: str, output_file: str) -> bool:
        # Your TTS implementation
        return True
    
    def is_available(self) -> bool:
        return True

# Register engine
engine.tts_manager.engines['custom'] = MyCustomTTS()
engine.tts_manager.preferred_engine = 'custom'
```

### Streaming Output

```python
async def stream_math_audio(expression: str):
    # Process expression
    result = engine.process_latex(expression)
    
    # Generate segments
    segments = result.processed.split('. ')
    
    for i, segment in enumerate(segments):
        # Generate audio for segment
        temp_file = f"segment_{i}.mp3"
        await engine.tts_manager.generate_speech(segment, temp_file)
        
        # Stream or play segment
        yield temp_file
```

### Web API Integration

```python
from flask import Flask, request, send_file
import asyncio

app = Flask(__name__)

@app.route('/mathspeak', methods=['POST'])
def mathspeak_api():
    expression = request.json.get('expression', '')
    context = request.json.get('context', None)
    
    # Process
    result = engine.process_latex(expression, force_context=context)
    
    # Generate audio
    output_file = f"temp_{int(time.time())}.mp3"
    asyncio.run(engine.speak_expression(result, output_file))
    
    return send_file(output_file, mimetype='audio/mp3')
```

### LaTeX Document Processing

```python
import re

def process_latex_document(filename: str):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Extract math expressions
    # Display math: \[ ... \] or $$ ... $$
    display_math = re.findall(r'\\\[(.*?)\\\]|\$\$(.*?)\$\$', content, re.DOTALL)
    
    # Inline math: \( ... \) or $ ... $
    inline_math = re.findall(r'\\\((.*?)\\\)|\$([^$]+)\$', content)
    
    # Process each expression
    for expr in display_math + inline_math:
        expr = expr[0] if expr[0] else expr[1]
        result = engine.process_latex(expr)
        # Generate audio files...
```

---

## Integration Examples

### Jupyter Notebook Integration

```python
# In Jupyter notebook
from IPython.display import Audio, display
import asyncio

async def speak_math(expression):
    result = engine.process_latex(expression)
    output_file = "temp_math.mp3"
    await engine.speak_expression(result, output_file)
    display(Audio(output_file))

# Usage in notebook
await speak_math("\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}")
```

### VS Code Extension

```javascript
// extension.js
const vscode = require('vscode');
const { exec } = require('child_process');

function activate(context) {
    let disposable = vscode.commands.registerCommand('mathspeak.speak', () => {
        const editor = vscode.window.activeTextEditor;
        const selection = editor.selection;
        const text = editor.document.getText(selection);
        
        // Call MathSpeak
        exec(`python mathspeak.py "${text}"`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`MathSpeak error: ${error}`);
                return;
            }
            vscode.window.showInformationMessage('MathSpeak: Audio generated!');
        });
    });
    
    context.subscriptions.push(disposable);
}
```

### Discord Bot Integration

```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def math(ctx, *, expression: str):
    """Speak mathematical expression"""
    try:
        # Process expression
        result = engine.process_latex(expression)
        
        # Generate audio
        output_file = f"math_{ctx.message.id}.mp3"
        await engine.speak_expression(result, output_file)
        
        # Send audio file
        await ctx.send(
            f"📐 {expression}\n🔊 {result.processed[:100]}...",
            file=discord.File(output_file)
        )
        
        # Cleanup
        os.remove(output_file)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

bot.run('YOUR_BOT_TOKEN')
```

### Accessibility Tool Integration

```python
# Screen reader integration
import pyautogui
import keyboard

def on_math_hotkey():
    # Get selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    
    # Get clipboard content
    import pyperclip
    expression = pyperclip.paste()
    
    if expression:
        # Process and speak
        result = engine.process_latex(expression)
        asyncio.run(engine.speak_expression(result, "accessibility.mp3"))
        
        # Play audio
        player = AudioPlayer()
        player.play_file("accessibility.mp3")

# Register hotkey
keyboard.add_hotkey('ctrl+alt+m', on_math_hotkey)
```

### Educational Platform Integration

```python
# LMS/Educational platform integration
class MathSpeakLesson:
    def __init__(self, engine):
        self.engine = engine
        self.audio_files = []
    
    def add_expression(self, expression: str, explanation: str = ""):
        """Add math expression with optional explanation"""
        result = self.engine.process_latex(expression)
        
        # Combine expression and explanation
        full_text = result.processed
        if explanation:
            full_text += f". {explanation}"
        
        # Generate audio
        audio_file = f"lesson_{len(self.audio_files)}.mp3"
        asyncio.run(self.engine.tts_manager.generate_speech(
            full_text, audio_file
        ))
        
        self.audio_files.append({
            'expression': expression,
            'text': full_text,
            'audio': audio_file
        })
    
    def generate_lesson(self, output_dir: str):
        """Generate complete lesson with all audio files"""
        # Create lesson package...
```

---

## Best Practices Summary

1. **Always test your expressions** first in interactive mode
2. **Use appropriate contexts** for domain-specific notation
3. **Break complex expressions** into smaller parts
4. **Enable caching** for repeated expressions
5. **Use batch processing** for multiple expressions
6. **Choose the right voice** for different content types
7. **Add textual context** for clearer pronunciation
8. **Monitor performance** with --stats flag
9. **Use offline TTS** when speed is critical
10. **Keep expressions readable** - if it's hard to read, it's hard to speak

---

## Getting Help

- GitHub Issues: [Report bugs and request features]
- Documentation: This guide and inline help (`python mathspeak.py --help`)
- Interactive Mode: Explore features with `/help` command
- Debug Mode: Use `--debug` flag for detailed logging

---

*MathSpeak - Making Mathematics Audible*