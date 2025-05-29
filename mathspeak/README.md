# MathSpeak - Ultimate Mathematical Text-to-Speech System

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/status-production--ready-brightgreen.svg" alt="Status">
</p>

Transform LaTeX mathematical expressions into natural, professor-quality speech with intelligent multi-voice narration.

## 🎯 Features

- **Complete Mathematical Coverage**: Handles notation from undergraduate through graduate level mathematics
- **7 Distinct Voice Roles**: Different voices for theorems, definitions, proofs, examples, and more
- **Intelligent Context Detection**: Automatically recognizes mathematical domains and adjusts pronunciation
- **Natural Language Processing**: Varies word choices and adds clarifications for human-like speech
- **9+ Mathematical Domains**: Topology, Complex Analysis, Numerical Analysis, and more
- **High Performance**: 1000+ tokens/second with intelligent caching
- **Professor Commentary**: Optional explanatory comments like a real math professor
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

```bash
# Basic installation
pip install mathspeak

# With audio playback support
pip install mathspeak[audio]

# Development installation
git clone https://github.com/yourusername/mathspeak.git
cd mathspeak
pip install -e .[dev]
```

### Basic Usage

```python
from mathspeak import MathSpeak

# Create instance
ms = MathSpeak()

# Convert and speak
ms.speak("∀ε>0 ∃δ>0 : |x-a|<δ ⟹ |f(x)-f(a)|<ε")
# Output: "for every epsilon greater than zero, there exists delta greater than zero such that..."

# Convert to text only
text = ms.to_text("∫_0^∞ e^{-x²} dx = √π/2")
print(text)
# Output: "the integral from 0 to infinity of e to the negative x squared d x equals square root of pi over 2"

# Save to audio file
ms.save_speech("e^{iπ} = -1", "euler_identity.mp3")
```

### Command Line Interface

```bash
# Convert a single expression
mathspeak "x^2 + y^2 = r^2"

# Interactive mode
mathspeak --interactive

# Convert a LaTeX file
mathspeak --file lecture.tex --output lecture.mp3

# Run tests
mathspeak --test
```

## 📚 Supported Mathematics

### Domains

- **Topology**: Point-set, algebraic, differential topology
- **Complex Analysis**: Holomorphic functions, contour integration, residues
- **Numerical Analysis**: Error analysis, iterative methods, matrix computations
- **Differential Geometry**: Manifolds, connections, curvature (coming soon)
- **ODEs**: Differential equations, stability analysis (coming soon)
- **Real Analysis**: Limits, continuity, measure theory (coming soon)
- **And more...**

### Example Expressions

```python
# Topology
"π₁(S¹) ≅ ℤ"  # "the fundamental group of the circle is isomorphic to the integers"

# Complex Analysis  
"∮_C f(z)dz = 2πi ∑ Res(f, z_k)"  # "the contour integral over C of f of z d z equals..."

# Numerical Analysis
"‖x_{k+1} - x_k‖ < ε"  # "the norm of x sub k plus 1 minus x sub k is less than epsilon"
```

## 🎤 Voice System

MathSpeak uses 7 distinct voices for different mathematical contexts:

| Voice Role | Usage | Example |
|------------|-------|---------|
| NARRATOR | Default narration | General text |
| DEFINITION | Clear, slow for definitions | "A space X is compact if..." |
| THEOREM | Authoritative for results | "Theorem 3.1 states..." |
| PROOF | Methodical for proofs | "We proceed by induction..." |
| EXAMPLE | Conversational | "For instance, consider..." |
| EMPHASIS | Critical insights | "This is the KEY observation..." |
| WARNING | Common mistakes | "Don't confuse this with..." |

## ⚙️ Configuration

```python
from mathspeak import MathSpeak, Config

# Create with custom config
config = Config()
config.voice.speed_multiplier = 1.2  # Faster speech
config.natural_language.add_clarifications = True
config.processing.enable_caching = True

ms = MathSpeak(config)

# Or modify after creation
ms.set_voice_speed(0.8)  # Slower
ms.enable_domain('topology')
ms.disable_domain('algorithms')
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_engine.py -v
pytest tests/test_domains.py::TestTopology

# Run with coverage
pytest --cov=mathspeak tests/
```

## 🔧 Advanced Usage

### Custom Domain Processors

```python
from mathspeak.core import MathematicalTTSEngine
from mathspeak.domains import TopologyProcessor

# Create engine with specific domains
engine = MathematicalTTSEngine()
engine.domain_processors['topology'] = TopologyProcessor()

# Process with forced context
result = engine.process_latex(
    "X is compact", 
    force_context=MathematicalContext.TOPOLOGY
)
```

### Context Memory

```python
# MathSpeak remembers defined symbols
ms.speak("Let X be a topological space")
ms.speak("Then X is Hausdorff")  # Knows X is a topological space
```

### Performance Monitoring

```python
info = ms.get_info()
print(f"Cache hit rate: {info['performance']['cache_hit_rate']*100:.1f}%")
print(f"Unknown commands: {info['performance']['unknown_commands']}")
```

## 📊 Architecture

```
mathspeak/
├── core/               # Core system components
│   ├── engine.py      # Main orchestration
│   ├── voice_manager.py # Multi-voice system
│   ├── context_memory.py # Symbol tracking
│   └── natural_language.py # Language processing
├── domains/           # Mathematical domain processors
│   ├── topology.py
│   ├── complex_analysis.py
│   └── ...
└── utils/             # Configuration and logging
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- Additional mathematical domains
- More natural language variations
- Performance optimizations
- Additional language support
- Better error handling for edge cases

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built for mathematics students and researchers
- Inspired by the need for accessible mathematical content
- Special thanks to the edge-tts project for speech synthesis

## 📞 Support

- **Documentation**: [https://mathspeak.readthedocs.io](https://mathspeak.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/yourusername/mathspeak/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mathspeak/discussions)

---

<p align="center">
Made with ❤️ for the mathematics community
</p>