#!/usr/bin/env python3
"""Dang MOT the anh len Page Me Tech, dang photo, qua Business Suite.

    python3 fb_photo.py token-la-gi --at 09:30
    python3 fb_photo.py token-la-gi              # dang ngay

Anh lay o render/cards/<slug>.png, caption lay o cards/caption/<slug>.txt
(khong co thi dung phan chu trong the lam caption).

Dung composer CHUNG (`/latest/composer/`), khong phai reels_composer — bai
nay la PHOTO, khong phai video.

So dang bai dung chung voi video: khoa "<slug>.png:facebook-photo".
"""
import argparse
import datetime as dt
import json
import os
import sys
sys.path.insert(0, ".")
from _conn import confirm_schedule, connect, require_login
import ledger

ASSET = "403727472998689"          # Page Mê Tech
HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
CARDS = os.path.join(PIPE, "..", "render", "cards")


def caption_for(slug):
    """Caption = tieu de + cac dong trong the, do thang tu file noi dung.
    Khong viet caption rieng mot noi khac roi de hai ban troi nhau."""
    d = json.load(open(os.path.join(PIPE, "cards", "thuong-xanh.json"),
                       encoding="utf-8"))
    c = next((x for x in d["cards"] if x["slug"] == slug), None)
    if not c:
        sys.exit("[X] khong co the '%s' trong cards/thuong-xanh.json" % slug)

    def plain(s):
        for a, b in (("<em>", ""), ("</em>", ""), ("<b>", ""), ("</b>", "")):
            s = s.replace(a, b)
        return s

    lines = [plain(c["title"])]
    if c.get("sub"):
        lines += ["", plain(c["sub"])]
    for r in c.get("rows", []):
        lines += ["", "• " + plain(r["t"])]
        if r.get("d"):
            lines[-1] += "\n  " + plain(r["d"])
    lines += ["", "Mê Tech — AI dễ hiểu, mỗi ngày một tin.", "",
              "#AI #congnghe #MeTech #hocAI"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--at", help="gio hen, dang HH:MM")
    ap.add_argument("--day", type=int, default=0, help="0 = hom nay, 1 = mai...")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    img = os.path.normpath(os.path.join(CARDS, a.slug + ".png"))
    if not os.path.exists(img):
        sys.exit("[X] khong thay anh: %s\n   ve bang: .venv/bin/python card.py "
                 "cards/thuong-xanh.json" % img)

    ledger.guard(a.slug + ".png", "facebook-photo", a.force)

    WHEN = None
    if a.at:
        h, m = (int(x) for x in a.at.split(":"))
        WHEN = dt.datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
        WHEN += dt.timedelta(days=a.day)
        if WHEN <= dt.datetime.now() + dt.timedelta(minutes=15):
            WHEN += dt.timedelta(days=1)
        print("hen:", WHEN.strftime("%d/%m/%Y %H:%M"))

    cap = caption_for(a.slug)
    print("caption %d dong, %d ky tu" % (cap.count("\n") + 1, len(cap)))

    pw, b, ctx = connect()
    require_login(ctx, "facebook").close()
    q = ctx.new_page()
    q.set_default_timeout(90000)
    q.goto("https://business.facebook.com/latest/composer/?asset_id=" + ASSET,
           wait_until="domcontentloaded")
    q.wait_for_timeout(12000)

    # "Add photo/video" mo hop chon file — khong co input[type=file] san trong DOM
    with q.expect_file_chooser() as fc:
        q.get_by_text("Add photo/video", exact=True).first.click()
    fc.value.set_files(img)
    print("da chon anh, cho tai len...")
    for _ in range(25):
        q.wait_for_timeout(2500)
        if q.locator("img[src^='blob:'], img[src*='scontent']").count():
            break
    q.wait_for_timeout(3000)

    # Caption: o nhap cua composer anh KHONG co role=textbox (khac composer
    # reel). No la contenteditable, va co HAI cai cung aria-label — cai dau
    # an, cai sau moi hien. Lay dung cai dang hien, dung .first.
    tb = q.locator("[contenteditable='true']:visible").first
    tb.click()
    q.wait_for_timeout(600)
    for i, line in enumerate(cap.split("\n")):
        if i:
            q.keyboard.press("Shift+Enter")
        if line:
            q.keyboard.type(line, delay=3)
    q.wait_for_timeout(1500)
    print("mo ta:", tb.inner_text()[:80].replace("\n", " "))

    if WHEN:
        # === CONG NGAY — dung go ===
        # 22.09.2026: ca 30 the do don vao MOT ngay thay vi rai sau ngay.
        # Ly do: doan nay chi dien GIO va PHUT, khong bao gio dien NGAY, nen
        # o ngay giu nguyen mac dinh la hom nay. confirm_schedule co doc o
        # ngay, nhung `want` khong co khoa "ngay" nen no chi kiem KHAC RONG —
        # ma o ngay luon khac rong, nen luon lot.
        # Chua lam duoc phan chon ngay (lich dang calendar, phai bam o ngay,
        # go chu vao bi backdrop chan — giong YouTube). Nen tam thoi CHAN HAN:
        # khac ngay thi dung, dung doan.
        if WHEN.date() != dt.date.today():
            pw.stop()
            sys.exit("[X] fb_photo.py chi hen duoc TRONG NGAY.\n"
                     "    Muon %s nhung hom nay la %s.\n"
                     "    Chay lai dung ngay do, hoac lam phan chon ngay truoc."
                     % (WHEN.strftime("%d/%m"), dt.date.today().strftime("%d/%m")))
        q.get_by_text("Set date and time", exact=True).first.click()
        q.wait_for_timeout(3000)
        for lab, val in (("hours", WHEN.strftime("%H")),
                         ("minutes", WHEN.strftime("%M"))):
            f = q.locator("input[aria-label='%s']" % lab).first
            f.click()
            q.keyboard.press("Meta+a"); q.keyboard.press("Delete")
            f.type(val, delay=110)
            q.wait_for_timeout(900)
        # LUAT: doc lai roi moi duoc bam. O gio Facebook do React dieu khien,
        # input_value() tra ve rong — confirm_schedule doc them the cha.
        confirm_schedule(q,
                         {"ngay": "input[placeholder='dd/mm/yyyy']",
                          "gio": "input[aria-label='hours']",
                          "phut": "input[aria-label='minutes']"},
                         {"ngay": WHEN.strftime("%d %B %Y"),
                          "gio": WHEN.strftime("%H"), "phut": WHEN.strftime("%M")})
        q.screenshot(path="_scratch/fbphoto_sched.png")

    want = "Schedule" if WHEN else "Post"
    bt = q.get_by_role("button")
    tgt = None
    for i in range(bt.count()):
        e = bt.nth(i)
        try:
            lab = (e.get_attribute("aria-label") or e.inner_text() or "").strip()
            if e.is_visible() and lab == want:
                tgt = e            # nut that nam CUOI danh sach
        except Exception:
            pass
    if tgt is None:
        q.screenshot(path="_scratch/fbphoto_nobtn.png")
        sys.exit("[X] khong thay nut " + want)
    tgt.click()
    print("da bam", want)
    q.wait_for_timeout(30000)
    q.screenshot(path="_scratch/fbphoto_done.png")

    ledger.record(a.slug + ".png", "facebook-photo",
                  ("hen " + WHEN.strftime("%d/%m %H:%M")) if WHEN else "dang ngay")
    print("da ghi so dang bai")
    pw.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
