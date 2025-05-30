# MS Command Quick Reference

## 🎉 Your `ms` shortcut is ready!

The MathSpeak shortcut has replaced your old `ms` command. You can now use it from any terminal!

## 📋 Copy-Paste Examples

### Basic Usage
```bash
# Simple expressions
ms "x^2 + y^2 = r^2"
ms "2 + 2 = 4"
ms "\sqrt{16} = 4"

# Fractions
ms "\frac{1}{2} + \frac{1}{3} = \frac{5}{6}"
ms "\frac{d}{dx} x^n = nx^{n-1}"

# Integrals
ms "\int x^2 dx"
ms "\int_0^1 x dx = \frac{1}{2}"
ms "\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"

# Summations
ms "\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}"
ms "\sum_{k=0}^n \binom{n}{k} = 2^n"

# Limits
ms "\lim_{x \to 0} \frac{\sin x}{x} = 1"
ms "\lim_{n \to \infty} (1 + \frac{1}{n})^n = e"
```

### Save Audio Files
```bash
# Auto-generate filename
ms "\pi \approx 3.14159" --save

# Custom filename
ms "E = mc^2" --output einstein.mp3

# Save to specific directory
ms "\nabla \cdot \vec{F} = 0" --output ~/Desktop/divergence.mp3
```

### Advanced Features
```bash
# Show statistics
ms "x^2 + y^2 = z^2" --stats

# Use offline TTS (faster)
ms "\int \sin x dx = -\cos x + C" --offline

# Interactive mode
ms --interactive

# Process file
ms --file equations.tex

# Batch processing
ms --batch formulas.txt --batch-output ./audio/

# Slower speech
ms "\pi_1(S^1) \cong \mathbb{Z}" --speed 0.8

# Show help
ms --help
```

## 🚀 Quick Tips

### Shell Escaping
```bash
# Use single quotes to avoid escaping
ms '\sum_{i=1}^n i = \frac{n(n+1)}{2}'

# Or escape backslashes
ms "\\sum_{i=1}^n i = \\frac{n(n+1)}{2}"
```

### Complex Expressions
```bash
# Matrices
ms '\begin{bmatrix} a & b \\ c & d \end{bmatrix}'

# Greek letters
ms '\alpha + \beta = \gamma'

# Set notation
ms 'x \in \mathbb{R}, y \in \mathbb{C}'

# Logic
ms '\forall x \exists y : f(x) = y'

# Topology
ms '\pi_1(S^1) \cong \mathbb{Z}'

# Complex analysis
ms '\oint_C \frac{f(z)}{z-a} dz = 2\pi i f(a)'
```

## ⚡ Productivity Shortcuts

### Create Aliases for Common Uses
Add to ~/.bashrc:
```bash
# Quick save
alias mss='ms --save'

# Offline mode
alias mso='ms --offline'

# Interactive
alias msi='ms --interactive'

# With stats
alias mst='ms --stats'
```

### Bash Function for Note-Taking
Add to ~/.bashrc:
```bash
# Function to speak and save math notes
mathnote() {
    local expr="$1"
    local name="${2:-math_note}"
    ms "$expr" --output "${name}_$(date +%Y%m%d_%H%M%S).mp3"
}

# Usage: mathnote "\int x dx" "integral"
```

### Integration with Other Tools
```bash
# Pipe from other commands
echo '\frac{d}{dx} \sin x = \cos x' | xargs ms

# Use with find
find . -name "*.tex" -exec ms --file {} \;

# Watch clipboard (requires xclip)
watch -n 2 'xclip -o | xargs -I {} ms "{}"'
```

## 📁 File Locations

- **Alias**: `~/.bashrc` (search for "MathSpeak")
- **Script**: `~/bin/ms`
- **Logs**: `~/.mathspeak/logs/`
- **Cache**: `~/.mathspeak/cache/`

## 🔧 Troubleshooting

### If `ms` command not found:
```bash
# Reload bashrc
source ~/.bashrc

# Or add ~/bin to PATH manually
export PATH="$HOME/bin:$PATH"
```

### To update the shortcut:
```bash
# Edit the script
nano ~/bin/ms

# Or recreate alias
alias ms='python /path/to/mathspeak.py'
```

## 🎯 Most Used Commands

Based on typical usage, here are the commands you'll use most:

```bash
# Quick expression
ms '\int_0^1 x^2 dx'

# Save for later
ms '\sum_{n=1}^\infty \frac{1}{n!} = e - 1' --save

# Offline for speed
ms '\nabla^2 f = 0' --offline

# From clipboard (if you have xclip)
xclip -o | xargs ms

# Interactive for multiple
ms -i
```

Enjoy your new MathSpeak command! 🎉