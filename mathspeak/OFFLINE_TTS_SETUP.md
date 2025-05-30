# Offline TTS Setup Guide

MathSpeak supports both online and offline Text-to-Speech engines. While online engines (Microsoft Edge TTS, Google TTS) provide higher quality voices, offline engines ensure the system works without internet connectivity.

## Supported Offline Engines

### 1. **pyttsx3** (Cross-platform)
- Works on Windows, macOS, and Linux
- Uses system TTS engines:
  - Windows: SAPI5
  - macOS: NSSpeechSynthesizer ('say' command)
  - Linux: espeak-ng

### 2. **espeak-ng** (Linux/macOS)
- Lightweight, open-source speech synthesizer
- Supports multiple languages and voices
- Very fast but more robotic sounding

## Installation Instructions

### Quick Install

Run the installation helper:
```bash
python install_offline_tts.py
```

### Manual Installation

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y espeak-ng espeak-ng-data python3-dev

# Install Python packages
pip install pyttsx3 py-espeak-ng
```

#### Linux (Fedora/RHEL)
```bash
# Install system dependencies
sudo dnf install -y espeak-ng espeak-ng-devel python3-devel

# Install Python packages
pip install pyttsx3 py-espeak-ng
```

#### Linux (Arch)
```bash
# Install system dependencies
sudo pacman -S espeak-ng

# Install Python packages
pip install pyttsx3 py-espeak-ng
```

#### macOS
```bash
# Install espeak-ng (optional, macOS has built-in TTS)
brew install espeak-ng

# Install Python packages
pip install pyttsx3

# Note: macOS includes high-quality voices through the 'say' command
# which pyttsx3 will use automatically
```

#### Windows
```bash
# Windows has built-in SAPI5 voices
# Just install the Python package
pip install pyttsx3

# For additional voices:
# Go to Settings → Time & Language → Speech → Add voices
```

## Usage

### Command Line

Use offline TTS engines:
```bash
# Prefer offline engines
python mathspeak.py --offline "\\int_0^\\infty e^{-x^2} dx"

# Force specific offline engine (in code)
python mathspeak.py "x^2 + y^2 = r^2" --offline
```

### Python API

```python
from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

# Create engine preferring offline TTS
voice_manager = VoiceManager()
engine = MathematicalTTSEngine(
    voice_manager=voice_manager,
    prefer_offline_tts=True  # This prioritizes offline engines
)

# Process expression
result = engine.process_latex("\\frac{d}{dx} f(x) = f'(x)")

# Generate speech with offline engine
await engine.speak_expression(result, output_file="output.mp3")
```

## Voice Quality Comparison

| Engine | Quality | Speed | Offline | Voices |
|--------|---------|-------|---------|---------|
| Edge TTS | Excellent | Fast | No | Many |
| Google TTS | Very Good | Fast | No | Limited |
| pyttsx3 (Windows) | Good | Very Fast | Yes | System |
| pyttsx3 (macOS) | Very Good | Very Fast | Yes | System |
| espeak-ng | Robotic | Ultra Fast | Yes | Many |

## Troubleshooting

### Linux: "No module named 'espeak'"
```bash
# Ensure espeak-ng is installed
sudo apt-get install espeak-ng python3-dev
# Reinstall py-espeak-ng
pip install --force-reinstall py-espeak-ng
```

### macOS: "No voices found"
```bash
# Check available voices
say -v ?
# If no voices, download from System Preferences
```

### Windows: "No module named 'win32com'"
```bash
pip install pywin32
# Then restart Python/terminal
```

### General: Test offline engines
```bash
# Run the test script
python test_tts_engines.py
```

## Performance Tips

1. **Cache Enable**: Always keep caching enabled for offline use
   ```bash
   python mathspeak.py "expression" --offline  # cache is on by default
   ```

2. **Voice Selection**: Some offline voices are better for math:
   - Windows: Use "Microsoft David" or "Microsoft Zira"
   - macOS: Use "Alex" or "Samantha"
   - Linux: Use espeak-ng with 'en+m3' voice

3. **Batch Processing**: Offline engines are very fast for batch processing:
   ```bash
   python mathspeak.py --batch expressions.txt --offline --batch-output ./output/
   ```

## Engine Priority

When `prefer_offline_tts=True`:
1. pyttsx3 (if available)
2. espeak-ng (if available)
3. Edge TTS (fallback, requires internet)
4. Google TTS (fallback, requires internet)

When `prefer_offline_tts=False` (default):
1. Edge TTS (best quality)
2. Google TTS
3. pyttsx3 (fallback)
4. espeak-ng (fallback)

## Adding Custom Voices

### Windows
- Download additional SAPI5 voices
- Install voice packages from Microsoft

### macOS
- System Preferences → Accessibility → Spoken Content
- Download additional voices

### Linux
- Install mbrola voices for better quality:
  ```bash
  sudo apt-get install mbrola mbrola-us1
  ```

## Conclusion

Offline TTS ensures MathSpeak works anywhere, anytime. While the voice quality may not match online engines, the ultra-fast processing and zero-latency response make offline engines ideal for:
- Batch processing large documents
- Systems without internet access  
- Privacy-conscious users
- Real-time applications

For the best experience, we recommend having both online and offline engines installed, letting MathSpeak choose the best available option automatically.