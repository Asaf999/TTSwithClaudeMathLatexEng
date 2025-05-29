#!/usr/bin/env python3
"""
User Simulation Test
====================

Simulates real user interactions with the MathSpeak system.
"""

import subprocess
import time
import os
import tempfile
import random
from pathlib import Path


class UserSimulator:
    """Simulates user interactions with MathSpeak"""
    
    def __init__(self):
        self.results = []
        self.mathspeak_path = Path(__file__).parent / "mathspeak.py"
        
    def run_command(self, command: str) -> tuple:
        """Run a command and capture output"""
        start = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            duration = time.time() - start
            return (result.returncode == 0, result.stdout, result.stderr, duration)
        except subprocess.TimeoutExpired:
            return (False, "", "Command timed out", 30.0)
        except Exception as e:
            return (False, "", str(e), time.time() - start)
    
    def test_scenario(self, name: str, command: str):
        """Test a specific scenario"""
        print(f"\n🧪 Testing: {name}")
        success, stdout, stderr, duration = self.run_command(command)
        
        result = {
            'scenario': name,
            'command': command[:100] + ('...' if len(command) > 100 else ''),
            'success': success,
            'duration': duration,
            'stdout_preview': stdout[:200] if stdout else '',
            'stderr': stderr[:200] if stderr else ''
        }
        
        self.results.append(result)
        
        if success:
            print(f"   ✅ Success ({duration:.2f}s)")
        else:
            print(f"   ❌ Failed: {stderr[:100]}")
        
        return success
    
    def run_all_scenarios(self):
        """Run all user scenarios"""
        print("🎭 Starting User Simulation Tests")
        print("=" * 60)
        
        # Basic command-line usage
        self.test_scenario(
            "Help command",
            f"cd {self.mathspeak_path.parent} && python mathspeak.py --help"
        )
        
        self.test_scenario(
            "Version check",
            f"cd {self.mathspeak_path.parent} && python mathspeak.py --version"
        )
        
        # Simple expressions
        self.test_scenario(
            "Simple fraction",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "\\\\frac{{1}}{{2}}"'
        )
        
        self.test_scenario(
            "Quadratic formula",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "x = \\\\frac{{-b \\\\pm \\\\sqrt{{b^2 - 4ac}}}}{{2a}}"'
        )
        
        # Different domains
        self.test_scenario(
            "Topology expression",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "\\\\pi_1(S^1) \\\\cong \\\\mathbb{{Z}}" --context topology'
        )
        
        self.test_scenario(
            "Complex analysis",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "f(z) = e^z" --context complex_analysis'
        )
        
        # File input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(r"""
\documentclass{article}
\begin{document}
The fundamental theorem of calculus states:
$$\int_a^b f'(x) dx = f(b) - f(a)$$
\end{document}
""")
            tex_file = f.name
        
        self.test_scenario(
            "LaTeX file input",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py --file {tex_file}'
        )
        
        os.unlink(tex_file)
        
        # Output to file
        self.test_scenario(
            "Save to audio file",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "e^{{i\\\\pi}} = -1" --output /tmp/euler.mp3'
        )
        
        # Test if file was created
        if os.path.exists('/tmp/euler.mp3'):
            print("   📁 Audio file created successfully")
            os.unlink('/tmp/euler.mp3')
        
        # Different voices
        self.test_scenario(
            "Theorem voice",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "Every compact space is complete" --voice theorem'
        )
        
        # Speed adjustment
        self.test_scenario(
            "Slow speed",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "\\\\sum_{{n=1}}^{{\\\\infty}} \\\\frac{{1}}{{n^2}}" --speed 0.8'
        )
        
        # Error cases
        self.test_scenario(
            "Invalid LaTeX",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "\\\\undefined{{command}}"'
        )
        
        self.test_scenario(
            "Empty input",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py ""'
        )
        
        self.test_scenario(
            "Very long expression",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "' + 'x + ' * 500 + 'y"'
        )
        
        # Special characters
        self.test_scenario(
            "Unicode math",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "∫∞₀ e^(-x²) dx = √π/2"'
        )
        
        # Multiple expressions
        self.test_scenario(
            "Multiple lines",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "x = 1\\\\\\\\y = 2\\\\\\\\z = 3"'
        )
        
        # Test mode
        self.test_scenario(
            "Run tests",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py --test basic'
        )
        
        # Stats
        self.test_scenario(
            "Show stats",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "x^2" --stats'
        )
        
        # Invalid options
        self.test_scenario(
            "Invalid option",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py --invalid-option'
        )
        
        self.test_scenario(
            "Invalid context",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "x" --context invalid_domain'
        )
        
        # Stress test with special cases
        self.test_scenario(
            "Null bytes",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "x\\x00y"'
        )
        
        self.test_scenario(
            "Shell injection attempt",
            f'cd {self.mathspeak_path.parent} && python mathspeak.py "x; rm -rf /"'
        )
        
        # Interactive mode test (with timeout)
        self.test_scenario(
            "Interactive mode help",
            f'cd {self.mathspeak_path.parent} && echo "/help" | timeout 5 python mathspeak.py --interactive'
        )
        
        # Summary
        print("\n" + "=" * 60)
        print("USER SIMULATION SUMMARY")
        print("=" * 60)
        
        total = len(self.results)
        successes = sum(1 for r in self.results if r['success'])
        
        print(f"Total Scenarios: {total}")
        print(f"Successful: {successes} ({successes/total*100:.1f}%)")
        print(f"Failed: {total - successes} ({(total-successes)/total*100:.1f}%)")
        
        # Show failures
        failures = [r for r in self.results if not r['success']]
        if failures:
            print("\n❌ Failed Scenarios:")
            for f in failures:
                print(f"  - {f['scenario']}: {f['stderr'][:100]}")
        
        # Performance issues
        slow = [r for r in self.results if r['duration'] > 5.0]
        if slow:
            print(f"\n⏱️  Slow Scenarios ({len(slow)}):")
            for s in slow:
                print(f"  - {s['scenario']}: {s['duration']:.2f}s")
        
        return self.results


def test_edge_cases():
    """Test specific edge cases that might break the system"""
    print("\n🔨 Testing Edge Cases")
    print("=" * 60)
    
    simulator = UserSimulator()
    
    # Memory stress
    print("\n💾 Memory Stress Test:")
    large_expr = "\\sum_{i=1}^{1000000} x_i"
    simulator.test_scenario(
        "Very large sum",
        f'cd {simulator.mathspeak_path.parent} && python mathspeak.py "{large_expr}"'
    )
    
    # Recursive definitions
    print("\n🔄 Recursive Test:")
    recursive = "Let $f(x) = f(f(f(f(f(x)))))$"
    simulator.test_scenario(
        "Recursive definition",
        f'cd {simulator.mathspeak_path.parent} && python mathspeak.py "{recursive}"'
    )
    
    # Mixed languages
    print("\n🌍 International Test:")
    mixed = "Пусть $x = $ 速度 where السرعة = $v$"
    simulator.test_scenario(
        "Mixed languages",
        f'cd {simulator.mathspeak_path.parent} && python mathspeak.py "{mixed}"'
    )
    
    # Malicious patterns
    print("\n🔒 Security Test:")
    patterns = [
        "\\input{/etc/passwd}",
        "\\write18{cat /etc/passwd}",
        "$()$",
        "${HOME}",
        "\\def\\x{\\x}\\x",
    ]
    
    for i, pattern in enumerate(patterns):
        simulator.test_scenario(
            f"Security pattern {i+1}",
            f'cd {simulator.mathspeak_path.parent} && python mathspeak.py "{pattern}"'
        )


def test_concurrent_users():
    """Simulate multiple concurrent users"""
    print("\n👥 Testing Concurrent Users")
    print("=" * 60)
    
    import concurrent.futures
    
    def run_user(user_id: int):
        """Simulate a single user"""
        expressions = [
            "\\int_0^1 x dx",
            "\\sum_{n=1}^{10} n",
            "\\frac{d}{dx} e^x",
            "\\lim_{x \\to 0} \\frac{\\sin x}{x}",
        ]
        
        expr = random.choice(expressions)
        command = f'cd {Path(__file__).parent} && python mathspeak.py "{expr}"'
        
        start = time.time()
        result = subprocess.run(command, shell=True, capture_output=True, timeout=10)
        duration = time.time() - start
        
        return {
            'user_id': user_id,
            'success': result.returncode == 0,
            'duration': duration
        }
    
    # Run 10 concurrent users
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(run_user, i) for i in range(10)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    successes = sum(1 for r in results if r['success'])
    avg_duration = sum(r['duration'] for r in results) / len(results)
    
    print(f"Concurrent Users: 10")
    print(f"Successful: {successes}/10")
    print(f"Average Duration: {avg_duration:.2f}s")
    
    if successes < 10:
        print("⚠️  Some concurrent requests failed!")


if __name__ == "__main__":
    # Run main user simulation
    simulator = UserSimulator()
    results = simulator.run_all_scenarios()
    
    # Run edge case tests
    test_edge_cases()
    
    # Run concurrent user test
    test_concurrent_users()
    
    print("\n✅ User simulation complete!")