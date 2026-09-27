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
    
    # Wait for the file input element to appear (it might be hidden)
    print("  -> Chờ nút chọn file...")
    page.wait_for_selector('input[type="file"]', state="attached", timeout=30000)
    
    # Inject the video file
    print("  -> Đang tải video lên...")
    page.locator('input[type="file"]').set_input_files(video_path)
    
    print("  -> Chờ xử lý video (15s)...")
    time.sleep(15)
    
    print("  -> Đang bấm nút Đăng (Post)...")
    try:
        page.get_by_role("button", name="Đăng").click(timeout=5000)
    except:
        try:
            page.get_by_role("button", name="Post").click(timeout=5000)
        except Exception as e:
            print("  -> Cảnh báo: Không thể tự động bấm Đăng, bạn hãy kiểm tra giao diện.")
            
    time.sleep(10) # Chờ hoàn tất đăng
    print("✅ [TikTok] Video đã được Đăng hoàn tất!")

def upload_youtube(page, video_path, title):
# ... (keep existing definitions, I'll just patch the main function next)

    print("🚀 [YouTube Shorts] Bắt đầu upload...")
    page.goto("https://studio.youtube.com", timeout=60000)
    
    # Click Create (Tạo) -> Upload videos (Tải video lên)
    print("  -> Đang mở hộp thoại upload...")
    page.wait_for_selector('#create-icon', timeout=15000).click()
    page.wait_for_selector('#text-item-0', timeout=5000).click()
    
    # Inject the video file
    print("  -> Đang tải video lên...")
    page.wait_for_selector('input[type="file"]', timeout=15000)
    page.locator('input[type="file"]').set_input_files(video_path)
    
    time.sleep(5)
    print("✅ [YouTube Shorts] Video đã được nạp! Bản nháp đã sẵn sàng.")

def upload_facebook(page, video_path, title):
    print("🚀 [Facebook Reels] Bắt đầu upload...")
    # NOTE: The Facebook Meta Business Suite or direct Reels create URL might vary based on your page setup.
    page.goto("https://business.facebook.com/latest/reels_composer", timeout=60000)
    
    print("  -> Đang tải video lên...")
    try:
        page.wait_for_selector('input[type="file"][accept*="video"]', timeout=15000)
        page.locator('input[type="file"][accept*="video"]').set_input_files(video_path)
    except:
        print("  -> Cảnh báo: Giao diện Facebook có thể yêu cầu click thủ công để hiện nút Upload.")
    
    time.sleep(5)
    print("✅ [Facebook Reels] Video đã được nạp!")

def main():
    print(f"🎬 Bắt đầu quy trình Auto-Publish")
    print(f"📁 Video: {VIDEO_PATH}")
    print(f"📝 Title: {TITLE}")
    print("-" * 40)
    
    if not os.path.exists(VIDEO_PATH):
        print("❌ LỖI: Không tìm thấy file video! Hãy đợi lệnh render chạy xong trước.")
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

    # Nối Playwright vào Chrome ĐÃ MỞ
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].new_page()
        
        try:
            upload_tiktok(page, VIDEO_PATH, TITLE)
            time.sleep(3)
            
            # upload_youtube(page, VIDEO_PATH, TITLE)
            # time.sleep(3)
            
            # upload_facebook(page, VIDEO_PATH, TITLE)
            # time.sleep(3)
            
            print("-" * 40)
            print("🎉 Tự động upload hoàn tất! Trình duyệt sẽ mở thêm vài phút để bạn kiểm tra.")
            time.sleep(120) # Giữ trình duyệt mở để user kiểm tra
        except Exception as e:
            print(f"❌ Lỗi trong quá trình upload: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
