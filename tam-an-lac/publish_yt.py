import os
import time
from playwright.sync_api import sync_playwright
import urllib.request
import sys
import json
from identity import require_identity, guard, record, seen_on_platform

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # 29.09.2026: bỏ /Users/thientm/... cứng
SLUG = next((a for a in sys.argv[1:] if not a.startswith("-")), "002_y_dan_dau")
VIDEO_PATH = os.path.join(ROOT_DIR, "content", SLUG, "video.mp4")
META = json.load(open(os.path.join(ROOT_DIR, "content", SLUG, "meta.json"), encoding="utf-8"))
TITLE = META["yt_title"]
PORT = int(os.environ.get("TAL_PORT", "9555"))  # 29.09.2026: cổng đổi được (Chrome dùng chung)

def main():
    print("🚀 [YouTube] Bắt đầu quá trình upload (Tập trung)")
    if not os.path.exists(VIDEO_PATH):
        print("❌ LỖI: Không tìm thấy video.")
        return

    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    except Exception:
        print(f"❌ LỖI: Chrome chưa chạy ở cổng {PORT}. Hãy chạy ./open_browser.sh trước.")
        return

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        guard(SLUG, "youtube")
        require_identity(browser.contexts[0], "youtube")
        n = seen_on_platform(browser.contexts[0], "youtube", TITLE[:40])
        if n:
            sys.exit(f"[X] Kênh đã có {n} bài trùng tiêu đề — không upload lại.")
        page = browser.contexts[0].new_page()
        
        try:
            # Dùng URL trực tiếp mở modal upload của YouTube Studio
            upload_url = "https://studio.youtube.com/channel/UCjEteQMJ4zzFV9_iKvChpvA/videos/upload?d=ud"
            print(f"  -> Đang mở trang tải lên trực tiếp...")
            page.goto(upload_url, timeout=60000)
            
            print("  -> Chờ hộp thoại tải lên xuất hiện...")
            page.wait_for_selector('input[type="file"]', state="attached", timeout=30000)
            
            print("  -> Đang inject file video...")
            page.locator('input[type="file"]').set_input_files(VIDEO_PATH)
            
            # 29.09.2026: bản cũ dừng ở Draft (không tiêu đề). Hoàn tất theo me-tech/pipeline/publish/yt.py
            page.wait_for_selector("#title-textarea #textbox", timeout=120000)
            page.wait_for_timeout(3000)
            t = page.locator("#title-textarea #textbox").first
            t.click(); page.keyboard.press("Meta+a"); page.keyboard.press("Delete")
            t.type(TITLE, delay=6)
            d = page.locator("#description-textarea #textbox").first
            d.click(); d.type(META["yt_desc"], delay=3)
            page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first.click()
            print("  -> Tiêu đề:", t.inner_text()[:120])
            for i in range(3):
                page.click("#next-button"); page.wait_for_timeout(2500)
            page.locator("tp-yt-paper-radio-button[name='PUBLIC']").first.click()
            page.wait_for_timeout(1500)
            page.locator("#done-button").first.click()
            page.wait_for_timeout(14000)
            sh = page.locator("ytcp-video-share-dialog")
            print(sh.first.inner_text()[:400] if sh.count() else page.inner_text("body")[:300])
            page.screenshot(path=os.path.join(ROOT_DIR, "_scratch", "yt_done.png"))
            record(SLUG, "youtube", "dang ngay")
            print("✅ [YouTube] Đã bấm Publish (Public).")
        except Exception as e:
            print(f"❌ Lỗi YouTube: {e}")
            
if __name__ == "__main__":
    main()
