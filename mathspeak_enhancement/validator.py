"""
Improvement validator - verifies that improvements actually work
"""

import json
from pathlib import Path
from typing import Dict
import sys
sys.path.append('..')

from test_suite import NaturalnessTestSuite


class ImprovementValidator:
    """Validate that improvements work correctly"""
    
    def __init__(self, cycle: int):
        self.cycle = cycle
        
    def validate_cycle(self) -> Dict:
        """
        Validate improvements for a cycle
        Returns validation results with score
        """
        
        print(f"\n✅ Validating improvements for Cycle {self.cycle}...")
        
        # Re-run tests on updated codebase
        test_suite = NaturalnessTestSuite(self.cycle)
        results = test_suite.run_all_tests()
        
        # Check if we meet criteria
        overall_score = results['overall_score']
        target_score = 0.98
        
        validation_results = {
            'cycle': self.cycle,
            'score': overall_score,
            'passed': overall_score >= target_score,
            'improvement': self.calculate_improvement(overall_score),
            'remaining_gap': max(0, target_score - overall_score),
            'category_scores': {
                cat: data['average_score'] 
                for cat, data in results['categories'].items()
            }
        }
        
        # Save validation results
        validation_path = Path(f'results/cycle_{self.cycle}_validation.json')
        with open(validation_path, 'w') as f:
            json.dump(validation_results, f, indent=2)
            
        return validation_results
        
    def calculate_improvement(self, new_score: float) -> float:
        """Calculate improvement from previous cycle"""
        if self.cycle == 1:
            return new_score  # First cycle, no previous score
            
        # Load previous validation
        prev_path = Path(f'results/cycle_{self.cycle - 1}_validation.json')
        if prev_path.exists():
            with open(prev_path, 'r') as f:
                prev_results = json.load(f)
                prev_score = prev_results.get('score', 0)
                return new_score - prev_score
        else:
            return 0