"""
Module: crypto_dashboard.server
Threading HTTP Server routing /api/* and serving static web assets.
Authoritative source: PROJECT.md §F8; explorer_dashboard_1/report.md §1.2 & §4.
Zero external dependencies (Python 3 Standard Library only).
"""

from __future__ import annotations
import http.server
import json
import mimetypes
import os
import socketserver
import sys
import threading
import webbrowser
from typing import Optional, Tuple, Dict, Any

from crypto_dashboard.api_handlers import handle_api_route

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class DashboardRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler routing /api/* requests and serving static assets."""

    server_version = "CryptoDashboardServer/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress standard access logging to keep terminal clean unless requested."""
        if os.environ.get("DASHBOARD_VERBOSE"):
            super().log_message(format, *args)

    def _send_cors_headers(self) -> None:
        """Set standard CORS headers for cross-origin local dashboard access."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self) -> None:
        """Handle CORS pre-flight requests."""
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        """Handle GET requests for both API endpoints and static assets."""
        self._route_request("GET")

    def do_POST(self) -> None:
        """Handle POST requests for API endpoints."""
        self._route_request("POST")

    def do_PUT(self) -> None:
        """Handle PUT requests for API endpoints."""
        self._route_request("PUT")

    def do_DELETE(self) -> None:
        """Handle DELETE requests for API endpoints."""
        self._route_request("DELETE")

    def _route_request(self, method: str) -> None:
        """Main dispatcher for API routes and static asset delivery."""
        clean_path = self.path.split("?")[0]

        if clean_path.startswith("/api/") or clean_path == "/api":
            body = None
            if method in ("POST", "PUT"):
                content_len = self.headers.get("Content-Length")
                if content_len:
                    try:
                        raw_body = self.rfile.read(int(content_len))
                        body = json.loads(raw_body.decode("utf-8")) if raw_body else None
                    except Exception:
                        body = "malformed-json"

            status_code, response_data = handle_api_route(method, clean_path, body)

            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()

            body_bytes = json.dumps(response_data, indent=2, ensure_ascii=False).encode("utf-8")
            self.wfile.write(body_bytes)
            return

        # Static file serving for web UI
        if method != "GET":
            self.send_response(405)
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(b"Method Not Allowed")
            return

        self._serve_static(clean_path)

    def _serve_static(self, rel_path: str) -> None:
        """Serve static files from the web directory safely without directory traversal."""
        subpath = rel_path.lstrip("/")
        if not subpath or subpath == "/":
            subpath = "index.html"

        safe_path = os.path.normpath(os.path.join(WEB_DIR, subpath))

        # Security check: directory traversal protection
        if not safe_path.startswith(os.path.abspath(WEB_DIR)):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        if not os.path.exists(safe_path) or not os.path.isfile(safe_path):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"File not found: {subpath}\n".encode("utf-8"))
            return

        mime_type, _ = mimetypes.guess_type(safe_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        try:
            with open(safe_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "javascript" in mime_type or "json" in mime_type else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {e}".encode("utf-8"))


class DashboardServer(http.server.ThreadingHTTPServer):
    """Threading HTTP server allowing address reuse and clean shutdown."""
    allow_reuse_address = True


_CURRENT_SERVER: Optional[DashboardServer] = None


def create_server(host: str = "127.0.0.1", port: int = 8088) -> DashboardServer:
    """Factory creating configured DashboardServer instance."""
    return DashboardServer((host, port), DashboardRequestHandler)


def start_server(
    port: int = 8088,
    host: str = "127.0.0.1",
    open_browser: bool = False,
) -> None:
    """
    Start the Crypto Dashboard HTTP daemon on the specified host and port.
    """
    global _CURRENT_SERVER
    server = create_server(host, port)
    _CURRENT_SERVER = server

    url = f"http://{host}:{port}"
    print(f"🚀 Crypto Dashboard Server running at: {url}")
    print(f"📊 REST APIs available under: {url}/api/")
    print("Press Ctrl+C to terminate.")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Note: Could not open browser automatically: {e}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown requested by user.")
    finally:
        stop_server()


def stop_server() -> None:
    """Gracefully stop the running dashboard server."""
    global _CURRENT_SERVER
    if _CURRENT_SERVER is not None:
        try:
            _CURRENT_SERVER.shutdown()
            _CURRENT_SERVER.server_close()
        except Exception:
            pass
        _CURRENT_SERVER = None
        print("Server shutdown complete.")
