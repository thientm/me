#!/usr/bin/env python3
"""Đăng một video lên cả ba nền tảng bằng một lệnh.

    python3 post.py                 đăng ngay
    python3 post.py --at 21:00      hẹn giờ (cả ba đều hỗ trợ hẹn giờ sẵn)
    python3 post.py --only tiktok   chạy lại một nền tảng bị lỗi

Hẹn giờ dùng tính năng CÓ SẴN của từng nền tảng, không phải cron chạy lúc 21h.
Lý do: cron đòi máy phải thức, Chrome phải còn đăng nhập, và mạng phải thông
đúng thời điểm đó. Hẹn bằng nền tảng thì đặt xong là xong, tắt máy cũng chạy.

Sau mỗi nền tảng đều KIỂM CHỨNG LẠI thay vì tin cú bấm — 19.09 YouTube nhận
cú bấm Publish nhưng video vẫn nằm ở Draft, không kiểm thì không biết.
"""
import argparse, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
STEPS = {"youtube": "yt.py", "facebook": "fb.py", "tiktok": "tt.py"}
VERIFY = {"youtube": "yt_verify.py", "facebook": "fb_verify.py", "tiktok": None}


def run(script, args=()):
    r = subprocess.run([PY, os.path.join(HERE, script), *args], cwd=HERE)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", help="giờ hẹn hôm nay, dạng HH:MM (giờ máy)")
    ap.add_argument("--only", choices=list(STEPS), action="append")
    a = ap.parse_args()

    which = a.only or list(STEPS)
    extra = ["--at", a.at] if a.at else []
    ok, fail = [], []

    for w in which:
        print(f"\n{'='*52}\n>> {w.upper()}{'  (hẹn ' + a.at + ')' if a.at else ''}\n{'='*52}")
        if not run(STEPS[w], extra):
            fail.append(w); print(f"❌ {w} lỗi"); continue
        if VERIFY[w] and not run(VERIFY[w]):
            fail.append(w); print(f"⚠ {w}: đăng xong nhưng kiểm chứng không đạt"); continue
        ok.append(w)

    print(f"\n{'='*52}")
    print("✅ xong:", ", ".join(ok) or "không có")
    if fail:
        print("❌ lỗi :", ", ".join(fail))
        print(f"   chạy lại riêng: python3 post.py --only {fail[0]}" + (f" --at {a.at}" if a.at else ""))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
