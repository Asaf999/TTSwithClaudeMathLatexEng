#!/usr/bin/env python3
"""Debug specific failing devil tests"""

import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from math_ast import parse_latex, MathAST
from math_speech import MathSpeech
import re

def debug_test(test_num, latex, expected):
    """Debug a single test case"""
    print(f"\n{'='*60}")
    print(f"DEBUGGING DEVIL TEST {test_num}")
    print(f"{'='*60}")
    print(f"LaTeX: {latex}")
    print(f"Expected: {expected}")
    
    try:
        # Parse and convert
        ast = parse_latex(latex)
        speech = MathSpeech()
        result = speech.convert(ast)
        
        print(f"Got: {result}")
        print(f"Match: {result == expected}")
        
        # Show AST structure
        print(f"\nAST Structure:")
        print_ast(ast, indent=0)
        
        # Show step-by-step processing
        print(f"\nStep-by-step processing:")
        debug_speech = DebugMathSpeech()
        debug_speech.convert(ast)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def print_ast(node, indent=0):
    """Pretty print AST structure"""
    if node is None:
        return
    
    prefix = "  " * indent
    if hasattr(node, 'type'):
        print(f"{prefix}{node.type}", end="")
        if hasattr(node, 'content') and node.content:
            print(f": {node.content}", end="")
        if hasattr(node, 'attrs') and node.attrs:
            print(f" attrs={node.attrs}", end="")
        print()
        
        # Print children
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                print_ast(child, indent + 1)

class DebugMathSpeech(MathSpeech):
    """MathSpeech with debug output"""
    
    def convert(self, node):
        """Convert with debug output"""
        if node is None:
            return ""
        
        method_name = f"convert_{node.type}"
        print(f"  -> Calling {method_name}")
        
        if hasattr(self, method_name):
            result = getattr(self, method_name)(node)
        else:
            result = self.convert_generic(node)
        
        print(f"     Result: '{result}'")
        return result

# Test cases
test_cases = [
    (10, r"\\begin{pmatrix} \\begin{pmatrix} a & b \\\\\\\\ c & d \\end{pmatrix} & \\begin{pmatrix} e & f \\\\\\\\ g & h \\end{pmatrix} \\end{pmatrix}",
     "matrix matrix a b c d matrix e f g h"),
    
    (14, r"\\sum_{\\substack{i=1\\\\\\\\j=1}}^{\\substack{n\\\\\\\\m}} a_{i,j}",
     "sum from i equals 1 j equals 1 to n m a i j"),
    
    (23, r"\\begin{bmatrix} a & b \\\\\\\\ c & d \\end{bmatrix} \\begin{bmatrix} e & f \\\\\\\\ g & h \\end{bmatrix}",
     "matrix a b c d matrix e f g h"),
    
    (24, r"\\text{tr}\\left(\\begin{pmatrix} a & b \\\\\\\\ c & d \\end{pmatrix}\\right)",
     "trace of matrix a b c d"),
    
    (107, r"\\frac{d}{dt} \\mathbb{E}[X(t)] = \\mathbb{E}\\left[\\frac{dX(t)}{dt}\\right]",
     "derivative with respect to t expected value of X of t equals expected value of derivative of X of t with respect to t")
]

if __name__ == "__main__":
    # Test specific case if provided
    if len(sys.argv) > 1:
        test_num = int(sys.argv[1])
        for num, latex, expected in test_cases:
            if num == test_num:
                debug_test(num, latex, expected)
                break
    else:
        # Test all cases
        for num, latex, expected in test_cases:
            debug_test(num, latex, expected)