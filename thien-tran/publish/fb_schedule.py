import os, re, sys, time
sys.path.insert(0, ".")
import ledger
from meta import VIDEO

ledger.guard(VIDEO, "facebook", force=("--force" in sys.argv))

from playwright.sync_api import sync_playwright

def find_composer_tab(ctx):
    for x in ctx.pages:
        if not x.url.startswith("https://www.facebook.com"):
            continue
        try:
            t = x.inner_text("body")
            if "Meta vừa tung ra siêu mẫu Muse Wonder" in t or "Reel settings" in t:
                return x
        except Exception:
            pass
    raise RuntimeError("Khong tim thay tab Reel composer")

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9333")
    ctx = b.contexts[0]
    p = find_composer_tab(ctx)
    print("Tim thay tab:", p.url)

    # 1. Dong goi y hashtag
    try:
        p.get_by_text("Reel settings", exact=True).first.click()
        p.wait_for_timeout(1500)
    except Exception:
        pass

    # 2. Cho kiem tra ban quyen
    print("Cho copyright check...")
    for _ in range(40):
        if "Checking for copyrighted content" not in p.inner_text("body"):
            break
        p.wait_for_timeout(3000)

    body = p.inner_text("body")
    print("public:", "Public\nAnyone on or off Facebook" in body, "| safe:", "safe to publish" in body)

    # 3. Mo Scheduling options
    p.locator("[role=button]:has-text('Scheduling options')").first.click()
    p.wait_for_timeout(2500)

    # 4. Dien gio 08:00
    t = [e for e in p.locator("input[type=text]").all() if e.is_visible() and ":" in e.input_value()][0]
    t.click()
    p.wait_for_timeout(500)
    p.keyboard.press("Meta+A")
    p.keyboard.type("08:00", delay=120)
    p.wait_for_timeout(800)
    p.keyboard.press("Tab")
    p.wait_for_timeout(1000)

    vals = [e.input_value() for e in p.locator("input[type=text]").all() if e.is_visible()]
    print("vals:", vals)
    assert "08:00" in vals and "14 Oct 2026" in vals, f"Gia tri gio khong dung: {vals}"

    # 5. Bam Schedule for later
    p.get_by_text("Schedule for later", exact=True).first.click()
    p.wait_for_timeout(2500)

    body = p.inner_text("body")
    print("today08:", "Today at 08:00" in body, "| public:", "Public\nAnyone on or off Facebook" in body, "| safe:", "safe to publish" in body)
    assert "Today at 08:00" in body and "Public\nAnyone on or off Facebook" in body and "safe to publish" in body

    # 6. Bam nut Schedule
    btn = [x for x in p.get_by_role("button", name=re.compile(r"^\s*(Schedule|Lên lịch)\s*$")).all() if x.is_visible()][-1]
    print("nut disabled:", btn.get_attribute("aria-disabled"))
    btn.focus()
    p.wait_for_timeout(300)
    p.keyboard.press("Enter")
    print("Da bam Enter tren nut Schedule")
    p.wait_for_timeout(20000)

    # 7. Record ledger
    import ledger
    from meta import VIDEO
    ledger.record(VIDEO, "facebook", "hen 08:00")
    print("Hen gio Facebook thien-tran hoan tat.")
