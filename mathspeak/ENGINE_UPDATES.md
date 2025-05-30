# Mathematical TTS Engine Updates

## Overview
The MathematicalTTSEngine in `core/engine.py` has been updated with several new features and improvements for better performance, reliability, and user experience.

## Key Updates

### 1. **LRU Cache System** (`utils/cache.py`)
- Replaced simple dictionary cache with advanced LRU (Least Recently Used) cache
- Features:
  - Thread-safe operations
  - Memory-aware eviction (configurable max memory)
  - Persistent storage (saves/loads from disk)
  - Detailed statistics tracking
  - Computation time tracking for cache effectiveness
- Benefits:
  - Better memory management
  - Faster repeated processing
  - Cache persistence across sessions

### 2. **Timeout Protection** (`utils/timeout.py`)
- Added timeout decorators and utilities
- Dynamic timeout calculation based on expression length
- Operation-specific timeouts:
  - Parsing: 5 seconds base
  - Processing: 10 seconds base
  - Domain processing: 5 seconds base
  - TTS generation: 30 seconds base
- Graceful handling of timeout errors with informative messages

### 3. **TTS Engine Manager** (`core/tts_engines.py`)
- Abstracted TTS functionality with multiple engine support:
  - Microsoft Edge TTS (online, high quality)
  - Google TTS (online)
  - Pyttsx3 (offline)
  - Espeak (offline, Linux/Mac)
- Features:
  - Automatic fallback between engines
  - Online/offline preference configuration
  - Engine-specific voice and rate settings
  - Availability checking

### 4. **Progress Indicators** (`utils/progress.py`)
- Visual progress tracking for long operations
- Multiple indicator types:
  - Console progress bars with ETA
  - Spinner for indeterminate progress
  - Log-based progress for non-interactive environments
- Integrated into:
  - LaTeX processing (6 steps)
  - Speech generation (per segment)
  - Batch operations

### 5. **Improved Error Handling**
- Empty input validation with appropriate messages
- Better error messages based on error type:
  - Timeout errors
  - Unknown LaTeX commands
  - Processing failures
- Graceful degradation instead of crashes

### 6. **Enhanced Features Integration**

#### Cache Integration
```python
# Old: Simple dictionary cache
self.expression_cache: Dict[str, ProcessedExpression] = {}

# New: Advanced LRU cache with persistence
self.expression_cache = get_expression_cache()  # Singleton with disk persistence
```

#### Timeout Protection
```python
# Processing steps now wrapped with timeouts
@timeout(5.0)
def _detect_context_with_timeout(self, latex: str, ...):
    # Prevents hanging on complex expressions
```

#### Progress Tracking
```python
# Visual feedback for long operations
if show_progress and len(latex) > 100:
    progress = ProgressIndicator(total=6, description="Processing LaTeX")
    # Updates after each major step
```

## Usage Examples

### Basic Usage (unchanged)
```python
engine = MathematicalTTSEngine()
result = engine.process_latex(r"$x^2 + y^2 = z^2$")
```

### With New Features
```python
# Initialize with preferences
engine = MathematicalTTSEngine(
    enable_caching=True,
    prefer_offline_tts=False  # Use online engines for better quality
)

# Process with progress indicator
result = engine.process_latex(
    long_latex_expression,
    show_progress=True  # Shows progress bar
)

# Generate speech with specific engine
await engine.speak_expression(
    result,
    output_file="output.mp3",
    engine_name="Microsoft Edge TTS",
    show_progress=True
)

# Get detailed performance metrics
report = engine.get_performance_report()
# Includes cache stats, TTS engine availability, processing metrics
```

## Benefits

1. **Performance**: LRU cache dramatically speeds up repeated processing
2. **Reliability**: Timeouts prevent hanging on complex expressions
3. **Flexibility**: Multiple TTS engines with automatic fallback
4. **User Experience**: Progress indicators for long operations
5. **Debugging**: Better error messages and performance metrics
6. **Offline Support**: Can work without internet using offline TTS engines

## Migration Notes

- The API remains backward compatible
- Cache is now persistent (saved in `~/.mathspeak/cache/`)
- Unknown commands database location unchanged
- New optional parameters don't affect existing code

## Testing

Run the test script to verify all features:
```bash
python test_updated_engine.py
```

This will test:
- Empty input handling
- Progress indicators
- Cache functionality
- TTS engine availability
- Unknown command tracking
- Timeout handling
- Performance metrics