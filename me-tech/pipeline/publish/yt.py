import sys
sys.path.insert(0, ".")
from _conn import connect
from meta import VIDEO, YT_TITLE, YT_DESC

CH = "UCnElgDX9q_AYGdFc2oDuWUA"
pw, b, ctx = connect()
p = ctx.pages[0] if ctx.pages else ctx.new_page()
p.set_default_timeout(120000)

def dismiss():
    for lab in ["Continue", "Tiep tuc", "Got it", "Da hieu"]:
        try:
            btn = p.get_by_role("button", name=lab, exact=False)
            if btn.count() and btn.first.is_visible():
                btn.first.click()
                p.wait_for_timeout(1200)
        except Exception:
            pass

p.goto("https://studio.youtube.com/channel/%s/videos/upload?d=ud" % CH,
       wait_until="domcontentloaded")
p.wait_for_timeout(9000)
dismiss()
p.wait_for_timeout(2000)
print("url:", p.url)

p.locator("input[type=file]").first.set_input_files(VIDEO)
print("da chon file")

p.wait_for_selector("#title-textarea #textbox", timeout=120000)
p.wait_for_timeout(3000)
dismiss()

t = p.locator("#title-textarea #textbox").first
t.click()
p.keyboard.press("Meta+a")
p.keyboard.press("Delete")
t.type(YT_TITLE, delay=6)
p.wait_for_timeout(600)

d = p.locator("#description-textarea #textbox").first
d.click()
d.type(YT_DESC, delay=3)
p.wait_for_timeout(600)

p.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first.click()
p.wait_for_timeout(1000)
print("tieu de:", t.inner_text()[:150])

# Next x3
for i in range(3):
    p.click("#next-button")
    p.wait_for_timeout(2500)
    print("next", i + 1)

# cong khai
p.wait_for_selector("tp-yt-paper-radio-button[name='PUBLIC']", timeout=60000)
p.locator("tp-yt-paper-radio-button[name='PUBLIC']").first.click()
p.wait_for_timeout(1500)
p.screenshot(path="shot_yt_before_publish.png")
print(p.inner_text("ytcp-uploads-dialog")[:900])
pw.stop()
