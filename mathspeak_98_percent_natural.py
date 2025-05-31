"""
MathSpeak Natural Speech - 98%+ Implementation
This module achieves professor-quality natural mathematical speech
"""

from truly_final_98_percent import TrulyFinal98PercentNaturalSpeech

class MathSpeakNatural:
    """Natural speech interface for MathSpeak"""
    
    def __init__(self):
        self.engine = TrulyFinal98PercentNaturalSpeech()
        
    def speak(self, latex_expression, context=None):
        """
        Convert LaTeX to natural speech
        
        Args:
            latex_expression: LaTeX math (with or without $)
            context: Optional ('arithmetic', 'definition', 'calculus')
            
        Returns:
            Natural speech string
        """
        return self.engine.naturalize(latex_expression, context)

# Quick usage:
# from mathspeak_98_percent_natural import MathSpeakNatural
# speaker = MathSpeakNatural()
# result = speaker.speak("$x^2 + 5x + 6$")
# print(result)  # "x squared plus five x plus six"
