import os
import json
import datetime as dt
from typing import Optional, Dict, Any, List

PLATFORMS = ("youtube", "tiktok", "facebook")

def get_current_slot(now: Optional[dt.datetime] = None) -> int:
    """Determine closest publishing slot (8, 12, or 20) based on current hour."""
    cur = now or dt.datetime.now()
    h = cur.hour
    if h < 10:
        return 8
    elif h < 16:
        return 12
    else:
        return 20

def _find_posted_files(channel: str, root_dir: str) -> List[str]:
    candidates = []
    if channel == "me-tech":
        candidates.append(os.path.join(root_dir, "me-tech", "logs", "posted.json"))
    elif channel == "thien-tran":
        candidates.extend([
            os.path.join(root_dir, "thien-tran", "_pubkit", "logs", "posted.json"),
            os.path.join(root_dir, "thien-tran", "logs", "posted.json"),
            os.path.join(root_dir, "thien-tran", "publish", "posted.json")
        ])
    elif channel == "tam-an-lac":
        candidates.extend([
            os.path.join(root_dir, "tam-an-lac", "_pubkit", "logs", "posted.json"),
            os.path.join(root_dir, "tam-an-lac", "logs", "posted.json")
        ])

    return [c for c in candidates if os.path.exists(c)]

def check_channel_slot(channel: str, slot: int, today: Optional[dt.date] = None, root_dir: Optional[str] = None) -> Dict[str, Any]:
    """Check whether a channel has published or scheduled posts for a given slot today."""
    root = root_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    t_date = today or dt.date.today()
    log_files = _find_posted_files(channel, root)

    hits: Dict[str, set] = {}

    for log_file in log_files:
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for key, v in data.items():
                slug, _, plat = key.rpartition(":")
                if plat not in PLATFORMS:
                    continue
                luc_str = v.get("luc", "")
                try:
                    luc = dt.datetime.strptime(luc_str, "%d.%m.%Y %H:%M")
                except ValueError:
                    continue

                if luc.date() != t_date:
                    continue

                note = v.get("ghi_chu", "")
                if note.startswith("hen "):
                    ok = note[4:6] == f"{slot:02d}"
                else:
                    # Chấp nhận bài đăng ngay trong khung chuẩn bị 2 tiếng trước slot
                    ok = luc >= dt.datetime.combine(t_date, dt.time(max(slot - 2, 0)))

                if ok:
                    hits.setdefault(slug, set()).add(plat)
        except Exception:
            pass

    best = max(hits.items(), key=lambda kv: len(kv[1]), default=None)
    if best and len(best[1]) == len(PLATFORMS):
        return {
            "channel": channel,
            "slot": slot,
            "status": "done",
            "slug": best[0],
            "posted": sorted(list(best[1])),
            "missing": []
        }
    elif best:
        missing = [p for p in PLATFORMS if p not in best[1]]
        return {
            "channel": channel,
            "slot": slot,
            "status": "partial",
            "slug": best[0],
            "posted": sorted(list(best[1])),
            "missing": missing
        }
    else:
        return {
            "channel": channel,
            "slot": slot,
            "status": "none",
            "slug": None,
            "posted": [],
            "missing": list(PLATFORMS)
        }

def check_all_channels(slot: Optional[int] = None, today: Optional[dt.date] = None, root_dir: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Check slot status for all 3 channels."""
    s = slot if slot is not None else get_current_slot()
    return {
        "me-tech": check_channel_slot("me-tech", slot=s, today=today, root_dir=root_dir),
        "thien-tran": check_channel_slot("thien-tran", slot=s, today=today, root_dir=root_dir),
        "tam-an-lac": check_channel_slot("tam-an-lac", slot=s, today=today, root_dir=root_dir),
    }
