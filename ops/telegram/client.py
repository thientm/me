"""Lightweight Telegram Bot HTTP client using standard urllib."""
import json
import logging
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

from ops.telegram import config

logger = logging.getLogger(__name__)

def send_message(
    text: str,
    chat_id: Optional[str] = None,
    parse_mode: str = "HTML",
    reply_markup: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
    timeout: float = 10.0,
) -> Dict[str, Any]:
    """Send text message to Telegram chat."""
    token = config.TELEGRAM_BOT_TOKEN
    target_chat = chat_id or config.TELEGRAM_CHAT_ID

    if dry_run:
        print(f"[DRY-RUN Telegram Message to {target_chat}]:\n{text}")
        return {"ok": True, "dry_run": True, "result": {"text": text}}

    if not token or not target_chat:
        err = "Telegram credentials not configured. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env."
        logger.warning(err)
        return {"ok": False, "description": err}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload: Dict[str, Any] = {
        "chat_id": target_chat,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        logger.error("Telegram API HTTP error %d: %s", e.code, error_body)
        try:
            return json.loads(error_body)
        except Exception:
            return {"ok": False, "description": f"HTTPError {e.code}: {error_body}"}
    except Exception as e:
        logger.error("Failed to send Telegram message: %s", e)
        return {"ok": False, "description": str(e)}

def send_photo(
    photo_path: str,
    caption: Optional[str] = None,
    chat_id: Optional[str] = None,
    parse_mode: str = "HTML",
    dry_run: bool = False,
    timeout: float = 20.0,
) -> Dict[str, Any]:
    """Send a photo with multipart/form-data."""
    token = config.TELEGRAM_BOT_TOKEN
    target_chat = chat_id or config.TELEGRAM_CHAT_ID

    if dry_run:
        print(f"[DRY-RUN Telegram Photo to {target_chat}]: path={photo_path}, caption={caption}")
        return {"ok": True, "dry_run": True}

    if not token or not target_chat:
        err = "Telegram credentials not configured."
        logger.warning(err)
        return {"ok": False, "description": err}

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    boundary = "----TelegramFormBoundary7MA4YWxkTrZu0gW"
    
    body = bytearray()
    # chat_id field
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{target_chat}\r\n'.encode("utf-8"))
    
    # caption field
    if caption:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode("utf-8"))
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="parse_mode"\r\n\r\n{parse_mode}\r\n'.encode("utf-8"))

    # photo file
    with open(photo_path, "rb") as f:
        file_bytes = f.read()

    filename = photo_path.split("/")[-1]
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(b'Content-Type: application/octet-stream\r\n\r\n')
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content)
    except Exception as e:
        logger.error("Failed to send photo: %s", e)
        return {"ok": False, "description": str(e)}
