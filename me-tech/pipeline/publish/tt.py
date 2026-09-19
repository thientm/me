"""Đăng lên TikTok Studio. KHÔNG chọn nhạc TikTok — video đã có nhạc nền."""
import sys
sys.path.insert(0, ".")
from _conn import connect, require_login
from meta import VIDEO, TT_CAPTION

pw, b, ctx = connect()
require_login(ctx, 'tiktok').close()
q = ctx.new_page()
q.set_default_timeout(120000)

q.goto("https://www.tiktok.com/tiktokstudio/upload?from=webapp", wait_until="domcontentloaded")
q.wait_for_timeout(10000)
q.locator("input[type=file]").first.set_input_files(VIDEO)
print("da chon file, cho upload…")
for _ in range(30):
    q.wait_for_timeout(3000)
    if "Uploaded" in q.inner_text("body"):
        break
print("upload xong")

ed = q.locator("div[contenteditable='true']").first
ed.click()
q.keyboard.press("Meta+a")
q.keyboard.press("Delete")
q.wait_for_timeout(500)
for tok in TT_CAPTION.split(" "):
    q.keyboard.type(tok, delay=10)
    if tok.startswith("#"):
        q.wait_for_timeout(350)
        q.keyboard.press("Escape")   # đóng menu hashtag, nếu không nó nuốt chữ sau
    q.keyboard.type(" ", delay=10)
q.wait_for_timeout(1500)
print("mo ta:", ed.inner_text()[:90])

t = q.inner_text("body")
print("Original sound giữ nguyên:", "Original sound" in t)

q.get_by_role("button", name="Post", exact=True).first.click()
q.wait_for_timeout(8000)
# TikTok hỏi "Continue to post?" khi check chưa xong
try:
    pn = q.get_by_role("button", name="Post now", exact=True)
    if pn.count() and pn.first.is_visible():
        pn.first.click()
        print("da bam Post now")
except Exception as e:
    print("khong co hop xac nhan:", e)
q.wait_for_timeout(25000)
q.screenshot(path="_scratch/tt_done.png")
print("url:", q.url)
print(q.inner_text("body")[:700])
pw.stop()
