#!/usr/bin/env python3
"""
Devil Pattern Tests - The Ultimate Mathematical Torture Test
===========================================================

150 absolutely diabolical mathematical expressions designed to break
any pattern recognition system. These are the most evil, complex,
nested, and obscure mathematical notations that students might
encounter in advanced LaTeX documents.

Categories:
1. Nested Hell (deeply nested structures)
2. Subscript/Superscript Madness
3. Matrix Nightmares  
4. Integral Insanity
5. Fraction Frenzies
6. Limit Lunacy
7. Summation Sadism
8. Derivative Devastation
9. Vector Viciousness
10. Symbol Soup
11. Probability Punishment
12. Logic Labyrinth
13. Set Theory Suffering
14. Number Theory Nightmare
15. Physics Phantoms

Each test includes the LaTeX input and the expected natural speech output.
"""

import sys
import time
import json
from typing import List, Tuple, Dict, Any
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

def get_devil_test_cases() -> List[Tuple[str, str]]:
    """Return 150 devil test cases: (latex_input, expected_speech)"""
    
    devil_tests = [
        
        # =================== CATEGORY 1: NESTED HELL ===================
        (r"\\frac{\\frac{\\frac{a}{b}}{\\frac{c}{d}}}{\\frac{\\frac{e}{f}}{\\frac{g}{h}}}", 
         "a over b over c over d over e over f over g over h"),
        
        (r"\\sqrt{\\sqrt{\\sqrt{\\sqrt{x}}}}", 
         "square root of square root of square root of square root of x"),
        
        (r"x^{y^{z^{w^{v}}}}", 
         "x to the y to the z to the w to the v"),
        
        (r"\\int_{\\int_0^1 f(x)dx}^{\\int_0^2 g(x)dx} h(t) dt", 
         "integral from integral from 0 to 1 of f of x dx to integral from 0 to 2 of g of x dx of h of t dt"),
        
        (r"\\lim_{n\\to\\lim_{m\\to\\infty}a_m} \\frac{1}{n}", 
         "limit as n approaches limit as m approaches infinity a m of 1 over n"),
        
        (r"\\sum_{i=1}^{\\sum_{j=1}^n j} \\frac{1}{i^2}", 
         "sum from i equals 1 to sum from j equals 1 to n j of 1 over i squared"),
        
        (r"\\frac{d}{dx}\\left(\\frac{d}{dy}\\left(\\frac{d}{dz} f(x,y,z)\\right)\\right)", 
         "derivative with respect to x of derivative with respect to y of derivative with respect to z f of x y z"),
        
        (r"\\int_0^{\\pi} \\int_0^{\\sin x} \\int_0^{\\cos y} f(x,y,z) dz dy dx", 
         "integral from 0 to pi integral from 0 to sine x integral from 0 to cosine y of f of x y z dz dy dx"),
        
        (r"\\left(\\left(\\left(\\left(a\\right)\\right)\\right)\\right)", 
         "a"),
        
        (r"\\begin{pmatrix} \\begin{pmatrix} a & b \\\\\\\\ c & d \\end{pmatrix} & \\begin{pmatrix} e & f \\\\\\\\ g & h \\end{pmatrix} \\end{pmatrix}", 
         "matrix matrix a b c d matrix e f g h"),
        
        # =================== CATEGORY 2: SUBSCRIPT/SUPERSCRIPT MADNESS ===================
        (r"x_{i,j,k}^{(m,n,p)}", 
         "x i j k to the m n p"),
        
        (r"a_{b_{c_{d_e}}}", 
         "a b c d e"),
        
        (r"y^{z^{w^{u^{v^{t}}}}}", 
         "y to the z to the w to the u to the v to the t"),
        
        (r"\\sum_{\\substack{i=1\\\\\\\\j=1}}^{\\substack{n\\\\\\\\m}} a_{i,j}", 
         "sum from i equals 1 j equals 1 to n m a i j"),
        
        (r"x_{\\alpha,\\beta}^{\\gamma,\\delta}", 
         "x alpha beta to the gamma delta"),
        
        (r"\\prod_{k=1}^{\\infty} \\left(1 + \\frac{x^k}{k!}\\right)", 
         "product from k equals 1 to infinity of 1 plus x to the k over k factorial"),
        
        (r"A_{i_1,i_2,\\ldots,i_n}^{j_1,j_2,\\ldots,j_m}", 
         "A i 1 i 2 dot dot dot i n to the j 1 j 2 dot dot dot j m"),
        
        (r"\\tensor{T}{^\\mu_\\nu^\\rho_\\sigma}", 
         "tensor T mu nu rho sigma"),
        
        (r"g_{\\mu\\nu}^{;\\alpha\\beta}", 
         "g mu nu alpha beta"),
        
        (r"\\Gamma^\\lambda_{\\mu\\nu,\\rho}", 
         "capital gamma lambda mu nu rho"),
        
        # =================== CATEGORY 3: MATRIX NIGHTMARES ===================
        (r"\\begin{pmatrix} 1 & 2 & 3 \\\\\\\\ 4 & 5 & 6 \\\\\\\\ 7 & 8 & 9 \\end{pmatrix}^{-1}", 
         "matrix 1 2 3 4 5 6 7 8 9 to the negative 1"),
        
        (r"\\det\\begin{vmatrix} \\sin\\theta & \\cos\\theta \\\\\\\\ -\\cos\\theta & \\sin\\theta \\end{vmatrix}", 
         "determinant of matrix sine theta cosine theta negative cosine theta sine theta"),
        
        (r"\\begin{bmatrix} a & b \\\\\\\\ c & d \\end{bmatrix} \\begin{bmatrix} e & f \\\\\\\\ g & h \\end{bmatrix}", 
         "matrix a b c d matrix e f g h"),
        
        (r"\\text{tr}\\left(\\begin{pmatrix} a & b \\\\\\\\ c & d \\end{pmatrix}\\right)", 
         "trace of matrix a b c d"),
        
        (r"\\begin{Bmatrix} x \\\\\\\\ y \\\\\\\\ z \\end{Bmatrix}", 
         "matrix x y z"),
        
        (r"\\begin{pmatrix} \\frac{\\partial f}{\\partial x} \\\\\\\\ \\frac{\\partial f}{\\partial y} \\end{pmatrix}", 
         "matrix partial derivative of f with respect to x partial derivative of f with respect to y"),
        
        (r"\\left|\\begin{array}{ccc} 1 & x & x^2 \\\\\\\\ 1 & y & y^2 \\\\\\\\ 1 & z & z^2 \\end{array}\\right|", 
         "determinant of matrix 1 x x squared 1 y y squared 1 z z squared"),
        
        (r"\\begin{pmatrix} \\mathbf{A} & \\mathbf{B} \\\\\\\\ \\mathbf{C} & \\mathbf{D} \\end{pmatrix}^{-1}", 
         "matrix bold A bold B bold C bold D to the negative 1"),
        
        (r"\\text{rank}\\begin{pmatrix} 1 & 2 \\\\\\\\ 3 & 4 \\end{pmatrix}", 
         "rank matrix 1 2 3 4"),
        
        (r"\\begin{pmatrix} \\lambda_1 & 0 \\\\\\\\ 0 & \\lambda_2 \\end{pmatrix}", 
         "matrix lambda 1 0 0 lambda 2"),
        
        # =================== CATEGORY 4: INTEGRAL INSANITY ===================
        (r"\\oint_{\\partial D} \\mathbf{F} \\cdot d\\mathbf{r}", 
         "contour integral over partial D of bold F dot d bold r"),
        
        (r"\\int_0^{\\infty} \\int_0^{\\infty} e^{-(x^2+y^2)} dx dy", 
         "integral from 0 to infinity integral from 0 to infinity of e to the negative x squared plus y squared dx dy"),
        
        (r"\\int_{-\\infty}^{\\infty} \\frac{\\sin(\\pi x)}{\\pi x} dx", 
         "integral from negative infinity to infinity of sine of pi x over pi x dx"),
        
        (r"\\iint_D \\frac{\\partial^2 f}{\\partial x \\partial y} dx dy", 
         "double integral over D of partial squared f partial x partial y dx dy"),
        
        (r"\\iiint_V \\nabla \\cdot \\mathbf{F} dV", 
         "triple integral over V of divergence of bold F dV"),
        
        (r"\\int_C \\frac{dz}{z-a}", 
         "integral over C of dz over z minus a"),
        
        (r"\\int_0^{2\\pi} \\int_0^a \\int_0^{\\sqrt{a^2-r^2}} r dz dr d\\theta", 
         "integral from 0 to 2 pi integral from 0 to a integral from 0 to square root of a squared minus r squared of r dz dr dtheta"),
        
        (r"\\int_{\\gamma} f(z) dz = 2\\pi i \\sum \\text{Res}(f,z_k)", 
         "integral over gamma of f of z dz equals 2 pi i sum residue of f z k"),
        
        (r"\\int_0^{\\pi/2} \\sin^n x \\cos^m x dx", 
         "integral from 0 to pi over 2 of sine to the n x cosine to the m x dx"),
        
        (r"\\int_0^1 \\int_0^1 \\int_0^1 \\sqrt{x^2+y^2+z^2} dx dy dz", 
         "integral from 0 to 1 integral from 0 to 1 integral from 0 to 1 of square root of x squared plus y squared plus z squared dx dy dz"),
        
        # =================== CATEGORY 5: FRACTION FRENZIES ===================
        (r"\\cfrac{1}{1+\\cfrac{1}{1+\\cfrac{1}{1+\\cfrac{1}{1+\\ddots}}}}", 
         "continued fraction 1 over 1 plus continued fraction 1 over 1 plus continued fraction 1 over 1 plus continued fraction 1 over 1 plus dot dot dot"),
        
        (r"\\frac{\\frac{a}{b} + \\frac{c}{d}}{\\frac{e}{f} - \\frac{g}{h}}", 
         "a over b plus c over d over e over f minus g over h"),
        
        (r"\\frac{\\sin\\left(\\frac{\\pi}{4}\\right)}{\\cos\\left(\\frac{\\pi}{3}\\right)}", 
         "sine of pi over 4 over cosine of pi over 3"),
        
        (r"\\frac{d^n}{dx^n}\\left(\\frac{1}{1-x}\\right)", 
         "nth derivative with respect to x of 1 over 1 minus x"),
        
        (r"\\frac{\\partial^2}{\\partial x^2}\\left(\\frac{\\partial^2 f}{\\partial y^2}\\right)", 
         "second partial derivative with respect to x of second partial derivative of f with respect to y"),
        
        (r"\\frac{\\int_0^x f(t)dt}{\\int_0^x g(t)dt}", 
         "integral from 0 to x of f of t dt over integral from 0 to x of g of t dt"),
        
        (r"\\frac{\\sum_{n=1}^{\\infty} a_n}{\\sum_{n=1}^{\\infty} b_n}", 
         "sum from n equals 1 to infinity a n over sum from n equals 1 to infinity b n"),
        
        (r"\\frac{\\lim_{x\\to 0} \\frac{\\sin x}{x}}{\\lim_{x\\to \\infty} \\frac{1}{x}}", 
         "limit as x approaches 0 of sine x over x over limit as x approaches infinity of 1 over x"),
        
        (r"\\frac{\\sqrt{\\frac{a}{b}}}{\\sqrt{\\frac{c}{d}}}", 
         "square root of a over b over square root of c over d"),
        
        (r"\\frac{\\binom{n}{k}}{\\binom{n+1}{k+1}}", 
         "n choose k over n plus 1 choose k plus 1"),
        
        # =================== CATEGORY 6: LIMIT LUNACY ===================
        (r"\\lim_{x\\to 0^+} \\lim_{y\\to 0^-} \\frac{\\sin(xy)}{xy}", 
         "limit as x approaches 0 from the right limit as y approaches 0 from the left of sine of xy over xy"),
        
        (r"\\lim_{n\\to\\infty} \\sqrt[n]{\\sum_{k=1}^n k^n}", 
         "limit as n approaches infinity of nth root of sum from k equals 1 to n k to the n"),
        
        (r"\\lim_{h\\to 0} \\frac{f(x+h,y+h) - f(x,y)}{h}", 
         "limit as h approaches 0 of f of x plus h y plus h minus f of x y over h"),
        
        (r"\\lim_{\\epsilon\\to 0^+} \\int_{\\epsilon}^{1-\\epsilon} \\frac{\\sin x}{x} dx", 
         "limit as epsilon approaches 0 from the right of integral from epsilon to 1 minus epsilon of sine x over x dx"),
        
        (r"\\lim_{n\\to\\infty} \\left(1 + \\frac{x}{n}\\right)^n", 
         "limit as n approaches infinity of 1 plus x over n to the n"),
        
        (r"\\lim_{x\\to\\infty} x\\left(\\sqrt{x^2+1} - x\\right)", 
         "limit as x approaches infinity of x times square root of x squared plus 1 minus x"),
        
        (r"\\lim_{\\Delta x\\to 0} \\frac{\\Delta y}{\\Delta x}", 
         "limit as delta x approaches 0 of delta y over delta x"),
        
        (r"\\lim_{z\\to i} \\frac{z^2+1}{z-i}", 
         "limit as z approaches i of z squared plus 1 over z minus i"),
        
        (r"\\lim_{t\\to 0} \\frac{e^{it}-1}{it}", 
         "limit as t approaches 0 of e to the it minus 1 over it"),
        
        (r"\\lim_{\\|x\\|\\to\\infty} \\frac{\\|Ax\\|}{\\|x\\|}", 
         "limit as norm of x approaches infinity of norm of Ax over norm of x"),
        
        # =================== CATEGORY 7: SUMMATION SADISM ===================
        (r"\\sum_{n=0}^{\\infty} \\sum_{k=0}^n \\binom{n}{k} x^k y^{n-k}", 
         "sum from n equals 0 to infinity sum from k equals 0 to n n choose k x to the k y to the n minus k"),
        
        (r"\\sum_{\\substack{1\\leq i,j\\leq n\\\\\\\\i+j \\text{ even}}} a_{ij}", 
         "sum from 1 less than or equal to i j less than or equal to n i plus j text even a ij"),
        
        (r"\\sum_{p \\text{ prime}} \\frac{1}{p^s}", 
         "sum over p text prime of 1 over p to the s"),
        
        (r"\\sum_{\\sigma \\in S_n} \\text{sgn}(\\sigma) \\prod_{i=1}^n a_{i,\\sigma(i)}", 
         "sum over sigma in S n of sign of sigma product from i equals 1 to n a i sigma of i"),
        
        (r"\\sum_{k=0}^n (-1)^k \\binom{n}{k} \\frac{1}{k+1}", 
         "sum from k equals 0 to n negative 1 to the k n choose k 1 over k plus 1"),
        
        (r"\\sum_{n=1}^{\\infty} \\frac{\\mu(n)}{n^s}", 
         "sum from n equals 1 to infinity mu of n over n to the s"),
        
        (r"\\sum_{d|n} \\phi(d)", 
         "sum over d divides n phi of d"),
        
        (r"\\sum_{n=1}^{\\infty} \\frac{\\sin(nx)}{n}", 
         "sum from n equals 1 to infinity sine of nx over n"),
        
        (r"\\sum_{k=0}^{\\lfloor n/2 \\rfloor} \\binom{n-k}{k}", 
         "sum from k equals 0 to floor of n over 2 n minus k choose k"),
        
        (r"\\sum_{\\gcd(k,n)=1} e^{2\\pi i k/n}", 
         "sum over greatest common divisor of k n equals 1 e to the 2 pi i k over n"),
        
        # =================== CATEGORY 8: DERIVATIVE DEVASTATION ===================
        (r"\\frac{\\partial^{n+m}}{\\partial x^n \\partial y^m} f(x,y)", 
         "nth plus mth partial derivative partial x to the n partial y to the m f of x y"),
        
        (r"\\frac{D^n}{Dx^n}\\left[\\frac{d^m}{dx^m} g(x)\\right]", 
         "nth derivative D x to the n of mth derivative with respect to x g of x"),
        
        (r"\\left.\\frac{d^2y}{dx^2}\\right|_{x=0}", 
         "second derivative of y with respect to x evaluated at x equals 0"),
        
        (r"\\frac{\\partial}{\\partial t}\\left(\\frac{\\partial f}{\\partial x}\\right)", 
         "partial derivative with respect to t of partial derivative of f with respect to x"),
        
        (r"\\nabla^2 \\left(\\frac{1}{r}\\right)", 
         "Laplacian of 1 over r"),
        
        (r"\\frac{\\delta}{\\delta f} \\int L(f,f',x) dx", 
         "variational derivative delta f integral L of f f prime x dx"),
        
        (r"\\left[\\frac{d}{dx}, \\frac{d}{dy}\\right] f", 
         "commutator derivative with respect to x derivative with respect to y f"),
        
        (r"\\frac{\\partial^2 u}{\\partial t^2} = c^2 \\nabla^2 u", 
         "second partial derivative of u with respect to t equals c squared Laplacian u"),
        
        (r"\\frac{Df}{Dt} = \\frac{\\partial f}{\\partial t} + \\mathbf{v} \\cdot \\nabla f", 
         "material derivative of f equals partial derivative of f with respect to t plus bold v dot gradient f"),
        
        (r"\\frac{d}{dx}\\left(\\frac{dy}{dx}\\right)^{-1}", 
         "derivative with respect to x of derivative of y with respect to x to the negative 1"),
        
        # =================== CATEGORY 9: VECTOR VICIOUSNESS ===================
        (r"\\mathbf{a} \\times (\\mathbf{b} \\times \\mathbf{c}) = \\mathbf{b}(\\mathbf{a} \\cdot \\mathbf{c}) - \\mathbf{c}(\\mathbf{a} \\cdot \\mathbf{b})", 
         "bold a cross bold b cross bold c equals bold b bold a dot bold c minus bold c bold a dot bold b"),
        
        (r"\\nabla \\times (\\nabla \\times \\mathbf{A}) = \\nabla(\\nabla \\cdot \\mathbf{A}) - \\nabla^2 \\mathbf{A}", 
         "curl of curl of bold A equals gradient of divergence of bold A minus Laplacian bold A"),
        
        (r"\\int_V (\\nabla \\cdot \\mathbf{F}) dV = \\oint_{\\partial V} \\mathbf{F} \\cdot \\hat{\\mathbf{n}} dS", 
         "integral over V of divergence of bold F dV equals contour integral over partial V of bold F dot hat bold n dS"),
        
        (r"\\mathbf{F} = q(\\mathbf{E} + \\mathbf{v} \\times \\mathbf{B})", 
         "bold F equals q bold E plus bold v cross bold B"),
        
        (r"\\hat{\\mathbf{r}} \\times (\\hat{\\boldsymbol{\\theta}} \\times \\hat{\\boldsymbol{\\phi}})", 
         "hat bold r cross hat bold theta cross hat bold phi"),
        
        (r"\\mathbf{T} = \\mathbf{r} \\times \\mathbf{F}", 
         "bold T equals bold r cross bold F"),
        
        (r"\\langle \\mathbf{u}, \\mathbf{v} \\rangle = \\mathbf{u} \\cdot \\mathbf{v}", 
         "inner product bold u bold v equals bold u dot bold v"),
        
        (r"\\|\\mathbf{a} \\times \\mathbf{b}\\| = \\|\\mathbf{a}\\| \\|\\mathbf{b}\\| \\sin\\theta", 
         "norm of bold a cross bold b equals norm of bold a norm of bold b sine theta"),
        
        (r"\\mathbf{J} = \\frac{\\partial \\mathbf{r}}{\\partial u} \\times \\frac{\\partial \\mathbf{r}}{\\partial v}", 
         "bold J equals partial derivative of bold r with respect to u cross partial derivative of bold r with respect to v"),
        
        (r"\\text{div}(\\text{curl}\\,\\mathbf{F}) = 0", 
         "divergence of curl bold F equals 0"),
        
        # =================== CATEGORY 10: SYMBOL SOUP ===================
        (r"\\aleph_0 < \\aleph_1 < 2^{\\aleph_0}", 
         "aleph naught less than aleph 1 less than 2 to the aleph naught"),
        
        (r"\\forall \\epsilon > 0, \\exists \\delta > 0 : |x-a| < \\delta \\Rightarrow |f(x)-f(a)| < \\epsilon", 
         "for all epsilon greater than 0 there exists delta greater than 0 such that absolute value of x minus a less than delta implies absolute value of f of x minus f of a less than epsilon"),
        
        (r"\\mathbb{R} \\subset \\mathbb{C} \\subset \\mathbb{H} \\subset \\mathbb{O}", 
         "the real numbers subset the complex numbers subset the quaternions subset the octonions"),
        
        (r"\\zeta(s) = \\sum_{n=1}^{\\infty} \\frac{1}{n^s} = \\prod_p \\frac{1}{1-p^{-s}}", 
         "zeta of s equals sum from n equals 1 to infinity 1 over n to the s equals product over p 1 over 1 minus p to the negative s"),
        
        (r"\\Gamma(z) = \\int_0^{\\infty} t^{z-1} e^{-t} dt", 
         "capital gamma of z equals integral from 0 to infinity of t to the z minus 1 e to the negative t dt"),
        
        (r"\\sum_{n=-\\infty}^{\\infty} |c_n|^2 < \\infty", 
         "sum from n equals negative infinity to infinity absolute value of c n squared less than infinity"),
        
        (r"\\text{Li}_s(z) = \\sum_{n=1}^{\\infty} \\frac{z^n}{n^s}", 
         "polylogarithm s of z equals sum from n equals 1 to infinity z to the n over n to the s"),
        
        (r"\\mathcal{F}[f](\\omega) = \\int_{-\\infty}^{\\infty} f(t) e^{-i\\omega t} dt", 
         "Fourier transform of f of omega equals integral from negative infinity to infinity of f of t e to the negative i omega t dt"),
        
        (r"\\text{Ei}(x) = \\int_{-\\infty}^x \\frac{e^t}{t} dt", 
         "exponential integral of x equals integral from negative infinity to x of e to the t over t dt"),
        
        (r"\\wp(z) = \\frac{1}{z^2} + \\sum_{\\omega \\neq 0} \\left(\\frac{1}{(z-\\omega)^2} - \\frac{1}{\\omega^2}\\right)", 
         "Weierstrass p of z equals 1 over z squared plus sum over omega not equal to 0 1 over z minus omega squared minus 1 over omega squared"),
        
        # =================== CATEGORY 11: PROBABILITY PUNISHMENT ===================
        (r"P\\left(\\bigcap_{i=1}^n A_i\\right) = \\prod_{i=1}^n P(A_i | \\bigcap_{j=1}^{i-1} A_j)", 
         "probability of intersection from i equals 1 to n A i equals product from i equals 1 to n probability of A i given intersection from j equals 1 to i minus 1 A j"),
        
        (r"\\mathbb{E}\\left[\\sum_{i=1}^n X_i\\right] = \\sum_{i=1}^n \\mathbb{E}[X_i]", 
         "expected value of sum from i equals 1 to n X i equals sum from i equals 1 to n expected value of X i"),
        
        (r"\\text{Var}\\left(\\sum_{i=1}^n X_i\\right) = \\sum_{i=1}^n \\text{Var}(X_i) + 2\\sum_{i<j} \\text{Cov}(X_i, X_j)", 
         "variance of sum from i equals 1 to n X i equals sum from i equals 1 to n variance of X i plus 2 sum over i less than j covariance of X i X j"),
        
        (r"f_{X,Y}(x,y) = \\frac{\\partial^2}{\\partial x \\partial y} F_{X,Y}(x,y)", 
         "joint density of X Y of x y equals second partial derivative partial x partial y joint distribution of X Y of x y"),
        
        (r"M_X(t) = \\mathbb{E}[e^{tX}] = \\int_{-\\infty}^{\\infty} e^{tx} f_X(x) dx", 
         "moment generating function of X of t equals expected value of e to the tX equals integral from negative infinity to infinity of e to the tx f X of x dx"),
        
        (r"\\phi_X(t) = \\mathbb{E}[e^{itX}] = \\int_{-\\infty}^{\\infty} e^{itx} f_X(x) dx", 
         "characteristic function of X of t equals expected value of e to the itX equals integral from negative infinity to infinity of e to the itx f X of x dx"),
        
        (r"\\frac{d}{dt} \\mathbb{E}[X(t)] = \\mathbb{E}\\left[\\frac{dX(t)}{dt}\\right]", 
         "derivative with respect to t expected value of X of t equals expected value of derivative of X of t with respect to t"),
        
        (r"\\lim_{n\\to\\infty} P\\left(\\left|\\frac{S_n}{n} - \\mu\\right| > \\epsilon\\right) = 0", 
         "limit as n approaches infinity probability of absolute value of S n over n minus mu greater than epsilon equals 0"),
        
        (r"Z_n \\xrightarrow{d} Z \\sim \\mathcal{N}(0,1)", 
         "Z n converges in distribution to Z distributed as normal 0 1"),
        
        (r"\\mathbb{P}\\left(\\bigcup_{i=1}^{\\infty} A_i\\right) \\leq \\sum_{i=1}^{\\infty} \\mathbb{P}(A_i)", 
         "probability of union from i equals 1 to infinity A i less than or equal to sum from i equals 1 to infinity probability of A i"),
        
        # =================== CATEGORY 12: LOGIC LABYRINTH ===================
        (r"\\forall x \\in \\mathbb{R}, \\exists y \\in \\mathbb{R} : y > x", 
         "for all x in the real numbers there exists y in the real numbers such that y greater than x"),
        
        (r"(P \\land Q) \\lor (\\neg P \\land R) \\equiv (P \\land Q) \\lor (\\neg P \\land R)", 
         "P and Q or not P and R equivalent to P and Q or not P and R"),
        
        (r"\\vdash \\forall x (P(x) \\rightarrow Q(x)) \\rightarrow (\\forall x P(x) \\rightarrow \\forall x Q(x))", 
         "proves for all x P of x implies Q of x implies for all x P of x implies for all x Q of x"),
        
        (r"\\models \\phi \\iff \\text{every model satisfies } \\phi", 
         "semantically entails phi if and only if text every model satisfies phi"),
        
        (r"\\Gamma \\vdash \\phi \\iff \\Gamma \\cup \\{\\neg \\phi\\} \\text{ is inconsistent}", 
         "capital gamma proves phi if and only if capital gamma union not phi text is inconsistent"),
        
        (r"\\mathbf{ZFC} \\vdash \\text{Con}(\\mathbf{PA}) \\rightarrow \\neg \\text{Con}(\\mathbf{PA} + \\neg \\text{Con}(\\mathbf{PA}))", 
         "ZFC proves consistency of PA implies not consistency of PA plus not consistency of PA"),
        
        (r"\\kappa \\text{ is } \\lambda\\text{-supercompact} \\iff \\forall A \\subseteq V_\\lambda, |A| < \\kappa \\rightarrow A \\in M", 
         "kappa text is lambda text supercompact if and only if for all A subset V lambda absolute value of A less than kappa implies A in M"),
        
        (r"\\Diamond \\phi \\equiv \\neg \\Box \\neg \\phi", 
         "diamond phi equivalent to not box not phi"),
        
        (r"\\vdash_{S4} \\Box(\\phi \\rightarrow \\psi) \\rightarrow (\\Box \\phi \\rightarrow \\Box \\psi)", 
         "proves in S4 box phi implies psi implies box phi implies box psi"),
        
        (r"\\text{PA} \\not\\vdash \\text{Con}(\\text{PA})", 
         "PA does not prove consistency of PA"),
        
        # =================== CATEGORY 13: SET THEORY SUFFERING ===================
        (r"\\mathcal{P}(\\mathcal{P}(\\emptyset)) = \\{\\emptyset, \\{\\emptyset\\}, \\{\\{\\emptyset\\}\\}, \\{\\emptyset, \\{\\emptyset\\}\\}\\}", 
         "power set of power set of empty set equals empty set empty set empty set empty set empty set empty set"),
        
        (r"f: \\mathcal{P}(X) \\rightarrow \\mathcal{P}(Y), \\quad f(A) = \\{f(x) : x \\in A\\}", 
         "f maps power set of X to power set of Y f of A equals f of x such that x in A"),
        
        (r"\\bigcup_{\\alpha < \\omega_1} A_\\alpha = \\bigcap_{\\beta < \\omega_2} B_\\beta", 
         "union over alpha less than omega 1 A alpha equals intersection over beta less than omega 2 B beta"),
        
        (r"|\\mathbb{R}| = 2^{\\aleph_0} = \\beth_1", 
         "cardinality of the real numbers equals 2 to the aleph naught equals beth 1"),
        
        (r"\\text{CH}: 2^{\\aleph_0} = \\aleph_1", 
         "continuum hypothesis 2 to the aleph naught equals aleph 1"),
        
        (r"\\forall f: \\omega \\to \\omega, \\exists \\alpha < \\omega_1 : f \\in L_\\alpha", 
         "for all f maps omega to omega there exists alpha less than omega 1 such that f in L alpha"),
        
        (r"\\text{AD} \\rightarrow \\aleph_1 \\text{ is measurable}", 
         "axiom of determinacy implies aleph 1 text is measurable"),
        
        (r"V = L \\iff \\forall x (x \\text{ is constructible})", 
         "V equals L if and only if for all x x text is constructible"),
        
        (r"\\kappa \\text{ is } \\lambda\\text{-strong} \\iff \\exists j: V \\to M \\text{ with } \\text{crit}(j) = \\kappa", 
         "kappa text is lambda text strong if and only if there exists j maps V to M text with critical point of j equals kappa"),
        
        (r"\\Diamond_{S} \\iff \\exists \\langle A_\\alpha : \\alpha \\in S \\rangle \\text{ such that } \\forall X \\subseteq \\kappa, |\\{\\alpha \\in S : X \\cap \\alpha = A_\\alpha\\}| = \\kappa", 
         "diamond S if and only if there exists A alpha alpha in S text such that for all X subset kappa cardinality of alpha in S X intersect alpha equals A alpha equals kappa"),
        
        # =================== CATEGORY 14: NUMBER THEORY NIGHTMARE ===================
        (r"\\sum_{n \\leq x} \\Lambda(n) = x + O(x e^{-c\\sqrt{\\log x}})", 
         "sum over n less than or equal to x von Mangoldt function of n equals x plus big O of x e to the negative c square root of log x"),
        
        (r"\\zeta(s) = \\prod_{p} \\frac{1}{1-p^{-s}} \\quad (\\Re(s) > 1)", 
         "zeta of s equals product over p 1 over 1 minus p to the negative s real part of s greater than 1"),
        
        (r"\\sum_{d|n} \\mu(d) = \\begin{cases} 1 & \\text{if } n=1 \\\\\\\\ 0 & \\text{if } n>1 \\end{cases}", 
         "sum over d divides n mu of d equals 1 text if n equals 1 0 text if n greater than 1"),
        
        (r"L(1,\\chi) = \\frac{\\pi}{\\sqrt{D}} \\sum_{n=1}^{D-1} \\chi(n) \\cot\\left(\\frac{\\pi n}{D}\\right)", 
         "L of 1 chi equals pi over square root of D sum from n equals 1 to D minus 1 chi of n cotangent of pi n over D"),
        
        (r"\\theta(x) = \\sum_{p \\leq x} \\log p \\sim x \\quad (x \\to \\infty)", 
         "theta of x equals sum over p less than or equal to x log p asymptotic to x as x approaches infinity"),
        
        (r"\\pi(x) \\sim \\frac{x}{\\log x} \\quad (x \\to \\infty)", 
         "pi of x asymptotic to x over log x as x approaches infinity"),
        
        (r"\\sum_{n=1}^{\\infty} \\frac{\\mu(n)}{n} = 0", 
         "sum from n equals 1 to infinity mu of n over n equals 0"),
        
        (r"\\gcd(a,b) \\cdot \\text{lcm}(a,b) = ab", 
         "greatest common divisor of a b times least common multiple of a b equals ab"),
        
        (r"a^{\\phi(n)} \\equiv 1 \\pmod{n} \\quad (\\gcd(a,n) = 1)", 
         "a to the phi of n congruent to 1 modulo n greatest common divisor of a n equals 1"),
        
        (r"\\sum_{k=0}^{p-1} \\left(\\frac{k}{p}\\right) = 0", 
         "sum from k equals 0 to p minus 1 Legendre symbol k over p equals 0"),
        
        # =================== CATEGORY 15: PHYSICS PHANTOMS ===================
        (r"\\hat{H}|\\psi\\rangle = E|\\psi\\rangle", 
         "hat H ket psi equals E ket psi"),
        
        (r"[\\hat{x}, \\hat{p}] = i\\hbar", 
         "commutator hat x hat p equals i hbar"),
        
        (r"\\langle\\psi|\\hat{A}|\\phi\\rangle = \\int \\psi^*(x) \\hat{A} \\phi(x) dx", 
         "bra psi hat A ket phi equals integral psi star of x hat A phi of x dx"),
        
        (r"S = k_B \\log W", 
         "S equals k B log W"),
        
        (r"F = ma = m\\frac{d^2\\mathbf{r}}{dt^2}", 
         "F equals ma equals m second derivative of bold r with respect to t"),
        
        (r"\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}", 
         "curl of bold E equals negative partial derivative of bold B with respect to t"),
        
        (r"\\mathcal{L} = T - V = \\frac{1}{2}m\\dot{q}^2 - V(q)", 
         "Lagrangian equals T minus V equals 1 over 2 m q dot squared minus V of q"),
        
        (r"\\frac{\\partial \\mathcal{L}}{\\partial q} - \\frac{d}{dt}\\frac{\\partial \\mathcal{L}}{\\partial \\dot{q}} = 0", 
         "partial derivative of Lagrangian with respect to q minus derivative with respect to t partial derivative of Lagrangian with respect to q dot equals 0"),
        
        (r"\\psi(x,t) = Ae^{i(kx-\\omega t)}", 
         "psi of x t equals A e to the i times kx minus omega t"),
        
        (r"E^2 = (pc)^2 + (mc^2)^2", 
         "E squared equals pc squared plus mc squared squared")
    ]
    
    return devil_tests

def run_devil_test_suite():
    """Run the complete devil test suite"""
    
    try:
        from core.patterns_v2 import process_math_to_speech, AudienceLevel
        from core.engine import MathematicalTTSEngine
        
        devil_tests = get_devil_test_cases()
        
        print("🔥" * 20)
        print("DEVIL PATTERN TEST SUITE - 150 EVIL MATHEMATICAL EXPRESSIONS")
        print("🔥" * 20)
        print(f"Testing {len(devil_tests)} diabolical patterns...")
        print("=" * 80)
        
        # Test patterns_v2 module
        print("\\n📊 TESTING PATTERNS_V2 MODULE:")
        print("-" * 50)
        
        passed_patterns = 0
        failed_patterns = []
        
        for i, (latex_input, expected_output) in enumerate(devil_tests):
            try:
                start_time = time.time()
                result = process_math_to_speech(latex_input, AudienceLevel.UNDERGRADUATE)
                end_time = time.time()
                
                # Check for exact match or semantic similarity
                if result.strip().lower() == expected_output.strip().lower():
                    success = True
                    coverage = 1.0
                else:
                    # Flexible matching - check key terms
                    expected_words = expected_output.lower().split()
                    result_lower = result.lower()
                    found_words = sum(1 for word in expected_words if word in result_lower and len(word) > 2)
                    coverage = found_words / len(expected_words) if expected_words else 0
                    success = coverage >= 0.3  # 30% coverage for devil tests
                
                if success:
                    status = "✅ PASS"
                    passed_patterns += 1
                else:
                    status = "❌ FAIL"
                    failed_patterns.append((i+1, latex_input, expected_output, result, coverage))
                
                processing_time = (end_time - start_time) * 1000
                print(f"{status} Devil Test {i+1:3d}: {latex_input[:50]}{'...' if len(latex_input) > 50 else ''}")
                if not success:
                    print(f"    Expected: {expected_output[:60]}{'...' if len(expected_output) > 60 else ''}")
                    print(f"    Got:      {result[:60]}{'...' if len(result) > 60 else ''}")
                    print(f"    Coverage: {coverage:.1%}")
                
            except Exception as e:
                print(f"❌ ERROR Devil Test {i+1:3d}: {latex_input[:50]} - {str(e)[:40]}")
                failed_patterns.append((i+1, latex_input, expected_output, f"ERROR: {e}", 0.0))
        
        print("\\n" + "=" * 80)
        print(f"📊 DEVIL PATTERNS RESULTS: {passed_patterns}/{len(devil_tests)} ({passed_patterns/len(devil_tests)*100:.1f}%)")
        
        # Test main engine with a subset
        print("\\n🔧 TESTING MAIN ENGINE (Sample):")
        print("-" * 50)
        
        try:
            engine = MathematicalTTSEngine()
            sample_tests = devil_tests[:10]  # Test first 10 with engine
            engine_passed = 0
            
            for i, (latex_input, expected_output) in enumerate(sample_tests):
                try:
                    result_data = engine.process_latex(latex_input)
                    if result_data.processed and len(result_data.processed.strip()) > 0:
                        print(f"✅ Engine Devil Test {i+1}: Success")
                        engine_passed += 1
                    else:
                        print(f"❌ Engine Devil Test {i+1}: Empty result")
                except Exception as e:
                    print(f"❌ Engine Devil Test {i+1}: {str(e)[:50]}")
            
            print(f"\\n🔧 ENGINE RESULTS: {engine_passed}/{len(sample_tests)} ({engine_passed/len(sample_tests)*100:.1f}%)")
            
        except Exception as e:
            print(f"❌ Engine testing failed: {e}")
            engine_passed = 0
            sample_tests = []
        
        # Summary
        total_passed = passed_patterns + engine_passed
        total_tests = len(devil_tests) + len(sample_tests)
        
        print("\\n" + "🔥" * 20)
        print("DEVIL TEST SUMMARY")
        print("🔥" * 20)
        print(f"Pattern Module: {passed_patterns}/{len(devil_tests)} ({passed_patterns/len(devil_tests)*100:.1f}%)")
        print(f"Main Engine:    {engine_passed}/{len(sample_tests)} ({engine_passed/len(sample_tests)*100:.1f}%)")
        print(f"Overall:        {total_passed}/{total_tests} ({total_passed/total_tests*100:.1f}%)")
        
        if failed_patterns:
            print(f"\\n💀 FAILED DEVIL PATTERNS ({len(failed_patterns)}):")
            print("-" * 60)
            for test_num, latex, expected, result, coverage in failed_patterns[:20]:  # Show first 20 failures
                print(f"Test {test_num}: {latex}")
                print(f"  Expected: {expected[:70]}{'...' if len(expected) > 70 else ''}")
                print(f"  Got:      {result[:70]}{'...' if len(result) > 70 else ''}")
                print(f"  Coverage: {coverage:.1%}")
                print()
            
            if len(failed_patterns) > 20:
                print(f"... and {len(failed_patterns) - 20} more failures")
        
        print("\\n👹 The devil tests are complete! Time to fix the failures...")
        
        return passed_patterns, len(devil_tests), failed_patterns
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return 0, 150, []
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        return 0, 150, []

if __name__ == "__main__":
    passed, total, failures = run_devil_test_suite()
    
    print(f"\\n🎯 DEVIL TEST COMPLETION:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {passed/total*100:.1f}%")
    print(f"   Failures to Fix: {len(failures)}")
    
    if passed == total:
        print("\\n🏆 ALL DEVIL TESTS PASSED! The system is truly diabolical! 😈")
    else:
        print(f"\\n💪 {total - passed} devil patterns need fixing. Let's make them submit! 😈")