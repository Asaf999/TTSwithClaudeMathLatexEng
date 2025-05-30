# MathSpeak Architecture

## System Overview

MathSpeak is a modular mathematical text-to-speech system designed for scalability, maintainability, and extensibility. The architecture follows clean separation of concerns with well-defined interfaces between components.

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  CLI Interface  │  Anki Addon  │  Python API  │  Web Interface  │
└─────────────────┴──────────────┴──────────────┴─────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────┐
│                      Core Engine Layer                          │
├─────────────────────────────────────────────────────────────────┤
│                  MathematicalTTSEngine                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   LaTeX Parser  │  │ Pattern Manager │  │ Context Manager │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Layer                              │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ Pattern Handlers │ │ Domain Processors│ │ Natural Language │ │
│ │                  │ │                  │ │   Enhancement    │ │
│ │ • Arithmetic     │ │ • Calculus       │ │                  │ │
│ │ • Algebra        │ │ • Topology       │ │ • Professor Style│ │
│ │ • Calculus       │ │ • Analysis       │ │ • Explanations   │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────┐
│                      Voice Layer                                │
├─────────────────────────────────────────────────────────────────┤
│                     VoiceManager                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Voice Roles   │  │  Speed Profiles │  │ Speech Segments │ │
│  │                 │  │                 │  │                 │ │
│  │ • Professor     │  │ • Slow          │  │ • Introduction  │ │
│  │ • Assistant     │  │ • Normal        │  │ • Math Content  │ │
│  │ • Student       │  │ • Fast          │  │ • Explanation   │ │
│  │ • Narrator      │  │ • Variable      │  │ • Conclusion    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────┐
│                      TTS Engine Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                   TTSEngineManager                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Edge TTS      │  │     gTTS        │  │   Pyttsx3       │ │
│  │   (Online)      │  │   (Online)      │  │   (Offline)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │    eSpeak       │  │ Connection Pool │                      │
│  │   (Offline)     │  │   & Fallback    │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                         │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │      Cache       │ │     Logging      │ │   Monitoring     │ │
│ │                  │ │                  │ │                  │ │
│ │ • Expression     │ │ • Structured     │ │ • Performance    │ │
│ │ • Audio          │ │ • Configurable   │ │ • Metrics        │ │
│ │ • Pattern        │ │ • Multi-level    │ │ • Health Checks  │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. MathematicalTTSEngine

The central orchestrator that coordinates all system components.

**Responsibilities:**
- LaTeX expression parsing and validation
- Pattern-based text transformation
- Context management and audience adaptation
- Performance monitoring and caching
- Error handling and recovery

**Key Features:**
- Asynchronous processing pipeline
- Comprehensive caching with TTL
- Unknown command tracking and learning
- Performance metrics collection
- Thread-safe operations

### 2. Pattern Processing System

A modular system for converting mathematical notation to natural language.

#### Pattern Handlers
```
PatternHandler (Abstract Base Class)
├── ArithmeticHandler
│   ├── Basic operations (+, -, *, /)
│   ├── Fractions and percentages
│   └── Number formatting
├── AlgebraHandler
│   ├── Polynomials and equations
│   ├── Functions and relations
│   └── Set notation
└── CalculusHandler
    ├── Derivatives and integrals
    ├── Limits and continuity
    └── Series and sequences
```

#### Pattern Rules
Each pattern rule contains:
- **Regex Pattern**: Matches LaTeX expressions
- **Replacement Template**: Natural language template
- **Priority Level**: Processing order
- **Domain Classification**: Mathematical domain
- **Audience Level**: Complexity appropriateness
- **Examples**: Test cases and documentation

### 3. Domain Processors

Specialized processors for advanced mathematical domains.

```
DomainProcessor (Abstract Base Class)
├── TopologyProcessor
│   ├── Topological spaces
│   ├── Continuity and compactness
│   └── Homology and homotopy
├── AnalysisProcessor
│   ├── Real and complex analysis
│   ├── Measure theory
│   └── Functional analysis
└── AlgebraicProcessor
    ├── Group theory
    ├── Ring theory
    └── Field theory
```

### 4. Voice Management System

#### Voice Roles
- **Professor**: Authoritative, measured delivery for main content
- **Assistant**: Helpful, clarifying tone for explanations
- **Student**: Questioning, curious tone for examples
- **Narrator**: Neutral, documentary style for context
- **Emphasis**: Strong, clear delivery for important concepts
- **Example**: Practical, demonstration tone
- **Definition**: Precise, formal tone for definitions

#### Speech Segments
- **Introduction**: Context and setup
- **Mathematical Content**: Core equations and expressions
- **Explanation**: Detailed breakdowns
- **Examples**: Practical demonstrations
- **Conclusion**: Summary and implications

### 5. TTS Engine Layer

#### Supported Engines
1. **Edge TTS** (Primary)
   - High-quality neural voices
   - Multiple languages and accents
   - Cloud-based processing
   - SSML support

2. **Google TTS (gTTS)**
   - Google's text-to-speech API
   - Reliable cloud service
   - Multiple language support
   - Good quality output

3. **Pyttsx3** (Offline fallback)
   - Local system TTS
   - Cross-platform compatibility
   - No internet required
   - Configurable voices

4. **eSpeak** (Lightweight fallback)
   - Fast, lightweight synthesis
   - Highly portable
   - Low resource usage
   - Mathematical symbol support

#### Connection Management
- **Connection Pooling**: Reuse connections for efficiency
- **Automatic Fallback**: Graceful degradation when engines fail
- **Load Balancing**: Distribute requests across available engines
- **Health Monitoring**: Track engine availability and performance

## Data Flow

### Processing Pipeline

```
LaTeX Input
    │
    ▼
┌─────────────────┐
│ Input Validation│
│ & Preprocessing │
└─────────────────┘
    │
    ▼
┌─────────────────┐    ┌─────────────────┐
│ Cache Lookup    │────│ Return Cached   │
│                 │    │ Result          │
└─────────────────┘    └─────────────────┘
    │ (Cache Miss)
    ▼
┌─────────────────┐
│ Pattern Matching│
│ & Transformation│
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Domain-Specific │
│ Processing      │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Natural Language│
│ Enhancement     │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Voice Role      │
│ Assignment      │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ TTS Synthesis   │
│ with Fallback   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Audio Output    │
│ & Caching       │
└─────────────────┘
```

### Error Handling Flow

```
Error Occurs
    │
    ▼
┌─────────────────┐
│ Error Type      │
│ Classification  │
└─────────────────┘
    │
    ├── Syntax Error ────► Pattern Fallback ────► Generic Processing
    │
    ├── TTS Error ──────► Engine Fallback ────► Alternative Engine
    │
    ├── Network Error ──► Offline Mode ──────► Local Processing
    │
    └── Unknown Error ──► Logging & Recovery ► Graceful Degradation
```

## Extensibility Points

### Adding New Pattern Handlers

```python
from core.patterns.base import PatternHandler, PatternRule, MathDomain

class GeometryHandler(PatternHandler):
    @property
    def domain(self):
        return MathDomain.GEOMETRY
    
    @property
    def name(self):
        return "Geometry"
    
    def get_patterns(self, audience_level=None):
        return [
            PatternRule(
                pattern=r"\\angle\s*([A-Z]+)",
                replacement="angle {0}",
                priority=10,
                domain=self.domain,
                audience_level=audience_level
            )
        ]
```

### Adding New TTS Engines

```python
from core.base_engines import EnhancedTTSEngine

class CustomTTSEngine(EnhancedTTSEngine):
    def __init__(self):
        super().__init__(name="CustomTTS")
    
    async def _initialize_connection(self):
        # Initialize custom TTS connection
        pass
    
    async def _synthesize_speech(self, text: str, voice: str = None) -> bytes:
        # Implement custom synthesis
        pass
```

### Adding New Domain Processors

```python
from domains.base import DomainProcessor

class PhysicsProcessor(DomainProcessor):
    @property
    def domain(self):
        return MathDomain.PHYSICS
    
    def process(self, text, context=None):
        # Physics-specific processing
        return processed_text
    
    def can_handle(self, text):
        return any(keyword in text for keyword in self.physics_keywords)
```

## Performance Considerations

### Caching Strategy
- **Expression Cache**: Processed mathematical expressions
- **Audio Cache**: Generated speech files with TTL
- **Pattern Cache**: Compiled regex patterns
- **Connection Cache**: Pooled TTS engine connections

### Optimization Techniques
- **Lazy Loading**: Load components on demand
- **Async Processing**: Non-blocking operations
- **Connection Pooling**: Reuse expensive connections
- **Batch Processing**: Handle multiple expressions efficiently
- **Memory Management**: Automatic cleanup and garbage collection

### Scalability Features
- **Horizontal Scaling**: Multiple engine instances
- **Load Balancing**: Distribute processing load
- **Circuit Breakers**: Prevent cascade failures
- **Rate Limiting**: Control resource usage
- **Monitoring**: Track performance metrics

## Security and Privacy

### Data Handling
- **No Persistent Storage**: Mathematical expressions not stored
- **Local Processing**: Offline modes available
- **Secure Connections**: HTTPS for cloud TTS services
- **Input Validation**: Prevent malicious LaTeX code injection

### Privacy Protection
- **Minimal Data Transmission**: Only necessary text sent to cloud services
- **User Control**: Option to use offline-only mode
- **No User Tracking**: No personal information collected
- **Audit Logging**: Security event tracking

## Testing Architecture

### Test Organization
```
tests_organized/
├── unit/
│   ├── core/          # Core engine tests
│   ├── domains/       # Domain processor tests
│   └── utils/         # Utility function tests
├── integration/
│   ├── anki/          # Anki integration tests
│   ├── cli/           # Command-line interface tests
│   └── tts/           # TTS engine integration tests
├── performance/       # Performance and benchmark tests
└── docs/             # Documentation tests
```

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **Performance Tests**: Benchmark and load testing
- **End-to-End Tests**: Complete workflow testing
- **Regression Tests**: Prevent functionality degradation

## Deployment Considerations

### Environment Support
- **Cross-Platform**: Windows, macOS, Linux support
- **Python Versions**: 3.8+ compatibility
- **Container Ready**: Docker support available
- **Cloud Deployable**: Scalable cloud deployment options

### Configuration Management
- **Environment Variables**: Runtime configuration
- **Configuration Files**: Structured settings
- **CLI Arguments**: Command-line overrides
- **Default Fallbacks**: Sensible defaults

This architecture enables MathSpeak to be maintainable, scalable, and extensible while providing high-quality mathematical text-to-speech conversion across various platforms and use cases.