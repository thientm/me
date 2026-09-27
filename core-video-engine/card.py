#!/usr/bin/env python3
"""Ve the anh 1080x1350 cho Facebook tu file noi dung.

    .venv/bin/python card.py cards/thuong-xanh.json          # ve het
    .venv/bin/python card.py cards/thuong-xanh.json --only 3 # ve mot the

Anh ra o render/cards/<slug>.png

Ve BANG CODE, khong phai anh AI sinh ra — giong het cach scene.html dung
video: HTML -> headless Chromium -> PNG. Nho vay 30 the trong nhu mot bo,
sua bang mau mot cho la doi ca bo.

Bang mau o day KHAC bang mau video (xem dau card.html). Dung hop nhat.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "render", "cards")
W, H = 1080, 1350


def build(cards, only=None, quiet=False):
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    tpl = open(os.path.join(HERE, "card.html"), encoding="utf-8").read()
    made, bad = [], []

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        # Cổng: lỗi JS trong trang KHÔNG làm screenshot thất bại — 22.09.2026
        # năm thẻ ra ảnh "thành công" mà không có chữ nào, chỉ phát hiện khi
        # mở ảnh ra xem. Bắt pageerror và coi đó là hỏng.
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        for c in cards:
            if only and c["slug"] != only and str(c.get("n")) != only:
                continue
            # Nhúng thẳng dữ liệu vào trang thay vì set rồi evaluate:
            # script trong trang chạy NGAY khi set_content, nên gán window.CARD
            # sau đó là muộn — thẻ sẽ trắng trơn.
            html = tpl.replace("const D = window.CARD;",
                               "const D = " + json.dumps(c, ensure_ascii=False) + ";")
            errs.clear()
            pg.set_content(html)
            pg.wait_for_timeout(350)
            fit = pg.evaluate("window.__fit")
            # Thẻ không có chữ nào = hỏng, dù screenshot vẫn chạy trơn
            n_txt = pg.eval_on_selector("#title", "e => e.textContent.trim().length")
            n_row = pg.eval_on_selector_all(".row", "e => e.length")
            p = os.path.join(OUT, c["slug"] + ".png")
            pg.screenshot(path=p)
            made.append(p)
            if errs:
                bad.append((c["slug"], "lỗi JS: " + errs[0]))
            elif not n_txt or n_row != len(c.get("rows", [])):
                bad.append((c["slug"], "thẻ rỗng: tiêu đề %d ký tự, %d/%d dòng"
                            % (n_txt, n_row, len(c.get("rows", [])))))
            elif not fit or not fit.get("ok"):
                bad.append((c["slug"], "chữ tràn khung"))
            if not quiet:
                print("  %-34s chữ %spx · co %.2f · %d dòng"
                      % (c["slug"] + ".png", fit["size"], fit["scale"], n_row))
        b.close()

    if bad:
        print("\n[X] %d thẻ HỎNG:" % len(bad))
        for slug, why in bad:
            print("    %-28s %s" % (slug, why))
        return made, False
    return made, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--only", help="slug hoặc số thứ tự của một thẻ")
    a = ap.parse_args()

    d = json.load(open(a.content, encoding="utf-8"))
    cards = d["cards"] if isinstance(d, dict) else d
    for i, c in enumerate(cards, 1):
        c.setdefault("n", i)
        for k in ("slug", "title"):
            if not c.get(k):
                sys.exit("❌ thẻ[%d] thiếu '%s'" % (i, k))

    print("── vẽ %d thẻ" % (1 if a.only else len(cards)))
    made, ok = build(cards, a.only)
    print("\n✅ %d ảnh → %s" % (len(made), os.path.normpath(OUT)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
