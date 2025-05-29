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

# Import main components for easier access
from .engine import (
    MathematicalTTSEngine,
    MathematicalContext,
    ProcessedExpression,
    PerformanceMetrics,
    ContextDetector,
    UnknownLatexTracker,
    NaturalLanguageEnhancer,  # This was missing
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
    EpsilonDeltaHandler,
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

# Convenience function to create a fully configured engine
def create_engine(
    enable_caching: bool = True,
    enable_all_domains: bool = True,
    config_path: Optional[Path] = None
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
    # Import here to avoid circular imports
    from pathlib import Path as PathType
    if config_path and not isinstance(config_path, PathType):
        config_path = PathType(config_path)
    
    # Create components
    voice_manager = VoiceManager()
    context_memory = ContextMemory()
    natural_language = NaturalLanguageProcessor()
    pattern_processor = PatternProcessor()
    
    # Create engine
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        config_path=config_path,
        enable_caching=enable_caching
    )
    
    # Attach additional components
    engine.context_memory = context_memory
    engine.language_enhancer = natural_language
    engine.pattern_processor = pattern_processor
    
    # Load domain processors if requested
    if enable_all_domains:
        _load_domain_processors(engine)
    
    return engine

def _load_domain_processors(engine: MathematicalTTSEngine, config: Config) -> None:
    """Load enabled domain processors into engine"""
    # Import domain processors
    from ..domains import (
        TopologyProcessor,
        ComplexAnalysisProcessor,
        NumericalAnalysisProcessor,
    )
    
    # Map of domain names to processor classes
    domain_map = {
        "topology": TopologyProcessor,
        "complex_analysis": ComplexAnalysisProcessor,
        "numerical_analysis": NumericalAnalysisProcessor,
        # Add more as they are implemented
    }
    
    # Load enabled domains
    for domain_name in config.domains.enabled_domains:
        if domain_name in domain_map:
            try:
                processor_class = domain_map[domain_name]
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

# Import typing for better IDE support
from pathlib import Path
from typing import Optional

import logging
logger = logging.getLogger(__name__)