import time
from playwright.sync_api import sync_playwright

TITLE = "Đỉnh cao của sự buông bỏ - Lời Phật Dạy 🙏 #tamanlac #phatphap #trietly #cuocsong"
DESC = "Video Tâm An Lạc mang đến những triết lý Phật Pháp sâu sắc giúp bạn tìm thấy sự bình yên trong tâm hồn. Hãy đăng ký kênh để nhận thêm nhiều bài học ý nghĩa."
PORT = 9555

def main():
    print("🚀 Đang sửa lại tiêu đề và mô tả trên YouTube...")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].new_page()
        
        try:
            print("  -> Mở trang danh sách Video (Tab Shorts)...")
            page.goto("https://studio.youtube.com/channel/UCjEteQMJ4zzFV9_iKvChpvA/videos/short", timeout=60000)
            
            print("  -> Đang tìm video mới nhất...")
            page.wait_for_selector('a#video-title', timeout=30000)
            
            print("  -> Bấm vào Edit video...")
            page.locator('a#video-title').first.click()
            
            print("  -> Chờ hộp thoại chỉnh sửa tải xong...")
            page.wait_for_selector('#title-textarea #textbox', timeout=30000)
            time.sleep(3) # Wait for JS to fully attach events
            
            print("  -> Đang xóa tiêu đề cũ và nhập tiêu đề mới...")
            title_box = page.locator('#title-textarea #textbox').first
            title_box.click()
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            title_box.fill(TITLE)
            
            print("  -> Đang nhập mô tả...")
            desc_box = page.locator('#description-textarea #textbox').first
            desc_box.click()
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            desc_box.fill(DESC)
            
            print("  -> Đang lưu thay đổi...")
            save_btn = page.locator('#save-button')
            # Nút Save có thể bị disable nếu text không đổi, hoặc cần click chuột
            if save_btn.is_visible() and not save_btn.get_attribute("disabled"):
                save_btn.click()
                print("✅ Đã lưu thành công!")
            else:
                print("✅ Đã nhập xong! Nút Save hiện đang mờ (hoặc đang tải), bạn có thể kiểm tra và bấm Save tay nếu cần.")
                
            time.sleep(3)
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        finally:
            browser.disconnect()

if __name__ == "__main__":
    main()
