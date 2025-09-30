#!/usr/bin/env python3
"""Compatibility wrapper around the :mod:`pdf_export` package CLI."""

from __future__ import annotations

import sys

from pdf_export.cli import main


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        raise
