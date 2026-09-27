import os
import time
from playwright.sync_api import sync_playwright
import urllib.request
import sys

ROOT_DIR = "/Users/thientm/Documents/GitHub/me/tam-an-lac"
VIDEO_PATH = os.path.join(ROOT_DIR, "content", "001_khau_nghiep", "video.mp4")
TITLE = "Đỉnh cao của sự buông bỏ - Lời Phật Dạy 🙏 #tamanlac #phatphap #trietly #cuocsong"
PORT = 9555

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
            
            print("  -> Chờ xử lý video (15s)...")
            time.sleep(15)
            
            print("✅ [YouTube] Đã tải video lên thành công! (Dừng ở bản nháp để bạn kiểm tra và bấm Đăng)")
        except Exception as e:
            print(f"❌ Lỗi YouTube: {e}")
            
if __name__ == "__main__":
    main()
