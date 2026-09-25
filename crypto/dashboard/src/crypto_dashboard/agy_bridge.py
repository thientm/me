"""
Module: crypto_dashboard.agy_bridge
Tokenless local agy command generator and subprocess runner.
Authoritative source: PROJECT.md §F9; spec_miner_agy_1/report.md §1 & §3.
"""

from __future__ import annotations
import json
import os
import shutil
import subprocess
from typing import List, Dict, Any, Optional, Union

DEFAULT_AGY_PATH = "/Users/thien.tm/.local/bin/agy"
DEFAULT_PROMPT = (
    "Review crypto portfolio according to crypto-plan.md, "
    "evaluate 540tr hard floor and generate action proposals."
)


def find_agy_binary() -> str:
    """Locate the agy CLI binary using search path or system PATH."""
    if os.path.exists(DEFAULT_AGY_PATH) and os.access(DEFAULT_AGY_PATH, os.X_OK):
        return DEFAULT_AGY_PATH
    which_path = shutil.which("agy")
    if which_path:
        return which_path
    return "agy"


def generate_agy_command(
    action: Optional[str] = "review",
    add_dirs: Optional[Union[List[str], str]] = None
) -> List[str]:
    """
    Generate non-interactive, tokenless agy CLI command argument list.
    
    Returns:
        List of command argument strings immune to shell injection.
    """
    binary = find_agy_binary()

    if not action or not str(action).strip():
        prompt = DEFAULT_PROMPT
    elif action.strip().lower() == "review":
        prompt = DEFAULT_PROMPT
    else:
        prompt = str(action)

    cmd: List[str] = [
        binary,
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--output-format", "json",
    ]

    if add_dirs:
        dirs_list = [add_dirs] if isinstance(add_dirs, str) else add_dirs
        for d in dirs_list:
            if isinstance(d, str) and os.path.exists(d):
                cmd.extend(["--add-dir", d])

    return cmd


def execute_agy_cli(
    action: Optional[str] = "review",
    add_dirs: Optional[Union[List[str], str]] = None,
    dry_run: bool = False,
    timeout: int = 60
) -> Dict[str, Any]:
    """
    Execute local agy CLI command safely via subprocess.
    """
    cmd = generate_agy_command(action=action, add_dirs=add_dirs)
    cmd_str = " ".join(cmd)

    if dry_run:
        return {
            "status": "dry_run",
            "is_dry_run": True,
            "command": cmd_str,
            "args": cmd,
        }

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        parsed = None
        if proc.stdout:
            try:
                parsed = json.loads(proc.stdout)
            except Exception:
                parsed = None

        return {
            "status": "ok" if proc.returncode == 0 else "error",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "parsed": parsed,
            "command": cmd_str,
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "error": f"Command timed out after {timeout} seconds",
            "command": cmd_str,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "command": cmd_str,
        }
