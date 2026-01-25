"""Main entry point for python -m anki_artisan."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
