import os
import sys
import argparse
import subprocess
from typing import Optional, List, Dict, Any

from ops.render.config import get_render_config, RenderSpec
from ops.render.validator import validate_motion_deck, validate_zen_meditation
from ops.render.doctor import check_environment

def run_dry_run(channel: str, slug: str, root_dir: Optional[str] = None) -> Dict[str, Any]:
    """Execute dry-run validations for content, assets, and render environment."""
    spec = get_render_config(channel, slug, root_dir=root_dir)
    
    if spec.engine_type == "motion_deck":
        errors, warnings, est_duration = validate_motion_deck(spec.content_path, shots_dir=spec.shots_dir)
    elif spec.engine_type == "zen_meditation":
        errors, warnings, est_duration = validate_zen_meditation(spec.content_path, content_dir=spec.content_dir)
    else:
        errors = [f"Unsupported engine type: {spec.engine_type}"]
        warnings = []
        est_duration = 0.0

    doctor = check_environment()
    if not doctor["ok"]:
        for issue in doctor["issues"]:
            errors.append(f"[Môi trường] {issue}")

    return {
        "valid": len(errors) == 0,
        "channel": channel,
        "slug": slug,
        "engine_type": spec.engine_type,
        "content_path": spec.content_path,
        "output_video": spec.output_video,
        "est_duration": est_duration,
        "errors": errors,
        "warnings": warnings,
        "doctor": doctor
    }

def print_dry_run_report(result: Dict[str, Any]) -> None:
    sep = "=" * 62
    print(sep)
    print(f"🎬 PRE-FLIGHT RENDER REPORT: [{result['channel'].upper()}] - {result['slug']}")
    print(sep)
    print(f"• Engine Type:       {result['engine_type']}")
    print(f"• Content File:      {result['content_path']}")
    print(f"• Target Output:     {result['output_video']}")
    print(f"• Estimated Length:  {result['est_duration']}s")

    doc = result["doctor"]
    chk = doc["checks"]
    doc_summary = []
    for k, v in chk.items():
        doc_summary.append(f"{k}: {'✓' if v else '✗'}")
    print(f"• System Health:     {' '.join(doc_summary)}")

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
        print("✅ PRE-FLIGHT PASSED - Ready to render")
    else:
        print("❌ PRE-FLIGHT FAILED - Please resolve errors before rendering")
    print(sep)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified Multi-Channel Video Render CLI")
    parser.add_argument("--channel", choices=["me-tech", "thien-tran", "tam-an-lac"], help="Target channel")
    parser.add_argument("--slug", help="Content slug")
    parser.add_argument("--dry-run", action="store_true", help="Validate content, assets, and environment without rendering")
    parser.add_argument("--doctor", action="store_true", help="Check system render dependencies and environment")
    parser.add_argument("--skip-tts", action="store_true", help="Skip text-to-speech synthesis (use existing audio)")
    parser.add_argument("--vo-only", action="store_true", help="Generate voiceover audio only")
    return parser

def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.doctor and not args.channel:
        doc = check_environment()
        print("── System Render Doctor Check ──")
        for k, v in doc["checks"].items():
            print(f"  {'✓' if v else '✗'} {k}")
        if doc["issues"]:
            print("\n❌ Issues detected:")
            for issue in doc["issues"]:
                print(f"  - {issue}")
            return 1
        print("\n✅ System environment is fully ready for rendering!")
        return 0

    if not args.channel or not args.slug:
        parser.error("Both --channel and --slug are required unless running --doctor alone.")

    if args.dry_run:
        result = run_dry_run(channel=args.channel, slug=args.slug)
        print_dry_run_report(result)
        return 0 if result["valid"] else 1

    # Full render execution
    result = run_dry_run(channel=args.channel, slug=args.slug)
    if not result["valid"]:
        print_dry_run_report(result)
        print("[ERROR] Cannot start rendering: pre-flight validation failed.")
        return 1

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    spec = get_render_config(args.channel, args.slug, root_dir=root_dir)
    venv_py = os.path.join(root_dir, "me-tech", "pipeline", ".venv", "bin", "python")
    if not os.path.exists(venv_py):
        venv_py = sys.executable

    print(f"\n🚀 Starting render for [{args.channel}] slug: {args.slug}...")
    extra_flags = []
    if args.skip_tts:
        extra_flags.append("--skip-tts")
    if args.vo_only:
        extra_flags.append("--vo-only")

    env = dict(os.environ)
    env["HF_HUB_OFFLINE"] = "1"
    ca_pem = os.path.join(root_dir, "me-tech", "pipeline", "ca-bundle.pem")
    if os.path.exists(ca_pem):
        env["SSL_CERT_FILE"] = ca_pem
        env["REQUESTS_CA_BUNDLE"] = ca_pem

    if spec.engine_type == "motion_deck":
        build_script = os.path.join(root_dir, "core-video-engine", "build.py")
        cmd = [venv_py, build_script, spec.content_path] + extra_flags
        cwd = os.path.join(root_dir, "core-video-engine")
    elif spec.engine_type == "zen_meditation":
        build_script = os.path.join(root_dir, "tam-an-lac", "render_pipeline", "build.py")
        cmd = [venv_py, build_script, args.slug] + extra_flags
        cwd = os.path.join(root_dir, "tam-an-lac")
    else:
        print(f"Unknown engine: {spec.engine_type}")
        return 1

    proc = subprocess.run(cmd, cwd=cwd, env=env)
    return proc.returncode

if __name__ == "__main__":
    sys.exit(main())
