import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
p = ctx.new_page()
p.set_default_timeout(60000)
p.goto("https://studio.youtube.com/channel/UCnElgDX9q_AYGdFc2oDuWUA/videos/short",
       wait_until="domcontentloaded")
p.wait_for_timeout(12000)
t = p.inner_text("body")
i = t.find("chủ trì 26%")
print("== DANH SACH SHORTS ==")
print(t[max(0,i-300):i+400] if i > 0 else t[-1200:])
pw.stop()
