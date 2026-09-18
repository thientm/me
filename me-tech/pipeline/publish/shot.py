import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
m = sys.argv[1] if len(sys.argv) > 1 else ""
cand = [x for x in ctx.pages if m in x.url]
p = cand[0] if cand else ctx.pages[0]
print("url:", p.url)
p.screenshot(path=sys.argv[2] if len(sys.argv) > 2 else "shot.png")
print(p.inner_text("body")[:2500])
pw.stop()
