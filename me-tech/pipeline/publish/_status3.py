import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()

p = ctx.new_page()
p.set_default_timeout(60000)
KEY = "ba người dùng Claude"

# --- Facebook ---
try:
    p.goto("https://business.facebook.com/latest/posts/published_posts?asset_id=403727472998689",
           wait_until="domcontentloaded")
    p.wait_for_timeout(13000)
    t = p.inner_text("body")
    print("FACEBOOK :", "✅ ĐÃ ĐĂNG" if KEY in t else "❌ CHƯA THẤY",
          "| so lan xuat hien:", t.count(KEY))
except Exception as e:
    print("FACEBOOK : loi", str(e)[:80])

# --- TikTok ---
try:
    p.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded")
    p.wait_for_timeout(11000)
    t = p.inner_text("body")
    k2 = "vào được tài khoản nhân viên OpenAI"
    print("TIKTOK   :", "✅ ĐÃ ĐĂNG" if k2 in t else "❌ CHƯA THẤY",
          "| so lan:", t.count(k2))
    import re
    m = re.search(r"Posts\s*(\d+)", t)
    print("           tong so Posts:", m.group(1) if m else "?")
except Exception as e:
    print("TIKTOK   : loi", str(e)[:80])
pw.stop()
