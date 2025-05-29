#!/usr/bin/env python3
"""
Input Validation Utilities
=========================

Provides validation functions for mathematical expressions and system inputs.
"""

import re
from typing import Optional, Tuple


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


def validate_latex_expression(expression: str, max_length: int = 10000) -> Tuple[bool, Optional[str]]:
    """
    Validate a LaTeX expression for safety and correctness.
    
    Args:
        expression: The LaTeX expression to validate
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not expression:
        return True, None  # Empty is valid
        
    if len(expression) > max_length:
        return False, f"Expression too long ({len(expression)} > {max_length} characters)"
    
    # Check for potentially malicious patterns
    dangerous_patterns = [
        r'\\input\{',
        r'\\include\{',
        r'\\write',
        r'\\immediate',
        r'\\openout',
        r'\\closeout',
        r'\\read',
        r'\\newwrite',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, expression, re.IGNORECASE):
            return False, f"Potentially dangerous LaTeX command detected: {pattern}"
    
    # Check for balanced braces
    brace_count = 0
    for char in expression:
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        if brace_count < 0:
            return False, "Unbalanced braces in expression"
    
    if brace_count != 0:
        return False, "Unbalanced braces in expression"
    
    # Check for valid characters (allow most unicode for international math)
    if re.search(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', expression):
        return False, "Expression contains invalid control characters"
    
    return True, None


def validate_file_path(path: str, must_exist: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate a file path for safety.
    
    Args:
        path: The file path to validate
        must_exist: Whether the file must already exist
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path:
        return False, "Path cannot be empty"
    
    # Check for path traversal attempts
    if '..' in path or path.startswith('/etc') or path.startswith('/sys'):
        return False, "Invalid path: potential security risk"
    
    # Check for null bytes
    if '\x00' in path:
        return False, "Path contains null bytes"
    
    # Limit path length
    if len(path) > 4096:  # Common filesystem limit
        return False, "Path too long"
    
    if must_exist:
        from pathlib import Path
        if not Path(path).exists():
            return False, f"File does not exist: {path}"
    
    return True, None


def sanitize_output_filename(filename: str) -> str:
    """
    Sanitize a filename for safe output.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    import os
    filename = os.path.basename(filename)
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s.-]', '_', filename)
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]
    filename = name + ext
    
    # Ensure it has an extension
    if not ext:
        filename += '.mp3'
    
    return filename


def validate_voice_speed(speed: float) -> Tuple[bool, Optional[str]]:
    """
    Validate voice speed parameter.
    
    Args:
        speed: The speed multiplier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(speed, (int, float)):
        return False, "Speed must be a number"
    
    if speed < 0.5 or speed > 2.0:
        return False, "Speed must be between 0.5 and 2.0"
    
    return True, None


def validate_domain_name(domain: str, valid_domains: list) -> Tuple[bool, Optional[str]]:
    """
    Validate a mathematical domain name.
    
    Args:
        domain: The domain name to validate
        valid_domains: List of valid domain names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not domain:
        return False, "Domain name cannot be empty"
    
    if domain not in valid_domains:
        return False, f"Invalid domain: {domain}. Valid domains: {', '.join(valid_domains)}"
    
    return True, None