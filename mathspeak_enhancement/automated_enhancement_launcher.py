#!/usr/bin/env python3
"""
Automated MathSpeak Enhancement Launcher
[FATHER] Process - Main orchestrator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from father_child_protocol import FatherProcess
import subprocess
from datetime import datetime

def main():
    """Launch the automated enhancement system"""
    
    print("="*60)
    print("MATHSPEAK NATURAL SPEECH ENHANCEMENT SYSTEM")
    print("Automated Father-Son Claude-Code Enhancement")
    print("="*60)
    print(f"Launch Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Initialize Father Process
    print("[FATHER] Initializing MathSpeak Enhancement System")
    
    # Verify Python environment
    result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
    print(f"[FATHER] Python version: {result.stdout.strip()}")
    
    # Check current MathSpeak implementation exists
    impl_path = "/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak_enhancement/truly_final_98_percent.py"
    
    if os.path.exists(impl_path):
        print(f"[FATHER] Found implementation: {impl_path}")
        
        # Try to check current status
        try:
            # Import and test current implementation
            sys.path.insert(0, os.path.dirname(impl_path))
            from truly_final_98_percent import process_latex, run_natural_speech_tests
            
            print("[FATHER] Running initial assessment...")
            test_result = run_natural_speech_tests()
            print(f"[FATHER] Current naturalness: {test_result['passed']}/{test_result['total']} ({test_result['percentage']:.1%})")
            
        except Exception as e:
            print(f"[FATHER] Could not assess current status: {e}")
            print("[FATHER] Starting with baseline assumption: 91.7%")
    else:
        print(f"[FATHER] Implementation not found at {impl_path}")
        print("[FATHER] Will create during enhancement process")
    
    # Step 2: Begin Enhancement Loop
    print("\n[FATHER] Starting automated enhancement loop...")
    print("[FATHER] Target: 98%+ naturalness")
    print("[FATHER] Maximum cycles: 20")
    print()
    
    # Create and run father process
    father = FatherProcess()
    
    try:
        # Run the main enhancement loop
        father.run_enhancement_loop()
        
        print("\n[FATHER] Enhancement complete!")
        print(f"[FATHER] Final report available at: mathspeak_enhancement/FINAL_REPORT.md")
        
    except KeyboardInterrupt:
        print("\n[FATHER] Enhancement interrupted by user")
        print(f"[FATHER] Completed {father.current_cycle - 1} cycles")
        
    except Exception as e:
        print(f"\n[FATHER] Enhancement failed with error: {e}")
        print(f"[FATHER] Completed {father.current_cycle - 1} cycles before failure")
        
    finally:
        # Always generate report
        if father.current_cycle > 1:
            father.generate_final_report()

if __name__ == "__main__":
    main()