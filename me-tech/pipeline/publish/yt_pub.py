import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
p = [x for x in ctx.pages if "studio.youtube.com" in x.url][0]
p.set_default_timeout(90000)
p.locator("#done-button").first.click(force=True)
p.wait_for_timeout(12000)
sh = p.locator("ytcp-video-share-dialog")
if sh.count():
    print("== ĐÃ ĐĂNG ==")
    print(sh.first.inner_text()[:500])
else:
    print("chua thay hop chia se:")
    print(p.inner_text("body")[:500])
pw.stop()
