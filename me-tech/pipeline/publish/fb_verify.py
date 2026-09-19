import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
p = ctx.new_page()
p.set_default_timeout(60000)
p.goto("https://business.facebook.com/latest/posts/published_posts?asset_id=403727472998689",
       wait_until="domcontentloaded")
p.wait_for_timeout(14000)
t = p.inner_text("body")
i = t.find("chủ trì một phần tư")
print("== BAI MOI NHAT ==")
print(t[max(0, i - 120):i + 420] if i > 0 else "KHONG THAY — co the chua publish xong")
pw.stop()
