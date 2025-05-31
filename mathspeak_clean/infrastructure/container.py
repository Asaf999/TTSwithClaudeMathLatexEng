"""Dependency injection container for MathSpeak."""

import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from mathspeak_clean.adapters.legacy_pattern_adapter import LegacyPatternAdapter
from mathspeak_clean.adapters.enhanced_pattern_adapter import EnhancedPatternAdapter
from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionUseCase,
)
from mathspeak_clean.domain.interfaces.pattern_repository import PatternRepository
from mathspeak_clean.domain.services.pattern_processor import PatternProcessorService
from mathspeak_clean.domain.services.enhanced_pattern_processor import EnhancedPatternProcessorService
from mathspeak_clean.infrastructure.config.settings import Settings, get_settings
from mathspeak_clean.infrastructure.logging.logger import get_logger
from mathspeak_clean.infrastructure.persistence.lru_cache import LRUCache
from mathspeak_clean.infrastructure.persistence.memory_pattern_repository import (
    MemoryPatternRepository,
)
from mathspeak_clean.shared.types import Cache

T = TypeVar("T")

logger = get_logger(__name__)


class Container:
    """Dependency injection container.
    
    This container manages the creation and lifecycle of application components,
    ensuring proper dependency injection and singleton management.
    """
    
    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Initialize container.
        
        Args:
            settings: Application settings (uses default if not provided)
        """
        self.settings = settings or get_settings()
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable[[], Any]] = {}
        
        # Register default factories
        self._register_defaults()
    
    def _register_defaults(self) -> None:
        """Register default component factories."""
        # Infrastructure
        self.register_factory(Settings, lambda: self.settings)
        self.register_factory(
            Cache,
            lambda: LRUCache(
                max_size=self.settings.cache_max_size,
                default_ttl=self.settings.cache_ttl,
            ),
        )
        
        # Domain
        self.register_factory(
            PatternRepository,
            self._create_pattern_repository,
        )
        
        # Use enhanced processor if enabled
        use_enhanced = getattr(self.settings, 'use_enhanced_processor', True)
        if use_enhanced:
            self.register_factory(
                PatternProcessorService,
                lambda: EnhancedPatternProcessorService(
                    pattern_repository=self.get(PatternRepository),
                    timeout=self.settings.pattern_timeout,
                ),
            )
        else:
            self.register_factory(
                PatternProcessorService,
                lambda: PatternProcessorService(
                    pattern_repository=self.get(PatternRepository),
                    timeout=self.settings.pattern_timeout,
                ),
            )
        
        # Application
        self.register_factory(
            ProcessExpressionUseCase,
            lambda: ProcessExpressionUseCase(
                pattern_processor=self.get(PatternProcessorService),
                cache=self.get(Cache) if self.settings.cache_enabled else None,
            ),
        )
        
        # Adapters
        self.register_factory(
            LegacyPatternAdapter,
            lambda: LegacyPatternAdapter(),
        )
        self.register_factory(
            EnhancedPatternAdapter,
            lambda: EnhancedPatternAdapter(),
        )
    
    def _create_pattern_repository(self) -> PatternRepository:
        """Create pattern repository based on configuration.
        
        Returns:
            Pattern repository instance
        """
        # For now, always use memory repository
        # In the future, this could check settings to determine
        # whether to use file-based or database repository
        repository = MemoryPatternRepository()
        
        # Load patterns based on configuration
        use_enhanced = getattr(self.settings, 'use_enhanced_processor', True)
        use_legacy = getattr(self.settings, 'use_legacy_patterns', not use_enhanced)
        
        # Try enhanced patterns first if enabled
        if use_enhanced:
            try:
                adapter = self.get(EnhancedPatternAdapter)
                adapter.initialize()
                
                # Copy patterns from enhanced adapter
                enhanced_repo = adapter.get_pattern_repository()
                for pattern in enhanced_repo.get_all():
                    try:
                        repository.add(pattern)
                    except ValueError:
                        # Pattern already exists
                        pass
                
                logger.info(
                    f"Loaded {repository.count()} enhanced patterns (98% natural speech)"
                )
                
            except Exception as e:
                logger.warning(f"Failed to load enhanced patterns: {e}")
                use_legacy = True  # Fall back to legacy
        
        # Load legacy patterns if needed
        if use_legacy:
            try:
                adapter = self.get(LegacyPatternAdapter)
                adapter.initialize()
                
                # Copy patterns from adapter
                legacy_repo = adapter.get_pattern_repository()
                for pattern in legacy_repo.get_all():
                    try:
                        repository.add(pattern)
                    except ValueError:
                        # Pattern already exists
                        pass
                
                logger.info(
                    f"Loaded {repository.count()} patterns from legacy adapter"
                )
                
            except Exception as e:
                logger.warning(f"Failed to load legacy patterns: {e}")
        
        return repository
    
    def register_factory(
        self,
        interface: Type[T],
        factory: Callable[[], T],
    ) -> None:
        """Register a factory for creating instances.
        
        Args:
            interface: Interface or class type
            factory: Factory function that creates instances
        """
        self._factories[interface] = factory
        logger.debug(f"Registered factory for {interface.__name__}")
    
    def register_singleton(
        self,
        interface: Type[T],
        instance: T,
    ) -> None:
        """Register a singleton instance.
        
        Args:
            interface: Interface or class type
            instance: Singleton instance
        """
        self._singletons[interface] = instance
        logger.debug(f"Registered singleton for {interface.__name__}")
    
    def get(self, interface: Type[T]) -> T:
        """Get an instance of the requested type.
        
        Args:
            interface: Interface or class type
            
        Returns:
            Instance of the requested type
            
        Raises:
            ValueError: If no factory or singleton registered
        """
        # Check singletons first
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check if we have a factory
        if interface not in self._factories:
            raise ValueError(
                f"No factory or singleton registered for {interface.__name__}"
            )
        
        # Create instance
        factory = self._factories[interface]
        instance = factory()
        
        # Store as singleton if it's a service
        if interface.__name__.endswith("Service") or interface.__name__.endswith("UseCase"):
            self._singletons[interface] = instance
            logger.debug(f"Created singleton for {interface.__name__}")
        
        return instance
    
    def create_scope(self) -> "Container":
        """Create a scoped container.
        
        Scoped containers share factories but have separate singletons.
        
        Returns:
            New scoped container
        """
        scoped = Container(self.settings)
        scoped._factories = self._factories.copy()
        return scoped
    
    def reset(self) -> None:
        """Reset the container, clearing all singletons."""
        self._singletons.clear()
        logger.debug("Container reset")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get container statistics.
        
        Returns:
            Dictionary with container stats
        """
        return {
            "factories_registered": len(self._factories),
            "singletons_created": len(self._singletons),
            "singleton_types": [
                cls.__name__ for cls in self._singletons.keys()
            ],
        }


# Global container instance
_container: Optional[Container] = None


def get_container() -> Container:
    """Get global container instance.
    
    Returns:
        Container instance
    """
    global _container
    
    if _container is None:
        _container = Container()
        logger.info("Global container initialized")
    
    return _container


def reset_container() -> None:
    """Reset global container (mainly for testing)."""
    global _container
    if _container:
        _container.reset()
    _container = None