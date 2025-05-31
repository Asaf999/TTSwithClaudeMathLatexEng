"""
MathSpeak Ultra Natural Integration
Integrates the ultra-natural speech engine into MathSpeak
"""

import sys
sys.path.append('/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak_enhancement')

try:
    from ultra_natural_engine import UltraNaturalSpeechEngine
    
    class MathSpeakUltraNatural:
        """Ultra-natural speech interface for MathSpeak"""
        
        def __init__(self):
            self.engine = UltraNaturalSpeechEngine()
            
        def speak(self, latex_expression, context=None):
            """
            Convert LaTeX to ultra-natural speech
            
            Args:
                latex_expression: LaTeX math expression
                context: Optional context hint
                
            Returns:
                Ultra-natural speech string
            """
            return self.engine.naturalize(latex_expression, context)
            
        def detect_context(self, latex_expression):
            """Auto-detect mathematical context"""
            return self.engine._detect_context(latex_expression.strip('$'))
            
    # Global instance
    ultra_natural = MathSpeakUltraNatural()
    
except ImportError as e:
    print(f"Warning: Could not import ultra-natural engine: {e}")
    ultra_natural = None