#!/usr/bin/env python3
"""
Async Cleanup Utilities
=======================

Proper cleanup for async operations to prevent connection errors.
"""

import asyncio
import atexit
import logging
import weakref
from typing import Set

logger = logging.getLogger(__name__)

# Global set of sessions to cleanup
_active_sessions: Set[weakref.ref] = set()


def register_session(session):
    """Register an aiohttp session for cleanup"""
    _active_sessions.add(weakref.ref(session))


async def cleanup_sessions():
    """Cleanup all active sessions"""
    for session_ref in list(_active_sessions):
        session = session_ref()
        if session and not session.closed:
            try:
                await session.close()
            except Exception as e:
                logger.debug(f"Error closing session: {e}")
    _active_sessions.clear()


def cleanup_sync():
    """Synchronous cleanup for atexit"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop
        return
    
    if not loop.is_closed():
        loop.create_task(cleanup_sessions())


# Register cleanup
atexit.register(cleanup_sync)


class AsyncContextManager:
    """Context manager for proper async cleanup"""
    
    def __init__(self):
        self.tasks = []
        self.sessions = []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cancel pending tasks
        for task in self.tasks:
            if not task.done():
                task.cancel()
        
        # Wait for cancellation
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        
        # Close sessions
        for session in self.sessions:
            if not session.closed:
                await session.close()
    
    def add_task(self, task):
        """Add a task to be cleaned up"""
        self.tasks.append(task)
    
    def add_session(self, session):
        """Add a session to be cleaned up"""
        self.sessions.append(session)
        register_session(session)