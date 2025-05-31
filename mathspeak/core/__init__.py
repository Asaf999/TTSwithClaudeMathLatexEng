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

import logging
from typing import Optional, TYPE_CHECKING
from pathlib import Path

# Type checking imports to avoid circular imports
if TYPE_CHECKING:
    from ..utils import Config

logger = logging.getLogger(__name__)

# Lazy import pattern to avoid circular imports
_components_loaded = False

def _load_components():
    """Load components on first access to avoid circular imports"""
    global _components_loaded
    if _components_loaded:
        return
    
    # Import main components
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
    
    from .patterns_v2 import MathSpeechProcessor
    # PatternProcessor is legacy - use MathSpeechProcessor
    PatternProcessor = MathSpeechProcessor
    
    # Store in globals for access
    globals().update(locals())
    _components_loaded = True

# Public API functions
def create_engine(
    enable_caching: bool = True,
    enable_all_domains: bool = True,
    config_path: Optional[Path] = None
) -> 'MathematicalTTSEngine':
    """
    Create a fully configured Mathematical TTS Engine
    
    Args:
        enable_caching: Enable expression caching
        enable_all_domains: Load all available domain processors
        config_path: Path to configuration file
    
    Returns:
        Configured MathematicalTTSEngine instance
    """
    _load_components()
    
    # Import here to avoid circular imports
    from ..utils import Config
    
    # Create components
    voice_manager = VoiceManager()
    context_memory = ContextMemory()
    natural_language = NaturalLanguageProcessor()
    pattern_processor = PatternProcessor()
    
    # Create engine
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=enable_caching
    )
    
    # Attach additional components
    engine.context_memory = context_memory
    engine.pattern_processor = pattern_processor
    
    # Load domain processors if requested
    if enable_all_domains:
        app_config = Config(config_dir=config_path)
        _load_domain_processors(engine, app_config)
    
    return engine

def _load_domain_processors(engine: 'MathematicalTTSEngine', config: 'Config') -> None:
    """Load enabled domain processors into engine"""
    try:
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
    except ImportError as e:
        logger.warning(f"Some domain processors not available: {e}")

# Lazy loading for main exports
def __getattr__(name: str):
    """Implement lazy loading for exports"""
    _load_components()
    
    # Try to get from globals (loaded components)
    if name in globals():
        return globals()[name]
    
    # Define the mapping of names to their modules
    component_map = {
        # Engine components
        'MathematicalTTSEngine': 'engine',
        'MathematicalContext': 'engine', 
        'ProcessedExpression': 'engine',
        'PerformanceMetrics': 'engine',
        'ContextDetector': 'engine',
        'UnknownLatexTracker': 'engine',
        'NaturalLanguageEnhancer': 'engine',
        
        # Voice Manager components
        'VoiceManager': 'voice_manager',
        'VoiceRole': 'voice_manager',
        'VoiceSettings': 'voice_manager',
        'SpeechSegment': 'voice_manager',
        'SpeedProfile': 'voice_manager',
        'SPEED_PROFILES': 'voice_manager',
        'ProfessorCommentary': 'voice_manager',
        
        # Context Memory components
        'ContextMemory': 'context_memory',
        'SymbolMemory': 'context_memory',
        'StructureMemory': 'context_memory',
        'MathematicalStructure': 'context_memory',
        'StructureType': 'context_memory',
        'DefinedSymbol': 'context_memory',
        'CrossReferenceHandler': 'context_memory',
        
        # Natural Language components
        'NaturalLanguageProcessor': 'natural_language',
        'MathematicalTone': 'natural_language',
        'EmphasisLevel': 'natural_language',
        'VariationEngine': 'natural_language',
        'MathematicalGrammarCorrector': 'natural_language',
        'PauseInserter': 'natural_language',
        'EmphasisDetector': 'natural_language',
        'ClarificationInjector': 'natural_language',
        
        # Pattern components
        'PatternProcessor': 'patterns',
        'MathSpeechProcessor': 'patterns',
    }
    
    if name in component_map:
        module_name = component_map[name]
        module = __import__(f'.{module_name}', package=__name__, level=1)
        return getattr(module, name)
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Export all - using __all__ for explicit exports
__all__ = [
    # Engine
    'MathematicalTTSEngine',
    'MathematicalContext', 
    'ProcessedExpression',
    'PerformanceMetrics',
    'ContextDetector',
    'UnknownLatexTracker',
    'NaturalLanguageEnhancer',
    
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
    'MathSpeechProcessor',
    
    # Convenience
    'create_engine',
]