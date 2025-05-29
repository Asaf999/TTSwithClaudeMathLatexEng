#!/usr/bin/env python3
"""
Natural Language Processor for Mathematical Text-to-Speech
=========================================================

Advanced language processing that transforms mathematical text into natural,
professor-quality speech with proper grammar, variations, and emphasis.

Features:
- Intelligent word variation to avoid robotic repetition
- Mathematical grammar correction
- Natural pause insertion
- Emphasis detection and marking
- Clarification injection for complex expressions
- Contextual phrasing adjustments
"""

import re
import random
import logging
from typing import Dict, List, Optional, Tuple, Set, Union, Callable, Any # Added Any here
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import json

logger = logging.getLogger(__name__)

# ===========================
# Linguistic Components
# ===========================

@dataclass
class PhraseMeaning:
    """Represents a phrase with its meaning and context"""
    phrase: str
    meaning: str
    formality: float  # 0.0 (casual) to 1.0 (formal)
    frequency: float  # How often to use (0.0 to 1.0)
    contexts: List[str] = field(default_factory=list)

class MathematicalTone(Enum):
    """Tone variations for mathematical speech"""
    FORMAL = "formal"
    CONVERSATIONAL = "conversational"
    EXPLANATORY = "explanatory"
    RIGOROUS = "rigorous"
    INTUITIVE = "intuitive"

class EmphasisLevel(Enum):
    """Levels of emphasis for important content"""
    NONE = 0
    MILD = 1
    MODERATE = 2
    STRONG = 3

# ===========================
# Variation System
# ===========================

class VariationEngine:
    """Manages word and phrase variations for natural speech"""
    
    def __init__(self):
        # Core variation pools with weighted options
        self.variations = {
            'equals': [
                ('equals', 0.3),
                ('is equal to', 0.25),
                ('is', 0.2),
                ('gives us', 0.15),
                ('yields', 0.1),
            ],
            'implies': [
                ('implies', 0.25),
                ('implies that', 0.2),
                ('tells us that', 0.2),
                ('means that', 0.2),
                ('shows that', 0.15),
            ],
            'therefore': [
                ('therefore', 0.25),
                ('thus', 0.2),
                ('hence', 0.2),
                ('so', 0.15),
                ('consequently', 0.1),
                ('it follows that', 0.1),
            ],
            'consider': [
                ('consider', 0.25),
                ("let's look at", 0.2),
                ('take', 0.15),
                ('examine', 0.15),
                ('observe', 0.15),
                ("let's examine", 0.1),
            ],
            'for_all': [
                ('for all', 0.3),
                ('for every', 0.25),
                ('for each', 0.2),
                ('for any', 0.15),
                ('for arbitrary', 0.1),
            ],
            'exists': [
                ('there exists', 0.3),
                ('there is', 0.25),
                ('we can find', 0.2),
                ('we have', 0.15),
                ('one can find', 0.1),
            ],
            'such_that': [
                ('such that', 0.35),
                ('so that', 0.25),
                ('with the property that', 0.15),
                ('satisfying', 0.15),
                ('where', 0.1),
            ],
            'if_and_only_if': [
                ('if and only if', 0.4),
                ('precisely when', 0.2),
                ('exactly when', 0.2),
                ('iff', 0.1),
                ('is equivalent to', 0.1),
            ],
            'let': [
                ('let', 0.3),
                ('suppose', 0.2),
                ('assume', 0.2),
                ('consider', 0.15),
                ('take', 0.15),
            ],
            'we_have': [
                ('we have', 0.25),
                ('we get', 0.2),
                ('we obtain', 0.2),
                ('this gives us', 0.15),
                ('we find', 0.1),
                ('one has', 0.1),
            ],
            'note_that': [
                ('note that', 0.25),
                ('observe that', 0.2),
                ('notice that', 0.2),
                ('recall that', 0.15),
                ('remember that', 0.1),
                ('it\'s worth noting that', 0.1),
            ],
        }
        
        # Usage tracking to ensure variety
        self.recent_usage: Dict[str, deque] = defaultdict(lambda: deque(maxlen=3))
        self.usage_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        # Context-sensitive adjustments
        self.context_adjustments = {
            'proof': {'formality': 0.8},
            'theorem': {'formality': 0.9},
            'example': {'formality': 0.4},
            'definition': {'formality': 0.7},
        }
    
    def get_variation(self, key: str, context: Optional[str] = None) -> str:
        """Get a varied phrase with context awareness"""
        if key not in self.variations:
            return key
        
        # Get weighted options
        options = self.variations[key]
        
        # Filter out recently used
        recent = self.recent_usage[key]
        available_options = [(phrase, weight) for phrase, weight in options 
                           if phrase not in recent]
        
        if not available_options:
            # All have been used recently, reset
            self.recent_usage[key].clear()
            available_options = options
        
        # Adjust weights based on context
        if context and context in self.context_adjustments:
            formality = self.context_adjustments[context]['formality']
            # Adjust weights based on formality
            # (This is simplified - a full implementation would have formality scores per phrase)
        
        # Select based on weights
        phrases, weights = zip(*available_options)
        selected = random.choices(phrases, weights=weights)[0]
        
        # Track usage
        self.recent_usage[key].append(selected)
        self.usage_counts[key][selected] += 1
        
        return selected
    
    def reset_usage(self) -> None:
        """Reset usage tracking for new session"""
        self.recent_usage.clear()
        self.usage_counts.clear()

# ===========================
# Grammar Correction
# ===========================

class MathematicalGrammarCorrector:
    """Corrects mathematical grammar for natural speech"""
    
    def __init__(self):
        # Grammar rules as (pattern, replacement, description)
        self.grammar_rules = [
            # Article corrections
            (r'\ba\s+([aeiouAEIOU])', r'an \1', 'Article before vowel'),
            (r'\ban\s+([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ])', r'a \1', 'Article before consonant'),
            
            # Mathematical function notation
            (r'f\s*:\s*X\s*→\s*Y', 'f maps X to Y', 'Function notation'),
            (r'f\s*:\s*X\s*\\to\s*Y', 'f maps X to Y', 'Function notation LaTeX'),
            (r'([a-zA-Z])\s*:\s*([A-Z])\s*→\s*([A-Z])', r'\1 maps \2 to \3', 'General function'),
            
            # Set notation
            (r'([xya-z])\s*∈\s*([A-Z])', r'\1 is in \2', 'Element membership'),
            (r'([xya-z])\s*\\in\s*([A-Z])', r'\1 is in \2', 'Element membership LaTeX'),
            (r'([A-Z])\s*⊆\s*([A-Z])', r'\1 is a subset of \2', 'Subset relation'),
            (r'([A-Z])\s*\\subseteq\s*([A-Z])', r'\1 is a subset of \2', 'Subset LaTeX'),
            
            # Quantifier improvements
            (r'∃!\s*', 'there exists a unique ', 'Unique existence'),
            (r'\\exists!\s*', 'there exists a unique ', 'Unique existence LaTeX'),
            (r'∀\s*([a-z])\s*∈', r'for all \1 in', 'Universal quantifier'),
            (r'\\forall\s*([a-z])\s*\\in', r'for all \1 in', 'Universal LaTeX'),
            
            # Definition patterns
            (r'[Ll]et\s+(\w+)\s*=\s*', r'Let \1 be ', 'Let definition'),
            (r'[Dd]efine\s+(\w+)\s*=\s*', r'Define \1 to be ', 'Define statement'),
            (r'[Ss]et\s+(\w+)\s*=\s*', r'Set \1 equal to ', 'Set statement'),
            
            # Logical connectives
            (r'\s*⇒\s*', ' implies ', 'Implication'),
            (r'\s*\\implies\s*', ' implies ', 'Implication LaTeX'),
            (r'\s*⇔\s*', ' if and only if ', 'Equivalence'),
            (r'\s*\\iff\s*', ' if and only if ', 'Equivalence LaTeX'),
            (r'\s*∧\s*', ' and ', 'Conjunction'),
            (r'\s*\\land\s*', ' and ', 'Conjunction LaTeX'),
            (r'\s*∨\s*', ' or ', 'Disjunction'),
            (r'\s*\\lor\s*', ' or ', 'Disjunction LaTeX'),
            
            # Common phrases
            (r'w\.?l\.?o\.?g\.?', 'without loss of generality', 'WLOG'),
            (r'w\.?r\.?t\.?', 'with respect to', 'WRT'),
            (r'i\.e\.', 'that is', 'Id est'),
            (r'e\.g\.', 'for example', 'Exempli gratia'),
            (r'cf\.', 'compare', 'Confer'),
            (r'resp\.', 'respectively', 'Respectively'),
            (r's\.?t\.?', 'such that', 'Such that'),
            
            # Natural connectives
            (r'\.\s*(?:Then|So|Now|Thus|Hence|Therefore)\s+', lambda m: f'. {m.group().strip()[1:].strip()}, ', 'Add comma after transition'),
            (r'(?:Then|So|Now|Thus|Hence|Therefore),\s*', lambda m: f'{m.group().strip()[:-1]}, ', 'Ensure comma after transition'),
            
            # Mathematical object descriptions
            (r'([A-Z])\s+is\s+a\s+([a-z]+)\s+space', r'\1 is a \2 space', 'Space description'),
            (r'the\s+map\s+([a-z])', r'the map \1', 'Map reference'),
            (r'the\s+function\s+([a-z])', r'the function \1', 'Function reference'),
        ]
        
        # Compile patterns
        self.compiled_rules = []
        for pattern, replacement, description in self.grammar_rules:
            try:
                compiled = re.compile(pattern)
                self.compiled_rules.append((compiled, replacement, description))
            except re.error as e:
                logger.warning(f"Failed to compile grammar rule '{description}': {e}")
    
    def correct(self, text: str) -> str:
        """Apply grammar corrections to text"""
        corrected = text
        
        for pattern, replacement, description in self.compiled_rules:
            if callable(replacement):
                corrected = pattern.sub(replacement, corrected)
            else:
                corrected = pattern.sub(replacement, corrected)
        
        # Additional corrections
        corrected = self._fix_punctuation_spacing(corrected)
        corrected = self._fix_mathematical_spacing(corrected)
        corrected = self._ensure_sentence_structure(corrected)
        
        return corrected
    
    def _fix_punctuation_spacing(self, text: str) -> str:
        """Fix spacing around punctuation"""
        # Remove space before punctuation
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        # Ensure space after punctuation (except decimals)
        text = re.sub(r'([.,;:!?])(?![0-9])(?!\s)', r'\1 ', text)
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _fix_mathematical_spacing(self, text: str) -> str:
        """Fix spacing in mathematical expressions"""
        # Space around operators
        operators = ['+', '-', '=', '<', '>', '≤', '≥', '≠', '∈', '⊆', '⊇']
        for op in operators:
            text = re.sub(f'\\s*{re.escape(op)}\\s*', f' {op} ', text)
        
        # No space in subscripts/superscripts
        text = re.sub(r'([a-zA-Z])\s+sub\s+([0-9a-zA-Z])', r'\1 sub \2', text)
        text = re.sub(r'([a-zA-Z])\s+to\s+the\s+([0-9a-zA-Z])', r'\1 to the \2', text)
        
        return text
    
    def _ensure_sentence_structure(self, text: str) -> str:
        """Ensure proper sentence structure"""
        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        # Capitalize after periods
        text = re.sub(r'(?<=[.!?])\s+([a-z])', lambda m: m.group(0).upper(), text)
        
        # Ensure ending punctuation
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text

# ===========================
# Pause Insertion
# ===========================

class PauseInserter:
    """Inserts natural pauses in mathematical speech"""
    
    def __init__(self):
        # Pause markers and durations
        self.pause_types = {
            'brief': 0.2,      # Brief pause
            'short': 0.4,      # Short pause
            'medium': 0.6,     # Medium pause
            'long': 0.8,       # Long pause
            'extended': 1.0,   # Extended pause
        }
        
        # Patterns for pause insertion
        self.pause_patterns = [
            # After mathematical statements
            (r'(\$[^$]+\$)([.!?])', r'\1\2 {{pause:short}}', 'After math expression'),
            
            # Before important transitions
            (r'\.\s+(Therefore|Thus|Hence|Now|So)', r'. {{pause:medium}} \1', 'Before conclusion'),
            (r'\.\s+(Proof|Example|Definition)', r'. {{pause:medium}} \1', 'Before new section'),
            
            # Around complex expressions
            (r'(\\frac\{[^}]+\}\{[^}]+\})', r'{{pause:brief}} \1 {{pause:brief}}', 'Around fractions'),
            (r'(\\int[^}]+)', r'{{pause:brief}} \1 {{pause:brief}}', 'Around integrals'),
            (r'(\\sum[^}]+)', r'{{pause:brief}} \1 {{pause:brief}}', 'Around sums'),
            
            # In lists
            (r',\s+(?=and)', r', {{pause:brief}} ', 'Before final item'),
            (r':\s*\n', r': {{pause:short}}\n', 'After colon'),
            
            # For emphasis
            (r'\b(UNIQUE|ONLY|MUST|ALWAYS|NEVER)\b', r'{{pause:brief}} \1 {{pause:brief}}', 'Emphasis words'),
            (r'\b(crucial|essential|fundamental|key|important)\b', r'{{pause:brief}} \1', 'Important words'),
            
            # Natural breathing points
            (r'([^.!?]{100,}?)([,;])', r'\1\2 {{pause:brief}}', 'Long clause break'),
        ]
        
        # Compile patterns
        self.compiled_patterns = []
        for pattern, replacement, description in self.pause_patterns:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
                self.compiled_patterns.append((compiled, replacement, description))
            except re.error as e:
                logger.warning(f"Failed to compile pause pattern '{description}': {e}")
    
    def insert_pauses(self, text: str) -> str:
        """Insert pause markers in text"""
        paused = text
        
        for pattern, replacement, description in self.compiled_patterns:
            paused = pattern.sub(replacement, paused)
        
        # Additional intelligent pauses
        paused = self._add_complexity_pauses(paused)
        paused = self._add_list_pauses(paused)
        paused = self._normalize_pauses(paused)
        
        return paused
    
    def _add_complexity_pauses(self, text: str) -> str:
        """Add pauses based on expression complexity"""
        # Count nesting depth for complex expressions
        segments = []
        current = ""
        depth = 0
        
        for char in text:
            current += char
            if char in '{([':
                depth += 1
            elif char in '})]':
                depth -= 1
                if depth == 0 and len(current) > 50:
                    # Complex expression ended
                    segments.append(current + " {{pause:brief}}")
                    current = ""
                    continue
        
        if current:
            segments.append(current)
        
        return ''.join(segments)
    
    def _add_list_pauses(self, text: str) -> str:
        """Add pauses in mathematical lists"""
        # Pattern: item1, item2, and item3
        pattern = r'([^,]+),\s*([^,]+),\s*and\s+([^,]+)'
        replacement = r'\1, {{pause:brief}} \2, {{pause:brief}} and \3'
        return re.sub(pattern, replacement, text)
    
    def _normalize_pauses(self, text: str) -> str:
        """Normalize multiple pauses"""
        # Remove duplicate pauses
        text = re.sub(r'(\{\{pause:[^}]+\}\}\s*)+', r'\1', text)
        # Remove pause at start
        text = re.sub(r'^\s*\{\{pause:[^}]+\}\}\s*', '', text)
        return text

# ===========================
# Emphasis Detection
# ===========================

class EmphasisDetector:
    """Detects and marks content requiring emphasis"""
    
    def __init__(self):
        # Emphasis patterns with levels
        self.emphasis_patterns = [
            # Strong emphasis
            (r'\b(UNIQUE|ONLY|MUST|ALWAYS|NEVER|NOT)\b', EmphasisLevel.STRONG),
            (r'\b(crucial|critical|essential|fundamental|vital)\b', EmphasisLevel.STRONG),
            
            # Moderate emphasis
            (r'\b(important|key|significant|main|primary|central)\b', EmphasisLevel.MODERATE),
            (r'\b(note that|observe that|notice that|recall that)\b', EmphasisLevel.MODERATE),
            (r'!\s*(?=\w)', EmphasisLevel.MODERATE),  # After exclamation
            
            # Mild emphasis
            (r'\b(interesting|useful|helpful|convenient)\b', EmphasisLevel.MILD),
            (r'\b(in particular|especially|specifically)\b', EmphasisLevel.MILD),
            
            # Mathematical emphasis
            (r'if and only if', EmphasisLevel.MODERATE),
            (r'necessary and sufficient', EmphasisLevel.MODERATE),
            (r'contradiction', EmphasisLevel.MODERATE),
        ]
        
        # Compile patterns
        self.compiled_patterns = []
        for pattern, level in self.emphasis_patterns:
            compiled = re.compile(pattern, re.IGNORECASE)
            self.compiled_patterns.append((compiled, level))
    
    def mark_emphasis(self, text: str) -> str:
        """Mark text segments requiring emphasis"""
        emphasized = text
        
        for pattern, level in self.compiled_patterns:
            def add_emphasis(match):
                return f'{{{{emphasis:{level.value}}}}}{match.group()}{{{{/emphasis}}}}'
            
            emphasized = pattern.sub(add_emphasis, emphasized)
        
        # Context-based emphasis
        emphasized = self._add_structural_emphasis(emphasized)
        
        return emphasized
    
    def _add_structural_emphasis(self, text: str) -> str:
        """Add emphasis based on mathematical structure"""
        # Emphasize theorem/lemma statements
        pattern = r'(Theorem|Lemma|Proposition|Corollary)\s+\d+\.?\d*\s*[:.]\s*([^.]+\.)'
        def emphasize_statement(match):
            return f'{match.group(1)} {match.group(2)}{{{{emphasis:1}}}}{match.group(3)}{{{{/emphasis}}}}'
        
        text = re.sub(pattern, emphasize_statement, text, flags=re.IGNORECASE)
        
        return text

# ===========================
# Clarification Injector
# ===========================

class ClarificationInjector:
    """Injects helpful clarifications for complex expressions"""
    
    def __init__(self):
        # Clarification templates
        self.clarifications = {
            'complex_fraction': [
                "that is, {} divided by {}",
                "which is {} over {}",
                "meaning {} in the numerator and {} in the denominator",
            ],
            'nested_expression': [
                "working from the inside out",
                "starting with the innermost expression",
                "evaluating step by step",
            ],
            'long_sum': [
                "summing over all {}",
                "adding up terms for each {}",
                "taking the sum as {} varies",
            ],
            'set_notation': [
                "the set of all {} such that {}",
                "meaning all {} satisfying {}",
                "that is, every {} with the property {}",
            ],
        }
        
        # Patterns requiring clarification
        self.clarification_patterns = [
            # Complex fractions
            (r'\\frac\{([^{}]+\{[^}]+\}[^{}]*)\}\{([^{}]+\{[^}]+\}[^{}]*)\}',
             'complex_fraction'),
            
            # Set builder notation
            (r'\{([^:|}]+)[:|]([^}]+)\}',
             'set_notation'),
            
            # Long summations
            (r'\\sum_\{([^}]{20,})\}',
             'long_sum'),
        ]
    
    def add_clarifications(self, text: str, complexity_threshold: float = 0.7) -> str:
        """Add clarifications to complex expressions"""
        clarified = text
        
        # Only add clarifications if complexity is high
        if self._estimate_complexity(text) < complexity_threshold:
            return text
        
        for pattern, clarification_type in self.clarification_patterns:
            regex = re.compile(pattern)
            matches = list(regex.finditer(clarified))
            
            for match in reversed(matches):  # Work backwards to preserve positions
                if clarification_type in self.clarifications:
                    clarification = self._generate_clarification(
                        clarification_type, 
                        match.groups()
                    )
                    if clarification:
                        # Insert after the complex expression
                        pos = match.end()
                        clarified = (
                            clarified[:pos] + 
                            f", {{{{clarify}}}}{clarification}{{{{/clarify}}}}, " +
                            clarified[pos:]
                        )
        
        return clarified
    
    def _estimate_complexity(self, text: str) -> float:
        """Estimate complexity of mathematical text"""
        complexity = 0.0
        
        # Factors that increase complexity
        complexity += len(re.findall(r'\\frac', text)) * 0.1
        complexity += len(re.findall(r'\\int', text)) * 0.15
        complexity += len(re.findall(r'\\sum', text)) * 0.1
        complexity += len(re.findall(r'\{[^}]{20,}\}', text)) * 0.05
        complexity += text.count('{') * 0.02
        
        # Normalize
        return min(complexity, 1.0)
    
    def _generate_clarification(self, 
                              clarification_type: str, 
                              groups: Tuple[str, ...]) -> Optional[str]:
        """Generate appropriate clarification"""
        if clarification_type not in self.clarifications:
            return None
        
        templates = self.clarifications[clarification_type]
        template = random.choice(templates)
        
        try:
            return template.format(*groups)
        except (IndexError, KeyError):
            return None

# ===========================
# Main Natural Language Processor
# ===========================

class NaturalLanguageProcessor:
    """Main processor integrating all natural language components"""
    
    def __init__(self, tone: MathematicalTone = MathematicalTone.CONVERSATIONAL):
        self.tone = tone
        
        # Initialize components
        self.variation_engine = VariationEngine()
        self.grammar_corrector = MathematicalGrammarCorrector()
        self.pause_inserter = PauseInserter()
        self.emphasis_detector = EmphasisDetector()
        self.clarification_injector = ClarificationInjector()
        
        # Processing options
        self.options = {
            'use_variations': True,
            'correct_grammar': True,
            'insert_pauses': True,
            'detect_emphasis': True,
            'add_clarifications': True,
            'max_clarifications_per_expression': 2,
        }
        
        logger.info(f"Natural language processor initialized with {tone.value} tone")
    
    def process(self, 
                text: str, 
                context: Optional[Dict[str, Any]] = None) -> str: # Corrected type hint here
        """Process text through all natural language components"""
        processed = text
        
        # Step 1: Grammar correction (do this first)
        if self.options['correct_grammar']:
            processed = self.grammar_corrector.correct(processed)
        
        # Step 2: Apply variations
        if self.options['use_variations']:
            processed = self._apply_variations(processed, context)
        
        # Step 3: Add clarifications for complex parts
        if self.options['add_clarifications']:
            processed = self.clarification_injector.add_clarifications(processed)
        
        # Step 4: Detect and mark emphasis
        if self.options['detect_emphasis']:
            processed = self.emphasis_detector.mark_emphasis(processed)
        
        # Step 5: Insert natural pauses
        if self.options['insert_pauses']:
            processed = self.pause_inserter.insert_pauses(processed)
        
        # Step 6: Final cleanup
        processed = self._final_cleanup(processed)
        
        return processed
    
    def _apply_variations(self, text: str, context: Optional[Dict[str, Any]]) -> str:
        """Apply word variations throughout text"""
        varied = text
        
        # Determine context type
        context_type = None
        if context:
            if context.get('in_proof'):
                context_type = 'proof'
            elif context.get('in_theorem'):
                context_type = 'theorem'
            elif context.get('in_example'):
                context_type = 'example'
        
        # Apply variations
        variation_patterns = [
            # Equals and equivalence
            (r'\s*=\s*', 'equals'),
            (r'\s*≡\s*', 'equals'),
            (r'\s*:=\s*', 'equals'),
            
            # Implications
            (r'\s*⇒\s*', 'implies'),
            (r'\s*\\implies\s*', 'implies'),
            (r'\s*\\Rightarrow\s*', 'implies'),
            
            # Therefore/thus
            (r'(?:^|\.\s+)(Therefore|Thus|Hence|So|Consequently)\b', 'therefore'),
            
            # Quantifiers
            (r'\\forall\s*', 'for_all'),
            (r'∀\s*', 'for_all'),
            (r'\\exists\s*', 'exists'),
            (r'∃\s*', 'exists'),
            
            # Such that
            (r'\s+s\.?t\.?\s+', 'such_that'),
            (r'\s*\|\s*', 'such_that'),  # In set notation
            
            # If and only if
            (r'\biff\b', 'if_and_only_if'),
            (r'⇔', 'if_and_only_if'),
            
            # Let/suppose
            (r'^Let\s+', 'let'),
            (r'(?<=\.\s)Let\s+', 'let'),
            
            # We have/get
            (r'[Ww]e\s+(?:have|get|obtain)\s+', 'we_have'),
            
            # Note that
            (r'[Nn]ote\s+that\s+', 'note_that'),
            (r'[Oo]bserve\s+that\s+', 'note_that'),
        ]
        
        for pattern, var_key in variation_patterns:
            regex = re.compile(pattern)
            
            def replacer(match):
                variation = self.variation_engine.get_variation(var_key, context_type)
                # Preserve capitalization and spacing
                if match.group(0)[0].isupper():
                    variation = variation[0].upper() + variation[1:]
                if pattern.startswith('(?:^|'):  # Beginning of sentence
                    return '. ' + variation
                return ' ' + variation + ' '
            
            varied = regex.sub(replacer, varied)
        
        return varied
    
    def _final_cleanup(self, text: str) -> str:
        """Final cleanup and formatting"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])(?![0-9])(?!\s|$)', r'\1 ', text)
        
        # Ensure proper sentence endings
        if text and not text[-1] in '.!?':
            text += '.'
        
        # Clean up markup spacing
        text = re.sub(r'\{\{\s*', '{{', text)
        text = re.sub(r'\s*\}\}', '}}', text)
        
        return text.strip()
    
    def set_tone(self, tone: MathematicalTone) -> None:
        """Change the mathematical tone"""
        self.tone = tone
        logger.info(f"Tone changed to {tone.value}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'tone': self.tone.value,
            'variation_usage': dict(self.variation_engine.usage_counts),
            'options': self.options.copy(),
        }
    
    def reset(self) -> None:
        """Reset processor state"""
        self.variation_engine.reset_usage()
        logger.info("Natural language processor reset")

# ===========================
# Testing Functions
# ===========================

def test_natural_language_processor():
    """Test natural language processing"""
    processor = NaturalLanguageProcessor()
    
    test_cases = [
        # Basic processing
        "Let X = Y. Then X = Z implies Y = Z.",
        "∀ε>0 ∃δ>0 s.t. |x-a|<δ ⇒ |f(x)-f(a)|<ε",
        "f: X → Y is continuous iff ∀ open U ⊆ Y, f^{-1}(U) is open.",
        
        # Complex expressions
        "The integral \\int_0^∞ e^{-x²} dx = \\frac{\\sqrt{π}}{2}.",
        "Consider the fraction \\frac{\\sum_{i=1}^n x_i²}{\\sqrt{\\sum_{i=1}^n y_i²}}.",
        
        # Emphasis and structure
        "This is CRUCIAL: X must be compact.",
        "Note that this is the ONLY case where the theorem fails.",
        "Theorem 3.1. Every compact Hausdorff space is normal.",
    ]
    
    print("Testing Natural Language Processor")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input:  {test}")
        result = processor.process(test)
        print(f"Output: {result}")
    
    print("\nStatistics:")
    stats = processor.get_statistics()
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    test_natural_language_processor()
