#!/usr/bin/env python3
"""
Setup script for MathSpeak - Mathematical Text-to-Speech System

Installation:
    pip install .
    
Development installation:
    pip install -e .
    
With all optional features:
    pip install .[all]
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Read the README file
here = Path(__file__).parent.absolute()
readme_path = here / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

# Read version from package
version_file = here / "mathspeak" / "__init__.py"
version = "1.0.0"
if version_file.exists():
    with open(version_file, encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

# Core requirements
install_requires = [
    "edge-tts>=6.1.9",
    "psutil>=5.9.0",
]

# Optional dependencies
extras_require = {
    "audio": [
        "pygame>=2.5.0",
    ],
    "dev": [
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-asyncio>=0.21.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "mypy>=1.5.0",
        "sphinx>=7.0.0",
        "sphinx-rtd-theme>=1.3.0",
    ],
    "notebook": [
        "jupyter>=1.0.0",
        "ipywidgets>=8.0.0",
    ],
    "advanced": [
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "sympy>=1.12",
    ],
}

# 'all' includes everything
extras_require["all"] = sum(extras_require.values(), [])

# Python version requirement
python_requires = ">=3.8"

# Package metadata
setup(
    name="mathspeak",
    version=version,
    author="MathSpeak Team",
    author_email="mathspeak@example.com",
    description="Ultimate Mathematical Text-to-Speech System with professor-quality narration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Asaf999/TTSwithClaudeMathLatexEng",
    project_urls={
        "Bug Tracker": "https://github.com/Asaf999/TTSwithClaudeMathLatexEng/issues",
        "Documentation": "https://mathspeak.readthedocs.io",
        "Source Code": "https://github.com/Asaf999/TTSwithClaudeMathLatexEng",
    },
    
    # Package configuration
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    include_package_data=True,
    package_data={
        "mathspeak": [
            "data/*.json",
            "config/*.json",
        ],
    },
    
    # Dependencies
    python_requires=python_requires,
    install_requires=install_requires,
    extras_require=extras_require,
    
    # Entry points
    entry_points={
        "console_scripts": [
            "mathspeak=mathspeak.mathspeak:main",
            "mathspeak-test=mathspeak:test",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    
    # Keywords for PyPI
    keywords=[
        "mathematics",
        "math",
        "text-to-speech",
        "tts",
        "latex",
        "education",
        "accessibility",
        "audio",
        "speech-synthesis",
        "mathematical-notation",
    ],
    
    # Zip safe
    zip_safe=False,
)

# Post-installation message
if "install" in sys.argv:
    print("\n" + "="*60)
    print("MathSpeak Installation Complete!")
    print("="*60)
    print("\nQuick test: python -m mathspeak.test")
    print("Interactive mode: mathspeak --interactive")
    print("Convert expression: mathspeak \"x^2 + y^2 = r^2\"")
    print("\nFor documentation, visit: https://mathspeak.readthedocs.io")
    print("="*60 + "\n")