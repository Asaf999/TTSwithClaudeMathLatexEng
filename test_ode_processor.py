#!/usr/bin/env python3
"""Test script for ODE processor"""

from mathspeak.domains.ode import ODEProcessor, ODEContext

def test_ode_coverage():
    """Test comprehensive ODE coverage"""
    processor = ODEProcessor()
    
    # Test cases organized by sub-context
    test_suites = {
        "Basic ODE": [
            r"Consider the ODE $\frac{dy}{dx} = f(x,y)$",
            r"The differential equation $y' = xy$ is separable",
            r"This is a 3rd-order ODE with constant coefficients",
        ],
        
        "First-Order": [
            r"$\frac{dy}{dx} + P(x)y = Q(x)$ is linear",
            r"$M(x,y)dx + N(x,y)dy = 0$ is exact",
            r"The Bernoulli equation $y' + xy = x^3y^2$",
            r"Riccati equation: $y' = y^2 + x$",
        ],
        
        "Second-Order": [
            r"$y'' + 3y' + 2y = 0$ has characteristic equation $r^2 + 3r + 2 = 0$",
            r"For complex roots: $y = e^{\alpha x}(c_1\cos\beta x + c_2\sin\beta x)$",
            r"Using variation of parameters: $y_p = u_1(x)y_1 + u_2(x)y_2$",
        ],
        
        "Series Solutions": [
            r"Bessel's equation: $x^2y'' + xy' + (x^2 - \nu^2)y = 0$",
            r"Legendre polynomial $P_n(x)$ satisfies the differential equation",
            r"Using Frobenius method: $y = x^r\sum_{n=0}^{\infty} a_n x^n$",
        ],
        
        "Laplace Transforms": [
            r"$\mathcal{L}\{f(t)\} = \int_0^\infty e^{-st}f(t)dt$",
            r"$\mathcal{L}\{u(t-a)f(t-a)\} = e^{-as}F(s)$",
            r"The inverse transform: $\mathcal{L}^{-1}\{F(s)\} = f(t)$",
        ],
        
        "Systems": [
            r"System: $\mathbf{x}' = \mathbf{A}\mathbf{x} + \mathbf{f}(t)$",
            r"Eigenvalues satisfy $\det(\mathbf{A} - \lambda\mathbf{I}) = 0$",
            r"The fundamental matrix $\mathbf{\Phi}(t)$ satisfies $\mathbf{\Phi}' = \mathbf{A}\mathbf{\Phi}$",
        ],
        
        "Qualitative Theory": [
            r"The equilibrium point is asymptotically stable",
            r"Phase portrait shows a saddle point at $(0,0)$",
            r"By Lyapunov's theorem, if $V > 0$ and $\dot{V} \leq 0$, then stable",
        ],
        
        "Numerical Methods": [
            r"Euler's method: $y_{n+1} = y_n + hf(x_n, y_n)$",
            r"RK4 has truncation error $O(h^5)$",
            r"For stiff ODEs, use implicit methods",
        ]
    }
    
    print("=" * 80)
    print("ODE PROCESSOR COMPREHENSIVE TEST")
    print("=" * 80)
    
    for suite_name, test_cases in test_suites.items():
        print(f"\n### {suite_name} ###")
        print("-" * 40)
        
        for test in test_cases:
            result = processor.process(test)
            print(f"\nInput:   {test}")
            print(f"Output:  {result}")
            print(f"Context: {processor.context.value}")
    
    # Test context detection
    print("\n\n### Context Detection Test ###")
    print("-" * 40)
    
    context_tests = [
        ("The Laplace transform of f", ODEContext.LAPLACE),
        ("eigenvalue problem for the system", ODEContext.SYSTEMS),
        ("using Runge-Kutta method", ODEContext.NUMERICAL),
        ("phase plane analysis shows", ODEContext.QUALITATIVE),
        ("Bessel function of order", ODEContext.SERIES_SOLUTIONS),
        ("second-order linear ODE", ODEContext.SECOND_ORDER),
        ("separable first-order equation", ODEContext.FIRST_ORDER),
    ]
    
    for text, expected_context in context_tests:
        detected = processor.detect_subcontext(text)
        status = "✓" if detected == expected_context else "✗"
        print(f"{status} '{text}' -> {detected.value} (expected: {expected_context.value})")
    
    # Show processor info
    print(f"\n\nProcessor Info: {processor.get_context_info()}")

if __name__ == "__main__":
    test_ode_coverage()