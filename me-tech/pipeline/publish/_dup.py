import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
p = [x for x in ctx.pages if "videos/short" in x.url]
p = p[0] if p else ctx.new_page()
if "videos/short" not in p.url:
    p.goto("https://studio.youtube.com/channel/UCnElgDX9q_AYGdFc2oDuWUA/videos/short",
           wait_until="domcontentloaded")
p.wait_for_timeout(9000)
rows = p.locator("ytcp-video-row")
for i in range(min(rows.count(), 3)):
    txt = rows.nth(i).inner_text()
    parts = [x.strip() for x in txt.split("\n") if x.strip()]
    # bỏ phần mô tả dài, chỉ lấy các cột trạng thái
    keep = [x for x in parts if len(x) < 40]
    print(f"[{i}] " + " | ".join(keep[:10]))
pw.stop()
