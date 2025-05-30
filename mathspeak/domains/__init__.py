"""
MathSpeak Domain Processors
==========================

Mathematical domain-specific processors that handle specialized notation
and pronunciation rules for different areas of mathematics.

Available domains:
- Topology: Point-set, algebraic, and differential topology
- Complex Analysis: Holomorphic functions, contour integration, residues
- Numerical Analysis: Error analysis, iterative methods, matrix computations
- (More domains to be implemented)
"""

from typing import List, Dict, Any, Optional

# Import all domain processors
from .topology import (
    TopologyProcessor,
    TopologyContext,
    TopologyVocabulary,
)

from .complex_analysis import (
    ComplexAnalysisProcessor,
    ComplexContext,
    ComplexAnalysisVocabulary,
)

from .numerical_analysis import (
    NumericalAnalysisProcessor,
    NumericalContext,
    NumericalAnalysisVocabulary,
)

# Import manifolds processor
from .manifolds import (
    ManifoldsProcessor,
    ManifoldsContext,
    ManifoldsVocabulary,
)

# Import ODE processor
from .ode import (
    ODEProcessor,
    ODEContext,
    ODEVocabulary,
)

# Import the new domain processors
from .real_analysis import RealAnalysisProcessor
from .measure_theory import MeasureTheoryProcessor
from .combinatorics import CombinatoricsProcessor
from .algorithms import AlgorithmsProcessor

# Domain registry for dynamic loading
DOMAIN_REGISTRY = {
    'topology': TopologyProcessor,
    'complex_analysis': ComplexAnalysisProcessor,
    'numerical_analysis': NumericalAnalysisProcessor,
    'manifolds': ManifoldsProcessor,
    'ode': ODEProcessor,
    'real_analysis': RealAnalysisProcessor,
    'measure_theory': MeasureTheoryProcessor,
    'combinatorics': CombinatoricsProcessor,
    'algorithms': AlgorithmsProcessor,
}

# Domain metadata
DOMAIN_INFO = {
    'topology': {
        'name': 'Topology',
        'description': 'Point-set, algebraic, and differential topology',
        'subcontexts': ['point_set', 'algebraic', 'differential', 'metric_spaces'],
        'priority': 1,
    },
    'complex_analysis': {
        'name': 'Complex Analysis',
        'description': 'Complex functions, integration, and residue theory',
        'subcontexts': ['basic_complex', 'holomorphic', 'integration', 'residues', 'conformal'],
        'priority': 1,
    },
    'numerical_analysis': {
        'name': 'Numerical Analysis',
        'description': 'Computational methods and error analysis',
        'subcontexts': ['error_analysis', 'iterative_methods', 'matrix_computations', 'interpolation'],
        'priority': 2,
    },
    'manifolds': {
        'name': 'Differential Geometry',
        'description': 'Manifolds, connections, and curvature',
        'subcontexts': ['charts', 'tangent_bundles', 'differential_forms', 'connections'],
        'priority': 3,
    },
    'ode': {
        'name': 'Ordinary Differential Equations',
        'description': 'ODEs, systems, and qualitative analysis',
        'subcontexts': ['basic_ode', 'systems', 'stability', 'phase_portraits'],
        'priority': 3,
    },
    'real_analysis': {
        'name': 'Real Analysis',
        'description': 'Limits, continuity, measure theory connections',
        'subcontexts': ['limits', 'continuity', 'differentiation', 'integration', 'sequences', 'series', 'function_spaces'],
        'priority': 1,
        'status': 'active',
    },
    'measure_theory': {
        'name': 'Measure Theory',
        'description': 'Measures, integration, and Lp spaces',
        'subcontexts': ['sigma_algebras', 'measures', 'integration', 'lp_spaces', 'convergence', 'radon_nikodym'],
        'priority': 2,
        'status': 'active',
    },
    'combinatorics': {
        'name': 'Combinatorics',
        'description': 'Counting, graphs, and generating functions',
        'subcontexts': ['counting', 'graph_theory', 'generating_functions', 'partitions', 'trees', 'posets'],
        'priority': 3,
        'status': 'active',
    },
    'algorithms': {
        'name': 'Computer Science Algorithms',
        'description': 'Algorithm notation and complexity',
        'subcontexts': ['complexity', 'algorithm_notation', 'data_structures', 'graph_algorithms', 'machine_learning', 'optimization'],
        'priority': 3,
        'status': 'active',
    },
}

def get_available_domains() -> List[str]:
    """Get list of available (implemented) domain processors"""
    return list(DOMAIN_REGISTRY.keys())

def get_all_domains() -> List[str]:
    """Get list of all domains (including planned)"""
    return list(DOMAIN_INFO.keys())

def get_domain_info(domain: str) -> Optional[Dict[str, Any]]:
    """Get information about a specific domain"""
    return DOMAIN_INFO.get(domain)

def create_domain_processor(domain: str):
    """Create a domain processor by name"""
    if domain not in DOMAIN_REGISTRY:
        raise ValueError(f"Unknown or unimplemented domain: {domain}")
    
    processor_class = DOMAIN_REGISTRY[domain]
    return processor_class()

def is_domain_available(domain: str) -> bool:
    """Check if a domain processor is available"""
    return domain in DOMAIN_REGISTRY

# Export all
__all__ = [
    # Processors
    'TopologyProcessor',
    'ComplexAnalysisProcessor',
    'NumericalAnalysisProcessor',
    'ManifoldsProcessor',
    'ODEProcessor',
    'RealAnalysisProcessor',
    'MeasureTheoryProcessor',
    'CombinatoricsProcessor',
    'AlgorithmsProcessor',
    
    # Context enums
    'TopologyContext',
    'ComplexContext',
    'NumericalContext',
    'ManifoldsContext',
    'ODEContext',
    
    # Vocabularies (for advanced users)
    'TopologyVocabulary',
    'ComplexAnalysisVocabulary',
    'NumericalAnalysisVocabulary',
    'ManifoldsVocabulary',
    'ODEVocabulary',
    
    # Registry and info
    'DOMAIN_REGISTRY',
    'DOMAIN_INFO',
    
    # Utility functions
    'get_available_domains',
    'get_all_domains',
    'get_domain_info',
    'create_domain_processor',
    'is_domain_available',
]

# Type imports
from typing import List, Dict, Any, Optional, Optional

import logging
logger = logging.getLogger(__name__)