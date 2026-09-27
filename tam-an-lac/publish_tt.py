"""Đăng lên TikTok cho kênh Tâm An Lạc. Một tab duy nhất, đầy đủ caption."""
import os
import re
import time
from playwright.sync_api import sync_playwright
import urllib.request

ROOT_DIR = "/Users/thientm/Documents/GitHub/me/tam-an-lac"
VIDEO_PATH = os.path.join(ROOT_DIR, "content", "001_khau_nghiep", "video.mp4")
CAPTION = "Đỉnh cao của sự buông bỏ - Lời Phật Dạy 🙏 #tamanlac #phatphap #trietly #cuocsong #loiphatday"
PORT = 9555

OVERLAY = "div.TUXModal-overlay"

def overlay_on(q):
    try:
        return q.locator(OVERLAY).count() > 0 and q.locator(OVERLAY).first.is_visible()
    except:
        return False

def clear_overlay(q):
    for _ in range(6):
        if not overlay_on(q):
            return
        q.keyboard.press("Escape")
        q.wait_for_timeout(2000)

def main():
    print("🚀 [TikTok] Bắt đầu upload đầy đủ (caption + post)")
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
        ctx = browser.contexts[0]
        q = ctx.new_page()
        q.set_default_timeout(120000)

        try:
            # 1. Mở trang upload
            print("  -> Mở TikTok Studio Upload...")
            q.goto("https://www.tiktok.com/tiktokstudio/upload?from=webapp", wait_until="domcontentloaded")
            q.wait_for_timeout(10000)

            # 2. Chọn file video
            print("  -> Đang chọn file video...")
            q.locator("input[type=file]").first.set_input_files(VIDEO_PATH)
            print("  -> Đã chọn file, chờ upload...")

            # Chờ video upload xong
            for _ in range(30):
                q.wait_for_timeout(3000)
                if "Uploaded" in q.inner_text("body"):
                    break
            print("  -> Upload xong!")

            # 3. Điền caption (giống thien-tran/tt.py)
            print("  -> Đang điền caption...")
            ed = q.locator("div[contenteditable='true']").first
            ed.click()
            q.keyboard.press("Meta+a")
            q.keyboard.press("Delete")
            q.wait_for_timeout(500)

            # Tách phần chữ và hashtag
            body, _, tags = CAPTION.partition(" #")
            q.keyboard.insert_text(body + " ")
            q.wait_for_timeout(800)

            # Gõ từng hashtag riêng (để TikTok nhận diện tag)
            for tok in ("#" + tags).split(" ") if tags else []:
                q.keyboard.type(tok, delay=10)
                if tok.startswith("#"):
                    q.wait_for_timeout(350)
                    q.keyboard.press("Escape")  # đóng menu hashtag
                q.keyboard.type(" ", delay=10)
            q.wait_for_timeout(1500)

            caption_text = ed.inner_text()[:120]
            print(f"  -> Caption: {caption_text}")

            # 4. Chờ TikTok kiểm tra xong
            print("  -> Chờ TikTok kiểm tra video...")
            for i in range(30):
                if q.inner_text("body").count("No issues found") >= 2:
                    print(f"  -> Checks xong sau ~{i*3}s")
                    break
                q.wait_for_timeout(3000)

            # 5. Bấm Post
            print("  -> Đang bấm Post...")
            clear_overlay(q)
            btn = q.get_by_role("button", name="Post", exact=True)
            if not btn.count():
                print("❌ Không tìm thấy nút Post!")
                return
            btn.last.click()
            q.wait_for_timeout(8000)
            clear_overlay(q)
            q.wait_for_timeout(14000)

            print("✅ [TikTok] Đã đăng thành công với đầy đủ caption!")
            print("  -> URL:", q.url)

        except Exception as e:
            print(f"❌ Lỗi TikTok: {e}")
        finally:
            q.close()

if __name__ == "__main__":
    main()
