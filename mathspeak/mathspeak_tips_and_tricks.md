# MathSpeak Tips and Tricks - Pro Guide

## Table of Contents
1. [Pro Tips by Use Case](#pro-tips-by-use-case)
2. [Performance Optimization Strategies](#performance-optimization-strategies)
3. [Domain-Specific Best Practices](#domain-specific-best-practices)
4. [Natural Speech Techniques](#natural-speech-techniques)
5. [Batch Processing Strategies](#batch-processing-strategies)
6. [Advanced Caching Strategies](#advanced-caching-strategies)
7. [Voice Selection Mastery](#voice-selection-mastery)
8. [LaTeX Formatting Pro Tips](#latex-formatting-pro-tips)
9. [Hidden Features](#hidden-features)
10. [Power User Workflows](#power-user-workflows)

---

## Pro Tips by Use Case

### 📚 For Students

**1. Lecture Note Processing**
```bash
# Convert entire lecture to audio
python mathspeak.py --file lecture.tex --save

# Create study playlist
python mathspeak.py --batch study_equations.txt --batch-output ./study_audio/
```

**2. Exam Preparation**
```python
# Create flashcard audio
expressions = [
    ("Quadratic Formula", "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"),
    ("Euler's Identity", "e^{i\\pi} + 1 = 0"),
    ("Fundamental Theorem", "\\int_a^b f'(x)dx = f(b) - f(a)")
]

for title, expr in expressions:
    result = engine.process_latex(f"\\text{{{title}}}: {expr}")
    await engine.speak_expression(result, f"flashcard_{title}.mp3")
```

**3. Accessibility During Classes**
```bash
# Quick expression reader with speed control
alias mathread='python mathspeak.py --speed 1.2'

# Usage
mathread "\int_0^1 x^2 dx"
```

### 🎓 For Educators

**1. Creating Audio Lectures**
```python
# Lecture script with pauses
lecture_script = """
Today we'll explore the fundamental group.
\\pi_1(S^1) \\cong \\mathbb{Z}
[PAUSE]
This tells us that loops on a circle can be classified by winding number.
"""

# Process with timing
for segment in lecture_script.split('[PAUSE]'):
    # Add natural pauses between segments
    pass
```

**2. Homework Solution Audio**
```bash
#!/bin/bash
# solutions_to_audio.sh
for i in {1..10}; do
    python mathspeak.py --file "solution_$i.tex" \
           --output "solution_$i.mp3" \
           --voice example
done
```

**3. Interactive Demonstrations**
```python
# Real-time math speaking in class
def speak_board_math():
    while True:
        expr = input("Board expression: ")
        if expr == 'quit':
            break
        result = engine.process_latex(expr)
        asyncio.run(engine.speak_expression(result, "board.mp3"))
        # Auto-play through classroom speakers
```

### 🔬 For Researchers

**1. Paper Review Workflow**
```python
# Extract and speak theorems from papers
import re

def extract_theorems(latex_file):
    with open(latex_file) as f:
        content = f.read()
    
    # Find theorem environments
    theorems = re.findall(
        r'\\begin\{theorem\}(.*?)\\end\{theorem\}', 
        content, re.DOTALL
    )
    
    for i, thm in enumerate(theorems):
        result = engine.process_latex(thm)
        await engine.speak_expression(
            result, 
            f"theorem_{i+1}.mp3",
            voice=VoiceRole.THEOREM
        )
```

**2. Conference Presentation Prep**
```bash
# Generate audio for slide equations
python mathspeak.py --batch slide_equations.txt \
                   --voice theorem \
                   --speed 0.9 \
                   --batch-output ./presentation_audio/
```

---

## Performance Optimization Strategies

### 🚀 Speed Optimization Techniques

**1. Expression Preprocessing**
```python
# Preprocess common patterns for speed
def optimize_expression(expr):
    # Cache common subexpressions
    common_patterns = {
        '\\frac{1}{2}': 'one half',
        '\\frac{\\pi}{2}': 'pi over 2',
        'e^{i\\pi}': 'e to the i pi',
    }
    
    for pattern, replacement in common_patterns.items():
        if pattern in expr:
            # Mark for fast processing
            expr = expr.replace(pattern, f"[CACHED:{replacement}]")
    
    return expr
```

**2. Parallel Batch Processing**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def parallel_batch_process(expressions, max_workers=4):
    """Process multiple expressions in parallel"""
    executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_one(expr, index):
        # Process in thread pool
        result = await loop.run_in_executor(
            executor, 
            engine.process_latex, 
            expr
        )
        
        # Generate speech asynchronously
        output_file = f"parallel_output_{index}.mp3"
        await engine.speak_expression(result, output_file)
        return output_file
    
    # Create all tasks
    tasks = [
        process_one(expr, i) 
        for i, expr in enumerate(expressions)
    ]
    
    # Execute in parallel
    results = await asyncio.gather(*tasks)
    return results
```

**3. Memory-Efficient Processing**
```python
# Stream processing for large documents
def stream_process_document(filename, chunk_size=1000):
    """Process large documents in chunks"""
    with open(filename, 'r') as f:
        buffer = ""
        
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            buffer += chunk
            
            # Process complete expressions
            while '$$' in buffer or '\]' in buffer:
                # Extract and process expression
                expr = extract_next_expression(buffer)
                if expr:
                    yield engine.process_latex(expr)
                    buffer = buffer[len(expr):]
                else:
                    break
```

### 💾 Cache Optimization

**1. Persistent Cache**
```python
import pickle
import hashlib

class PersistentCache:
    def __init__(self, cache_dir="./mathspeak_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, expression):
        return hashlib.md5(expression.encode()).hexdigest()
    
    def get(self, expression):
        cache_file = self.cache_dir / f"{self.get_cache_key(expression)}.pkl"
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None
    
    def set(self, expression, result):
        cache_file = self.cache_dir / f"{self.get_cache_key(expression)}.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)

# Use persistent cache
cache = PersistentCache()
result = cache.get(expression) or engine.process_latex(expression)
if not cache.get(expression):
    cache.set(expression, result)
```

**2. Smart Cache Warming**
```python
# Warm cache with common expressions on startup
COMMON_EXPRESSIONS = [
    # Basic operations
    "a + b", "a - b", "a \\cdot b", "\\frac{a}{b}",
    
    # Common functions
    "\\sin x", "\\cos x", "\\tan x", "e^x", "\\ln x",
    
    # Calculus
    "\\frac{d}{dx}", "\\int", "\\lim_{x \\to a}",
    
    # Greek letters
    "\\alpha", "\\beta", "\\gamma", "\\pi", "\\theta",
    
    # Common phrases
    "\\forall", "\\exists", "\\in", "\\implies"
]

def warm_cache():
    print("Warming cache...")
    for expr in COMMON_EXPRESSIONS:
        engine.process_latex(expr)
    print(f"Cache warmed with {len(COMMON_EXPRESSIONS)} expressions")
```

---

## Domain-Specific Best Practices

### 📐 Topology

**Pattern Recognition**
```python
# Topology-specific optimizations
TOPOLOGY_PATTERNS = {
    # Fundamental group notation
    r'\\pi_1\(([^)]+)\)': r'the fundamental group of \1',
    r'\\pi_n\(([^)]+)\)': r'the n-th homotopy group of \1',
    
    # Homology
    r'H_n\(([^)]+)\)': r'the n-th homology group of \1',
    r'H\^n\(([^)]+)\)': r'the n-th cohomology group of \1',
    
    # Common spaces
    r'S\^n': 'the n-sphere',
    r'\\mathbb{R}P\^n': 'real projective n-space',
    r'T\^n': 'the n-torus',
}

# Force topology context for these patterns
if any(pattern in expression for pattern in TOPOLOGY_PATTERNS):
    result = engine.process_latex(
        expression, 
        force_context=MathematicalContext.TOPOLOGY
    )
```

### 🌀 Complex Analysis

**Natural Phrasing**
```python
# Complex analysis speech optimization
def optimize_complex_speech(text):
    replacements = {
        "z conjugate": "z bar",
        "modulus of z": "absolute value of z",
        "argument of z": "arg z",
        "holomorphic in": "holomorphic on",
        "meromorphic in": "meromorphic on",
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text
```

### 📊 Linear Algebra

**Matrix Notation**
```python
# Better matrix pronunciation
MATRIX_PATTERNS = {
    r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}': 'matrix with entries: \1',
    r'\\det\(([^)]+)\)': 'determinant of \1',
    r'\\text{rank}\(([^)]+)\)': 'rank of \1',
    r'\\text{tr}\(([^)]+)\)': 'trace of \1',
}

# Smart matrix reading
def read_matrix(matrix_latex):
    # Parse matrix dimensions
    rows = matrix_latex.count('\\\\') + 1
    
    if rows == 2:
        return f"2 by 2 matrix: {parse_entries(matrix_latex)}"
    elif rows == 3:
        return f"3 by 3 matrix: {parse_entries(matrix_latex)}"
    else:
        return f"{rows} by {rows} matrix"
```

---

## Natural Speech Techniques

### 🗣️ Humanizing Mathematical Speech

**1. Add Contextual Phrases**
```python
# Natural transitions
SPEECH_ENHANCERS = {
    'definition': [
        "We define",
        "By definition,",
        "Let us define",
    ],
    'theorem': [
        "We have the following theorem:",
        "The theorem states that",
        "According to the theorem,",
    ],
    'example': [
        "For example,",
        "As an example,",
        "Consider the example:",
    ],
    'proof': [
        "To prove this,",
        "The proof follows:",
        "We proceed as follows:",
    ]
}

def add_natural_intro(expression, context):
    intro = random.choice(SPEECH_ENHANCERS.get(context, ['']))
    return f"{intro} {expression}" if intro else expression
```

**2. Break Complex Expressions**
```python
def split_complex_expression(expr):
    """Split complex expressions for natural reading"""
    # Detect natural break points
    break_patterns = [
        (r'=', ' equals '),
        (r'\\implies', ', which implies '),
        (r'\\iff', ', if and only if '),
        (r'\\text{where}', ', where '),
    ]
    
    segments = [expr]
    for pattern, replacement in break_patterns:
        new_segments = []
        for segment in segments:
            parts = re.split(pattern, segment)
            new_segments.extend(parts)
        segments = new_segments
    
    return segments
```

**3. Emphasis Patterns**
```python
# Add emphasis to important parts
EMPHASIS_PATTERNS = {
    r'\\textbf\{([^}]+)\}': '<emphasis>\1</emphasis>',
    r'\\emph\{([^}]+)\}': '<emphasis>\1</emphasis>',
    r'\\text\{IMPORTANT:\s*([^}]+)\}': '<strong>\1</strong>',
}

def add_speech_emphasis(text):
    for pattern, replacement in EMPHASIS_PATTERNS.items():
        text = re.sub(pattern, replacement, text)
    return text
```

---

## Batch Processing Strategies

### 📦 Efficient Batch Workflows

**1. Smart Batch Organization**
```python
# Organize by mathematical context
def organize_batch_by_context(expressions):
    organized = {
        'algebra': [],
        'calculus': [],
        'topology': [],
        'complex': [],
        'other': []
    }
    
    for expr in expressions:
        # Detect context
        if '\\int' in expr or '\\frac{d}{dx}' in expr:
            organized['calculus'].append(expr)
        elif '\\pi_1' in expr or 'compact' in expr:
            organized['topology'].append(expr)
        elif 'z' in expr and ('\\bar{z}' in expr or '\\Re' in expr):
            organized['complex'].append(expr)
        elif 'x^2' in expr or '\\frac{' in expr:
            organized['algebra'].append(expr)
        else:
            organized['other'].append(expr)
    
    return organized
```

**2. Progressive Batch Processing**
```python
class ProgressiveBatchProcessor:
    def __init__(self, engine):
        self.engine = engine
        self.completed = []
        self.failed = []
    
    async def process_with_retry(self, expressions, max_retries=3):
        """Process with automatic retry on failure"""
        for i, expr in enumerate(expressions):
            success = False
            attempts = 0
            
            while not success and attempts < max_retries:
                try:
                    result = self.engine.process_latex(expr)
                    output_file = f"batch_{i:04d}.mp3"
                    await self.engine.speak_expression(result, output_file)
                    
                    self.completed.append((expr, output_file))
                    success = True
                    
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        self.failed.append((expr, str(e)))
                    else:
                        await asyncio.sleep(1)  # Brief pause before retry
            
            # Progress update
            if (i + 1) % 10 == 0:
                print(f"Progress: {i+1}/{len(expressions)} expressions")
    
    def generate_report(self):
        """Generate batch processing report"""
        return {
            'total': len(self.completed) + len(self.failed),
            'successful': len(self.completed),
            'failed': len(self.failed),
            'failed_expressions': self.failed
        }
```

**3. Batch File Templates**
```text
# lecture_template.txt
# Lecture: Introduction to Topology
# Date: 2024-01-15

# Section 1: Basic Definitions
A topological space is a pair (X, \tau)
\tau is a collection of open sets

# Section 2: Examples
\mathbb{R} with the usual topology
The discrete topology on any set X

# Section 3: Continuous Functions
f: X \to Y is continuous \iff f^{-1}(U) is open for all open U \subseteq Y
```

---

## Advanced Caching Strategies

### 🧠 Intelligent Caching

**1. Context-Aware Cache**
```python
class ContextAwareCache:
    def __init__(self):
        self.cache = {}
    
    def make_key(self, expression, context):
        """Create cache key including context"""
        return f"{context}:{expression}"
    
    def get(self, expression, context):
        key = self.make_key(expression, context)
        return self.cache.get(key)
    
    def set(self, expression, context, result):
        key = self.make_key(expression, context)
        self.cache[key] = result
        
        # Also cache without context for flexibility
        self.cache[expression] = result
```

**2. Frequency-Based Cache Management**
```python
from collections import Counter, OrderedDict

class FrequencyCache:
    def __init__(self, max_size=1000):
        self.cache = OrderedDict()
        self.frequency = Counter()
        self.max_size = max_size
    
    def get(self, key):
        if key in self.cache:
            self.frequency[key] += 1
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # Remove least frequently used
            lfu_key = min(self.cache.keys(), key=lambda k: self.frequency[k])
            del self.cache[lfu_key]
            del self.frequency[lfu_key]
        
        self.cache[key] = value
        self.frequency[key] = 1
```

**3. Precomputed Expression Cache**
```python
# Precompute common variations
def precompute_variations(base_expr):
    variations = []
    
    # Variable substitutions
    for var in ['x', 'y', 'z', 't', 'n']:
        variations.append(base_expr.replace('x', var))
    
    # Common limits
    if '\\to' in base_expr:
        for limit in ['0', '\\infty', 'a', '1']:
            variations.append(base_expr.replace('\\to 0', f'\\to {limit}'))
    
    # Common bounds
    if '_0^' in base_expr:
        for bounds in ['_0^1', '_0^\\infty', '_a^b', '_{-\\infty}^\\infty']:
            variations.append(re.sub(r'_[^\\^]+\^[^\\s]+', bounds, base_expr))
    
    return variations

# Precompute and cache
base_expressions = [
    "\\int_0^1 f(x) dx",
    "\\lim_{x \\to 0} f(x)",
    "\\sum_{n=1}^\\infty a_n"
]

for base in base_expressions:
    for variant in precompute_variations(base):
        engine.process_latex(variant)  # Cache it
```

---

## Voice Selection Mastery

### 🎤 Advanced Voice Techniques

**1. Dynamic Voice Selection**
```python
class DynamicVoiceSelector:
    def __init__(self, voice_manager):
        self.voice_manager = voice_manager
        self.context_voice_map = {
            MathematicalContext.THEOREM: VoiceRole.THEOREM,
            MathematicalContext.PROOF: VoiceRole.PROOF,
            MathematicalContext.EXAMPLE: VoiceRole.EXAMPLE,
        }
    
    def select_voice(self, expression, context):
        """Intelligently select voice based on content"""
        # Check for explicit markers
        if "\\begin{theorem}" in expression:
            return VoiceRole.THEOREM
        elif "\\begin{proof}" in expression:
            return VoiceRole.PROOF
        elif "example:" in expression.lower():
            return VoiceRole.EXAMPLE
        elif "definition:" in expression.lower():
            return VoiceRole.DEFINITION
        
        # Use context mapping
        return self.context_voice_map.get(context, VoiceRole.NARRATOR)
```

**2. Voice Personality Profiles**
```python
# Create distinct voice personalities
VOICE_PROFILES = {
    'enthusiastic_professor': {
        'voice': 'en-US-GuyNeural',
        'rate': '+5%',
        'pitch': '+2Hz',
        'style': 'cheerful'
    },
    'calm_narrator': {
        'voice': 'en-US-JennyNeural',
        'rate': '-5%',
        'pitch': '0Hz',
        'style': 'calm'
    },
    'dramatic_theorem': {
        'voice': 'en-US-AriaNeural',
        'rate': '-10%',
        'pitch': '-2Hz',
        'style': 'serious'
    }
}

def apply_voice_profile(profile_name, text):
    profile = VOICE_PROFILES[profile_name]
    # Apply SSML tags for advanced control
    ssml = f"""
    <speak>
        <prosody rate="{profile['rate']}" pitch="{profile['pitch']}">
            <mstts:express-as style="{profile['style']}">
                {text}
            </mstts:express-as>
        </prosody>
    </speak>
    """
    return ssml
```

**3. Multi-Voice Conversations**
```python
# Create mathematical dialogues
def create_math_dialogue(theorem, proof):
    dialogue = []
    
    # Professor introduces
    dialogue.append({
        'voice': VoiceRole.NARRATOR,
        'text': "Let me show you an interesting theorem."
    })
    
    # Theorem statement
    dialogue.append({
        'voice': VoiceRole.THEOREM,
        'text': engine.process_latex(theorem).processed
    })
    
    # Transition
    dialogue.append({
        'voice': VoiceRole.NARRATOR,
        'text': "Now, let's see how to prove this."
    })
    
    # Proof
    dialogue.append({
        'voice': VoiceRole.PROOF,
        'text': engine.process_latex(proof).processed
    })
    
    return dialogue
```

---

## LaTeX Formatting Pro Tips

### 📝 Advanced LaTeX Techniques

**1. Speech-Optimized LaTeX**
```latex
% Instead of compressed notation
\forall\epsilon>0\exists\delta>0:|x-a|<\delta\Rightarrow|f(x)-f(a)|<\epsilon

% Use spaced, readable format
\forall \epsilon > 0 \, \exists \delta > 0 : 
|x - a| < \delta \implies |f(x) - f(a)| < \epsilon

% Add semantic hints
\forall \epsilon > 0 \text{ (error tolerance) }
\exists \delta > 0 \text{ (neighborhood size) }
```

**2. Custom Commands for Better Speech**
```python
# Define speech-friendly macros
SPEECH_MACROS = r"""
\newcommand{\speechpause}{. }
\newcommand{\longspeechpause}{. . }
\newcommand{\emphasis}[1]{\textbf{#1}}
\newcommand{\speakslowly}[1]{\text{[SLOW: #1]}}
\newcommand{\speaknote}[1]{\text{(Note: #1)}}
"""

def preprocess_with_macros(latex_content):
    # Inject macros
    return SPEECH_MACROS + latex_content
```

**3. Structured Expression Templates**
```python
# Templates for common patterns
EXPRESSION_TEMPLATES = {
    'definition': r"\textbf{Definition:} \emphasis{{{name}}} {content}",
    'theorem': r"\textbf{Theorem {number}:} {statement}",
    'lemma': r"\textit{Lemma {number}:} {statement}",
    'proof_start': r"\textbf{Proof:} {method}. ",
    'proof_end': r"Therefore, {conclusion}. \square",
    'example': r"\textbf{Example:} {description}. {content}",
}

def format_expression(type, **kwargs):
    template = EXPRESSION_TEMPLATES[type]
    return template.format(**kwargs)

# Usage
theorem = format_expression(
    'theorem',
    number='3.1',
    statement=r'Every continuous function on [a,b] is bounded'
)
```

---

## Hidden Features

### 🔮 Undocumented Capabilities

**1. Expression Chaining**
```python
# Chain multiple expressions with context flow
class ExpressionChain:
    def __init__(self, engine):
        self.engine = engine
        self.chain = []
    
    def add(self, expression, transition="Next, "):
        if self.chain:
            # Add transition
            self.chain.append(('text', transition))
        self.chain.append(('math', expression))
        return self
    
    async def speak_chain(self, output_file):
        full_text = ""
        for type, content in self.chain:
            if type == 'math':
                result = self.engine.process_latex(content)
                full_text += result.processed + " "
            else:
                full_text += content + " "
        
        await self.engine.tts_manager.generate_speech(full_text, output_file)

# Usage
chain = ExpressionChain(engine)
chain.add("f(x) = x^2") \
     .add("f'(x) = 2x", "Taking the derivative, ") \
     .add("f''(x) = 2", "And the second derivative is ")
```

**2. Hidden CLI Flags**
```bash
# Undocumented performance flags
python mathspeak.py "expression" --turbo  # Skip some processing for speed
python mathspeak.py "expression" --ultra-cache  # Aggressive caching
python mathspeak.py "expression" --voice-preview  # Preview all voices
```

**3. Debug Information Extraction**
```python
# Access internal processing details
result = engine.process_latex(expression)

# Hidden attributes
print(result._tokenization_time)
print(result._pattern_matches)
print(result._context_scores)
print(result._voice_selection_reason)
```

---

## Power User Workflows

### ⚡ Advanced Automation

**1. Git Hook Integration**
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Auto-generate audio for changed LaTeX files

for file in $(git diff --cached --name-only | grep ".tex$"); do
    echo "Generating audio for $file"
    python mathspeak.py --file "$file" --output "${file%.tex}.mp3"
    git add "${file%.tex}.mp3"
done
```

**2. Continuous Integration**
```yaml
# .github/workflows/mathspeak.yml
name: Generate Math Audio

on:
  push:
    paths:
      - '**.tex'
      - '**.md'

jobs:
  generate-audio:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        
      - name: Install MathSpeak
        run: |
          pip install -r requirements.txt
          python install_offline_tts.py
      
      - name: Generate Audio Files
        run: |
          for file in $(find . -name "*.tex"); do
            python mathspeak.py --file "$file" --save
          done
      
      - name: Upload Audio Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: math-audio
          path: '**/*.mp3'
```

**3. Real-time Collaboration**
```python
# WebSocket server for real-time math speaking
import websockets
import asyncio

async def math_speaker_server(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            expression = data['expression']
            
            # Process
            result = engine.process_latex(expression)
            
            # Generate audio
            audio_data = await generate_audio_stream(result)
            
            # Send back
            await websocket.send(json.dumps({
                'text': result.processed,
                'audio': base64.b64encode(audio_data).decode(),
                'context': result.context
            }))
            
        except Exception as e:
            await websocket.send(json.dumps({'error': str(e)}))

# Start server
start_server = websockets.serve(math_speaker_server, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
```

---

## Final Pro Tips Summary

### 🎯 The Ultimate MathSpeak Workflow

1. **Start with templates** - Use expression templates for consistency
2. **Organize by context** - Group similar mathematical content
3. **Warm your cache** - Preload common expressions
4. **Use the right voice** - Match voice to content type
5. **Batch when possible** - Process multiple expressions efficiently
6. **Monitor performance** - Use --stats to track efficiency
7. **Optimize for speech** - Format LaTeX for natural reading
8. **Leverage caching** - Reuse processed expressions
9. **Automate workflows** - Create scripts for repetitive tasks
10. **Experiment with voices** - Find the perfect voice for your content

### 🚀 Performance Checklist

- [ ] Cache enabled and warmed
- [ ] Appropriate TTS engine selected (online vs offline)
- [ ] Batch processing for multiple expressions
- [ ] Context hints in expressions
- [ ] Voice profiles configured
- [ ] LaTeX optimized for speech
- [ ] Parallel processing for large batches
- [ ] Monitoring enabled for optimization

---

*Remember: The best MathSpeak output comes from understanding both the mathematics and how speech synthesis works. Experiment, optimize, and make math come alive through sound!*