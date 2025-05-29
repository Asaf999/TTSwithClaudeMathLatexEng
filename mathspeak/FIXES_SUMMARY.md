# Domain Processor Fixes Summary

## Issues Fixed

### 1. Complex Analysis (complex_analysis.py)
- Added `_escape_for_both_backslashes` method to handle both single and double backslash LaTeX commands
- Updated `_compile_patterns` to use the escape method for patterns containing LaTeX commands
- This allows patterns like `\\mathbb{C}` to match both `\mathbb{C}` and `\\mathbb{C}` input

### 2. Topology (topology.py)
- Added the same `_escape_for_both_backslashes` method
- Updated `_compile_patterns` to use flexible pattern matching for LaTeX commands
- Fixed vocabulary pattern matching for topology-specific notation

### 3. Numerical Analysis (numerical_analysis.py)
- Added the same `_escape_for_both_backslashes` method
- Fixed regex patterns with pipe characters (`|`) by properly escaping them:
  - Changed `r'\\|e\\|'` to `r'\\\|e\\\|'` to match literal pipes
  - Fixed all norm patterns that were matching every character due to unescaped pipes
- Added missing vocabulary entries:
  - `\\mathcal{O}(h^2)` → "order h squared"
  - `\\nabla^2 u` → "the Laplacian of u"
  - Other Big-O notation variants

## Key Technical Changes

### Pattern Escaping
The `_escape_for_both_backslashes` method converts LaTeX command patterns to match both single and double backslash versions:
```python
def _escape_for_both_backslashes(self, pattern: str) -> str:
    # Converts \\command to match both \command and \\command
    # Uses regex pattern (?:\\\\|\\)command
```

### Pipe Character Escaping
Fixed patterns containing `|` (norm notation) by properly escaping:
- Before: `r'\\|e\\|'` (matches empty strings due to OR operator)
- After: `r'\\\|e\\\|'` (matches literal pipe characters)

## Result
All domain processors now correctly apply vocabulary transformations instead of passing through raw LaTeX.