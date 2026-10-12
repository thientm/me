import os
import sys
import argparse
import urllib.request
from typing import Optional, List, Tuple, Dict, Any

from ops.publish.config import get_channel_config, ChannelConfig
from ops.publish.meta_loader import load_meta, MetaData

def validate_meta(meta: MetaData) -> Tuple[List[str], List[str]]:
    """Validate metadata fields and video file existence.
    Returns (errors, warnings).
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(meta.video_path):
        errors.append(f"Video file not found: {meta.video_path}")

    # YouTube Shorts: title max 100 characters
    if len(meta.yt_title) > 100:
        errors.append(f"YouTube title exceeds 100 chars limit (current: {len(meta.yt_title)} chars)")
    elif not meta.yt_title.strip():
        warnings.append("YouTube title is empty")

    # TikTok: caption max 2200 characters
    if len(meta.tt_caption) > 2200:
        errors.append(f"TikTok caption exceeds 2200 chars limit (current: {len(meta.tt_caption)} chars)")
    elif not meta.tt_caption.strip():
        warnings.append("TikTok caption is empty")

    # Facebook caption
    if len(meta.fb_caption) > 5000:
        warnings.append(f"Facebook caption is unusually long ({len(meta.fb_caption)} chars)")
    elif not meta.fb_caption.strip():
        warnings.append("Facebook caption is empty")

    return errors, warnings

def check_cdp_connection(port: int, timeout: float = 2.0) -> bool:
    """Check if Chrome DevTools Protocol port is open and responding."""
    url = f"http://127.0.0.1:{port}/json/version"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def run_dry_run(channel: str, slug: str, platform: str = "all", at_time: Optional[str] = None, root_dir: Optional[str] = None) -> Dict[str, Any]:
    """Execute dry-run validations for a channel and slug."""
    cfg = get_channel_config(channel)
    meta = load_meta(channel=channel, slug=slug, root_dir=root_dir)

    errors, warnings = validate_meta(meta)

    main_cdp = check_cdp_connection(cfg.cdp_port)
    fb_cdp = check_cdp_connection(cfg.fb_cdp_port) if platform in ("all", "fb") else None

    if not main_cdp:
        warnings.append(f"Chrome CDP port {cfg.cdp_port} is not accessible (Browser offline?)")
    if fb_cdp is False:
        warnings.append(f"Facebook Chrome CDP port {cfg.fb_cdp_port} is not accessible")

    return {
        "valid": len(errors) == 0,
        "channel": channel,
        "slug": slug,
        "platform": platform,
        "at_time": at_time,
        "video_path": meta.video_path,
        "video_exists": os.path.exists(meta.video_path),
        "meta": {
            "yt_title": meta.yt_title,
            "yt_title_len": len(meta.yt_title),
            "tt_caption": meta.tt_caption,
            "tt_caption_len": len(meta.tt_caption),
            "fb_caption": meta.fb_caption,
            "fb_caption_len": len(meta.fb_caption),
        },
        "cdp": {
            "main_port": cfg.cdp_port,
            "main_connected": main_cdp,
            "fb_port": cfg.fb_cdp_port,
            "fb_connected": fb_cdp,
        },
        "errors": errors,
        "warnings": warnings,
    }

def print_dry_run_report(result: Dict[str, Any]) -> None:
    sep = "=" * 60
    print(sep)
    print(f"🔍 DRY RUN REPORT: [{result['channel'].upper()}] - {result['slug']}")
    print(sep)
    print(f"• Platform target: {result['platform']}")
    if result.get("at_time"):
        print(f"• Schedule at:     {result['at_time']}")
    
    video_status = "✓ FOUND" if result["video_exists"] else "✗ MISSING"
    print(f"• Video file:      {result['video_path']} [{video_status}]")

    m = result["meta"]
    print(f"• YT Title:        ({m['yt_title_len']}/100 chars) {m['yt_title'][:50]}...")
    print(f"• TT Caption:      ({m['tt_caption_len']}/2200 chars)")
    print(f"• FB Caption:      ({m['fb_caption_len']} chars)")

    cdp = result["cdp"]
    main_cdp_stat = "✓ CONNECTED" if cdp["main_connected"] else "✗ OFFLINE"
    print(f"• Main CDP (Port {cdp['main_port']}): {main_cdp_stat}")
    if cdp["fb_port"] is not None:
        fb_cdp_stat = "✓ CONNECTED" if cdp["fb_connected"] else "✗ OFFLINE"
        print(f"• FB CDP   (Port {cdp['fb_port']}): {fb_cdp_stat}")

    if result["warnings"]:
        print("\n⚠️ WARNINGS:")
        for w in result["warnings"]:
            print(f"  - {w}")

    if result["errors"]:
        print("\n❌ ERRORS:")
        for e in result["errors"]:
            print(f"  - {e}")

    print(sep)
    if result["valid"]:
        print("✅ DRY RUN PASSED - Ready to publish")
    else:
        print("❌ DRY RUN FAILED - Please resolve errors before publishing")
    print(sep)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified Multi-Channel Publisher CLI")
    parser.add_argument("--channel", required=True, choices=["me-tech", "thien-tran", "tam-an-lac"], help="Target channel")
    parser.add_argument("--slug", required=True, help="Content slug")
    parser.add_argument("--platform", choices=["all", "yt", "tt", "fb"], default="all", help="Target platform (default: all)")
    parser.add_argument("--at", default=None, help="Scheduled publish time (e.g. 08:00, 12:00, 20:00)")
    parser.add_argument("--dry-run", action="store_true", help="Validate metadata, video, and connection without publishing")
    return parser

def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.dry_run:
        result = run_dry_run(
            channel=args.channel,
            slug=args.slug,
            platform=args.platform,
            at_time=args.at
        )
        print_dry_run_report(result)
        return 0 if result["valid"] else 1
    else:
        # Non-dry-run mode: Perform dry-run checks first
        result = run_dry_run(
            channel=args.channel,
            slug=args.slug,
            platform=args.platform,
            at_time=args.at
        )
        if not result["valid"]:
            print_dry_run_report(result)
            print("[ERROR] Cannot publish: validation failed.")
            return 1
        
        # When dry run passes, invoke channel-specific publish runner
        print(f"[INFO] Publishing {args.slug} on {args.channel} ({args.platform})...")
        # Legacy bridge: update ACTIVE file if applicable
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if args.channel == "me-tech":
            active_file = os.path.join(root_dir, "me-tech", "pipeline", "publish", "ACTIVE")
            if os.path.exists(os.path.dirname(active_file)):
                with open(active_file, "w", encoding="utf-8") as f:
                    f.write(args.slug)
        elif args.channel == "thien-tran":
            active_file = os.path.join(root_dir, "thien-tran", "publish", "ACTIVE")
            if os.path.exists(os.path.dirname(active_file)):
                with open(active_file, "w", encoding="utf-8") as f:
                    f.write(args.slug)
        return 0

if __name__ == "__main__":
    sys.exit(main())
