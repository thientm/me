#!/usr/bin/env python3
"""Bấm Post cho composer TikTok mà người đã tự đặt lịch/đặt giờ sẵn.

Dùng khi tt.py dừng lại nhờ bật 'Schedule' bằng tay.
"""
import sys
sys.path.insert(0, ".")
from _conn import connect

pw, b, ctx = connect()
q = [x for x in ctx.pages if "tiktok" in x.url][-1]
q.set_default_timeout(60000)

t = q.inner_text("body")
print("Original sound giữ nguyên:", "Original sound" in t)
i = t.find("When to post")
print("mục hẹn giờ:", t[i:i + 90].replace("\n", " | "))

btn = None
for name in ("Schedule", "Post"):
    c = q.get_by_role("button", name=name, exact=True)
    if c.count() and c.first.is_visible():
        btn = c.first
        print("nút sẽ bấm:", name)
        break
if btn is None:
    raise SystemExit("❌ không thấy nút Post/Schedule")
btn.click()
q.wait_for_timeout(8000)

pn = q.get_by_role("button", name="Post now", exact=True)
if pn.count() and pn.first.is_visible():
    pn.first.click()
    print("da bam Post now")
q.wait_for_timeout(22000)

print("url:", q.url)
print(q.inner_text("body")[:600])
pw.stop()
