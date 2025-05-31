"""Mathematical expression entity."""

from dataclasses import dataclass, field
from typing import List, Optional

from mathspeak_clean.shared.constants import DEFAULT_MAX_EXPRESSION_LENGTH
from mathspeak_clean.shared.exceptions import ValidationError
from mathspeak_clean.shared.types import AudienceLevel, LaTeXExpression, SpeechText


@dataclass
class MathExpression:
    """Mathematical expression entity.
    
    This is the core domain entity representing a mathematical expression
    that needs to be converted to speech.
    """
    
    latex: LaTeXExpression
    audience_level: AudienceLevel = "undergraduate"
    _speech_text: Optional[SpeechText] = field(default=None, init=False)
    _validated: bool = field(default=False, init=False)
    
    def __post_init__(self) -> None:
        """Validate expression after initialization."""
        self.validate()
    
    def validate(self) -> None:
        """Validate the mathematical expression.
        
        Raises:
            ValidationError: If expression is invalid
        """
        if not self.latex:
            raise ValidationError("latex", "Expression cannot be empty")
        
        if len(self.latex) > DEFAULT_MAX_EXPRESSION_LENGTH:
            raise ValidationError(
                "latex",
                f"Expression exceeds maximum length of {DEFAULT_MAX_EXPRESSION_LENGTH}",
                len(self.latex),
            )
        
        # Check for basic LaTeX validity
        if self.latex.count("{") != self.latex.count("}"):
            raise ValidationError("latex", "Unbalanced braces in expression")
        
        if self.latex.count("[") != self.latex.count("]"):
            raise ValidationError("latex", "Unbalanced brackets in expression")
        
        if self.latex.count("(") != self.latex.count(")"):
            raise ValidationError("latex", "Unbalanced parentheses in expression")
        
        # Check for maximum nesting depth
        max_depth = self._calculate_nesting_depth()
        if max_depth > 20:  # Reasonable limit for nesting
            raise ValidationError("latex", f"Expression too deeply nested (depth: {max_depth})")
        
        # Check for invalid LaTeX commands
        import re
        commands = re.findall(r"\\([a-zA-Z]+)", self.latex)
        
        # List of known valid LaTeX commands
        valid_commands = {
            "frac", "sqrt", "sin", "cos", "tan", "log", "ln", "exp",
            "sum", "prod", "int", "lim", "inf", "sup",
            "alpha", "beta", "gamma", "delta", "theta", "pi",
            "partial", "nabla", "forall", "exists", "in", "subset",
            "cup", "cap", "times", "cdot", "to", "infty",
            "mathbb", "text", "mathcal", "mathfrak", "mathrm",
            "det", "dim", "ker", "rank", "tr",
            "left", "right", "big", "Big", "bigg", "Bigg",
            "le", "ge", "ne", "approx", "sim", "equiv",
            "ldots", "cdots", "vdots", "ddots",
            "substack", "limits", "nolimits",
            "binom", "choose", "over", "atop",
            "hat", "bar", "vec", "dot", "ddot", "tilde",
            "quad", "qquad", "!", ",", ":", ";", "\\", " ",
            "i", "j", "k", "l", "m", "n", "a", "b", "c", "d", "e", "f", "g", "h",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        }
        
        for cmd in commands:
            if cmd not in valid_commands and not cmd.startswith("text"):
                raise ValidationError("latex", f"Invalid LaTeX command: \\{cmd}")
        
        self._validated = True
    
    @property
    def is_validated(self) -> bool:
        """Check if expression has been validated."""
        return self._validated
    
    @property
    def speech_text(self) -> Optional[SpeechText]:
        """Get speech text if processed."""
        return self._speech_text
    
    def set_speech_text(self, text: SpeechText) -> None:
        """Set the speech text after processing.
        
        Args:
            text: Processed speech text
        """
        if not text:
            raise ValidationError("speech_text", "Speech text cannot be empty")
        self._speech_text = text
    
    @property
    def complexity_score(self) -> int:
        """Calculate complexity score of the expression.
        
        Returns:
            Complexity score (0-100)
        """
        score = 0
        
        # Count nested structures
        max_depth = self._calculate_nesting_depth()
        score += min(max_depth * 10, 30)
        
        # Count special commands
        command_count = self.latex.count("\\")
        score += min(command_count * 2, 20)
        
        # Count mathematical symbols
        symbols = ["^", "_", "∫", "∑", "∏", "∂", "∇"]
        symbol_count = sum(self.latex.count(s) for s in symbols)
        score += min(symbol_count * 3, 20)
        
        # Length factor
        length_factor = min(len(self.latex) // 50, 30)
        score += length_factor
        
        return min(score, 100)
    
    def _calculate_nesting_depth(self) -> int:
        """Calculate maximum nesting depth of braces."""
        max_depth = 0
        current_depth = 0
        
        for char in self.latex:
            if char == "{":
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == "}":
                current_depth -= 1
        
        return max_depth
    
    def extract_commands(self) -> List[str]:
        """Extract all LaTeX commands from expression.
        
        Returns:
            List of commands (without backslash)
        """
        import re
        
        pattern = r"\\([a-zA-Z]+)"
        matches = re.findall(pattern, self.latex)
        return list(set(matches))
    
    def contains_domain(self, domain_keywords: List[str]) -> bool:
        """Check if expression contains domain-specific keywords.
        
        Args:
            domain_keywords: Keywords to check for
            
        Returns:
            True if any keyword is found
        """
        expression_lower = self.latex.lower()
        return any(keyword.lower() in expression_lower for keyword in domain_keywords)
    
    def __str__(self) -> str:
        """String representation."""
        return f"MathExpression({self.latex[:50]}{'...' if len(self.latex) > 50 else ''})"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"MathExpression(latex={self.latex!r}, "
            f"audience_level={self.audience_level!r}, "
            f"complexity={self.complexity_score})"
        )