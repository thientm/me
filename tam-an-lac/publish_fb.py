"""Đăng Reel lên Page Tâm An Lạc qua Meta Business Suite.

Lưu ý (27.09.2026):
- Reels composer KHÔNG có sẵn input[type=file] — phải bấm "Add video" và bắt file chooser.
- Không dùng facebook.com/reels/create: profile Chrome đang đứng ở tài khoản cá nhân,
  sẽ đăng nhầm lên trang cá nhân thay vì Page.
"""
import argparse
import os
import urllib.request
from playwright.sync_api import sync_playwright

ROOT_DIR = "/Users/thientm/Documents/GitHub/me/tam-an-lac"
VIDEO_PATH = os.path.join(ROOT_DIR, "content", "001_khau_nghiep", "video.mp4")
CAPTION = "Đỉnh cao của sự buông bỏ - Lời Phật Dạy 🙏\nTâm An Lạc mang đến những triết lý Phật Pháp giúp bạn tìm thấy sự bình yên trong tâm hồn."
TAGS = "#tamanlac #phatphap #loiphatday #trietly #cuocsong"
PAGE_ID = "686899491163120"
PORT = 9555

ap = argparse.ArgumentParser()
ap.add_argument("--draft", action="store_true", help="Điền xong tới bước Share, không bấm Share")
DRAFT = ap.parse_args().draft


def wait_enabled(btn, page, tries=60):
    for _ in range(tries):
        if btn.get_attribute("aria-disabled") != "true":
            return
        page.wait_for_timeout(2000)


def main():
    print("🚀 [Facebook] Đăng Reel lên Page Tâm An Lạc")
    if not os.path.exists(VIDEO_PATH):
        print("❌ Không tìm thấy video:", VIDEO_PATH)
        return
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    except Exception:
        print(f"❌ Chrome chưa chạy ở cổng {PORT}. Chạy ./open_browser.sh trước.")
        return

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].new_page()
        page.set_default_timeout(30000)

        try:
            print("  -> Mở Reels composer...")
            page.goto(f"https://business.facebook.com/latest/reels_composer/?asset_id={PAGE_ID}",
                      wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            print("  -> Bấm Add video và nạp file...")
            with page.expect_file_chooser() as fc:
                page.locator("[role=button]", has_text="Add video").first.click()
            fc.value.set_files(VIDEO_PATH)
            page.wait_for_timeout(20000)

            print("  -> Điền caption...")
            tb = page.locator("div[role=textbox][contenteditable=true]").first
            tb.click()
            page.keyboard.press("Meta+a")
            page.keyboard.press("Delete")
            for i, line in enumerate(CAPTION.split("\n")):
                if i:
                    page.keyboard.press("Shift+Enter")
                page.keyboard.insert_text(line)
            page.keyboard.press("Shift+Enter")
            page.keyboard.press("Shift+Enter")
            for tag in TAGS.split():
                page.keyboard.type(tag, delay=15)
                page.wait_for_timeout(400)
                page.keyboard.press("Escape")  # đóng menu hashtag
                page.keyboard.type(" ")
            print("  -> Caption:", tb.inner_text().replace("\n", " ")[:120])

            print("  -> Next x2 (Create -> Edit -> Share)...")
            for _ in range(2):
                nb = page.locator("[role=button]", has_text="Next").last
                wait_enabled(nb, page)
                nb.click()
                page.wait_for_timeout(4000)

            if DRAFT:
                print("⏸️ --draft: đã tới bước Share, chưa bấm. Kiểm tra rồi bấm Share tay.")
                return

            page.get_by_role("button", name="Share", exact=True).last.click()
            page.wait_for_timeout(20000)
            print("✅ [Facebook] Đã bấm Share. Kiểm tra: "
                  f"https://business.facebook.com/latest/posts/published_posts/?asset_id={PAGE_ID}")
        except Exception as e:
            print(f"❌ Lỗi Facebook: {e}")


if __name__ == "__main__":
    main()
