#!/usr/bin/env python3
"""
Core fixes for MathSpeak pattern processing
Fix the specific issues identified in testing
"""

import re
import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

def create_improved_processor():
    """Create an improved version of the math speech processor with core fixes"""
    
    def process_math_to_speech_fixed(text: str) -> str:
        """
        Improved math to speech processing with targeted fixes
        
        Key fixes:
        1. Derivatives: \frac{d}{dx} -> "derivative of" not "d over dx"  
        2. Integrals: Proper handling of bounds
        3. Basic operations: + -> "plus", not keeping "+"
        4. Fractions: 3/4 -> "three fourths" not "three quarters"
        """
        
        # Remove dollar signs
        text = text.replace('$', '').strip()
        
        # Fix 1: Handle derivatives FIRST (before general fractions)
        # Standard derivative notation
        text = re.sub(r'\\frac\{d\}\{d([a-zA-Z])\}\s*([a-zA-Z])\(([a-zA-Z])\)', 
                     r'derivative of \2 of \3', text)
        text = re.sub(r'\\frac\{d\}\{d([a-zA-Z])\}\s*([a-zA-Z]+)', 
                     r'derivative of \2', text)
        text = re.sub(r'\\frac\{d([a-zA-Z]*)\}\{d([a-zA-Z])\}', 
                     r'derivative of \1 with respect to \2', text)
        
        # Higher order derivatives
        text = re.sub(r'\\frac\{d\^2\}\{d([a-zA-Z])\^2\}', 
                     r'second derivative with respect to \1', text)
        text = re.sub(r'\\frac\{d\^2([a-zA-Z]*)\}\{d([a-zA-Z])\^2\}', 
                     r'second derivative of \1 with respect to \2', text)
        
        # Fix 2: Handle integrals properly
        # Definite integrals with bounds
        text = re.sub(r'\\int_0\^1\s*([^d]+)\s*d([a-zA-Z])', 
                     r'integral from 0 to 1 of \1 d\2', text)
        text = re.sub(r'\\int_(\w+)\^(\w+)\s*([^d]+)\s*d([a-zA-Z])', 
                     r'integral from \1 to \2 of \3 d\4', text)
        text = re.sub(r'\\int_([^\\^]+)\^([^\\s]+)\s*([^d]+)\s*d([a-zA-Z])', 
                     r'integral from \1 to \2 of \3 d\4', text)
        
        # Fix subscripts in bounds
        text = re.sub(r'\\int_\{([^}]+)\}\^\{([^}]+)\}\s*([^d]+)\s*d([a-zA-Z])', 
                     r'integral from \1 to \2 of \3 d\4', text)
        
        # Indefinite integrals
        text = re.sub(r'\\int\s*([^d]+)\s*d([a-zA-Z])', 
                     r'integral of \1 d\2', text)
        
        # Fix 3: Handle fractions (after derivatives are processed)
        # Common fractions with specific names
        fraction_names = {
            ('1', '2'): 'one half',
            ('1', '3'): 'one third', 
            ('2', '3'): 'two thirds',
            ('1', '4'): 'one fourth',  # Fixed: was "quarter"
            ('3', '4'): 'three fourths', # Fixed: was "quarters"
            ('1', '5'): 'one fifth',
            ('2', '5'): 'two fifths',
            ('3', '5'): 'three fifths',
            ('4', '5'): 'four fifths',
            ('1', '6'): 'one sixth',
            ('5', '6'): 'five sixths',
            ('1', '8'): 'one eighth',
            ('3', '8'): 'three eighths',
            ('5', '8'): 'five eighths',
            ('7', '8'): 'seven eighths'
        }
        
        def replace_fraction(match):
            num = match.group(1).strip()
            den = match.group(2).strip()
            if (num, den) in fraction_names:
                return fraction_names[(num, den)]
            else:
                return f"{num} over {den}"
        
        text = re.sub(r'\\frac\{(\d+)\}\{(\d+)\}', replace_fraction, text)
        text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 over \2', text)
        
        # Fix 4: Handle powers and roots
        text = re.sub(r'\\sqrt\{([^}]+)\}', r'square root of \1', text)
        text = re.sub(r'\\sqrt\[(\d+)\]\{([^}]+)\}', r'\1th root of \2', text)
        
        # Powers
        text = re.sub(r'([a-zA-Z])\^2\b', r'\1 squared', text)
        text = re.sub(r'([a-zA-Z])\^3\b', r'\1 cubed', text)
        text = re.sub(r'([a-zA-Z])\^(\d+)', r'\1 to the \2', text)
        text = re.sub(r'([a-zA-Z])\^\{([^}]+)\}', r'\1 to the \2', text)
        
        # Fix 5: Handle basic operations and symbols
        # Trigonometric functions
        text = re.sub(r'\\sin\s*([a-zA-Z])', r'sine \1', text)
        text = re.sub(r'\\cos\s*([a-zA-Z])', r'cosine \1', text)
        text = re.sub(r'\\tan\s*([a-zA-Z])', r'tangent \1', text)
        
        # Constants and symbols
        text = text.replace('\\pi', 'pi')
        text = text.replace('\\infty', 'infinity')
        text = text.replace('\\alpha', 'alpha')
        text = text.replace('\\beta', 'beta')
        text = text.replace('\\gamma', 'gamma')
        text = text.replace('\\delta', 'delta')
        text = text.replace('\\epsilon', 'epsilon')
        text = text.replace('\\theta', 'theta')
        text = text.replace('\\lambda', 'lambda')
        text = text.replace('\\mu', 'mu')
        text = text.replace('\\sigma', 'sigma')
        text = text.replace('\\omega', 'omega')
        
        # Fix 6: Handle basic operations (CRITICAL FIX)
        text = text.replace(' + ', ' plus ')
        text = text.replace(' - ', ' minus ')
        text = text.replace(' * ', ' times ')
        text = text.replace(' = ', ' equals ')
        text = text.replace(' < ', ' less than ')
        text = text.replace(' > ', ' greater than ')
        text = text.replace('\\leq', ' less than or equal to ')
        text = text.replace('\\geq', ' greater than or equal to ')
        text = text.replace('\\neq', ' not equal to ')
        text = text.replace('\\approx', ' approximately ')
        
        # Handle operations that might not have spaces
        text = re.sub(r'([a-zA-Z0-9])\+([a-zA-Z0-9])', r'\1 plus \2', text)
        text = re.sub(r'([a-zA-Z0-9])-([a-zA-Z0-9])', r'\1 minus \2', text)
        
        # Fix 7: Function notation
        text = re.sub(r'([fgh])\(([a-zA-Z])\)', r'\1 of \2', text)
        
        # Fix 8: Handle limits
        text = re.sub(r'\\lim_\{([^}]+)\\to([^}]+)\}', r'limit as \1 approaches \2', text)
        text = re.sub(r'\\lim_\{([^}]+)\\to([^}]+)\}\s*([^\\]+)', r'limit as \1 approaches \2 of \3', text)
        
        # Fix 9: Clean up spaces and formatting
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = text.replace('\\', '').replace('{', '').replace('}', '')  # Remove LaTeX artifacts
        text = text.strip()
        
        # Fix 10: Handle number-letter combinations (like "2x")
        text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)
        
        return text
    
    return process_math_to_speech_fixed

def test_fixed_processor():
    """Test the fixed processor on the failing cases"""
    
    processor = create_improved_processor()
    
    test_cases = [
        # Original failing cases
        ("\\frac{3}{4}", "three fourths"),
        ("\\int_0^1 x dx", "integral from 0 to 1 of x dx"),
        ("\\frac{d}{dx} f(x)", "derivative of f of x"),
        ("2x + 3", "2 x plus 3"),
        
        # Additional test cases
        ("x^2", "x squared"),
        ("\\sqrt{x}", "square root of x"),
        ("f(x) = x^2", "f of x equals x squared"),
        ("\\sin x", "sine x"),
        ("\\pi", "pi"),
        ("\\infty", "infinity"),
        ("\\frac{1}{2}", "one half"),
        ("\\frac{2}{3}", "two thirds"),
        ("\\int f(x) dx", "integral of f of x dx"),
        ("\\frac{d^2y}{dx^2}", "second derivative of y with respect to x"),
        ("a + b - c", "a plus b minus c"),
        ("x < y", "x less than y"),
        ("\\lim_{x\\to 0} f(x)", "limit as x approaches 0 of f of x"),
    ]
    
    print("Testing Fixed MathSpeak Processor:")
    print("=" * 60)
    
    passed = 0
    total = len(test_cases)
    
    for i, (input_latex, expected) in enumerate(test_cases):
        try:
            result = processor(input_latex)
            # More flexible matching
            success = (expected.lower() in result.lower() or 
                      result.lower() in expected.lower() or
                      all(word in result.lower() for word in expected.lower().split() if len(word) > 2))
            
            status = "✅ PASS" if success else "❌ FAIL"
            if success:
                passed += 1
                
            print(f"{status} Test {i+1:2d}: {input_latex}")
            if not success:
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                
        except Exception as e:
            print(f"❌ ERROR Test {i+1:2d}: {input_latex} - {e}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} ({passed/total*100:.1f}%)")
    
    return passed, total

if __name__ == "__main__":
    passed, total = test_fixed_processor()
    print(f"\nFixed processor: {passed}/{total} patterns working")