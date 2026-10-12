import os
import sys
import argparse
import datetime as dt
from typing import Optional, List, Dict, Any

from ops.orchestrator.slot import check_all_channels, check_channel_slot, get_current_slot
from ops.orchestrator.gates import evaluate_gate1, evaluate_gate2, GateResult

def _get_active_slug(channel: str, root_dir: str) -> Optional[str]:
    """Find current active slug for a channel from ACTIVE file or content directory."""
    if channel == "me-tech":
        active_f = os.path.join(root_dir, "me-tech", "pipeline", "publish", "ACTIVE")
    elif channel == "thien-tran":
        active_f = os.path.join(root_dir, "thien-tran", "publish", "ACTIVE")
    else:
        active_f = os.path.join(root_dir, "tam-an-lac", "_pubkit", "a", "publish", "ACTIVE")
    
    if os.path.exists(active_f):
        try:
            with open(active_f, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
        except Exception:
            pass
    return None

def run_orchestration_dashboard(slot: Optional[int] = None, channel: str = "all", slug: Optional[str] = None, root_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate pipeline orchestration dashboard across channels."""
    root = root_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target_slot = slot if slot is not None else get_current_slot()
    
    channels_to_check = ["me-tech", "thien-tran", "tam-an-lac"] if channel == "all" else [channel]
    
    channel_status = {}
    ok = True

    for ch in channels_to_check:
        s_res = check_channel_slot(ch, slot=target_slot, root_dir=root)
        
        # Check active slug
        current_slug = slug if (slug and channel != "all") else s_res.get("slug") or _get_active_slug(ch, root)
        
        g1_res = None
        g2_res = None
        if current_slug:
            g1_res = evaluate_gate1(ch, current_slug, root_dir=root)
            g2_res = evaluate_gate2(ch, current_slug, root_dir=root)
            if not g1_res.passed or not g2_res.passed:
                # Notice: not fatal for slot check, but noted
                pass

        channel_status[ch] = {
            "slot_status": s_res,
            "active_slug": current_slug,
            "gate1": g1_res,
            "gate2": g2_res
        }

    return {
        "ok": ok,
        "slot": target_slot,
        "channel": channel,
        "channels": channel_status,
        "timestamp": dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    }

def print_dashboard(dash: Dict[str, Any]) -> None:
    sep = "=" * 68
    sub_sep = "-" * 68
    print(sep)
    print(f"📡 3-CHANNEL VIDEO PIPELINE ORCHESTRATOR DASHBOARD")
    slot_num = dash.get('slot', 8)
    ts = dash.get('timestamp', '')
    print(f"• Khung giờ: {slot_num:02d}:00 | Thời gian quét: {ts}")
    print(sep)

    for ch, data in dash["channels"].items():
        s = data["slot_status"]
        status_tag = f"[{s['status'].upper()}]"
        if s["status"] == "done":
            status_desc = f"✓ Đã đủ 3 nền tảng ({', '.join(s['posted'])})"
        elif s["status"] == "partial":
            status_desc = f"⚠ Đang thiếu: {', '.join(s['missing'])} (Slug: {s['slug']})"
        else:
            status_desc = f"○ Chưa có bài nào trong khung {s['slot']:02d}:00"

        print(f"\n▶ [{ch.upper()}] — Trạng thái: {status_tag} {status_desc}")
        
        slug = data["active_slug"]
        if slug:
            print(f"  • Bài đang chọn (Slug): {slug}")
            g1 = data["gate1"]
            if g1:
                g1_tag = "✓ PASS" if g1.passed else "✗ FAIL"
                print(f"  • Gate 1 (Kịch bản & Assets): [{g1_tag}] (Ước lượng: {g1.est_duration}s)")
                if g1.errors:
                    for e in g1.errors:
                        print(f"      - [Lỗi G1] {e}")

            g2 = data["gate2"]
            if g2:
                g2_tag = "✓ PASS" if g2.passed else "✗ FAIL"
                print(f"  • Gate 2 (Video & Publish):    [{g2_tag}]")
                if g2.errors:
                    for e in g2.errors:
                        print(f"      - [Lỗi G2] {e}")
        else:
            print("  • Chưa có bài nào được gán cho khung giờ này")

    print(f"\n{sep}")
    print("💡 HƯỚNG DẪN ĐIỀU PHỐI:")
    print("1. Nếu kênh có trạng thái NONE: chạy lệnh brainstorm kịch bản cho đề tài mới.")
    print("2. Kiểm tra Gate 1:  python3 -m ops.render.cli --channel <ch> --slug <slug> --dry-run")
    print("3. Kiểm tra Gate 2:  python3 -m ops.publish.cli --channel <ch> --slug <slug> --dry-run")
    print(sep)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified 3-Channel Pipeline Orchestrator")
    parser.add_argument("--slot", type=int, choices=[8, 12, 20], default=None, help="Publishing slot (8, 12, 20)")
    parser.add_argument("--channel", choices=["all", "me-tech", "thien-tran", "tam-an-lac"], default="all", help="Target channel")
    parser.add_argument("--slug", default=None, help="Specific slug to verify Quality Gates")
    parser.add_argument("--dry-run", action="store_true", help="Run dashboard checks without mutating state")
    return parser

def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    dash = run_orchestration_dashboard(
        slot=args.slot,
        channel=args.channel,
        slug=args.slug
    )
    print_dashboard(dash)
    return 0 if dash["ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
