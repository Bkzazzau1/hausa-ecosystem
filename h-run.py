# h-run.py
"""Backward-compatible wrapper for the Hausa Ecosystem CLI."""

import sys

from hausa_ecosystem.cli import main


if __name__ == "__main__":
    sys.exit(main())
