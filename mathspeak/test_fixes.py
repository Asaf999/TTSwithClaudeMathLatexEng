#!/usr/bin/env python3
"""Test the fixes for domain processors"""

from domains.complex_analysis import ComplexAnalysisProcessor
from domains.topology import TopologyProcessor
from domains.numerical_analysis import NumericalAnalysisProcessor

# Test Complex Analysis
print("Testing Complex Analysis:")
ca_proc = ComplexAnalysisProcessor()
test_ca = [
    (r"\\mathbb{C}", "the complex numbers"),
    (r"\\text{Re}(z)", "real part of z"),
    (r"\\oint_\\gamma f(z)\\,dz", "contour integral"),
]
for inp, expected in test_ca:
    result = ca_proc.process(inp)
    print(f"Input: {repr(inp)}")
    print(f"Output: {result}")
    print(f"Expected contains: {expected}")
    print(f"Success: {expected.lower() in result.lower()}")
    print()

# Test Topology
print("\n\nTesting Topology:")
topo_proc = TopologyProcessor()
test_topo = [
    (r"\\mathcal{T}", "topology script T"),
    (r"T_0", "T naught"),
    (r"\\partial X", "boundary of X"),
]
for inp, expected in test_topo:
    result = topo_proc.process(inp)
    print(f"Input: {repr(inp)}")
    print(f"Output: {result}")
    print(f"Expected contains: {expected}")
    print(f"Success: {expected.lower() in result.lower()}")
    print()

# Test Numerical Analysis
print("\n\nTesting Numerical Analysis:")
num_proc = NumericalAnalysisProcessor()
test_num = [
    (r"\\mathcal{O}(h^2)", "order h squared"),
    (r"\\nabla^2 u", "Laplacian of u"),
    (r"x^{(k+1)} = x^{(k)} - [J(x^{(k)})]^{-1} F(x^{(k)})", "Newton"),
]
for inp, expected in test_num:
    result = num_proc.process(inp)
    print(f"Input: {repr(inp)}")
    print(f"Output: {result}")
    print(f"Expected contains: {expected}")
    print(f"Success: {expected.lower() in result.lower()}")
    print()