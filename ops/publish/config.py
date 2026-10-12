import os
import json
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ChannelConfig:
    name: str
    cdp_port: int
    fb_cdp_port: int
    yt_channel_id: str
    tt_username: str
    fb_type: str
    fb_asset_id: Optional[str]
    browser_profile: str

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "channels.json")

def load_all_configs(config_path: str = _CONFIG_PATH) -> Dict[str, ChannelConfig]:
    with open(config_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    res = {}
    for k, v in raw.items():
        res[k] = ChannelConfig(
            name=v["name"],
            cdp_port=v["cdp_port"],
            fb_cdp_port=v.get("fb_cdp_port", 9333),
            yt_channel_id=v["yt_channel_id"],
            tt_username=v["tt_username"],
            fb_type=v["fb_type"],
            fb_asset_id=v.get("fb_asset_id"),
            browser_profile=v.get("browser_profile", "")
        )
    return res

def get_channel_config(channel: str, config_path: str = _CONFIG_PATH) -> ChannelConfig:
    configs = load_all_configs(config_path)
    if channel not in configs:
        raise ValueError(f"Unknown channel: {channel}. Expected one of: {list(configs.keys())}")
    return configs[channel]
