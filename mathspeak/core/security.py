#!/usr/bin/env python3
"""
LaTeX Security Validator
========================

Validates and sanitizes LaTeX input to prevent:
- Denial of Service attacks through resource exhaustion
- Exponential expansion bombs
- Dangerous file I/O operations
- Excessive memory usage
"""

import re
import signal
import time
import logging
from typing import Tuple, List, Optional, Set
from contextlib import contextmanager
from dataclasses import dataclass
import threading

logger = logging.getLogger(__name__)


@dataclass
class SecurityConfig:
    """Security configuration parameters"""
    max_length: int = 50000
    max_depth: int = 20
    max_expansions: int = 1000
    max_processing_time: float = 5.0
    max_fractions: int = 50
    max_subscripts: int = 100
    max_repetitions: int = 5
    

class SecurityViolation(ValueError):
    """Raised when LaTeX input violates security constraints"""
    pass


class LaTeXSecurityValidator:
    """Validate and sanitize LaTeX input for security"""
    
    # Dangerous commands that could cause issues
    DANGEROUS_COMMANDS = [
        r'\\input', r'\\include', r'\\write', r'\\read',
        r'\\immediate', r'\\openout', r'\\closeout',
        r'\\newcommand', r'\\def', r'\\let', r'\\gdef',
        r'\\catcode', r'\\makeatletter', r'\\csname',
        r'\\expandafter', r'\\noexpand', r'\\special',
        r'\\shipout', r'\\output', r'\\everyjob'
    ]
    
    # Patterns that could cause expansion bombs
    EXPANSION_PATTERNS = [
        r'\\def.*\\def',  # Nested definitions
        r'\\newcommand.*\\newcommand',  # Nested commands
        r'(\^|_){.*(\^|_){.*(\^|_)',  # Deeply nested sub/superscripts
        r'\\frac{.*\\frac{.*\\frac{.*\\frac',  # Deeply nested fractions
    ]
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or SecurityConfig()
        self.expansion_count = 0
        self._processing_start_time = None
        
    def validate(self, latex_input: str) -> Tuple[bool, str]:
        """
        Validate LaTeX input for security issues
        
        Returns:
            (is_safe, error_message)
        """
        try:
            # Reset counters
            self.expansion_count = 0
            self._processing_start_time = time.time()
            
            # Check length
            if len(latex_input) > self.config.max_length:
                return False, f"Input too long ({len(latex_input)} > {self.config.max_length} characters)"
            
            # Check for dangerous commands
            for cmd in self.DANGEROUS_COMMANDS:
                if re.search(cmd, latex_input, re.IGNORECASE):
                    return False, f"Dangerous command detected: {cmd}"
            
            # Check for empty input
            if not latex_input.strip():
                return False, "Empty input"
            
            # Check nesting depth
            depth = self._check_nesting_depth(latex_input)
            if depth > self.config.max_depth:
                return False, f"Expression too deeply nested ({depth} > {self.config.max_depth})"
            
            # Check for expansion bombs
            if self._has_expansion_bomb(latex_input):
                return False, "Potential expansion bomb detected"
            
            # Check for excessive repetitions
            if self._has_excessive_repetitions(latex_input):
                return False, "Excessive repetitions detected"
            
            # Check for malformed commands
            if self._has_malformed_commands(latex_input):
                return False, "Malformed LaTeX commands detected"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Security validation error: {e}")
            return False, f"Validation error: {str(e)}"
    
    def sanitize(self, latex_input: str) -> str:
        """Remove potentially dangerous constructs"""
        if not latex_input:
            return ""
        
        # Remove comments
        sanitized = re.sub(r'%.*$', '', latex_input, flags=re.MULTILINE)
        
        # Remove dangerous commands
        for cmd in self.DANGEROUS_COMMANDS:
            # Remove command with arguments
            sanitized = re.sub(cmd + r'\s*\{[^}]*\}', '', sanitized, flags=re.IGNORECASE)
            # Remove command without arguments
            sanitized = re.sub(cmd + r'(?=\s|$|\\\\)', '', sanitized, flags=re.IGNORECASE)
        
        # Limit consecutive operators
        sanitized = re.sub(r'(\^|_){3,}', r'\1\1', sanitized)
        
        # Remove multiple consecutive backslashes
        sanitized = re.sub(r'\\{3,}', r'\\\\', sanitized)
        
        # Remove control characters
        sanitized = ''.join(c for c in sanitized if ord(c) >= 32 or c in '\n\r\t')
        
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        return sanitized.strip()
    
    def _check_nesting_depth(self, latex_input: str) -> int:
        """Check maximum nesting depth of braces"""
        max_depth = 0
        current_depth = 0
        
        # Also track bracket and parenthesis depth
        bracket_depth = 0
        paren_depth = 0
        
        i = 0
        while i < len(latex_input):
            char = latex_input[i]
            
            # Skip escaped characters
            if i > 0 and latex_input[i-1] == '\\':
                i += 1
                continue
            
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth = max(0, current_depth - 1)
            elif char == '[':
                bracket_depth += 1
                max_depth = max(max_depth, bracket_depth)
            elif char == ']':
                bracket_depth = max(0, bracket_depth - 1)
            elif char == '(':
                paren_depth += 1
                max_depth = max(max_depth, paren_depth)
            elif char == ')':
                paren_depth = max(0, paren_depth - 1)
            
            i += 1
        
        return max_depth
    
    def _has_expansion_bomb(self, latex_input: str) -> bool:
        """Check for patterns that could cause exponential expansion"""
        # Check for expansion patterns
        for pattern in self.EXPANSION_PATTERNS:
            if re.search(pattern, latex_input, re.IGNORECASE):
                return True
        
        # Check for deeply nested fractions
        frac_count = latex_input.count(r'\frac')
        if frac_count > self.config.max_fractions:
            return True
        
        # Check for nested fractions in a single expression
        if frac_count > 3:
            # Check if fractions are nested by looking at brace depth
            i = 0
            depth = 0
            frac_depths = []
            
            while i < len(latex_input):
                if latex_input[i:i+5] == r'\frac':
                    frac_depths.append(depth)
                    i += 5
                elif latex_input[i] == '{':
                    depth += 1
                    i += 1
                elif latex_input[i] == '}':
                    depth = max(0, depth - 1)
                    i += 1
                else:
                    i += 1
            
            # Check if we have nested fractions
            for j in range(1, len(frac_depths)):
                if frac_depths[j] > frac_depths[j-1]:
                    return True
        
        # Check for excessive subscripts/superscripts
        sub_super_count = latex_input.count('^') + latex_input.count('_')
        if sub_super_count > self.config.max_subscripts:
            return True
        
        # Check for potential infinite loops
        if re.search(r'\\(expandafter|csname|endcsname){3,}', latex_input):
            return True
        
        return False
    
    def _has_excessive_repetitions(self, latex_input: str) -> bool:
        """Check for excessive repetitions that might indicate an attack"""
        # Check for repeated characters
        if re.search(r'(.)\1{50,}', latex_input):
            return True
        
        # Check for repeated commands
        if re.search(r'(\\[a-zA-Z]+\s*){10,}', latex_input):
            return True
        
        # Check for repeated groups
        if re.search(r'(\{[^}]*\}){20,}', latex_input):
            return True
        
        return False
    
    def _has_malformed_commands(self, latex_input: str) -> bool:
        """Check for malformed LaTeX that might exploit parser bugs"""
        # Check for unmatched braces
        open_braces = latex_input.count('{') - latex_input.count(r'\{')
        close_braces = latex_input.count('}') - latex_input.count(r'\}')
        if abs(open_braces - close_braces) > 5:
            return True
        
        # Check for commands without proper spacing
        if re.search(r'\\[a-zA-Z]+[0-9]{5,}', latex_input):
            return True
        
        # Check for suspicious Unicode
        suspicious_chars = 0
        for char in latex_input:
            if ord(char) > 127 and ord(char) not in range(0x0391, 0x03C9):  # Not Greek
                suspicious_chars += 1
        if suspicious_chars > 10:
            return True
        
        return False
    
    @contextmanager
    def time_limit(self, seconds: float):
        """Context manager to limit execution time"""
        def signal_handler(signum, frame):
            raise TimeoutError("Processing time limit exceeded")
        
        # Set signal alarm
        old_handler = signal.signal(signal.SIGALRM, signal_handler)
        signal.setitimer(signal.ITIMER_REAL, seconds)
        
        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)
    
    def validate_and_sanitize(self, latex_input: str) -> str:
        """Validate and sanitize in one step, raising exception if invalid"""
        is_safe, error_msg = self.validate(latex_input)
        if not is_safe:
            raise SecurityViolation(error_msg)
        
        return self.sanitize(latex_input)


class RateLimiter:
    """Rate limiter for API protection"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
        self.lock = threading.Lock()
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        with self.lock:
            now = time.time()
            
            # Clean old entries
            cutoff = now - self.window_seconds
            self.requests = {
                cid: times for cid, times in self.requests.items()
                if times and times[-1] > cutoff
            }
            
            # Get client requests
            client_requests = self.requests.get(client_id, [])
            client_requests = [t for t in client_requests if t > cutoff]
            
            # Check limit
            if len(client_requests) >= self.max_requests:
                return False
            
            # Add request
            client_requests.append(now)
            self.requests[client_id] = client_requests
            
            return True
    
    def get_reset_time(self, client_id: str) -> Optional[float]:
        """Get time until rate limit resets"""
        with self.lock:
            client_requests = self.requests.get(client_id, [])
            if not client_requests:
                return None
            
            oldest = min(client_requests)
            return oldest + self.window_seconds


# Convenience functions
def validate_latex(latex_input: str, config: Optional[SecurityConfig] = None) -> Tuple[bool, str]:
    """Validate LaTeX input for security issues"""
    validator = LaTeXSecurityValidator(config)
    return validator.validate(latex_input)


def sanitize_latex(latex_input: str, config: Optional[SecurityConfig] = None) -> str:
    """Sanitize LaTeX input by removing dangerous constructs"""
    validator = LaTeXSecurityValidator(config)
    return validator.sanitize(latex_input)


def secure_latex(latex_input: str, config: Optional[SecurityConfig] = None) -> str:
    """Validate and sanitize LaTeX input, raising exception if invalid"""
    validator = LaTeXSecurityValidator(config)
    return validator.validate_and_sanitize(latex_input)