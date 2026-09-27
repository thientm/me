import time
import re
from playwright.sync_api import sync_playwright

PORT = 9555

def finish_tiktok(page):
    print("🚀 [TikTok] Đang tự động bấm Đăng...")
    try:
        page.get_by_role("button", name=re.compile(r"Đăng|Post", re.I)).last.click(timeout=10000)
        print("✅ [TikTok] Đã bấm Đăng!")
    except Exception as e:
        print("❌ Lỗi TikTok:", e)

def finish_youtube(page):
    print("🚀 [YouTube Shorts] Đang tự động bấm Next và Publish...")
    try:
        # Bấm Next x3
        for i in range(3):
            next_btn = page.locator("#next-button")
            if next_btn.is_visible():
                next_btn.click()
                time.sleep(2)
        
        # Chọn Public
        public_radio = page.locator("tp-yt-paper-radio-button[name='PUBLIC']")
        if public_radio.count():
            public_radio.first.click()
            time.sleep(1)
        
        # Bấm Publish
        done_btn = page.locator("#done-button")
        if done_btn.is_visible():
            done_btn.click()
            print("✅ [YouTube] Đã bấm Publish!")
    except Exception as e:
        print("❌ Lỗi YouTube:", e)

def finish_facebook(page):
    print("🚀 [Facebook Reels] Đang tự động bấm Next và Share...")
    try:
        # Bấm Next x2
        for _ in range(5):
            btn = page.get_by_role("button", name=re.compile(r"Next|Tiếp", re.I)).first
            if btn.is_visible() and btn.is_enabled():
                btn.click()
                time.sleep(1.5)
        
        # Bấm Share / Đăng
        pub_btn = page.get_by_role("button", name=re.compile(r"Share|Chia sẻ|Đăng", re.I)).last
        if pub_btn.is_visible() and pub_btn.is_enabled():
            pub_btn.click()
            print("✅ [Facebook] Đã bấm Share!")
    except Exception as e:
        print("❌ Lỗi Facebook:", e)

def main():
    print("🤖 Đang quét các tab đang mở để bấm hoàn tất Upload...")
    import urllib.request
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    except Exception:
        print(f"❌ LỖI: Trình duyệt Tâm An Lạc không mở ở cổng {PORT}")
        return

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        
        for page in ctx.pages:
            url = page.url
            if "tiktok.com" in url:
                finish_tiktok(page)
            elif "studio.youtube.com" in url:
                finish_youtube(page)
            elif "business.facebook.com" in url:
                finish_facebook(page)
                
        print("🎉 XONG! Quá trình auto-click đã kết thúc.")
        browser.disconnect()

if __name__ == "__main__":
    main()
