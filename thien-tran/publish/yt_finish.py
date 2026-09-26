import sys
sys.path.insert(0, ".")
from _conn import connect
pw, b, ctx = connect()
p = [x for x in ctx.pages if "videos/short" in x.url][0]
p.set_default_timeout(90000)

p.get_by_text("Edit draft", exact=True).first.click()
p.wait_for_timeout(9000)
print("da mo ban nhap")

# sang bước Visibility
for i in range(3):
    try:
        nb = p.locator("#next-button")
        if nb.count() and nb.first.is_visible():
            nb.first.click()
            p.wait_for_timeout(2500)
            print("next", i + 1)
    except Exception as e:
        print("bo qua next", i + 1, e)

p.wait_for_selector("tp-yt-paper-radio-button[name='PUBLIC']", timeout=60000)
p.locator("tp-yt-paper-radio-button[name='PUBLIC']").first.click()
p.wait_for_timeout(2000)

db = p.locator("#done-button").first
print("nut:", db.inner_text().strip(), "| disabled:", db.get_attribute("disabled"))
db.click()
p.wait_for_timeout(15000)

sh = p.locator("ytcp-video-share-dialog")
print("== KET QUA ==")
print(sh.first.inner_text()[:400] if sh.count() else "chua thay hop chia se")
pw.stop()
