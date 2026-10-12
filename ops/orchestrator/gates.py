import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from ops.render.config import get_render_config
from ops.render.validator import validate_motion_deck, validate_zen_meditation
from ops.publish.cli import run_dry_run as run_publish_dry_run

@dataclass
class GateResult:
    gate: int
    name: str
    channel: str
    slug: str
    passed: bool
    est_duration: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

def evaluate_gate1(channel: str, slug: str, root_dir: Optional[str] = None) -> GateResult:
    """Evaluate Quality Gate 1: Script & Assets Validation."""
    try:
        spec = get_render_config(channel, slug, root_dir=root_dir)
    except Exception as e:
        return GateResult(
            gate=1,
            name="Script & Assets Approval",
            channel=channel,
            slug=slug,
            passed=False,
            errors=[f"Lỗi cấu hình render: {e}"]
        )

    if spec.engine_type == "motion_deck":
        errors, warnings, est_dur = validate_motion_deck(spec.content_path, shots_dir=spec.shots_dir)
    elif spec.engine_type == "zen_meditation":
        errors, warnings, est_dur = validate_zen_meditation(spec.content_path, content_dir=spec.content_dir)
    else:
        errors = [f"Unsupported engine type: {spec.engine_type}"]
        warnings = []
        est_dur = 0.0

    return GateResult(
        gate=1,
        name="Script & Assets Approval",
        channel=channel,
        slug=slug,
        passed=len(errors) == 0,
        est_duration=est_dur,
        errors=errors,
        warnings=warnings,
        details={
            "content_path": spec.content_path,
            "engine_type": spec.engine_type
        }
    )

def evaluate_gate2(channel: str, slug: str, platform: str = "all", at_time: Optional[str] = None, root_dir: Optional[str] = None) -> GateResult:
    """Evaluate Quality Gate 2: Rendered Video & Pre-Publish Readiness."""
    pub_res = run_publish_dry_run(channel=channel, slug=slug, platform=platform, at_time=at_time, root_dir=root_dir)
    
    return GateResult(
        gate=2,
        name="Video & Publish Readiness",
        channel=channel,
        slug=slug,
        passed=pub_res["valid"],
        errors=pub_res.get("errors", []),
        warnings=pub_res.get("warnings", []),
        details=pub_res
    )
