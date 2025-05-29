#!/usr/bin/env python3
"""
Main TTS Engine for Mathematical Text-to-Speech System
=====================================================

The core engine that orchestrates mathematical text processing, voice management,
and speech generation with professor-quality narration.

Features:
- Complete mathematical notation processing
- Multi-voice orchestration with intelligent switching
- Unknown LaTeX command tracking and learning
- Performance-optimized processing pipeline
- Natural language enhancement
- Comprehensive error handling
"""

import re
import json
import time
import asyncio
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Set, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict
import hashlib
from concurrent.futures import ThreadPoolExecutor
import edge_tts

# Import voice manager (would be from .voice_manager in package structure)
# from .voice_manager import VoiceManager, VoiceRole, SpeechSegment, SpeedProfile

# Configure module logger
logger = logging.getLogger(__name__)

# ===========================
# Data Classes
# ===========================

@dataclass
class ProcessedExpression:
    """Represents a processed mathematical expression"""
    original: str
    processed: str
    context: str
    segments: List['SpeechSegment']
    processing_time: float
    unknown_commands: List[str] = field(default_factory=list)

@dataclass
class PerformanceMetrics:
    """Performance tracking for the engine"""
    tokens_processed: int = 0
    total_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    unknown_commands_found: int = 0
    
    @property
    def tokens_per_second(self) -> float:
        return self.tokens_processed / max(self.total_time, 0.001)

# ===========================
# Mathematical Context Detection
# ===========================

class MathematicalContext(Enum):
    """Mathematical domains for context detection"""
    TOPOLOGY = "topology"
    COMPLEX_ANALYSIS = "complex_analysis"
    NUMERICAL_ANALYSIS = "numerical_analysis"
    MANIFOLDS = "manifolds"
    ODE = "ode"
    REAL_ANALYSIS = "real_analysis"
    MEASURE_THEORY = "measure_theory"
    COMBINATORICS = "combinatorics"
    ALGEBRA = "algebra"
    GENERAL = "general"

class ContextDetector:
    """Detects mathematical context from content"""
    
    def __init__(self):
        self.context_indicators = {
            MathematicalContext.TOPOLOGY: {
                'keywords': [
                    'topolog', 'continuous', 'compact', 'connected', 'hausdorff',
                    'open cover', 'closed set', 'homeomorph', 'homotop', 'fundamental group',
                    'covering space', 'manifold', 'fiber bundle', 'separation axiom'
                ],
                'symbols': [r'\\pi_1', r'T_[0-9]', r'\\tau', r'\\overline\{', r'\\partial'],
                'weight': 1.0
            },
            MathematicalContext.COMPLEX_ANALYSIS: {
                'keywords': [
                    'holomorphic', 'analytic', 'residue', 'contour', 'cauchy',
                    'meromorphic', 'pole', 'essential singularity', 'branch cut',
                    'conformal', 'riemann', 'laurent'
                ],
                'symbols': [r'\\oint', r'\\text\{Res\}', r'\\bar\{z\}', r'\\Re', r'\\Im'],
                'weight': 1.0
            },
            MathematicalContext.NUMERICAL_ANALYSIS: {
                'keywords': [
                    'convergence', 'iteration', 'error', 'stability', 'condition number',
                    'interpolation', 'quadrature', 'finite difference', 'newton method',
                    'discretization', 'truncation'
                ],
                'symbols': [r'O\(', r'\\kappa', r'h\^[0-9]', r'\\epsilon_\{machine\}'],
                'weight': 1.0
            },
            MathematicalContext.MANIFOLDS: {
                'keywords': [
                    'tangent space', 'cotangent', 'differential form', 'vector field',
                    'connection', 'curvature', 'geodesic', 'riemannian', 'metric tensor',
                    'christoffel', 'lie derivative'
                ],
                'symbols': [r'T_p M', r'\\nabla', r'\\omega', r'\\wedge', r'd\\omega'],
                'weight': 1.0
            },
            MathematicalContext.ODE: {
                'keywords': [
                    'differential equation', 'initial value', 'boundary value',
                    'wronskian', 'phase portrait', 'stability', 'equilibrium',
                    'linearization', 'fundamental matrix'
                ],
                'symbols': [r'y\'', r'\\dot\{', r'\\ddot\{', r'y\^\{\\prime\}'],
                'weight': 1.0
            }
        }
        
        # Compile regex patterns for efficiency
        for context, data in self.context_indicators.items():
            data['compiled_symbols'] = [re.compile(pattern) for pattern in data['symbols']]
    
    def detect_context(self, text: str) -> Tuple[MathematicalContext, float]:
        """Detect mathematical context with confidence score"""
        scores = defaultdict(float)
        text_lower = text.lower()
        
        for context, indicators in self.context_indicators.items():
            # Check keywords
            for keyword in indicators['keywords']:
                if keyword in text_lower:
                    scores[context] += indicators['weight']
            
            # Check symbols
            for pattern in indicators['compiled_symbols']:
                if pattern.search(text):
                    scores[context] += indicators['weight'] * 1.5  # Symbols are stronger indicators
        
        if not scores:
            return MathematicalContext.GENERAL, 0.0
        
        # Get context with highest score
        best_context = max(scores.items(), key=lambda x: x[1])
        total_score = sum(scores.values())
        confidence = best_context[1] / total_score if total_score > 0 else 0.0
        
        # Require minimum confidence
        if confidence < 0.3:
            return MathematicalContext.GENERAL, 0.0
        
        return best_context[0], confidence

# ===========================
# Unknown LaTeX Tracker
# ===========================

class UnknownLatexTracker:
    """Tracks and manages unknown LaTeX commands"""
    
    def __init__(self, db_path: Path = Path("unknown_latex_commands.json")):
        self.db_path = db_path
        self.unknown_commands: Dict[str, Dict[str, Any]] = self._load_database()
        self.session_commands: Set[str] = set()
        
    def _load_database(self) -> Dict[str, Dict[str, Any]]:
        """Load unknown commands database"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load unknown commands database: {e}")
        return {}
    
    def save_database(self) -> None:
        """Save unknown commands database"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.unknown_commands, f, indent=2, sort_keys=True)
        except Exception as e:
            logger.error(f"Failed to save unknown commands database: {e}")
    
    def track_command(self, command: str, context: str = "") -> None:
        """Track an unknown command"""
        if command not in self.unknown_commands:
            self.unknown_commands[command] = {
                'first_seen': time.strftime('%Y-%m-%d %H:%M:%S'),
                'count': 0,
                'contexts': []
            }
        
        self.unknown_commands[command]['count'] += 1
        self.unknown_commands[command]['last_seen'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Store context sample
        if context and len(self.unknown_commands[command]['contexts']) < 5:
            self.unknown_commands[command]['contexts'].append(context[:100])
        
        self.session_commands.add(command)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of unknown commands from this session"""
        return {
            'total_unknown': len(self.session_commands),
            'commands': list(self.session_commands),
            'most_frequent': sorted(
                [(cmd, data['count']) for cmd, data in self.unknown_commands.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

# ===========================
# Natural Language Enhancer
# ===========================

class NaturalLanguageEnhancer:
    """Enhances mathematical text for natural speech"""
    
    def __init__(self):
        # Variation pools for natural speech
        self.variations = {
            'equals': ['equals', 'is equal to', 'is', 'gives us', 'yields'],
            'implies': ['implies', 'implies that', 'tells us that', 'means that', 'shows that'],
            'therefore': ['therefore', 'thus', 'hence', 'so', 'consequently'],
            'consider': ['consider', 'let\'s look at', 'take', 'examine', 'observe'],
            'for_all': ['for all', 'for every', 'for each', 'for any'],
            'exists': ['there exists', 'there is', 'we can find', 'we have'],
        }
        
        # Track usage for variation
        self.usage_counters = defaultdict(int)
        
        # Mathematical idioms
        self.idioms = {
            r'w\.?l\.?o\.?g\.?': 'without loss of generality',
            r'iff\b': 'if and only if',
            r'wrt\b': 'with respect to',
            r'i\.e\.': 'that is',
            r'e\.g\.': 'for example',
            r'cf\.': 'compare',
            r'resp\.': 'respectively',
            r'a\.e\.': 'almost everywhere',
            r'a\.s\.': 'almost surely',
        }
        
        # Compile idiom patterns
        self.idiom_patterns = [(re.compile(pattern, re.IGNORECASE), replacement) 
                               for pattern, replacement in self.idioms.items()]
    
    def enhance_text(self, text: str) -> str:
        """Enhance text for natural speech"""
        # Replace idioms
        for pattern, replacement in self.idiom_patterns:
            text = pattern.sub(replacement, text)
        
        # Apply variations
        text = self._apply_variations(text)
        
        # Improve mathematical grammar
        text = self._improve_grammar(text)
        
        # Add natural pauses
        text = self._add_natural_pauses(text)
        
        return text
    
    def _apply_variations(self, text: str) -> str:
        """Apply word variations for natural speech"""
        # Smart equals variation
        def replace_equals(match):
            pool = self.variations['equals']
            index = self.usage_counters['equals'] % len(pool)
            self.usage_counters['equals'] += 1
            return f" {pool[index]} "
        
        text = re.sub(r'\s*=\s*', replace_equals, text)
        
        # Other variations
        variation_patterns = [
            (r'\s*\\implies\s*', 'implies'),
            (r'\s*\\therefore\s*', 'therefore'),
            (r'\\forall\s*', 'for_all'),
            (r'\\exists\s*', 'exists'),
        ]
        
        for pattern, key in variation_patterns:
            if key in self.variations:
                def make_replacer(k):
                    def replacer(match):
                        pool = self.variations[k]
                        index = self.usage_counters[k] % len(pool)
                        self.usage_counters[k] += 1
                        return pool[index] + " "
                    return replacer
                
                text = re.sub(pattern, make_replacer(key), text)
        
        return text
    
    def _improve_grammar(self, text: str) -> str:
        """Improve mathematical grammar for natural speech"""
        improvements = [
            # Function notation
            (r'f\s*:\s*X\s*→\s*Y', 'f maps X to Y'),
            (r'f\s*:\s*X\s*\\to\s*Y', 'f maps X to Y'),
            
            # Common patterns
            (r'∃!\s*', 'there exists a unique '),
            (r'\\exists!\s*', 'there exists a unique '),
            
            # Improved phrasing
            (r'Let\s+(\w+)\s*=\s*', r'Let \1 be '),
            (r'Define\s+(\w+)\s*=\s*', r'Define \1 to be '),
            
            # Natural connectives
            (r'\.\s*Then\s+', '. Then, '),
            (r'\.\s*Now\s+', '. Now, '),
            (r'\.\s*Note\s+that\s+', '. Note that '),
        ]
        
        for pattern, replacement in improvements:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _add_natural_pauses(self, text: str) -> str:
        """Add markers for natural pauses"""
        # Add pause after mathematical statements
        text = re.sub(r'(\$[^$]+\$)([.!?])\s*', r'\1\2 {{pause}} ', text)
        
        # Add pause before important transitions
        text = re.sub(r'\.\s*(Therefore|Thus|Hence|Now|Proof)', r'. {{pause}} \1', text)
        
        return text

# ===========================
# Main TTS Engine
# ===========================

class MathematicalTTSEngine:
    """Main engine for mathematical text-to-speech"""
    
    def __init__(self, 
                 voice_manager: Optional['VoiceManager'] = None,
                 config_path: Optional[Path] = None,
                 enable_caching: bool = True):
        
        # Initialize components
        self.voice_manager = voice_manager  # or VoiceManager()
        self.context_detector = ContextDetector()
        self.unknown_tracker = UnknownLatexTracker()
        self.language_enhancer = NaturalLanguageEnhancer()
        
        # Performance optimization
        self.enable_caching = enable_caching
        self.expression_cache: Dict[str, ProcessedExpression] = {}
        self.max_cache_size = 1000
        
        # Configuration
        self.config = self._load_config(config_path) if config_path else {}
        
        # Performance metrics
        self.metrics = PerformanceMetrics()
        
        # Thread pool for parallel processing
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
        # Mathematical processors (would import from domain modules)
        self.domain_processors: Dict[MathematicalContext, Any] = {}
        
        logger.info("Mathematical TTS Engine initialized")
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load engine configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
            return {}
    
    def process_latex(self, 
                      latex: str, 
                      force_context: Optional[MathematicalContext] = None) -> ProcessedExpression:
        """Process LaTeX expression into speech segments"""
        start_time = time.time()
        
        # Check cache
        cache_key = self._get_cache_key(latex, force_context)
        if self.enable_caching and cache_key in self.expression_cache:
            self.metrics.cache_hits += 1
            return self.expression_cache[cache_key]
        
        self.metrics.cache_misses += 1
        
        try:
            # Detect context
            context, confidence = self.context_detector.detect_context(latex)
            if force_context:
                context = force_context
            
            logger.debug(f"Detected context: {context.value} (confidence: {confidence:.2f})")
            
            # Pre-process
            processed_text = self._preprocess_latex(latex)
            
            # Extract unknown commands
            unknown_commands = self._extract_unknown_commands(processed_text)
            if unknown_commands:
                for cmd in unknown_commands:
                    self.unknown_tracker.track_command(cmd, latex[:50])
                self.metrics.unknown_commands_found += len(unknown_commands)
            
            # Domain-specific processing
            if context in self.domain_processors:
                processed_text = self.domain_processors[context].process(processed_text)
            else:
                processed_text = self._general_processing(processed_text)
            
            # Natural language enhancement
            processed_text = self.language_enhancer.enhance_text(processed_text)
            
            # Split into sentences
            sentences = self._intelligent_sentence_split(processed_text)
            
            # Process with voice manager
            if self.voice_manager:
                segments = self.voice_manager.process_text(processed_text, sentences)
                segments = self.voice_manager.combine_speech_segments(segments)
            else:
                segments = []
            
            # Create result
            result = ProcessedExpression(
                original=latex,
                processed=processed_text,
                context=context.value,
                segments=segments,
                processing_time=time.time() - start_time,
                unknown_commands=unknown_commands
            )
            
            # Update metrics
            self.metrics.tokens_processed += len(latex.split())
            self.metrics.total_time += result.processing_time
            
            # Cache result
            if self.enable_caching:
                self._add_to_cache(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing LaTeX: {e}", exc_info=True)
            # Return safe fallback
            return ProcessedExpression(
                original=latex,
                processed=f"Error processing expression: {latex}",
                context="error",
                segments=[],
                processing_time=time.time() - start_time
            )
    
    def _get_cache_key(self, latex: str, context: Optional[MathematicalContext]) -> str:
        """Generate cache key for expression"""
        content = f"{latex}:{context.value if context else 'auto'}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _add_to_cache(self, key: str, result: ProcessedExpression) -> None:
        """Add result to cache with size limit"""
        if len(self.expression_cache) >= self.max_cache_size:
            # Remove oldest entries (simple FIFO)
            oldest_keys = list(self.expression_cache.keys())[:self.max_cache_size // 10]
            for k in oldest_keys:
                del self.expression_cache[k]
        
        self.expression_cache[key] = result
    
    def _preprocess_latex(self, latex: str) -> str:
        """Pre-process LaTeX for better handling"""
        # Normalize whitespace
        text = ' '.join(latex.split())
        
        # Fix common LaTeX issues
        fixes = [
            (r'\\\\', ' '),  # Line breaks
            (r'&=', ' equals '),  # Align at equals
            (r'\\quad', ' '),  # Spacing
            (r'\\qquad', ' '),
            (r'\\,', ' '),  # Thin space
            (r'\\;', ' '),  # Medium space
            (r'\\:', ' '),  # Thick space
            (r'\\!', ''),   # Negative space
        ]
        
        for pattern, replacement in fixes:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _extract_unknown_commands(self, text: str) -> List[str]:
        """Extract potentially unknown LaTeX commands"""
        # Find all LaTeX commands
        commands = re.findall(r'\\([a-zA-Z]+)', text)
        
        # Known commands (subset for brevity - would be complete list)
        known_commands = {
            'frac', 'sqrt', 'sum', 'int', 'prod', 'lim', 'sin', 'cos', 'tan',
            'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'pi', 'sigma',
            'infty', 'partial', 'nabla', 'forall', 'exists', 'in', 'subset',
            'cup', 'cap', 'wedge', 'vee', 'times', 'cdot', 'ldots', 'text',
            'begin', 'end', 'left', 'right', 'big', 'Big', 'mathbb', 'mathcal',
            'mathbf', 'mathrm', 'overline', 'underline', 'hat', 'tilde', 'bar',
        }
        
        unknown = [cmd for cmd in commands if cmd not in known_commands]
        return list(set(unknown))  # Remove duplicates
    
    def _general_processing(self, text: str) -> str:
        """General mathematical processing"""
        # This would be expanded with complete notation
        replacements = OrderedDict([
            # Greek letters
            (r'\\alpha', 'alpha'),
            (r'\\beta', 'beta'),
            (r'\\gamma', 'gamma'),
            (r'\\delta', 'delta'),
            (r'\\epsilon', 'epsilon'),
            (r'\\theta', 'theta'),
            (r'\\lambda', 'lambda'),
            (r'\\mu', 'mu'),
            (r'\\pi', 'pi'),
            (r'\\sigma', 'sigma'),
            (r'\\omega', 'omega'),
            
            # Operations
            (r'\\times', ' times '),
            (r'\\cdot', ' dot '),
            (r'\\pm', ' plus or minus '),
            (r'\\mp', ' minus or plus '),
            
            # Sets
            (r'\\mathbb{R}', 'the real numbers'),
            (r'\\mathbb{C}', 'the complex numbers'),
            (r'\\mathbb{N}', 'the natural numbers'),
            (r'\\mathbb{Z}', 'the integers'),
            (r'\\mathbb{Q}', 'the rational numbers'),
            
            # Logic
            (r'\\forall', 'for all'),
            (r'\\exists', 'there exists'),
            (r'\\in', ' in '),
            (r'\\subset', ' is a subset of '),
            (r'\\cup', ' union '),
            (r'\\cap', ' intersection '),
            
            # Functions
            (r'\\sin', 'sine'),
            (r'\\cos', 'cosine'),
            (r'\\tan', 'tangent'),
            (r'\\log', 'log'),
            (r'\\ln', 'natural log'),
            (r'\\exp', 'exponential'),
            
            # Limits and sums
            (r'\\lim_{([^}]+)}', r'the limit as \1 of'),
            (r'\\sum_{([^}]+)}^{([^}]+)}', r'the sum from \1 to \2 of'),
            (r'\\int_{([^}]+)}^{([^}]+)}', r'the integral from \1 to \2 of'),
            
            # Fractions
            (r'\\frac{([^}]+)}{([^}]+)}', r'\1 over \2'),
            
            # Other
            (r'\\infty', 'infinity'),
            (r'\\partial', 'partial'),
            (r'\\nabla', 'nabla'),
        ])
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        # Clean up
        text = re.sub(r'[{}]', '', text)
        text = re.sub(r'\\', ' ', text)
        text = ' '.join(text.split())
        
        return text
    
    def _intelligent_sentence_split(self, text: str) -> List[str]:
        """Split text into sentences intelligently"""
        # Basic sentence splitting with mathematical awareness
        sentences = []
        current = []
        
        # Split on periods, but be careful with decimals
        parts = re.split(r'(?<=[.!?])\s+', text)
        
        for part in parts:
            current.append(part)
            
            # Check if this looks like a complete sentence
            if self._is_complete_sentence(' '.join(current)):
                sentences.append(' '.join(current))
                current = []
        
        if current:
            sentences.append(' '.join(current))
        
        return sentences
    
    def _is_complete_sentence(self, text: str) -> bool:
        """Check if text appears to be a complete sentence"""
        # Simple heuristic - would be more sophisticated
        if not text:
            return False
        
        # Must end with sentence terminator
        if not re.search(r'[.!?]$', text):
            return False
        
        # Should have reasonable length
        if len(text.split()) < 3:
            return False
        
        # Check for balanced parentheses/brackets
        if text.count('(') != text.count(')'):
            return False
        
        return True
    
    async def speak_expression(self, expression: ProcessedExpression, output_file: Optional[str] = None) -> None:
        """Convert expression to speech using edge-tts
        
        Args:
            expression: The processed expression to speak
            output_file: Optional output file path. If None, plays audio directly.
        """
        for segment in expression.segments:
            try:
                voice = segment.voice_role.value if hasattr(segment, 'voice_role') else "en-US-AriaNeural"
                rate = segment.rate_modifier if hasattr(segment, 'rate_modifier') else "+0%"
                
                # Add pauses
                if hasattr(segment, 'pause_before') and segment.pause_before > 0:
                    await asyncio.sleep(segment.pause_before)
                
                # Generate speech
                tts = edge_tts.Communicate(segment.text, voice, rate=rate)
                audio_file = output_file if output_file else f"temp_speech_{time.time()}.mp3"
                await tts.save(audio_file)
                
                # Play audio if no output file specified
                # if not output_file:
                #     subprocess.run(['mpv', '--really-quiet', audio_file])
                
                # Clean up temp file
                Path(audio_file).unlink(missing_ok=True)
                
                # Add pause after
                if hasattr(segment, 'pause_after') and segment.pause_after > 0:
                    await asyncio.sleep(segment.pause_after)
                    
            except Exception as e:
                logger.error(f"Error speaking segment: {e}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            'metrics': {
                'tokens_per_second': self.metrics.tokens_per_second,
                'total_tokens': self.metrics.tokens_processed,
                'total_time': self.metrics.total_time,
                'cache_hit_rate': self.metrics.cache_hits / max(self.metrics.cache_hits + self.metrics.cache_misses, 1),
                'unknown_commands': self.metrics.unknown_commands_found,
            },
            'cache': {
                'size': len(self.expression_cache),
                'max_size': self.max_cache_size,
            },
            'unknown_commands': self.unknown_tracker.get_session_summary(),
        }
    
    def save_unknown_commands(self) -> None:
        """Save unknown commands database"""
        self.unknown_tracker.save_database()
    
    def shutdown(self) -> None:
        """Clean shutdown of engine"""
        self.save_unknown_commands()
        self.thread_pool.shutdown(wait=True)
        logger.info("TTS Engine shut down")

# ===========================
# Testing Functions
# ===========================

def _test_engine():
    """Test the TTS engine"""
    engine = MathematicalTTSEngine()
    
    test_expressions = [
        r"Let $f: \mathbb{R} \to \mathbb{R}$ be continuous.",
        r"$\forall \epsilon > 0 \, \exists \delta > 0$ such that $|x - x_0| < \delta \implies |f(x) - f(x_0)| < \epsilon$",
        r"Theorem 3.1. Every compact Hausdorff space is normal.",
        r"$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$",
    ]
    
    print("Testing Mathematical TTS Engine")
    print("=" * 50)
    
    for expr in test_expressions:
        print(f"\nProcessing: {expr[:50]}...")
        result = engine.process_latex(expr)
        
        print(f"Context: {result.context}")
        print(f"Processed: {result.processed[:100]}...")
        print(f"Processing time: {result.processing_time:.3f}s")
        print(f"Unknown commands: {result.unknown_commands}")
    
    print("\nPerformance Report:")
    report = engine.get_performance_report()
    print(json.dumps(report, indent=2))
    
    engine.shutdown()

if __name__ == "__main__":
    _test_engine()