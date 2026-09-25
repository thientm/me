"""
Package entrypoint: python3 -m crypto_dashboard
Authoritative source: PROJECT.md §F7; explorer_dashboard_1/report.md §2.
"""

import sys
from crypto_dashboard.cli import handle_cli

if __name__ == "__main__":
    sys.exit(handle_cli(sys.argv[1:]))
