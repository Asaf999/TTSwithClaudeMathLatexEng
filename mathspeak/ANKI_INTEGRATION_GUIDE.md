# MathSpeak Anki Integration Guide

## Overview

MathSpeak can automatically add audio pronunciations to your mathematical Anki cards! This integration:
- Finds LaTeX expressions in your cards
- Generates natural speech audio files
- Adds audio playback to your cards
- Works with all mathematical domains

## Quick Start

### 1. Basic Setup

```bash
# First, close Anki to avoid database conflicts

# Scan your collection for math cards
python anki_integration.py scan

# Process a specific deck
python anki_integration.py process --deck "Calculus"

# Process with auto-update (modifies your cards)
python anki_integration.py process --deck "Calculus" --auto-update
```

### 2. Installation

The integration script is included with MathSpeak. No additional installation needed!

## Usage Examples

### Scanning for Math Cards

Find all cards with mathematical expressions:

```bash
# Scan entire collection
python anki_integration.py scan

# Scan specific deck
python anki_integration.py scan --deck "Linear Algebra"

# Scan by tag
python anki_integration.py scan --tag "mathematics"

# Custom collection path
python anki_integration.py scan --collection "/path/to/collection.anki2"
```

### Processing Cards

Generate audio for mathematical expressions:

```bash
# Process deck (preview mode - no changes)
python anki_integration.py process --deck "Calculus"

# Process and update cards automatically
python anki_integration.py process --deck "Calculus" --auto-update

# Use offline TTS for privacy/speed
python anki_integration.py process --deck "Calculus" --offline --auto-update

# Filter by tag
python anki_integration.py process --deck "All" --tag "exam" --auto-update
```

### Exporting Audio Packages

Create shareable audio packages:

```bash
# Export all audio for a deck
python anki_integration.py export --deck "Topology" --output topology_audio.zip

# Share with classmates who can import into their Anki
```

## How It Works

### 1. **Expression Detection**

The integration detects various LaTeX formats:
- Inline math: `$x^2 + y^2 = r^2$`
- Display math: `$$\int_0^\infty e^{-x^2} dx$$`
- LaTeX delimiters: `\[...\]` and `\(...\)`
- Anki LaTeX: `[latex]...[/latex]`

### 2. **Audio Generation**

For each expression found:
- Processes through MathSpeak engine
- Generates MP3 audio file
- Saves to Anki media folder
- Names files uniquely to avoid conflicts

### 3. **Card Updates**

Two strategies for adding audio:

**Auto-play (default):**
```
Original: Find the derivative of $f(x) = x^2$
Updated:  Find the derivative of $f(x) = x^2$ [sound:mathspeak_12345_0_a1b2c3d4.mp3]
```

**Click-to-play:**
```
Original: Solve $\int x dx$
Updated:  Solve $\int x dx$ 🔊
```

## Card Format Examples

### Before Integration

**Front:**
```
What is the fundamental group of the circle?
```

**Back:**
```
$\pi_1(S^1) \cong \mathbb{Z}$

This shows that loops on a circle are classified by their winding number.
```

### After Integration

**Front:**
```
What is the fundamental group of the circle?
```

**Back:**
```
$\pi_1(S^1) \cong \mathbb{Z}$ [sound:mathspeak_12345_0_abc123.mp3]

This shows that loops on a circle are classified by their winding number.
```

## Advanced Usage

### Python API

```python
from anki_integration import AnkiMathSpeakIntegration

# Initialize
integration = AnkiMathSpeakIntegration(prefer_offline=True)

# Extract math from specific cards
cards = integration.extract_math_from_cards(
    deck_name="Calculus",
    tag_filter="derivatives"
)

# Process individual card
for card in cards:
    audio_files = await integration.generate_audio_for_card(card)
    updated_content = integration.update_card_with_audio(card, audio_files)
```

### Custom Audio Settings

```python
# Modify the integration class
integration.audio_format = "wav"  # Higher quality
integration.audio_prefix = "math_"  # Custom prefix

# Process with custom voice settings
integration.engine.voice_manager.set_speed(0.9)  # Slower
```

### Batch Processing Script

```python
#!/usr/bin/env python3
# process_all_math_decks.py

import asyncio
from anki_integration import AnkiMathSpeakIntegration

async def process_all_math_decks():
    integration = AnkiMathSpeakIntegration()
    
    math_decks = [
        "Calculus I",
        "Calculus II", 
        "Linear Algebra",
        "Topology",
        "Complex Analysis"
    ]
    
    for deck in math_decks:
        print(f"\nProcessing {deck}...")
        stats = integration.batch_process_deck(
            deck_name=deck,
            auto_update=True,
            backup_first=True
        )
        print(f"Completed: {stats['audio_generated']} audio files")

asyncio.run(process_all_math_decks())
```

## Best Practices

### 1. **Backup First**
Always backup before auto-updating:
```bash
# Automatic backup (default)
python anki_integration.py process --deck "Math" --auto-update

# Skip backup (not recommended)
python anki_integration.py process --deck "Math" --auto-update --no-backup
```

### 2. **Test First**
Process without updating to preview:
```bash
# Preview mode
python anki_integration.py process --deck "Test Deck"

# Check generated audio in collection.media folder
# If satisfied, run with --auto-update
```

### 3. **Organize by Tags**
Use tags for better organization:
```anki
Tags: mathematics calculus derivatives audio-enabled
```

Then process by tag:
```bash
python anki_integration.py process --tag "audio-enabled" --auto-update
```

### 4. **Performance Tips**

**For large collections:**
```bash
# Use offline TTS for speed
python anki_integration.py process --deck "Large Deck" --offline

# Process in batches
python anki_integration.py process --tag "chapter1" --auto-update
python anki_integration.py process --tag "chapter2" --auto-update
```

## Troubleshooting

### Common Issues

**1. "Anki collection not found"**
```bash
# Specify path manually
python anki_integration.py scan --collection "~/Documents/Anki/User 1/collection.anki2"
```

**2. "Database is locked"**
- Close Anki before running integration
- Ensure no other Anki processes are running

**3. "Audio not playing"**
- Check Anki media folder permissions
- Verify audio files exist in collection.media
- Try Tools → Check Media in Anki

**4. "Math not detected"**
Ensure proper LaTeX formatting:
- Use dollar signs: `$...$`
- Or LaTeX tags: `[latex]...[/latex]`
- Check for typos in expressions

### Manual Audio Addition

If auto-update fails, add manually:

1. Find audio files in `collection.media` folder
2. Edit card in Anki
3. Add sound tag: `[sound:mathspeak_xxxxx.mp3]`

## Tips for Different Subjects

### Calculus Cards
```latex
Front: Evaluate $\lim_{x \to 0} \frac{\sin x}{x}$
Back: $\lim_{x \to 0} \frac{\sin x}{x} = 1$ [sound:...]
```

### Linear Algebra
```latex
Front: Find eigenvalues of $\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$
Back: $\lambda_1 = \frac{5 + \sqrt{33}}{2}, \lambda_2 = \frac{5 - \sqrt{33}}{2}$ [sound:...]
```

### Topology
```latex
Front: Define compactness
Back: A space $X$ is compact if every open cover has a finite subcover [sound:...]
```

## Integration with Anki Add-ons

### AwesomeTTS Compatibility
MathSpeak audio files work with AwesomeTTS:
- Files are standard MP3 format
- Can be played with AwesomeTTS controls
- No conflicts with existing TTS

### MathJax Compatibility
Works perfectly with MathJax:
- Process after MathJax rendering
- Audio complements visual display

## Future Enhancements

Planned features:
1. Real-time audio generation in Anki
2. AnkiConnect API support
3. Mobile app integration
4. Automatic re-processing on card edits
5. Voice selection per card type

## Conclusion

MathSpeak Anki integration makes mathematical flashcards more accessible and effective. The audio pronunciation helps with:
- Learning correct mathematical terminology
- Studying without looking at screen
- Accessibility for visual impairments
- Reinforcement through multiple senses

Start with a small deck to test, then expand to your entire collection!