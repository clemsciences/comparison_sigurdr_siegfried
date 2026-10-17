"""Allow ``python -m sigurd``."""

import sys

from sigurd.cli import main

sys.exit(main())
