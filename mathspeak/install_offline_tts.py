#!/usr/bin/env python3
"""
Install Offline TTS Engines
===========================

Platform-specific installation helper for offline TTS engines.
"""

import sys
import os
import subprocess
import platform
from pathlib import Path


def install_on_linux():
    """Install offline TTS on Linux"""
    print("🐧 Linux detected - Installing offline TTS engines...")
    
    # Check for common package managers
    if os.path.exists('/usr/bin/apt-get'):
        # Debian/Ubuntu
        print("\n📦 Using apt-get...")
        print("Please run the following commands:")
        print("  sudo apt-get update")
        print("  sudo apt-get install -y espeak-ng espeak-ng-data python3-dev")
        print("  pip install pyttsx3 py-espeak-ng")
        
    elif os.path.exists('/usr/bin/dnf'):
        # Fedora/RHEL
        print("\n📦 Using dnf...")
        print("Please run the following commands:")
        print("  sudo dnf install -y espeak-ng espeak-ng-devel python3-devel")
        print("  pip install pyttsx3 py-espeak-ng")
        
    elif os.path.exists('/usr/bin/pacman'):
        # Arch Linux
        print("\n📦 Using pacman...")
        print("Please run the following commands:")
        print("  sudo pacman -S espeak-ng")
        print("  pip install pyttsx3 py-espeak-ng")
        
    else:
        print("\n⚠️  Unknown package manager")
        print("Please install 'espeak-ng' using your distribution's package manager")
        print("Then run: pip install pyttsx3 py-espeak-ng")
    
    # Check if espeak is already installed
    try:
        subprocess.run(['which', 'espeak-ng'], check=True, capture_output=True)
        print("\n✅ espeak-ng is already installed!")
    except:
        print("\n❌ espeak-ng not found. Please install it using the commands above.")


def install_on_macos():
    """Install offline TTS on macOS"""
    print("🍎 macOS detected - Installing offline TTS engines...")
    
    # Check for Homebrew
    try:
        subprocess.run(['which', 'brew'], check=True, capture_output=True)
        print("\n📦 Using Homebrew...")
        print("Please run the following commands:")
        print("  brew install espeak-ng")
        print("  pip install pyttsx3 py-espeak-ng")
        
        # macOS also has built-in 'say' command
        print("\n💡 Note: macOS also has a built-in 'say' command for TTS")
        print("   which pyttsx3 can use automatically.")
        
    except:
        print("\n⚠️  Homebrew not found")
        print("Please install Homebrew first: https://brew.sh")
        print("Then run:")
        print("  brew install espeak-ng")
        print("  pip install pyttsx3")


def install_on_windows():
    """Install offline TTS on Windows"""
    print("🪟 Windows detected - Installing offline TTS engines...")
    
    print("\n📦 Windows has built-in SAPI5 TTS engines")
    print("Please run the following command:")
    print("  pip install pyttsx3")
    
    print("\n💡 Additional voices can be installed from:")
    print("   Settings → Time & Language → Speech → Add voices")
    
    print("\n📝 For espeak on Windows (optional):")
    print("   1. Download from: http://espeak.sourceforge.net/download.html")
    print("   2. Install the Windows version")
    print("   3. Add espeak to your PATH")


def check_python_packages():
    """Check if Python TTS packages are installed"""
    print("\n🐍 Checking Python packages...")
    
    packages = {
        'pyttsx3': False,
        'gtts': False,
        'edge-tts': False,
    }
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            packages[package] = True
            print(f"  ✅ {package} is installed")
        except ImportError:
            print(f"  ❌ {package} is not installed")
    
    # Install missing packages
    missing = [pkg for pkg, installed in packages.items() if not installed]
    if missing:
        print(f"\n📦 To install missing packages:")
        print(f"  pip install {' '.join(missing)}")
    else:
        print("\n✅ All Python TTS packages are installed!")


def test_tts_engines():
    """Test available TTS engines"""
    print("\n🔊 Testing TTS engines...")
    
    # Test pyttsx3
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"\n✅ pyttsx3 is working with {len(voices)} voices available")
        engine.stop()
    except Exception as e:
        print(f"\n❌ pyttsx3 error: {e}")
    
    # Test system TTS
    system = platform.system()
    if system == "Linux":
        try:
            subprocess.run(['espeak-ng', '--version'], check=True, capture_output=True)
            print("✅ espeak-ng is available")
        except:
            print("❌ espeak-ng is not available")
    
    elif system == "Darwin":
        try:
            subprocess.run(['say', '-v', '?'], check=True, capture_output=True)
            print("✅ macOS 'say' command is available")
        except:
            print("❌ macOS 'say' command error")
    
    elif system == "Windows":
        print("✅ Windows SAPI5 should be available by default")


def main():
    """Main installation helper"""
    print("🎯 MathSpeak Offline TTS Installation Helper")
    print("=" * 50)
    
    system = platform.system()
    
    if system == "Linux":
        install_on_linux()
    elif system == "Darwin":
        install_on_macos()
    elif system == "Windows":
        install_on_windows()
    else:
        print(f"⚠️  Unknown operating system: {system}")
    
    # Check Python packages
    check_python_packages()
    
    # Test engines
    test_tts_engines()
    
    print("\n" + "=" * 50)
    print("📚 Installation complete!")
    print("\nTo use offline TTS in MathSpeak:")
    print("  python mathspeak.py --offline 'your expression'")
    print("\nOr set prefer_offline_tts=True when initializing the engine.")


if __name__ == "__main__":
    main()