"""
Package: crypto_dashboard
CLI, Backend Daemon & agy Bridge for Crypto Portfolio Management Dashboard.
Zero external dependencies (Python 3 Standard Library only).
"""

from .agy_bridge import (
    generate_agy_command,
    execute_agy_cli,
    find_agy_binary,
)

from .api_handlers import (
    handle_api_route,
    run_simulation,
    get_macro_data,
)

from .cli import (
    create_parser,
    handle_cli,
)

from .server import (
    start_server,
    stop_server,
    create_server,
    DashboardServer,
)

__all__ = [
    "generate_agy_command",
    "execute_agy_cli",
    "find_agy_binary",
    "handle_api_route",
    "run_simulation",
    "get_macro_data",
    "create_parser",
    "handle_cli",
    "start_server",
    "stop_server",
    "create_server",
    "DashboardServer",
]


