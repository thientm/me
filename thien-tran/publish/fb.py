"""Đăng Reel lên Trang Cá Nhân Facebook (facebook.com/thientm) qua facebook.com/reels/create."""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _conn import connect, require_login
from meta import FB_CAPTION, VIDEO
import ledger

_ap = argparse.ArgumentParser()
_ap.add_argument("--force", action="store_true")
_ap.add_argument("--draft", action="store_true", help="Chỉ điền thông tin, không bấm nút Đăng")
_a = _ap.parse_known_args()[0]
FORCE = _a.force
DRAFT = _a.draft

ledger.guard(VIDEO, "facebook", FORCE)

pw, b, ctx = connect()
require_login(ctx, "facebook")

p = ctx.new_page()
p.set_default_timeout(120000)

print(f"🚀 Mở trang đăng Reel cá nhân: https://www.facebook.com/reels/create")
p.goto("https://www.facebook.com/reels/create", wait_until="domcontentloaded")
p.wait_for_timeout(3000)

# 1. Chọn file video
file_inputs = p.locator('input[type=file]').all()
if not file_inputs:
    sys.exit("❌ Không tìm thấy ô tải video trên Facebook Reels")

print(f"📁 Đang nạp video: {os.path.basename(VIDEO)}")
file_inputs[0].set_input_files(VIDEO)
p.wait_for_timeout(4000)

# 2. Bấm Next từ bước 1 (Create -> Audio/Video)
for _ in range(15):
    btn = p.get_by_role("button", name=re.compile(r"Next|Tiếp", re.I)).first
    if btn.is_visible() and btn.is_enabled():
        btn.click()
        print("▶️ Đã bấm Tiếp (bước 1)")
        p.wait_for_timeout(2000)
        break
    p.wait_for_timeout(1000)

# 3. Bấm Next từ bước 2 (Edit/Audio -> Caption)
for _ in range(15):
    btn = p.get_by_role("button", name=re.compile(r"Next|Tiếp", re.I)).first
    if btn.is_visible() and btn.is_enabled():
        btn.click()
        print("▶️ Đã bấm Tiếp (bước 2)")
        p.wait_for_timeout(2000)
        break
    p.wait_for_timeout(1000)

# 4. Điền Caption mô tả
tb = p.locator('div[role="textbox"], textarea').first
if tb.is_visible():
    tb.click()
    p.wait_for_timeout(500)
    for i, line in enumerate(FB_CAPTION.split("\n")):
        if i:
            p.keyboard.press("Shift+Enter")
        p.keyboard.type(line, delay=3)
    print("📝 Đã điền caption mô tả:", FB_CAPTION[:60].replace("\n", " ") + "...")
    p.wait_for_timeout(2000)
else:
    print("⚠️ Không tìm thấy ô nhập caption")

# 5. Bấm Publish / Đăng (hoặc dừng nếu chỉ test/draft)
if DRAFT:
    print("⏸️ Chế độ --draft: Đã điền xong mọi thứ trên màn hình để bạn xem. Chưa bấm Đăng.")
else:
    pub_btn = p.get_by_role("button", name=re.compile(r"^(Post|Publish|Đăng)$", re.I)).first
    if pub_btn.is_visible() and pub_btn.is_enabled():
    # TODO (Quy tắc hệ thống): Facebook thường set mặc định "Only me". Cần click nút Audience chuyển sang Public trước khi Post.
        print("🚀 Đang bấm Đăng (Publish)...")
        pub_btn.click()
        p.wait_for_timeout(10000)
        print("✅ Đã đăng thành công Reel lên trang cá nhân Facebook!")
        ledger.record(VIDEO, "facebook")
    else:
        print("⚠️ Không thấy nút Publish/Đăng hoặc nút chưa khả dụng.")

p.close()
pw.stop()
