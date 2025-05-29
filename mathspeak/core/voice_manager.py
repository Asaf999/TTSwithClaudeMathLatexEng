#!/usr/bin/env python3
"""
Voice Manager for Mathematical Text-to-Speech System
===================================================

Manages multi-voice system with intelligent switching, dynamic speed control,
and professor-style commentary injection.

This module provides:
- 7 distinct voice roles for different mathematical contexts
- Intelligent voice switching based on content
- Dynamic speed profiles for optimal comprehension
- Natural professor commentary generation
- Phrase variation for human-like speech
"""

import re
import random
import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from collections import defaultdict, deque
import json
from pathlib import Path
import time

# Configure module logger
logger = logging.getLogger(__name__)

# ===========================
# Voice Role Definitions
# ===========================

class VoiceRole(Enum):
    """Voice roles for different mathematical contexts"""
    NARRATOR = "en-US-AriaNeural"          # Default narration
    DEFINITION = "en-US-JennyNeural"        # Slower, ultra-clear for definitions  
    THEOREM = "en-US-ChristopherNeural"     # Authoritative for theorems/lemmas
    PROOF = "en-US-EricNeural"              # Methodical for proofs
    EXAMPLE = "en-US-GuyNeural"             # Conversational for examples
    EMPHASIS = "en-US-MichelleNeural"       # For critical insights
    WARNING = "en-US-AndrewNeural"          # For common pitfalls

@dataclass
class VoiceSettings:
    """Settings for a specific voice configuration"""
    role: VoiceRole
    rate: str = "0%"
    pitch: str = "0Hz"
    volume: str = "100%"
    emphasis_level: float = 1.0

@dataclass
class SpeechSegment:
    """A segment of speech with voice and timing information"""
    text: str
    voice_role: VoiceRole
    rate_modifier: str = "0%"
    pause_before: float = 0.0
    pause_after: float = 0.0
    add_commentary: Optional[str] = None
    emphasis: bool = False

# ===========================
# Speed Control System
# ===========================

class SpeedProfile(Enum):
    """Speed profiles for different content types"""
    DEFINITION = "definition"
    THEOREM_STATEMENT = "theorem_statement"
    PROOF_START = "proof_start"
    PROOF_MIDDLE = "proof_middle"
    PROOF_END = "proof_end"
    EXAMPLE = "example"
    ROUTINE_CALCULATION = "routine_calculation"
    COMPLEX_FORMULA = "complex_formula"
    SIMPLE_FORMULA = "simple_formula"
    KEY_INSIGHT = "key_insight"
    WARNING = "warning"
    NORMAL = "normal"

# Speed modifiers for each profile (negative = slower, positive = faster)
SPEED_PROFILES: Dict[SpeedProfile, str] = {
    SpeedProfile.DEFINITION: "-20%",           # Very slow and clear
    SpeedProfile.THEOREM_STATEMENT: "-15%",    # Deliberate
    SpeedProfile.PROOF_START: "-10%",          # Careful
    SpeedProfile.PROOF_MIDDLE: "0%",           # Normal
    SpeedProfile.PROOF_END: "-5%",             # Slightly slow for emphasis
    SpeedProfile.EXAMPLE: "+10%",              # Slightly faster
    SpeedProfile.ROUTINE_CALCULATION: "+15%",  # Quick
    SpeedProfile.COMPLEX_FORMULA: "-25%",      # Very slow
    SpeedProfile.SIMPLE_FORMULA: "+5%",        # Slightly quick
    SpeedProfile.KEY_INSIGHT: "-30%",          # Maximum emphasis
    SpeedProfile.WARNING: "-15%",              # Clear warning
    SpeedProfile.NORMAL: "0%",                 # Default
}

# ===========================
# Professor Commentary System
# ===========================

class ProfessorCommentary:
    """Generates natural professor-style commentary"""
    
    def __init__(self):
        self.commentary_phrases = {
            'before_definition': [
                "Let's carefully define",
                "We need to precisely understand",
                "Pay attention to this definition of",
                "Now, we define",
                "Let me introduce the concept of",
                "It's important to understand what we mean by",
                "Here's a fundamental definition:",
            ],
            'before_theorem': [
                "Here's a fundamental result",
                "This theorem is crucial",
                "Let me state an important theorem",
                "We have the following key result",
                "This is a central theorem",
                "Now for a significant result",
                "The following theorem is essential",
            ],
            'after_theorem_name': [
                "which states that",
                "tells us that",
                "says that",
                "asserts that",
                "establishes that",
            ],
            'complex_expression': [
                "Let me break this down",
                "This looks complicated, but",
                "Step by step, this says",
                "Let's unpack this carefully",
                "Don't be intimidated, this just means",
                "Breaking this apart,",
                "Let's read this piece by piece:",
            ],
            'before_proof': [
                "Let's prove this",
                "Here's the proof",
                "We'll now show this is true",
                "Let me demonstrate why this holds",
                "The proof proceeds as follows",
                "To see why this is true,",
                "We'll establish this by",
            ],
            'proof_technique': {
                'induction': "We'll use induction",
                'contradiction': "We'll prove this by contradiction",
                'contrapositive': "We'll use the contrapositive",
                'direct': "We'll give a direct proof",
                'construction': "We'll prove this constructively",
                'cases': "We'll consider different cases",
            },
            'after_proof': [
                "So what we've shown is",
                "The key takeaway is",
                "This completes our proof that",
                "We've thus established that",
                "In summary, we've proven",
                "The essential point is that",
                "This demonstrates that",
            ],
            'common_confusion': [
                "Students often confuse this with",
                "Be careful not to mix this up with",
                "A common mistake here is thinking",
                "Don't confuse this with",
                "It's easy to mistakenly think",
                "A frequent error is assuming",
            ],
            'key_step': [
                "This is the crucial step",
                "Here's where the magic happens",
                "Pay special attention to",
                "The key observation is",
                "This is the heart of the argument",
                "Notice carefully that",
                "The critical point is",
            ],
            'example_intro': [
                "Let's see an example",
                "For instance",
                "To illustrate",
                "Here's a concrete example",
                "Let me show you what this means",
                "Consider, for example",
                "As an illustration",
            ],
            'insight': [
                "The intuition here is",
                "What's really going on is",
                "The key insight is",
                "Think of it this way:",
                "The underlying idea is",
                "Essentially,",
                "At its core,",
            ],
            'transition': [
                "Now,",
                "Next,",
                "Moving on,",
                "With this in mind,",
                "Building on this,",
                "From here,",
                "Consequently,",
            ]
        }
        
        # Track recently used phrases to avoid repetition
        self.recent_phrases: Dict[str, deque] = defaultdict(lambda: deque(maxlen=3))
        
    def get_commentary(self, context: str, specific_type: Optional[str] = None) -> str:
        """Get appropriate commentary for the context"""
        if specific_type and specific_type in self.commentary_phrases.get(context, {}):
            return self.commentary_phrases[context][specific_type]
        
        if context not in self.commentary_phrases:
            return ""
        
        phrases = self.commentary_phrases[context]
        if isinstance(phrases, list):
            # Avoid recently used phrases
            available = [p for p in phrases if p not in self.recent_phrases[context]]
            if not available:
                available = phrases
                self.recent_phrases[context].clear()
            
            chosen = random.choice(available)
            self.recent_phrases[context].append(chosen)
            return chosen
        
        return ""

# ===========================
# Voice Switching Rules
# ===========================

class VoiceSwitchingRules:
    """Manages intelligent voice switching based on content"""
    
    def __init__(self):
        self.switching_patterns = [
            # Definitions
            (r'(?:Definition|Def\.|Define)[\s:.]', VoiceRole.DEFINITION, SpeedProfile.DEFINITION),
            (r'We define|Let us define', VoiceRole.DEFINITION, SpeedProfile.DEFINITION),
            (r'is defined as|is called', VoiceRole.DEFINITION, SpeedProfile.DEFINITION),
            
            # Theorems and results
            (r'(?:Theorem|Lemma|Proposition|Corollary)\s*(?:\d+\.?\d*)?[\s:.]', 
             VoiceRole.THEOREM, SpeedProfile.THEOREM_STATEMENT),
            (r'Main (?:Theorem|Result)', VoiceRole.THEOREM, SpeedProfile.THEOREM_STATEMENT),
            
            # Proofs
            (r'(?:Proof|Pf)[\s:.]', VoiceRole.PROOF, SpeedProfile.PROOF_START),
            (r'We (?:prove|show) that', VoiceRole.PROOF, SpeedProfile.PROOF_START),
            (r'(?:Q\.E\.D\.|∎|□)', VoiceRole.PROOF, SpeedProfile.PROOF_END),
            
            # Examples
            (r'(?:Example|Ex\.|For instance|e\.g\.)[\s:.]', VoiceRole.EXAMPLE, SpeedProfile.EXAMPLE),
            (r'Consider the following example', VoiceRole.EXAMPLE, SpeedProfile.EXAMPLE),
            
            # Emphasis and insights
            (r'(?:Note that|Observe|Notice|The key is)', VoiceRole.EMPHASIS, SpeedProfile.KEY_INSIGHT),
            (r'(?:Important|Crucial|Essential|Fundamental):', VoiceRole.EMPHASIS, SpeedProfile.KEY_INSIGHT),
            (r'UNIQUE|ONLY|MUST|ALWAYS|NEVER', VoiceRole.EMPHASIS, SpeedProfile.KEY_INSIGHT),
            
            # Warnings
            (r'(?:Warning|Caution|Be careful|Don\'t confuse)', VoiceRole.WARNING, SpeedProfile.WARNING),
            (r'(?:Common mistake|Pitfall|Error)', VoiceRole.WARNING, SpeedProfile.WARNING),
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), voice, speed) 
            for pattern, voice, speed in self.switching_patterns
        ]
    
    def determine_voice_and_speed(self, text: str, current_context: Dict[str, Any]) -> Tuple[VoiceRole, SpeedProfile]:
        """Determine appropriate voice and speed for text segment"""
        # Check patterns
        for pattern, voice, speed in self.compiled_patterns:
            if pattern.search(text):
                return voice, speed
        
        # Context-based defaults
        if current_context.get('in_proof'):
            return VoiceRole.PROOF, SpeedProfile.PROOF_MIDDLE
        elif current_context.get('in_definition'):
            return VoiceRole.DEFINITION, SpeedProfile.DEFINITION
        elif current_context.get('in_example'):
            return VoiceRole.EXAMPLE, SpeedProfile.EXAMPLE
        
        # Default
        return VoiceRole.NARRATOR, SpeedProfile.NORMAL

# ===========================
# Main Voice Manager
# ===========================

class VoiceManager:
    """Manages voice selection, speed control, and commentary injection"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.commentary_generator = ProfessorCommentary()
        self.switching_rules = VoiceSwitchingRules()
        self.current_context = {
            'in_proof': False,
            'in_definition': False,
            'in_example': False,
            'in_theorem': False,
            'theorem_name': None,
            'proof_depth': 0,
            'complexity_score': 0,
        }
        
        # Performance tracking
        self.performance_stats = {
            'voice_switches': 0,
            'commentary_added': 0,
            'processing_time': 0,
        }
        
        # Load configuration if provided
        self.config = self._load_config(config_path) if config_path else {}
        
        # Initialize voice settings cache
        self._voice_cache: Dict[VoiceRole, VoiceSettings] = {
            role: VoiceSettings(role=role) for role in VoiceRole
        }
        
        logger.info("VoiceManager initialized")
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load voice config: {e}")
            return {}
    
    def update_context(self, text: str) -> None:
        """Update current mathematical context based on text"""
        # Update proof context
        if re.search(r'\\begin{proof}|(?:Proof|Pf)[\s:.]', text, re.IGNORECASE):
            self.current_context['in_proof'] = True
            self.current_context['proof_depth'] += 1
        elif re.search(r'\\end{proof}|(?:Q\.E\.D\.|∎|□)', text):
            self.current_context['in_proof'] = False
            self.current_context['proof_depth'] = max(0, self.current_context['proof_depth'] - 1)
        
        # Update definition context
        if re.search(r'\\begin{definition}|Definition[\s:.]', text, re.IGNORECASE):
            self.current_context['in_definition'] = True
        elif re.search(r'\\end{definition}', text):
            self.current_context['in_definition'] = False
        
        # Update theorem context
        theorem_match = re.search(r'(Theorem|Lemma|Proposition|Corollary)\s*(\d+\.?\d*)?', text, re.IGNORECASE)
        if theorem_match:
            self.current_context['in_theorem'] = True
            self.current_context['theorem_name'] = theorem_match.group(0)
        
        # Estimate complexity
        self.current_context['complexity_score'] = self._estimate_complexity(text)
    
    def _estimate_complexity(self, text: str) -> float:
        """Estimate mathematical complexity of text"""
        score = 0.0
        
        # Complex patterns add to score
        complexity_indicators = [
            (r'\\int.*\\int', 2.0),  # Multiple integrals
            (r'\\sum.*\\sum', 1.5),  # Nested sums
            (r'\\frac{.*\\frac{.*}{.*}.*}', 2.5),  # Nested fractions
            (r'\\lim.*\\lim', 1.5),  # Multiple limits
            (r'\\partial.*\\partial', 1.5),  # Partial derivatives
            (r'\|.*\|_.*\|.*\|', 2.0),  # Nested norms
            (r'\\forall.*\\exists', 1.0),  # Quantifiers
            (r'\\begin{cases}', 1.5),  # Case structures
        ]
        
        for pattern, weight in complexity_indicators:
            if re.search(pattern, text):
                score += weight
        
        # Length factor
        score += len(text) / 1000.0
        
        return min(score, 10.0)  # Cap at 10
    
    def process_text(self, text: str, sentences: List[str]) -> List[SpeechSegment]:
        """Process text and create speech segments with appropriate voices"""
        start_time = time.time()
        segments = []
        
        for i, sentence in enumerate(sentences):
            # Update context
            self.update_context(sentence)
            
            # Determine voice and speed
            voice_role, speed_profile = self.switching_rules.determine_voice_and_speed(
                sentence, self.current_context
            )
            
            # Check if we need commentary
            commentary = self._get_appropriate_commentary(sentence, i == 0)
            
            # Create segment
            segment = SpeechSegment(
                text=sentence,
                voice_role=voice_role,
                rate_modifier=SPEED_PROFILES[speed_profile],
                pause_before=self._calculate_pause_before(sentence, i),
                pause_after=self._calculate_pause_after(sentence),
                add_commentary=commentary,
                emphasis=self._should_emphasize(sentence)
            )
            
            # Add commentary segment if needed
            if commentary:
                commentary_segment = SpeechSegment(
                    text=commentary,
                    voice_role=voice_role,
                    rate_modifier=SPEED_PROFILES[SpeedProfile.NORMAL],
                    pause_after=0.3
                )
                segments.append(commentary_segment)
                self.performance_stats['commentary_added'] += 1
            
            segments.append(segment)
            
            # Track voice switches
            if i > 0 and segments[-2].voice_role != voice_role:
                self.performance_stats['voice_switches'] += 1
        
        self.performance_stats['processing_time'] = time.time() - start_time
        return segments
    
    def _get_appropriate_commentary(self, sentence: str, is_first: bool) -> Optional[str]:
        """Determine if commentary should be added"""
        # Definition start
        if re.search(r'Definition[\s:.]', sentence, re.IGNORECASE) and is_first:
            return self.commentary_generator.get_commentary('before_definition')
        
        # Theorem start
        if re.search(r'(Theorem|Lemma|Proposition)\s*\d*[\s:.]', sentence, re.IGNORECASE):
            return self.commentary_generator.get_commentary('before_theorem')
        
        # Complex expression
        if self.current_context['complexity_score'] > 5:
            if random.random() < 0.3:  # 30% chance for complex expressions
                return self.commentary_generator.get_commentary('complex_expression')
        
        # Proof start
        if re.search(r'Proof[\s:.]', sentence, re.IGNORECASE):
            # Check for proof technique
            if 'induction' in sentence.lower():
                return self.commentary_generator.get_commentary('proof_technique', 'induction')
            elif 'contradiction' in sentence.lower():
                return self.commentary_generator.get_commentary('proof_technique', 'contradiction')
            else:
                return self.commentary_generator.get_commentary('before_proof')
        
        # Key insights
        if re.search(r'key|crucial|important|observe|notice', sentence, re.IGNORECASE):
            if random.random() < 0.5:
                return self.commentary_generator.get_commentary('key_step')
        
        return None
    
    def _calculate_pause_before(self, sentence: str, index: int) -> float:
        """Calculate pause duration before sentence"""
        if index == 0:
            return 0.0
        
        # Longer pause before theorem/definition
        if re.search(r'(Theorem|Definition|Lemma)[\s:.]', sentence, re.IGNORECASE):
            return 0.7
        
        # Pause before proof
        if re.search(r'Proof[\s:.]', sentence, re.IGNORECASE):
            return 0.5
        
        # Standard sentence pause
        return 0.3
    
    def _calculate_pause_after(self, sentence: str) -> float:
        """Calculate pause duration after sentence"""
        # Long pause after theorem statement
        if self.current_context.get('in_theorem') and re.search(r'\.$', sentence):
            return 0.6
        
        # Pause after definition
        if self.current_context.get('in_definition') and re.search(r'\.$', sentence):
            return 0.8
        
        # Pause after proof end
        if re.search(r'(Q\.E\.D\.|∎|□)$', sentence):
            return 1.0
        
        # Standard
        return 0.4
    
    def _should_emphasize(self, sentence: str) -> bool:
        """Determine if sentence should be emphasized"""
        emphasis_patterns = [
            r'\b(UNIQUE|ONLY|MUST|ALWAYS|NEVER)\b',
            r'(crucial|essential|fundamental|important)',
            r'(key point|main result|central)',
        ]
        
        for pattern in emphasis_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                return True
        
        return False
    
    def get_voice_settings(self, role: VoiceRole) -> VoiceSettings:
        """Get voice settings for a role"""
        return self._voice_cache[role]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return self.performance_stats.copy()
    
    def reset_context(self) -> None:
        """Reset mathematical context"""
        self.current_context = {
            'in_proof': False,
            'in_definition': False,
            'in_example': False,
            'in_theorem': False,
            'theorem_name': None,
            'proof_depth': 0,
            'complexity_score': 0,
        }
        
    def combine_speech_segments(self, segments: List[SpeechSegment]) -> List[SpeechSegment]:
        """Optimize segments by combining where appropriate"""
        if not segments:
            return segments
        
        optimized = []
        current = segments[0]
        
        for next_segment in segments[1:]:
            # Combine if same voice and no pause between
            if (current.voice_role == next_segment.voice_role and 
                current.pause_after < 0.1 and 
                next_segment.pause_before < 0.1 and
                not next_segment.add_commentary):
                # Combine
                current.text += " " + next_segment.text
                current.pause_after = next_segment.pause_after
                current.emphasis = current.emphasis or next_segment.emphasis
            else:
                optimized.append(current)
                current = next_segment
        
        optimized.append(current)
        return optimized

# ===========================
# Testing and Validation
# ===========================

def _test_voice_manager():
    """Test voice manager functionality"""
    vm = VoiceManager()
    
    test_sentences = [
        "Definition 3.1. A topological space X is called compact if every open cover has a finite subcover.",
        "Theorem 5.2 (Heine-Borel). A subset of Euclidean space is compact if and only if it is closed and bounded.",
        "Proof. We first show the forward direction.",
        "Note that this is the crucial step in our argument.",
        "Example 2.1. Consider the interval [0,1] with the usual topology.",
        "Warning: Don't confuse compactness with connectedness.",
    ]
    
    segments = vm.process_text(" ".join(test_sentences), test_sentences)
    
    print("Voice Manager Test Results:")
    print(f"Total segments: {len(segments)}")
    print(f"Voice switches: {vm.performance_stats['voice_switches']}")
    print(f"Commentary added: {vm.performance_stats['commentary_added']}")
    
    for i, segment in enumerate(segments):
        print(f"\nSegment {i+1}:")
        print(f"  Voice: {segment.voice_role.name}")
        print(f"  Rate: {segment.rate_modifier}")
        print(f"  Text: {segment.text[:50]}...")
        if segment.add_commentary:
            print(f"  Commentary: {segment.add_commentary}")

if __name__ == "__main__":
    # Run tests if executed directly
    _test_voice_manager()