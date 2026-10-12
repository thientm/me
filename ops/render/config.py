import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RenderSpec:
    channel: str
    slug: str
    engine_type: str  # 'motion_deck' or 'zen_meditation'
    content_path: str
    output_video: str
    shots_dir: Optional[str] = None
    content_dir: Optional[str] = None

def get_render_config(channel: str, slug: str, root_dir: Optional[str] = None) -> RenderSpec:
    root = root_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    if channel == "me-tech":
        return RenderSpec(
            channel=channel,
            slug=slug,
            engine_type="motion_deck",
            content_path=os.path.join(root, "me-tech", "pipeline", "content", f"{slug}.json"),
            output_video=os.path.join(root, "me-tech", "render", f"{slug}.mp4"),
            shots_dir=os.path.join(root, "me-tech", "pipeline", "shots")
        )
    elif channel == "thien-tran":
        return RenderSpec(
            channel=channel,
            slug=slug,
            engine_type="motion_deck",
            content_path=os.path.join(root, "thien-tran", "content", f"{slug}.json"),
            output_video=os.path.join(root, "thien-tran", "render", f"{slug}.mp4"),
            shots_dir=os.path.join(root, "thien-tran", "shots")
        )
    elif channel == "tam-an-lac":
        content_dir = os.path.join(root, "tam-an-lac", "content", slug)
        return RenderSpec(
            channel=channel,
            slug=slug,
            engine_type="zen_meditation",
            content_path=os.path.join(content_dir, "script.json"),
            output_video=os.path.join(content_dir, "video.mp4"),
            content_dir=content_dir
        )
    else:
        raise ValueError(f"Unknown channel: {channel}. Expected one of: me-tech, thien-tran, tam-an-lac")
