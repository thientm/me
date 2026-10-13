import os
import sys
import argparse
from ledger import EngagementLedger
from lock import check_conflicts, EngagementLock
from adapters.yt_studio import YouTubeStudioAdapter
from adapters.fb_business import FacebookBusinessAdapter
from adapters.tt_studio import TikTokStudioAdapter

DEFAULT_CONFLICT_LOCKS = [
    ".run/build.lock",
    "me-tech/.run/build.lock",
    "me-tech/.run/fb9333.lock"
]

ENGAGEMENT_LOCK_PATH = ".run/engagement.lock"
DEFAULT_LEDGER_PATH = "me-tech/ops/engagement/logs/engagement_ledger.json"

CHANNEL_CONFIGS = {
    "metech": {
        "name": "metech",
        "yt_port": 9333,
        "yt_channel_id": "UCnElgDX9q_AYGdFc2oDuWUA",
        "fb_port": 9333,
        "fb_asset_id": "403727472998689",
        "tt_port": 9333,
    },
    "tamanlac": {
        "name": "tamanlac",
        "yt_port": 9555,
        "yt_channel_id": "UCjEteQMJ4zzFV9_iKvChpvA",
        "fb_port": 9333,  # FB của Tâm An Lạc cũng quản lý qua Chrome 9333
        "fb_asset_id": "686899491163120",
        "tt_port": 9555,
    }
}

def parse_args(args_list=None):
    parser = argparse.ArgumentParser(description="Auto Engagement Bot Runner")
    parser.add_argument("--channel", choices=["metech", "tamanlac", "all"], default="all", help="Target channel")
    parser.add_argument("--platform", choices=["yt", "fb", "tt", "all"], default="all", help="Target platform")
    parser.add_argument("--dry-run", action="store_true", help="Run in dry-run mode (no real clicks/replies)")
    parser.add_argument("--limit", type=int, default=5, help="Limit number of replies per platform")
    parser.add_argument("--notify-telegram", action="store_true", help="Send summary card to Telegram")
    return parser.parse_args(args_list)

def build_channel_targets(channel_choice: str) -> list[dict]:
    if channel_choice == "all":
        return [CHANNEL_CONFIGS["metech"], CHANNEL_CONFIGS["tamanlac"]]
    return [CHANNEL_CONFIGS[channel_choice]]

def aggregate_stats(results: list[dict]) -> dict:
    stats = {
        "replies": 0,
        "hearts": 0,
        "likes": 0,
        "spam": 0,
        "sample_replies": []
    }
    for item in results:
        actions = item.get("actions", [])
        if "reply" in actions:
            stats["replies"] += 1
            if item.get("reply_text"):
                stats["sample_replies"].append(item["reply_text"])
        if "heart" in actions:
            stats["hearts"] += 1
        if "like" in actions:
            stats["likes"] += 1
        if "skip_spam" in actions:
            stats["spam"] += 1
    return stats

import urllib.request
import subprocess

def is_port_alive(port: int) -> bool:
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1.5)
        return True
    except Exception:
        return False

def ensure_port(port: int) -> bool:
    """Returns True if Chrome was started by this call."""
    if is_port_alive(port):
        return False
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        script = os.path.join(root_dir, "me-tech", "ops", "open_chrome.py")
        subprocess.run([sys.executable, script, str(port)], check=True, timeout=35)
        return True
    except Exception as e:
        print(f"[Runner] Không thể mở Chrome cổng {port}: {e}")
        return False

def close_port(port: int) -> None:
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        script = os.path.join(root_dir, "me-tech", "ops", "close_browser.py")
        subprocess.run([sys.executable, script, str(port)], timeout=15)
    except Exception as e:
        print(f"[Runner] Lỗi đóng Chrome cổng {port}: {e}")

def main():
    args = parse_args()

    # 1. Check for conflicts with video rendering / publishing
    if check_conflicts(DEFAULT_CONFLICT_LOCKS):
        print("[Runner] Phát hiện pipeline dựng hoặc đăng video đang chạy (Lock detected). Tự động hoãn ca tương tác.")
        sys.exit(0)

    # 2. Acquire Engagement Lock
    eng_lock = EngagementLock(ENGAGEMENT_LOCK_PATH)
    if not eng_lock.acquire():
        print("[Runner] Một phiên engagement khác đang chạy. Bỏ qua.")
        sys.exit(0)

    try:
        ledger = EngagementLedger(DEFAULT_LEDGER_PATH)
        targets = build_channel_targets(args.channel)

        for tgt in targets:
            ch_name = tgt["name"]
            print(f"=== Đang xử lý kênh: {ch_name} (Dry-run: {args.dry_run}) ===")
            ch_results = []
            started_ports = set()

            # Ensure required ports are running
            required_ports = set(filter(None, [tgt.get("yt_port"), tgt.get("fb_port"), tgt.get("tt_port")]))
            for p in required_ports:
                if ensure_port(p):
                    started_ports.add(p)

            try:
                # YouTube
                if args.platform in ["yt", "all"]:
                    print(f"[{ch_name}] Đang quét YouTube Studio (cổng {tgt['yt_port']})...")
                    yt = YouTubeStudioAdapter(port=tgt["yt_port"])
                    yt_res = yt.scan_and_engage(
                        channel_id=tgt["yt_channel_id"],
                        channel_name=ch_name,
                        ledger=ledger,
                        dry_run=args.dry_run,
                        limit_replies=args.limit
                    )
                    ch_results.extend(yt_res)
                    print(f"[{ch_name}] YouTube hoàn tất: {len(yt_res)} tương tác.")

                # Facebook Business
                if args.platform in ["fb", "all"]:
                    print(f"[{ch_name}] Đang quét Facebook Business Inbox (cổng {tgt['fb_port']})...")
                    fb = FacebookBusinessAdapter(port=tgt["fb_port"])
                    fb_res = fb.scan_and_engage(
                        asset_id=tgt["fb_asset_id"],
                        channel_name=ch_name,
                        ledger=ledger,
                        dry_run=args.dry_run,
                        limit_replies=args.limit
                    )
                    ch_results.extend(fb_res)
                    print(f"[{ch_name}] Facebook hoàn tất: {len(fb_res)} tương tác.")

                # TikTok Studio
                if args.platform in ["tt", "all"]:
                    print(f"[{ch_name}] Đang quét TikTok Studio (cổng {tgt['tt_port']})...")
                    tt = TikTokStudioAdapter(port=tgt["tt_port"])
                    tt_res = tt.scan_and_engage(
                        channel_name=ch_name,
                        ledger=ledger,
                        dry_run=args.dry_run,
                        limit_replies=args.limit
                    )
                    ch_results.extend(tt_res)
                    print(f"[{ch_name}] TikTok hoàn tất: {len(tt_res)} tương tác.")

            finally:
                for p in started_ports:
                    if p != 9333:  # Giữ cổng 9333 cho FB chung
                        print(f"[{ch_name}] Đóng Chrome cổng {p} sau khi tương tác xong...")
                        close_port(p)

            if args.notify_telegram:
                ch_stats = aggregate_stats(ch_results)
                try:
                    from ops.telegram import notifier
                    notifier.notify_engagement_report(
                        channel=ch_name,
                        stats=ch_stats,
                        dry_run=args.dry_run
                    )
                    print(f"[{ch_name}] Đã gửi báo cáo kết quả tương tác tới Telegram.")
                except Exception as e:
                    print(f"[{ch_name}] Lỗi gửi báo cáo Telegram: {e}")

    finally:
        eng_lock.release()
        print("[Runner] Đã dọn lock và kết thúc phiên engagement thành công.")

if __name__ == "__main__":
    main()
