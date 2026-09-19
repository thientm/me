import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
p = ctx.new_page()
p.set_default_timeout(60000)
for url, name in [("https://studio.youtube.com/", "YouTube Studio"),
                  ("https://business.facebook.com/latest/home", "Facebook Page"),
                  ("https://www.tiktok.com/tiktokstudio/upload", "TikTok Studio")]:
    try:
        p.goto(url, wait_until="domcontentloaded", timeout=60000)
        p.wait_for_timeout(6000)
        bad = "accounts.google.com" in p.url or "/login" in p.url
        print(f"{name}: {'❌ MẤT ĐĂNG NHẬP' if bad else '✅ còn đăng nhập'}  -> {p.url[:90]}")
    except Exception as e:
        print(f"{name}: lỗi {e}")
pw.stop()
