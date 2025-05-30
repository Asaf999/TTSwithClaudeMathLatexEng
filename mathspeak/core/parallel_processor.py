#!/usr/bin/env python3
"""
Parallel Processing for MathSpeak
=================================

Enables parallel processing of large documents and multiple expressions.
"""

import asyncio
import concurrent.futures
import multiprocessing
import logging
import time
from typing import List, Dict, Any, Tuple, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import re
from tqdm import tqdm

from .engine import MathematicalTTSEngine, ProcessedExpression


logger = logging.getLogger(__name__)


@dataclass
class ProcessingTask:
    """A single processing task"""
    id: int
    expression: str
    context: Optional[str] = None
    output_file: Optional[str] = None
    
    
@dataclass
class ProcessingResult:
    """Result of processing a task"""
    task_id: int
    success: bool
    result: Optional[ProcessedExpression] = None
    error: Optional[str] = None
    duration: float = 0.0


class ParallelProcessor:
    """Processes multiple expressions in parallel"""
    
    def __init__(self, 
                 num_workers: Optional[int] = None,
                 use_multiprocessing: bool = False,
                 show_progress: bool = True):
        """
        Initialize parallel processor.
        
        Args:
            num_workers: Number of workers (None for auto)
            use_multiprocessing: Use multiprocessing instead of threading
            show_progress: Show progress bar
        """
        self.num_workers = num_workers or multiprocessing.cpu_count()
        self.use_multiprocessing = use_multiprocessing
        self.show_progress = show_progress
        
        # Create engine pool
        self.engines = []
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize processing engines"""
        for _ in range(self.num_workers):
            self.engines.append(MathematicalTTSEngine())
    
    async def process_tasks(self, tasks: List[ProcessingTask]) -> List[ProcessingResult]:
        """
        Process multiple tasks in parallel.
        
        Args:
            tasks: List of processing tasks
            
        Returns:
            List of results
        """
        if not tasks:
            return []
        
        logger.info(f"Processing {len(tasks)} tasks with {self.num_workers} workers")
        
        # Create progress bar
        pbar = None
        if self.show_progress:
            pbar = tqdm(total=len(tasks), desc="Processing expressions")
        
        # Process based on mode
        if self.use_multiprocessing:
            results = await self._process_multiprocessing(tasks, pbar)
        else:
            results = await self._process_asyncio(tasks, pbar)
        
        if pbar:
            pbar.close()
        
        # Sort results by task ID
        results.sort(key=lambda r: r.task_id)
        
        return results
    
    async def _process_asyncio(self, tasks: List[ProcessingTask], 
                              pbar: Optional[tqdm]) -> List[ProcessingResult]:
        """Process tasks using asyncio"""
        semaphore = asyncio.Semaphore(self.num_workers)
        
        async def process_task(task: ProcessingTask, engine_idx: int) -> ProcessingResult:
            async with semaphore:
                start_time = time.time()
                try:
                    engine = self.engines[engine_idx % len(self.engines)]
                    result = engine.process_latex(task.expression)
                    
                    duration = time.time() - start_time
                    
                    if pbar:
                        pbar.update(1)
                    
                    return ProcessingResult(
                        task_id=task.id,
                        success=True,
                        result=result,
                        duration=duration
                    )
                    
                except Exception as e:
                    logger.error(f"Task {task.id} failed: {e}")
                    
                    if pbar:
                        pbar.update(1)
                    
                    return ProcessingResult(
                        task_id=task.id,
                        success=False,
                        error=str(e),
                        duration=time.time() - start_time
                    )
        
        # Create tasks
        coroutines = [
            process_task(task, i) for i, task in enumerate(tasks)
        ]
        
        # Run all tasks
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ProcessingResult(
                    task_id=tasks[i].id,
                    success=False,
                    error=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _process_multiprocessing(self, tasks: List[ProcessingTask],
                                     pbar: Optional[tqdm]) -> List[ProcessingResult]:
        """Process tasks using multiprocessing"""
        loop = asyncio.get_event_loop()
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            # Submit all tasks
            futures = []
            for task in tasks:
                future = loop.run_in_executor(
                    executor,
                    _process_task_worker,
                    task
                )
                futures.append(future)
            
            # Collect results
            results = []
            for future in asyncio.as_completed(futures):
                result = await future
                results.append(result)
                
                if pbar:
                    pbar.update(1)
            
            return results
    
    def shutdown(self):
        """Shutdown all engines"""
        for engine in self.engines:
            engine.shutdown()


def _process_task_worker(task: ProcessingTask) -> ProcessingResult:
    """Worker function for multiprocessing"""
    start_time = time.time()
    
    try:
        # Create new engine in worker process
        engine = MathematicalTTSEngine()
        result = engine.process_latex(task.expression)
        engine.shutdown()
        
        return ProcessingResult(
            task_id=task.id,
            success=True,
            result=result,
            duration=time.time() - start_time
        )
        
    except Exception as e:
        return ProcessingResult(
            task_id=task.id,
            success=False,
            error=str(e),
            duration=time.time() - start_time
        )


class DocumentProcessor:
    """Processes entire LaTeX documents"""
    
    def __init__(self, parallel_processor: Optional[ParallelProcessor] = None):
        self.processor = parallel_processor or ParallelProcessor()
        
        # Regex patterns for LaTeX environments
        self.math_patterns = [
            # Display math
            (r'\$\$(.*?)\$\$', 'display'),
            # Inline math
            (r'\$(.*?)\$', 'inline'),
            # Display environments
            (r'\\begin\{equation\}(.*?)\\end\{equation\}', 'equation'),
            (r'\\begin\{align\}(.*?)\\end\{align\}', 'align'),
            (r'\\begin\{gather\}(.*?)\\end\{gather\}', 'gather'),
            # Inline environments
            (r'\\\((.*?)\\\)', 'inline'),
            (r'\\\[(.*?)\\\]', 'display'),
        ]
    
    def extract_math_expressions(self, document: str) -> List[Tuple[str, str, int]]:
        """
        Extract mathematical expressions from document.
        
        Returns:
            List of (expression, type, position) tuples
        """
        expressions = []
        
        for pattern, math_type in self.math_patterns:
            for match in re.finditer(pattern, document, re.DOTALL):
                expression = match.group(1).strip()
                if expression:
                    expressions.append((expression, math_type, match.start()))
        
        # Sort by position
        expressions.sort(key=lambda x: x[2])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_expressions = []
        for expr, math_type, pos in expressions:
            if expr not in seen:
                seen.add(expr)
                unique_expressions.append((expr, math_type, pos))
        
        return unique_expressions
    
    async def process_document(self, document: str) -> Dict[str, Any]:
        """
        Process an entire LaTeX document.
        
        Args:
            document: LaTeX document content
            
        Returns:
            Dictionary with processed expressions and metadata
        """
        start_time = time.time()
        
        # Extract expressions
        expressions = self.extract_math_expressions(document)
        logger.info(f"Found {len(expressions)} mathematical expressions")
        
        if not expressions:
            return {
                'expressions': [],
                'total_time': 0.0,
                'success_rate': 1.0
            }
        
        # Create tasks
        tasks = [
            ProcessingTask(
                id=i,
                expression=expr,
                context=math_type
            )
            for i, (expr, math_type, _) in enumerate(expressions)
        ]
        
        # Process in parallel
        results = await self.processor.process_tasks(tasks)
        
        # Compile results
        processed_expressions = []
        successes = 0
        
        for i, result in enumerate(results):
            expr_data = {
                'original': expressions[i][0],
                'type': expressions[i][1],
                'position': expressions[i][2],
                'success': result.success,
                'processed': result.result.processed if result.result else None,
                'error': result.error,
                'duration': result.duration
            }
            processed_expressions.append(expr_data)
            
            if result.success:
                successes += 1
        
        total_time = time.time() - start_time
        
        return {
            'expressions': processed_expressions,
            'total_time': total_time,
            'success_rate': successes / len(results) if results else 1.0,
            'total_expressions': len(expressions),
            'successful': successes,
            'failed': len(expressions) - successes
        }
    
    async def process_file(self, filepath: Path) -> Dict[str, Any]:
        """Process a LaTeX file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = await self.process_document(content)
            result['filename'] = filepath.name
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to process file {filepath}: {e}")
            return {
                'filename': filepath.name,
                'error': str(e),
                'success_rate': 0.0
            }


class BatchProcessor:
    """Process multiple files or expressions in batch"""
    
    def __init__(self, parallel_processor: Optional[ParallelProcessor] = None):
        self.processor = parallel_processor or ParallelProcessor()
        self.document_processor = DocumentProcessor(self.processor)
    
    async def process_files(self, filepaths: List[Path]) -> Dict[str, Any]:
        """Process multiple files"""
        results = []
        
        for filepath in filepaths:
            logger.info(f"Processing file: {filepath}")
            result = await self.document_processor.process_file(filepath)
            results.append(result)
        
        # Aggregate statistics
        total_expressions = sum(r.get('total_expressions', 0) for r in results)
        total_successful = sum(r.get('successful', 0) for r in results)
        total_time = sum(r.get('total_time', 0) for r in results)
        
        return {
            'files': results,
            'total_files': len(filepaths),
            'total_expressions': total_expressions,
            'total_successful': total_successful,
            'total_failed': total_expressions - total_successful,
            'total_time': total_time,
            'overall_success_rate': total_successful / total_expressions if total_expressions > 0 else 1.0
        }
    
    async def process_expressions(self, expressions: List[str]) -> List[ProcessingResult]:
        """Process a list of expressions"""
        tasks = [
            ProcessingTask(id=i, expression=expr)
            for i, expr in enumerate(expressions)
        ]
        
        return await self.processor.process_tasks(tasks)
    
    def shutdown(self):
        """Shutdown the processor"""
        self.processor.shutdown()