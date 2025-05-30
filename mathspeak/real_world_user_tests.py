#!/usr/bin/env python3
"""
Real-World User Simulation Tests
================================

Simulates actual user behavior patterns and common use cases
"""

import asyncio
import time
import random
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

class UserSimulation:
    """Simulates different types of users"""
    
    def __init__(self, user_type: str, engine: MathematicalTTSEngine):
        self.user_type = user_type
        self.engine = engine
        self.actions = []
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    async def simulate(self) -> Dict[str, Any]:
        """Run user simulation"""
        self.start_time = datetime.now()
        
        if self.user_type == "student":
            await self._simulate_student()
        elif self.user_type == "professor":
            await self._simulate_professor()
        elif self.user_type == "researcher":
            await self._simulate_researcher()
        elif self.user_type == "casual":
            await self._simulate_casual_user()
        elif self.user_type == "power":
            await self._simulate_power_user()
        
        self.end_time = datetime.now()
        
        return self._generate_report()
    
    async def _simulate_student(self):
        """Simulate a student doing homework"""
        homework_problems = [
            # Calculus homework
            "Find the derivative of $f(x) = x^3 - 3x^2 + 2x - 1$",
            "$f'(x) = 3x^2 - 6x + 2$",
            "Evaluate $\\int_0^2 (x^2 + 1) dx$",
            "$\\int_0^2 (x^2 + 1) dx = \\left[\\frac{x^3}{3} + x\\right]_0^2 = \\frac{8}{3} + 2 = \\frac{14}{3}$",
            
            # Linear algebra
            "Find the determinant of $A = \\begin{pmatrix} 2 & 1 \\\\ 3 & 4 \\end{pmatrix}$",
            "$\\det(A) = 2 \\cdot 4 - 1 \\cdot 3 = 8 - 3 = 5$",
            
            # Make mistakes and corrections
            "$\\int x^2$ dx",  # Forgot bounds
            "$\\int x^2 dx = \\frac{x^3}{3} + C$",  # Correction
        ]
        
        for i, problem in enumerate(homework_problems):
            # Simulate thinking time
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # Extract math from problem
            import re
            math_parts = re.findall(r'\$[^$]+\$', problem)
            
            for math in math_parts:
                expr = math.strip('$')
                action = {
                    "time": datetime.now(),
                    "action": "process_expression",
                    "expression": expr,
                    "context": "homework"
                }
                
                try:
                    result = self.engine.process_latex(expr)
                    action["success"] = True
                    action["processing_time"] = result.processing_time
                    
                    # Simulate student checking unclear results
                    if i == 2 and random.random() < 0.3:
                        # Try again with slightly different notation
                        await asyncio.sleep(0.2)
                        retry_expr = expr.replace("dx", "\\,dx")
                        self.engine.process_latex(retry_expr)
                        action["retried"] = True
                    
                except Exception as e:
                    action["success"] = False
                    action["error"] = str(e)
                    self.errors.append(action)
                
                self.actions.append(action)
        
        # Simulate reviewing notes
        await self._simulate_note_review()
    
    async def _simulate_professor(self):
        """Simulate a professor preparing lectures"""
        lecture_sections = [
            {
                "title": "Introduction to Limits",
                "content": [
                    "Definition: $\\lim_{x \\to a} f(x) = L$ means",
                    "$\\forall \\epsilon > 0 \\, \\exists \\delta > 0 : 0 < |x - a| < \\delta \\implies |f(x) - L| < \\epsilon$",
                    "Example: $\\lim_{x \\to 2} (x^2 - 4) = 0$",
                    "Proof: Let $\\epsilon > 0$. Choose $\\delta = \\min(1, \\frac{\\epsilon}{5})$"
                ]
            },
            {
                "title": "L'Hôpital's Rule",
                "content": [
                    "If $\\lim_{x \\to a} f(x) = \\lim_{x \\to a} g(x) = 0$ or $\\pm\\infty$",
                    "Then $\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)}$",
                    "Example: $\\lim_{x \\to 0} \\frac{\\sin x}{x} = \\lim_{x \\to 0} \\frac{\\cos x}{1} = 1$"
                ]
            }
        ]
        
        for section in lecture_sections:
            action = {
                "time": datetime.now(),
                "action": "prepare_lecture",
                "section": section["title"],
                "expressions_processed": 0
            }
            
            for content_line in section["content"]:
                # Extract mathematical content
                math_parts = re.findall(r'\$[^$]+\$', content_line)
                
                for math in math_parts:
                    expr = math.strip('$')
                    try:
                        # Professor wants high quality
                        result = self.engine.process_latex(expr, show_progress=False)
                        action["expressions_processed"] += 1
                        
                        # Simulate checking pronunciation
                        if "epsilon" in expr or "delta" in expr:
                            # Professor cares about Greek letter pronunciation
                            await asyncio.sleep(0.1)
                        
                    except Exception as e:
                        self.errors.append({
                            "expression": expr,
                            "error": str(e),
                            "context": "lecture_prep"
                        })
            
            self.actions.append(action)
            
            # Simulate break between sections
            await asyncio.sleep(0.5)
        
        # Test batch processing for problem sets
        await self._simulate_batch_processing()
    
    async def _simulate_researcher(self):
        """Simulate a researcher working with complex formulas"""
        research_formulas = [
            # Differential geometry
            "R_{\\mu\\nu\\rho\\sigma} = \\partial_\\rho \\Gamma_{\\mu\\nu\\sigma} - \\partial_\\sigma \\Gamma_{\\mu\\nu\\rho} + \\Gamma_{\\mu\\rho\\lambda}\\Gamma^\\lambda_{\\nu\\sigma} - \\Gamma_{\\mu\\sigma\\lambda}\\Gamma^\\lambda_{\\nu\\rho}",
            
            # Quantum mechanics
            "\\hat{H}\\psi = E\\psi \\text{ where } \\hat{H} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V(\\mathbf{r})",
            
            # Statistical mechanics
            "Z = \\sum_{i} e^{-\\beta E_i} = \\int e^{-\\beta H(\\mathbf{p}, \\mathbf{q})} d\\mathbf{p} d\\mathbf{q}",
            
            # Complex analysis
            "f(z) = \\sum_{n=-\\infty}^{\\infty} a_n (z-z_0)^n \\text{ where } a_n = \\frac{1}{2\\pi i} \\oint_C \\frac{f(\\zeta)}{(\\zeta - z_0)^{n+1}} d\\zeta"
        ]
        
        for formula in research_formulas:
            action = {
                "time": datetime.now(),
                "action": "process_research_formula",
                "formula_length": len(formula),
                "formula_preview": formula[:50] + "..."
            }
            
            try:
                # Researchers often work with very complex expressions
                start = time.time()
                result = self.engine.process_latex(formula, show_progress=True)
                processing_time = time.time() - start
                
                action["success"] = True
                action["processing_time"] = processing_time
                action["unknown_commands"] = len(result.unknown_commands)
                
                # Simulate iterative refinement
                if result.unknown_commands:
                    # Try to fix unknown commands
                    fixed_formula = formula
                    for cmd in result.unknown_commands[:2]:
                        fixed_formula = fixed_formula.replace(f"\\{cmd}", f"\\text{{{cmd}}}")
                    
                    # Reprocess
                    self.engine.process_latex(fixed_formula)
                    action["refined"] = True
                
            except Exception as e:
                action["success"] = False
                action["error"] = str(e)
                self.errors.append(action)
            
            self.actions.append(action)
            
            # Simulate research workflow - checking references
            await asyncio.sleep(random.uniform(0.2, 0.5))
    
    async def _simulate_casual_user(self):
        """Simulate casual/curious user"""
        casual_queries = [
            "e^{i\\pi} + 1 = 0",  # Euler's identity
            "a^2 + b^2 = c^2",    # Pythagorean theorem
            "E = mc^2",           # Einstein's equation
            "\\sum_{n=1}^{\\infty} \\frac{1}{n^2}",  # Basel problem
            "\\phi = \\frac{1 + \\sqrt{5}}{2}",  # Golden ratio
        ]
        
        for query in casual_queries:
            action = {
                "time": datetime.now(),
                "action": "casual_query",
                "query": query
            }
            
            try:
                # Casual users might not use proper LaTeX
                if random.random() < 0.3:
                    # Simulate improper formatting
                    query = query.replace("\\", "")
                
                result = self.engine.process_latex(query)
                action["success"] = True
                action["response_time"] = result.processing_time
                
            except Exception as e:
                action["success"] = False
                action["error"] = str(e)
                # Casual users might give up after errors
                if random.random() < 0.5:
                    break
            
            self.actions.append(action)
            
            # Casual users have longer gaps between queries
            await asyncio.sleep(random.uniform(1, 3))
    
    async def _simulate_power_user(self):
        """Simulate power user pushing limits"""
        # Power users know the system well and push boundaries
        
        # Test batch processing
        batch_expressions = [f"\\int_0^{i} x^{i} dx" for i in range(1, 21)]
        
        action = {
            "time": datetime.now(),
            "action": "batch_process",
            "batch_size": len(batch_expressions)
        }
        
        start = time.time()
        results = []
        for expr in batch_expressions:
            try:
                result = self.engine.process_latex(expr)
                results.append(result)
            except:
                pass
        
        action["total_time"] = time.time() - start
        action["success_rate"] = len(results) / len(batch_expressions)
        self.actions.append(action)
        
        # Test caching behavior
        test_expr = "\\frac{d}{dx} e^{x^2}"
        cache_times = []
        
        for i in range(5):
            start = time.time()
            self.engine.process_latex(test_expr)
            cache_times.append(time.time() - start)
        
        self.actions.append({
            "time": datetime.now(),
            "action": "cache_test",
            "cache_times": cache_times,
            "speedup": cache_times[0] / cache_times[-1] if cache_times[-1] > 0 else 0
        })
        
        # Test complex nested structures
        nested = "\\sum_{i=1}^{n} \\prod_{j=1}^{m} \\int_{0}^{\\infty} e^{-x_{ij}^2} dx_{ij}"
        try:
            result = self.engine.process_latex(nested)
            self.actions.append({
                "time": datetime.now(),
                "action": "complex_nested",
                "success": True,
                "processing_time": result.processing_time
            })
        except Exception as e:
            self.errors.append({"action": "complex_nested", "error": str(e)})
    
    async def _simulate_note_review(self):
        """Simulate reviewing notes with many formulas"""
        note_formulas = [
            "v = \\frac{dx}{dt}",
            "a = \\frac{dv}{dt} = \\frac{d^2x}{dt^2}",
            "F = ma",
            "W = \\int F \\cdot dx",
            "KE = \\frac{1}{2}mv^2"
        ]
        
        for formula in note_formulas:
            self.engine.process_latex(formula)
            await asyncio.sleep(0.1)
    
    async def _simulate_batch_processing(self):
        """Simulate batch processing workflow"""
        problem_set = [
            f"Problem {i}: Evaluate $\\int x^{i} e^{-x} dx$"
            for i in range(1, 11)
        ]
        
        action = {
            "time": datetime.now(),
            "action": "batch_problems",
            "count": len(problem_set)
        }
        
        start = time.time()
        for problem in problem_set:
            math_match = re.search(r'\$([^$]+)\$', problem)
            if math_match:
                self.engine.process_latex(math_match.group(1))
        
        action["total_time"] = time.time() - start
        self.actions.append(action)
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate user simulation report"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            "user_type": self.user_type,
            "duration": duration,
            "total_actions": len(self.actions),
            "errors": len(self.errors),
            "error_rate": len(self.errors) / len(self.actions) if self.actions else 0,
            "actions_per_minute": len(self.actions) / (duration / 60) if duration > 0 else 0,
            "action_summary": self._summarize_actions(),
            "error_summary": self._summarize_errors()
        }
    
    def _summarize_actions(self) -> Dict[str, int]:
        """Summarize actions by type"""
        summary = {}
        for action in self.actions:
            action_type = action.get("action", "unknown")
            summary[action_type] = summary.get(action_type, 0) + 1
        return summary
    
    def _summarize_errors(self) -> List[str]:
        """Summarize error types"""
        return [e.get("error", "Unknown error")[:50] for e in self.errors[:5]]


class RealWorldTestRunner:
    """Runs real-world user simulations"""
    
    def __init__(self):
        self.engine = None
        self.results = {}
    
    async def setup(self):
        """Initialize engine"""
        voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=voice_manager,
            enable_caching=True
        )
        
        # Load domain processors
        try:
            from mathspeak.domains.topology import TopologyProcessor
            from mathspeak.domains.complex_analysis import ComplexAnalysisProcessor
            from mathspeak.domains.ode import ODEProcessor
            
            self.engine.domain_processors[MathematicalContext.TOPOLOGY] = TopologyProcessor()
            self.engine.domain_processors[MathematicalContext.COMPLEX_ANALYSIS] = ComplexAnalysisProcessor()
            self.engine.domain_processors[MathematicalContext.ODE] = ODEProcessor()
        except:
            pass
    
    async def run_simulations(self):
        """Run all user simulations"""
        user_types = ["student", "professor", "researcher", "casual", "power"]
        
        print("Running Real-World User Simulations")
        print("=" * 50)
        
        for user_type in user_types:
            print(f"\nSimulating {user_type} user...")
            
            simulation = UserSimulation(user_type, self.engine)
            result = await simulation.simulate()
            self.results[user_type] = result
            
            print(f"  Actions: {result['total_actions']}")
            print(f"  Errors: {result['errors']}")
            print(f"  Error rate: {result['error_rate']*100:.1f}%")
            print(f"  Actions/min: {result['actions_per_minute']:.1f}")
    
    def generate_report(self) -> str:
        """Generate simulation report"""
        report = """# Real-World User Simulation Report

## Overview

This report summarizes real-world usage patterns simulated for different user types.

## User Type Analysis

"""
        
        for user_type, result in self.results.items():
            report += f"""### {user_type.capitalize()} User

- **Total Actions**: {result['total_actions']}
- **Error Rate**: {result['error_rate']*100:.1f}%
- **Actions per Minute**: {result['actions_per_minute']:.1f}
- **Session Duration**: {result['duration']:.1f} seconds

**Action Breakdown**:
"""
            for action, count in result['action_summary'].items():
                report += f"  - {action}: {count}\n"
            
            if result['error_summary']:
                report += f"\n**Common Errors**:\n"
                for error in result['error_summary']:
                    report += f"  - {error}\n"
            
            report += "\n"
        
        # Overall analysis
        total_actions = sum(r['total_actions'] for r in self.results.values())
        total_errors = sum(r['errors'] for r in self.results.values())
        overall_error_rate = total_errors / total_actions if total_actions > 0 else 0
        
        report += f"""## Overall Analysis

- **Total Simulated Actions**: {total_actions}
- **Total Errors**: {total_errors}
- **Overall Error Rate**: {overall_error_rate*100:.1f}%

## Key Findings

1. **Student Users**: {"Stable" if self.results.get('student', {}).get('error_rate', 1) < 0.1 else "Experiencing issues"}
2. **Professor Users**: {"Satisfied" if self.results.get('professor', {}).get('error_rate', 1) < 0.05 else "Need improvements"}
3. **Researcher Users**: {"Well-served" if self.results.get('researcher', {}).get('error_rate', 1) < 0.1 else "Complex formulas problematic"}
4. **Casual Users**: {"Good experience" if self.results.get('casual', {}).get('error_rate', 1) < 0.15 else "Too many errors"}
5. **Power Users**: {"System handles load" if self.results.get('power', {}).get('error_rate', 1) < 0.05 else "Performance issues"}

## Recommendations

"""
        
        if overall_error_rate > 0.1:
            report += "- Improve error handling and user guidance\n"
        
        if any(r.get('error_rate', 0) > 0.15 for r in self.results.values()):
            report += "- Add better input validation and suggestions\n"
        
        report += "- Continue monitoring real-world usage patterns\n"
        report += "- Consider user-specific optimizations\n"
        
        return report
    
    def save_report(self, filename: str = "user_simulation_report.md"):
        """Save report to file"""
        with open(filename, 'w') as f:
            f.write(self.generate_report())
        
        # Save raw data
        with open(filename.replace('.md', '.json'), 'w') as f:
            json.dump(self.results, f, indent=2, default=str)


async def main():
    """Run user simulations"""
    runner = RealWorldTestRunner()
    
    try:
        await runner.setup()
        await runner.run_simulations()
        runner.save_report()
        
        print("\n" + "=" * 50)
        print("User simulation complete!")
        print("Report saved to: user_simulation_report.md")
        
    finally:
        if runner.engine:
            runner.engine.shutdown()


if __name__ == "__main__":
    import re  # Add missing import
    from mathspeak.core.engine import MathematicalContext  # Add missing import
    asyncio.run(main())