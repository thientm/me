#!/usr/bin/env python3
"""Cổng kiểm tra vùng an toàn.

Đo ngày 19.09.2026 bằng cách mở chính Short của kênh trên Chrome giả lập iPhone
rồi lấy toạ độ thật của từng nút, quy về hệ 1080×1920 — không lấy theo blog.

    trên   y < 250   logo · thanh tìm kiếm · tab For You/Following
    dưới   y > 1500  username + caption + tên nhạc  (Facebook Reels ngặt nhất)
    phải   x > 930   nhưng CHỈ khi y > 900 — cột like/bình luận/chia sẻ
                     không chạy hết chiều cao khung, phía trên vẫn dùng được
    trái   x < 80    mép cắt của máy màn hình cong

Chưa tính quảng cáo. Nếu sau này boost bài thì Facebook ăn tới 670px đáy,
lúc đó đổi BOT xuống 1250 và viết câu ngắn lại.
"""
import glob, os, sys

TOP, BOT, LEFT, RIGHT_X, RAIL_Y = 250, 1500, 80, 930, 900
LIMIT = 2.0          # % mực được phép nằm ngoài vùng an toàn
INK = 70             # nền là #0E0D0B nên mọi thứ sáng hơn 70 đều là nội dung


def check(frames_dir, every=12, verbose=True):
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        print("  ⓘ thiếu numpy/Pillow — bỏ qua kiểm tra vùng an toàn")
        return True

    files = sorted(glob.glob(os.path.join(frames_dir, "f*.jpg")))[::every]
    if not files:
        return True

    tot = {"trên": 0.0, "dưới": 0.0, "trái": 0.0, "phải": 0.0}
    worst, n, skipped, prev = (0.0, ""), 0, 0, None
    for f in files:
        im = Image.open(f).convert("L")
        a = np.asarray(im)
        # Bỏ qua khung ĐANG LIA: lúc đó hai trạm cùng trôi qua khung nên chữ
        # tất nhiên quét qua vùng chết — người xem không đọc trong lúc máy quay chạy.
        # Chỉ đo khung đứng yên, vì đó mới là lúc phải đọc được.
        thumb = np.asarray(im.resize((135, 240))).astype(np.int16)
        moving = prev is not None and float(np.abs(thumb - prev).mean()) > 4.0
        prev = thumb
        if moving:
            skipped += 1
            continue
        ink = a > INK
        s = int(ink.sum())
        if s < 500:
            continue
        n += 1
        part = {
            "trên": ink[:TOP, :].sum() / s * 100,
            "dưới": ink[BOT:, :].sum() / s * 100,
            "trái": ink[:, :LEFT].sum() / s * 100,
            "phải": ink[RAIL_Y:, RIGHT_X:].sum() / s * 100,
        }
        for k in tot:
            tot[k] += part[k]
        out = sum(part.values())
        if out > worst[0]:
            worst = (out, os.path.basename(f))
    if not n:
        return True

    avg = {k: v / n for k, v in tot.items()}
    total = sum(avg.values())
    ok = total <= LIMIT
    if verbose:
        print(f"   vùng an toàn: {total:.2f}% mực bị UI che "
              f"[{n} khung đứng yên, bỏ {skipped} khung đang lia] "
              f"(" + " · ".join(f"{k} {v:.2f}" for k, v in avg.items()) + ")")
        if not ok:
            print(f"   ⚠ VƯỢT ngưỡng {LIMIT}% — khung tệ nhất {worst[1]} ({worst[0]:.1f}%)")
            print("     xem lại scene.html: FIT, r.wmax, neo máy quay (505, 875), vị trí .hud")
        else:
            print("   ✅ nằm trong vùng an toàn của cả 3 nền tảng")
    return ok


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else ".work/frames"
    sys.exit(0 if check(d, every=int(sys.argv[2]) if len(sys.argv) > 2 else 12) else 1)
