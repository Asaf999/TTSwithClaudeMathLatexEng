#!/usr/bin/env python3
"""
MathSpeak API Server CLI
========================

Simple CLI to start the MathSpeak REST API server.
"""

import argparse
import logging
from mathspeak.api import run_server

def main():
    parser = argparse.ArgumentParser(description="MathSpeak REST API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print(f"Starting MathSpeak API server on {args.host}:{args.port}")
    print(f"API documentation will be available at http://{args.host}:{args.port}/docs")
    
    run_server(host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()