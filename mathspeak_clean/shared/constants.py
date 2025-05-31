"""Constants for MathSpeak Clean Architecture."""

from enum import Enum, auto


class ProcessingStage(Enum):
    """Stages of expression processing."""
    
    VALIDATION = auto()
    PREPROCESSING = auto()
    PATTERN_MATCHING = auto()
    POSTPROCESSING = auto()
    NATURAL_SPEECH = auto()
    TTS_GENERATION = auto()


class PatternDomain(Enum):
    """Mathematical domains for patterns."""
    
    GENERAL = "general"
    ALGEBRA = "algebra"
    CALCULUS = "calculus"
    LINEAR_ALGEBRA = "linear_algebra"
    STATISTICS = "statistics"
    NUMBER_THEORY = "number_theory"
    SET_THEORY = "set_theory"
    LOGIC = "logic"
    TOPOLOGY = "topology"
    COMPLEX_ANALYSIS = "complex_analysis"
    REAL_ANALYSIS = "real_analysis"
    COMBINATORICS = "combinatorics"
    ALGORITHMS = "algorithms"
    MEASURE_THEORY = "measure_theory"
    ODE = "ode"
    MANIFOLDS = "manifolds"
    NUMERICAL_ANALYSIS = "numerical_analysis"


# Default configuration values
DEFAULT_AUDIENCE_LEVEL = "undergraduate"
DEFAULT_CACHE_TTL = 3600  # 1 hour
DEFAULT_MAX_EXPRESSION_LENGTH = 10000
DEFAULT_PATTERN_TIMEOUT = 5.0  # seconds
DEFAULT_LOG_LEVEL = "INFO"

# Pattern priorities (higher = processed first)
PRIORITY_CRITICAL = 1000
PRIORITY_HIGH = 750
PRIORITY_MEDIUM = 500
PRIORITY_LOW = 250
PRIORITY_DEFAULT = 100

# Cache keys
CACHE_KEY_PREFIX = "mathspeak:"
CACHE_KEY_PATTERN = f"{CACHE_KEY_PREFIX}pattern:{{expression}}:{{level}}"
CACHE_KEY_VOICE_LIST = f"{CACHE_KEY_PREFIX}voices:{{engine}}"

# Regular expression patterns for validation
LATEX_COMMAND_PATTERN = r"\\[a-zA-Z]+(?:\{[^}]*\})*"
VALID_LATEX_CHARS = r"[a-zA-Z0-9\s\\\{\}\[\]\(\)_\^\-\+\*\/\=\<\>\.\,\;\:\!\?\|]+"

# Natural speech templates
SPEECH_TEMPLATES = {
    "fraction": "{numerator} over {denominator}",
    "power": "{base} to the {exponent}",
    "sqrt": "square root of {content}",
    "derivative": "derivative of {function} with respect to {variable}",
    "integral": "integral of {integrand} d{variable}",
    "sum": "sum from {lower} to {upper} of {expression}",
    "limit": "limit as {variable} approaches {value} of {expression}",
}

# Greek letter mappings
GREEK_LETTERS = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ε",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "omicron": "ο",
    "pi": "π",
    "rho": "ρ",
    "sigma": "σ",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "φ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
    # Capital letters
    "Alpha": "Α",
    "Beta": "Β",
    "Gamma": "Γ",
    "Delta": "Δ",
    "Epsilon": "Ε",
    "Zeta": "Ζ",
    "Eta": "Η",
    "Theta": "Θ",
    "Iota": "Ι",
    "Kappa": "Κ",
    "Lambda": "Λ",
    "Mu": "Μ",
    "Nu": "Ν",
    "Xi": "Ξ",
    "Omicron": "Ο",
    "Pi": "Π",
    "Rho": "Ρ",
    "Sigma": "Σ",
    "Tau": "Τ",
    "Upsilon": "Υ",
    "Phi": "Φ",
    "Chi": "Χ",
    "Psi": "Ψ",
    "Omega": "Ω",
}

# Mathematical symbols
MATH_SYMBOLS = {
    "+": "plus",
    "-": "minus",
    "*": "times",
    "/": "divided by",
    "=": "equals",
    "≠": "not equals",
    "<": "less than",
    ">": "greater than",
    "≤": "less than or equal to",
    "≥": "greater than or equal to",
    "∈": "in",
    "∉": "not in",
    "⊂": "subset of",
    "⊃": "superset of",
    "∪": "union",
    "∩": "intersection",
    "∞": "infinity",
    "∂": "partial",
    "∇": "nabla",
    "∫": "integral",
    "∑": "sum",
    "∏": "product",
    "√": "square root",
}

# Common LaTeX commands
LATEX_COMMANDS = {
    "frac": "fraction",
    "sqrt": "square root",
    "sin": "sine",
    "cos": "cosine",
    "tan": "tangent",
    "log": "logarithm",
    "ln": "natural logarithm",
    "exp": "exponential",
    "lim": "limit",
    "sum": "sum",
    "prod": "product",
    "int": "integral",
    "partial": "partial",
    "nabla": "nabla",
    "infty": "infinity",
    "alpha": "alpha",
    "beta": "beta",
    "gamma": "gamma",
    "delta": "delta",
    "epsilon": "epsilon",
    "theta": "theta",
    "lambda": "lambda",
    "mu": "mu",
    "pi": "pi",
    "sigma": "sigma",
    "phi": "phi",
    "omega": "omega",
}