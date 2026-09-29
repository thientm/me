"""Chặn đăng nhầm tài khoản (29.09.2026).

Chrome cổng 9555 từng bị đăng nhập tài khoản Thiện Trần (YT UCvoMD_dBm8z1i-Zd8Pwu7mQ,
TikTok @thientranx). "Đã đăng nhập" KHÔNG có nghĩa là "đúng kênh" — phải đọc danh tính.
Gọi require_identity(ctx, "youtube"|"tiktok"|"facebook") TRƯỚC khi upload; sai thì thoát.
Chỉ mở tab mới rồi đóng, không đụng tab sẵn có.
"""
import json
import re
import sys

YT_CHANNEL = "UCjEteQMJ4zzFV9_iKvChpvA"
TT_USER = "tamanlac.tiktok"
FB_PAGE_ID = "686899491163120"


def require_identity(ctx, which):
    pg = ctx.new_page()
    try:
        if which == "youtube":
            pg.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(9000)
            m = re.search(r"/channel/(UC[\w-]+)", pg.url)
            got = m.group(1) if m else pg.url
            ok = got == YT_CHANNEL
        elif which == "tiktok":
            pg.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(8000)
            raw = pg.evaluate("async()=>{try{const r=await fetch('/passport/web/account/info/?aid=1988',"
                              "{credentials:'include'});return await r.text()}catch(e){return ''}}")
            try:
                got = json.loads(raw).get("data", {}).get("username")
            except Exception:
                got = None
            ok = got == TT_USER
        else:
            pg.goto(f"https://business.facebook.com/latest/home?asset_id={FB_PAGE_ID}",
                    wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(10000)
            body = pg.inner_text("body")
            got = pg.url[:90]
            ok = "loginpage" not in pg.url and "Tâm An Lạc" in body
    finally:
        pg.close()
    if not ok:
        sys.exit(f"❌ {which}: danh tính đang đăng nhập là {got!r}, KHÔNG phải Tâm An Lạc. Không upload.")
    print(f"✅ {which}: đúng tài khoản Tâm An Lạc ({got})")


# --- Sổ đăng bài (chống trùng lớp 1, giống me-tech/pipeline/publish/ledger.py) ---
import os
import datetime as _dt
LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "posted.json")


def _load():
    try:
        return json.load(open(LEDGER, encoding="utf-8"))
    except Exception:
        return {}


def guard(slug, platform):
    hit = _load().get(f"{slug}:{platform}")
    if hit and "--force" not in sys.argv:
        sys.exit(f"[X] Sổ đăng bài: {slug} đã lên {platform} lúc {hit.get('luc')}. Không đăng lại.")


def record(slug, platform, note=""):
    d = _load()
    d[f"{slug}:{platform}"] = {"luc": _dt.datetime.now().strftime("%d.%m.%Y %H:%M"), "ghi_chu": note}
    json.dump(d, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)


def seen_on_platform(ctx, platform, needle):
    """Chống trùng lớp 2: đọc danh sách bài trên chính nền tảng. Trả số lần thấy `needle`."""
    urls = {"youtube": f"https://studio.youtube.com/channel/{YT_CHANNEL}/videos/short",
            "tiktok": "https://www.tiktok.com/tiktokstudio/content",
            "facebook": f"https://business.facebook.com/latest/posts/published_posts?asset_id={FB_PAGE_ID}"}
    pg = ctx.new_page()
    try:
        pg.goto(urls[platform], wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(12000)
        norm = lambda s: " ".join((s or "").split()).lower()
        return norm(pg.inner_text("body")).count(norm(needle))
    finally:
        pg.close()
