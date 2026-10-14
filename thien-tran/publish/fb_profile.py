"""Reel lên trang cá nhân thientm qua Chrome me-tech (9333). Mặc định chỉ điền, --post mới bấm."""
import re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, ".")
from meta import VIDEO, FB_CAPTION
POST = "--post" in sys.argv
with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9333"); ctx = b.contexts[0]
    if not POST:
        p = ctx.new_page(); p.set_default_timeout(120000)
        p.goto("https://www.facebook.com/reels/create", wait_until="domcontentloaded"); p.wait_for_timeout(5000)
        p.locator("input[type=file]").first.set_input_files(VIDEO); p.wait_for_timeout(6000)
        for step in (1, 2):
            for _ in range(30):
                nb = p.get_by_role("button", name=re.compile(r"^\s*(Next|Tiếp)\s*$")).first
                if nb.count() and nb.is_visible() and nb.get_attribute("aria-disabled") != "true":
                    nb.click(); p.wait_for_timeout(2500); print("Next", step); break
                p.wait_for_timeout(1000)
        tb = p.locator('div[role="textbox"][contenteditable="true"]').first
        tb.click(); p.wait_for_timeout(500)
        for i, line in enumerate(FB_CAPTION.split("\n")):
            if i: p.keyboard.press("Shift+Enter")
            p.keyboard.insert_text(line)
        p.wait_for_timeout(2000)
        print("caption:", " ".join(tb.inner_text().split())[:100])
        p.screenshot(path="_scratch/fb_profile_draft.png")
    else:
        # URL tab tự đổi sang /reel/<id của người khác> dù hộp soạn vẫn mở -> tìm theo nội dung
        p = [x for x in ctx.pages if "facebook.com" in x.url and "Reel settings" in x.inner_text("body")][-1]
        p.get_by_text("Reel settings", exact=True).first.click(); p.wait_for_timeout(1500)  # đóng menu gợi ý hashtag
        for _ in range(40):
            if "Checking for copyrighted content" not in p.inner_text("body"): break
            p.wait_for_timeout(3000)
        for c in p.get_by_role("button", name=re.compile(r"^(Close|Đóng)$")).all():  # thông báo chế độ tối che nút
            try:
                if c.is_visible() and "dark mode" in (c.locator("xpath=ancestor::div[3]").inner_text() or ""): c.click()
            except Exception: pass
        btn = [x for x in p.get_by_role("button", name=re.compile(r"^\s*(Post|Publish|Đăng)\s*$")).all() if x.is_visible()][-1]
        print("post disabled:", btn.get_attribute("aria-disabled")); btn.click(); p.wait_for_timeout(20000)
        p.screenshot(path="_scratch/fb_profile_after.png"); print("url:", p.url)
        try:
            import ledger
            ledger.record(VIDEO, "facebook", "dang ngay")
            print("Ledger recorded: facebook")
        except Exception as e:
            print("Ledger recording failed:", e)

