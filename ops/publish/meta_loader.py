import os
import json
import sys
import importlib.util
from dataclasses import dataclass
from typing import Optional

@dataclass
class MetaData:
    video_path: str
    yt_title: str
    yt_desc: str
    fb_caption: str
    tt_caption: str
    slug: str
    channel: str

def load_meta(channel: str, slug: str, root_dir: Optional[str] = None, legacy_dir: Optional[str] = None) -> MetaData:
    """Load metadata for a given channel and slug.
    
    Priority:
    1. content/<slug>/meta.json
    2. legacy_dir/meta_<slug>.py (Backward compatibility)
    """
    root = root_dir or os.getcwd()
    channel_dir = os.path.join(root, channel) if not root.endswith(channel) else root
    
    # Check 1: content/<slug>/meta.json
    candidates_json = [
        os.path.join(channel_dir, "content", slug, "meta.json"),
        os.path.join(root, "content", slug, "meta.json"),
    ]
    
    for c_json in candidates_json:
        if os.path.exists(c_json):
            with open(c_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Resolve video path
            video_path = data.get("video")
            if not video_path:
                # auto discover video path
                video_candidates = [
                    os.path.join(os.path.dirname(c_json), "video.mp4"),
                    os.path.join(channel_dir, "render", f"{slug}.mp4"),
                    os.path.join(channel_dir, "_pubkit", f"{slug}.mp4"),
                    os.path.join(root, "render", f"{slug}.mp4"),
                ]
                for v in video_candidates:
                    if os.path.exists(v):
                        video_path = v
                        break
                if not video_path:
                    video_path = video_candidates[0]

            return MetaData(
                video_path=video_path,
                yt_title=data.get("yt_title", ""),
                yt_desc=data.get("yt_desc", ""),
                fb_caption=data.get("fb_caption", ""),
                tt_caption=data.get("tt_caption", ""),
                slug=slug,
                channel=channel
            )
            
    # Check 2: legacy meta_<slug>.py
    legacy_candidates = []
    if legacy_dir:
        legacy_candidates.append(os.path.join(legacy_dir, f"meta_{slug}.py"))
    legacy_candidates.extend([
        os.path.join(channel_dir, "pipeline", "publish", f"meta_{slug}.py"),
        os.path.join(channel_dir, "_pubkit", "a", "publish", f"meta_{slug}.py"),
        os.path.join(channel_dir, "publish", f"meta_{slug}.py"),
    ])
    
    for l_py in legacy_candidates:
        if os.path.exists(l_py):
            spec = importlib.util.spec_from_file_location("legacy_meta_" + slug.replace("-", "_"), l_py)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return MetaData(
                video_path=getattr(mod, "VIDEO", ""),
                yt_title=getattr(mod, "YT_TITLE", ""),
                yt_desc=getattr(mod, "YT_DESC", ""),
                fb_caption=getattr(mod, "FB_CAPTION", ""),
                tt_caption=getattr(mod, "TT_CAPTION", ""),
                slug=slug,
                channel=channel
            )
            
    raise FileNotFoundError(f"Cannot find metadata for channel '{channel}' and slug '{slug}'. Checked json and legacy py.")
