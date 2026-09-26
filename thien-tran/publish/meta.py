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
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACTIVE = os.path.join(HERE, "ACTIVE")

try:
    SLUG = open(ACTIVE, encoding="utf-8").read().strip()
except FileNotFoundError:
    sys.exit("[X] chua chon bai nao. Chay:  python3 use.py <slug>")

_path = os.path.join(HERE, "meta_%s.py" % SLUG)
if not os.path.exists(_path):
    sys.exit("[X] khong co %s\n    Cac bai dang co: %s"
             % (os.path.basename(_path),
                ", ".join(sorted(f[5:-3] for f in os.listdir(HERE)
                                 if f.startswith("meta_") and f.endswith(".py")))))

_spec = importlib.util.spec_from_file_location("meta_" + SLUG.replace("-", "_"), _path)
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)

VIDEO = _m.VIDEO
YT_TITLE = _m.YT_TITLE
YT_DESC = _m.YT_DESC
FB_CAPTION = _m.FB_CAPTION
TT_CAPTION = _m.TT_CAPTION

if not os.path.exists(VIDEO):
    sys.exit("[X] khong thay file video: %s" % VIDEO)
