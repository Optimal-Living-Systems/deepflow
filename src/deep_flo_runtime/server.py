"""Deep Flo Runtime server — FastAPI app and CLI entry point.

This module exports the FastAPI ``app`` instance and the ``main()`` entry
point used by the ``deep-flo-runtime`` CLI command defined in pyproject.toml.
"""

from __future__ import annotations

import argparse
import logging
import sys

import uvicorn

from deep_flo_runtime.runtime_api import create_app

# Public FastAPI app — also used by uvicorn directly via ``deep_flo_runtime.server:app``
app = create_app()

logger = logging.getLogger("deep_flo.server")


def main() -> None:
    """Entry point for the ``deep-flo-runtime`` CLI command."""
    parser = argparse.ArgumentParser(
        prog="deep-flo-runtime",
        description="Deep Flo Runtime Server — HTTP bridge for Deep Agents",
    )
    subparsers = parser.add_subparsers(dest="command")

    serve_parser = subparsers.add_parser("serve", help="Start the runtime server")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    serve_parser.add_argument("--port", type=int, default=8100, help="Bind port (default: 8100)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable auto-reload (dev only)")
    serve_parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Uvicorn log level (default: info)",
    )

    args = parser.parse_args()

    if args.command == "serve" or args.command is None:
        host = getattr(args, "host", "0.0.0.0")
        port = getattr(args, "port", 8100)
        reload = getattr(args, "reload", False)
        log_level = getattr(args, "log_level", "info")

        logger.info("Starting Deep Flo runtime on %s:%d", host, port)
        uvicorn.run(
            "deep_flo_runtime.server:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
