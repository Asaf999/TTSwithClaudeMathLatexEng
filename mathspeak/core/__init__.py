"""
MathSpeak Core Components
========================

Core modules for the Mathematical Text-to-Speech system including:
- Engine: Main orchestration and processing
- Voice Manager: Multi-voice system with 7 distinct roles
- Context Memory: Symbol and structure tracking
- Natural Language: Advanced language processing
- Patterns: Common mathematical patterns
"""

# Version info
__version__ = "1.0.0"
__author__ = "MathSpeak Team"

# Typing imports at the top
from typing import Optional, Any # Assuming Any might be needed elsewhere, good to have
from pathlib import Path

# Import main components for easier access
from .engine import (
    MathematicalTTSEngine,
    MathematicalContext,
    ProcessedExpression,
    PerformanceMetrics,
    ContextDetector,
    UnknownLatexTracker,
    NaturalLanguageEnhancer,
)

from .voice_manager import (
    VoiceManager,
    VoiceRole,
    VoiceSettings,
    SpeechSegment,
    SpeedProfile,
    SPEED_PROFILES,
    ProfessorCommentary,
)

from .context_memory import (
    ContextMemory,
    SymbolMemory,
    StructureMemory,
    MathematicalStructure,
    StructureType,
    DefinedSymbol,
    CrossReferenceHandler,
)

from .natural_language import (
    NaturalLanguageProcessor,
    MathematicalTone,
    EmphasisLevel,
    VariationEngine,
    MathematicalGrammarCorrector,
    PauseInserter,
    EmphasisDetector,
    ClarificationInjector,
)

from .patterns import (
    PatternProcessor,
    PatternCategory,
    MathematicalPattern,
    EpsilonDeltaHandler, # Assuming these are classes in patterns.py
    LimitPatternHandler,
    SequenceSeriesHandler,
    SetNotationHandler,
    ProofPatternHandler,
    ReferencePatternHandler,
    CommonExpressionHandler,
    apply_common_patterns,
    apply_epsilon_delta_patterns,
    apply_proof_patterns,
)

# Forward declaration for Config type hint if necessary, or ensure it's imported before use
# from ..utils import Config # This relative import is problematic here.
# For type hinting, you can use a string: 'Config' if it causes circular import issues
# Or, ensure mathspeak.utils.config.Config is available.

# Convenience function to create a fully configured engine
def create_engine(
    enable_caching: bool = True,
    enable_all_domains: bool = True,
    config_path: Optional[Path] = None # Optional and Path are now defined
) -> MathematicalTTSEngine:
    """
    Create a fully configured Mathematical TTS Engine
    
    Args:
        enable_caching: Enable expression caching
        enable_all_domains: Load all available domain processors
        config_path: Path to configuration file
    
    Returns:
        Configured MathematicalTTSEngine instance
    """
    # Import here to avoid circular imports if Config is complex to get early
    from mathspeak.utils import Config # Absolute import

    # Create components
    voice_manager = VoiceManager()
    context_memory = ContextMemory()
    natural_language = NaturalLanguageProcessor()
    pattern_processor = PatternProcessor()
    
    # Create engine
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        # config_path=config_path, # config_path is for the Config object, not engine directly
        enable_caching=enable_caching
    )
    
    # Attach additional components
    engine.context_memory = context_memory
    # engine.language_enhancer = natural_language # engine.py already has this
    engine.pattern_processor = pattern_processor
    
    # Load domain processors if requested
    if enable_all_domains:
        app_config = Config(config_path=config_path) # Create config object
        _load_domain_processors(engine, app_config) # Pass the config object
    
    return engine

def _load_domain_processors(engine: MathematicalTTSEngine, config: 'Config') -> None: # Use string hint for Config
    """Load enabled domain processors into engine"""
    # Import domain processors using absolute paths
    from mathspeak.domains import (
        TopologyProcessor,
        ComplexAnalysisProcessor,
        NumericalAnalysisProcessor,
        # Import other planned processors here when available
    )
    from mathspeak.utils import Config # Ensure Config is imported if not just a string hint
    
    # Map of domain names to processor classes
    domain_map = {
        "topology": TopologyProcessor,
        "complex_analysis": ComplexAnalysisProcessor,
        "numerical_analysis": NumericalAnalysisProcessor,
        # Add more as they are implemented
    }
    
    # Load enabled domains from the passed config object
    for domain_name in config.domains.enabled_domains:
        if domain_name in domain_map:
            try:
                processor_class = domain_map[domain_name]
                # Assuming MathematicalContext enum values match domain_name strings
                engine.domain_processors[MathematicalContext(domain_name)] = processor_class()
                logger.info(f"Loaded {domain_name} processor")
            except Exception as e:
                logger.error(f"Failed to load {domain_name} processor: {e}")

# Export all
__all__ = [
    # Engine
    'MathematicalTTSEngine',
    'MathematicalContext', 
    'ProcessedExpression',
    'PerformanceMetrics',
    'ContextDetector',
    'UnknownLatexTracker',
    'NaturalLanguageEnhancer', # Added this as it was in your original file
    
    # Voice Manager
    'VoiceManager',
    'VoiceRole',
    'VoiceSettings',
    'SpeechSegment',
    'SpeedProfile',
    'SPEED_PROFILES',
    'ProfessorCommentary',
    
    # Context Memory
    'ContextMemory',
    'SymbolMemory',
    'StructureMemory',
    'MathematicalStructure',
    'StructureType',
    'DefinedSymbol',
    'CrossReferenceHandler',
    
    # Natural Language
    'NaturalLanguageProcessor',
    'MathematicalTone',
    'EmphasisLevel',
    'VariationEngine',
    'MathematicalGrammarCorrector',
    'PauseInserter',
    'EmphasisDetector',
    'ClarificationInjector',
    
    # Patterns
    'PatternProcessor',
    'PatternCategory',
    'MathematicalPattern',
    'apply_common_patterns',
    'apply_epsilon_delta_patterns',
    'apply_proof_patterns',
    
    # Convenience
    'create_engine',
]

import logging # Moved to bottom as it's standard practice for __init__
logger = logging.getLogger(__name__)