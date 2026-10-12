import os
import json
import pytest
from ledger import EngagementLedger
from lock import check_conflicts, EngagementLock

def test_ledger_record_and_has(tmp_path):
    ledger_file = tmp_path / "ledger.json"
    ledger = EngagementLedger(str(ledger_file))
    assert not ledger.has("yt:123")
    ledger.record("yt:123", "User A", ["heart", "like"], "Thanks!")
    ledger.save()
    
    # Reload from disk
    new_ledger = EngagementLedger(str(ledger_file))
    assert new_ledger.has("yt:123")
    entry = new_ledger.get("yt:123")
    assert entry["author"] == "User A"
    assert entry["actions"] == ["heart", "like"]
    assert entry["reply_text"] == "Thanks!"

def test_lock_conflict_detection(tmp_path):
    build_lock = tmp_path / "build.lock"
    build_lock.touch()
    assert check_conflicts([str(build_lock)]) is True

    non_existent = tmp_path / "other.lock"
    assert check_conflicts([str(non_existent)]) is False

def test_engagement_lock_acquisition(tmp_path):
    lock_file = tmp_path / "engagement.lock"
    lock = EngagementLock(str(lock_file))
    assert lock.acquire() is True
    # Second acquisition fails
    lock2 = EngagementLock(str(lock_file))
    assert lock2.acquire() is False
    lock.release()
    assert not lock_file.exists()
