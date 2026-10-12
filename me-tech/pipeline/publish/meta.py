"""Con tro toi bai DANG CHON. Dung sua tay file nay.

Moi bai co file rieng `meta_<slug>.py` (VIDEO · YT_TITLE · YT_DESC ·
FB_CAPTION · TT_CAPTION). File nay doc ten bai dang chon trong `ACTIVE` roi
nap dung file do.

    python3 use.py anthropic-ipo     # chon bai
    python3 use.py                   # xem dang chon bai nao

Vi sao: truoc day moi lan doi bai phai sua tay meta.py, nen khong the chuan bi
san hai bai trong mot ngay - bai sau de len bai truoc. Ba khung dang mot ngay
thi phai xep hang duoc.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACTIVE = os.path.join(HERE, "ACTIVE")

# Tìm REPO_ROOT để nạp ops.publish
REPO_ROOT = HERE
while REPO_ROOT and REPO_ROOT != "/" and not os.path.exists(os.path.join(REPO_ROOT, "ops", "publish", "meta_loader.py")):
    REPO_ROOT = os.path.dirname(REPO_ROOT)

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from ops.publish.meta_loader import load_meta

try:
    with open(ACTIVE, encoding="utf-8") as f:
        SLUG = f.read().strip()
except FileNotFoundError:
    sys.exit("[X] chua chon bai nao. Chay:  python3 use.py <slug>")

try:
    _m = load_meta(channel="me-tech", slug=SLUG, root_dir=REPO_ROOT, legacy_dir=HERE)
except Exception as e:
    sys.exit(f"[X] {e}")

VIDEO = _m.video_path
YT_TITLE = _m.yt_title
YT_DESC = _m.yt_desc
FB_CAPTION = _m.fb_caption
TT_CAPTION = _m.tt_caption

if not os.path.exists(VIDEO):
    # Cảnh báo nhẹ nếu đang test hoặc video chưa render xong
    pass

