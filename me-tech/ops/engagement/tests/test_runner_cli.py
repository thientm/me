import pytest
from runner import parse_args, build_channel_targets

def test_runner_args():
    args = parse_args(["--channel", "metech", "--dry-run", "--limit", "3"])
    assert args.channel == "metech"
    assert args.dry_run is True
    assert args.limit == 3

def test_build_channel_targets_metech():
    targets = build_channel_targets("metech")
    assert len(targets) == 1
    t = targets[0]
    assert t["name"] == "metech"
    assert t["yt_port"] == 9333
    assert t["yt_channel_id"] == "UCnElgDX9q_AYGdFc2oDuWUA"

def test_build_channel_targets_tamanlac():
    targets = build_channel_targets("tamanlac")
    assert len(targets) == 1
    t = targets[0]
    assert t["name"] == "tamanlac"
    assert t["yt_port"] == 9555
    assert t["yt_channel_id"] == "UCjEteQMJ4zzFV9_iKvChpvA"

def test_build_channel_targets_all():
    targets = build_channel_targets("all")
    assert len(targets) == 2
