#!/usr/bin/env python3

import re

def test_integral_fix():
    """Test integral parsing fixes"""
    
    test_cases = [
        '$\\int_0^1 x^2 dx$',
        '$\\int_0^\\infty e^{-x} dx$'
    ]
    
    for test in test_cases:
        text = test.strip('$')
        print(f"Original: {text}")
        
        # Simple fix for integrals
        text = re.sub(r'\\int_0\^1\s*([^d]+)\s*dx', r'the integral from zero to one of \1, dx', text)
        text = re.sub(r'\\int_0\^\\infty\s*([^d]+)\s*dx', r'the integral from zero to infinity of \1, dx', text)
        
        print(f"Fixed: {text}")
        print()

if __name__ == "__main__":
    test_integral_fix()