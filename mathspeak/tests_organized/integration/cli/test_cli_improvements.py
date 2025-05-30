#!/usr/bin/env python3
"""
Test the CLI improvements in MathSpeak
"""

import subprocess
import sys
import tempfile
from pathlib import Path

def test_cli_features():
    """Test various CLI features"""
    
    print("Testing MathSpeak CLI Improvements")
    print("=" * 70)
    
    # Test 1: Empty input handling
    print("\n1. Testing empty input handling...")
    result = subprocess.run(
        [sys.executable, "mathspeak.py"],
        capture_output=True,
        text=True
    )
    print(f"   Exit code: {result.returncode}")
    print(f"   Shows help: {'yes' if 'usage:' in result.stdout.lower() else 'no'}")
    
    # Test 2: Stats flag
    print("\n2. Testing --stats flag...")
    result = subprocess.run(
        [sys.executable, "mathspeak.py", "x^2 + y^2 = z^2", "--stats"],
        capture_output=True,
        text=True
    )
    print(f"   Exit code: {result.returncode}")
    print(f"   Shows stats: {'yes' if 'Performance Report' in result.stdout else 'no'}")
    if result.stderr:
        print(f"   Errors: {result.stderr[:200]}")
    
    # Test 3: Batch mode preparation
    print("\n3. Testing batch mode...")
    
    # Create test batch file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("x^2 + y^2 = z^2\n")
        f.write("\\int_0^1 x^2 dx = \\frac{1}{3}\n")
        f.write("\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}\n")
        batch_file = f.name
    
    # Test batch processing
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [sys.executable, "mathspeak.py", "--batch", batch_file, "--batch-output", tmpdir],
            capture_output=True,
            text=True
        )
        print(f"   Exit code: {result.returncode}")
        print(f"   Batch processing: {'success' if result.returncode == 0 else 'failed'}")
        
        # Check output files
        output_files = list(Path(tmpdir).glob("*.mp3"))
        report_files = list(Path(tmpdir).glob("batch_report_*.txt"))
        print(f"   Generated audio files: {len(output_files)}")
        print(f"   Generated report: {'yes' if report_files else 'no'}")
    
    # Clean up
    Path(batch_file).unlink()
    
    # Test 4: Progress indicators
    print("\n4. Testing progress indicators...")
    result = subprocess.run(
        [sys.executable, "mathspeak.py", 
         "Let $f: \\mathbb{R}^n \\to \\mathbb{R}$ be a continuously differentiable function. " * 5],
        capture_output=True,
        text=True
    )
    print(f"   Long expression processing: {'success' if result.returncode == 0 else 'failed'}")
    
    # Test 5: Help improvements
    print("\n5. Testing help system...")
    result = subprocess.run(
        [sys.executable, "mathspeak.py", "--help"],
        capture_output=True,
        text=True
    )
    print(f"   Help includes batch: {'yes' if '--batch' in result.stdout else 'no'}")
    print(f"   Help includes stats: {'yes' if '--stats' in result.stdout else 'no'}")
    
    print("\n" + "=" * 70)
    print("CLI improvements test complete!")

if __name__ == "__main__":
    test_cli_features()