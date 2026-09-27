import os
import time
from playwright.sync_api import sync_playwright

# Configuration
ROOT_DIR = "/Users/thientm/Documents/GitHub/me/tam-an-lac"
PROFILE_DIR = os.path.join(ROOT_DIR, "chrome_profile")
VIDEO_PATH = os.path.join(ROOT_DIR, "content", "001_khau_nghiep", "video.mp4")

# SEO / Meta details
TITLE = "Đỉnh cao của sự buông bỏ - Lời Phật Dạy 🙏 #tamanlac #phatphap #trietly #cuocsong"

def upload_tiktok(page, video_path, title):
    print("🚀 [TikTok] Bắt đầu upload...")
    page.goto("https://www.tiktok.com/creator-center/upload?from=upload", timeout=60000)
    
    print("  -> Chờ nút chọn file...")
    page.wait_for_selector('input[type="file"]', state="attached", timeout=30000)
    
    print("  -> Đang tải video lên...")
    page.locator('input[type="file"]').set_input_files(video_path)
    
    print("  -> Chờ xử lý video (15s)...")
    time.sleep(15)
    print("✅ [TikTok] Video đã tải lên! (Dừng lại để bạn tự bấm Đăng)")

def upload_youtube(page, video_path, title):
    print("🚀 [YouTube Shorts] Bắt đầu upload...")
    page.goto("https://studio.youtube.com/channel/UCjEteQMJ4zzFV9_iKvChpvA", timeout=60000)
    
    print("  -> Đang mở hộp thoại upload...")
    page.wait_for_selector('#create-icon', timeout=15000).click()
    page.wait_for_selector('#text-item-0', timeout=5000).click()
    
    print("  -> Đang tải video lên...")
    page.wait_for_selector('input[type="file"]', timeout=15000)
    page.locator('input[type="file"]').set_input_files(video_path)
    
    time.sleep(15)
    print("✅ [YouTube Shorts] Video đã được nạp! (Dừng lại để bạn tự bấm Đăng)")

def upload_facebook(page, video_path, title):
    print("🚀 [Facebook Reels] Bắt đầu upload...")
    page.goto("https://business.facebook.com/latest/reels_composer?page_id=686899491163120", timeout=60000)
    
    print("  -> Đang tải video lên...")
    try:
        page.wait_for_selector('input[type="file"][accept*="video"]', timeout=15000)
        page.locator('input[type="file"][accept*="video"]').set_input_files(video_path)
    except:
        print("  -> Cảnh báo: Giao diện Facebook có thể yêu cầu click thủ công để hiện nút Upload.")
    
    time.sleep(15)
    print("✅ [Facebook Reels] Video đã được nạp! (Dừng lại để bạn tự bấm Đăng)")

def main():
    print(f"🎬 Bắt đầu quy trình Auto-Publish CẨN THẬN (Draft Mode)")
    print(f"📁 Video: {VIDEO_PATH}")
    print("-" * 40)
    
    if not os.path.exists(VIDEO_PATH):
        print("❌ LỖI: Không tìm thấy file video!")
        return

    import urllib.request
    import sys

    PORT = 9555
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    except Exception:
        print(f"❌ LỖI: Chrome Tâm An Lạc chưa chạy ở cổng {PORT}.")
        print("   Hãy chạy lệnh: ./open_browser.sh để mở trình duyệt gốc TRƯỚC KHI chạy script upload!")
        return

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].new_page()
        
        try:
            upload_tiktok(page, VIDEO_PATH, TITLE)
        except Exception as e:
            print(f"❌ Lỗi Tiktok: {e}")
            
        try:
            upload_youtube(page, VIDEO_PATH, TITLE)
        except Exception as e:
            print(f"❌ Lỗi YouTube: {e}")
            
        try:
            upload_facebook(page, VIDEO_PATH, TITLE)
        except Exception as e:
            print(f"❌ Lỗi Facebook: {e}")
            
        print("-" * 40)
        print("🎉 Quy trình nạp file đã xong! Hãy kiểm tra các tab thành công.")
        print("🛑 TRÌNH DUYỆT SẼ GIỮ MỞ để bạn kiểm tra và BẤM ĐĂNG THỦ CÔNG.")
        browser.disconnect()


if __name__ == "__main__":
    main()
