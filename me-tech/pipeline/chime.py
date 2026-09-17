#!/usr/bin/env python3
"""Tiếng chuông kết — tự tổng hợp nên không dính bản quyền.

Hai nốt đi lên (A5 -> E6), kiểu tiếng báo của nút theo dõi.

    python demo/chime.py demo/chime.wav
"""
import sys, wave
import numpy as np

SR = 48000
NOTES = [(880.00, 0.00, 1.00),      # A5
         (1318.51, 0.17, 0.85)]     # E6, vào sau một nhịp ngắn
PARTIALS = [(1.000, 1.00, 0.62),    # (bội âm, biên độ, thời gian tắt)
            (2.003, 0.42, 0.40),
            (3.011, 0.22, 0.26),
            (4.17,  0.10, 0.17),
            (5.43,  0.05, 0.12)]
DUR = 2.0


def bell(f0, gain):
    n = int(DUR * SR)
    t = np.arange(n) / SR
    out = np.zeros(n, dtype=np.float64)
    for mult, amp, tau in PARTIALS:
        out += amp * np.sin(2 * np.pi * f0 * mult * t) * np.exp(-t / tau)
    atk = np.clip(t / 0.004, 0, 1)                  # vào nhanh nhưng không kêu "tách"
    return out * atk * gain


def main():
    dst = sys.argv[1] if len(sys.argv) > 1 else "chime.wav"
    n = int((DUR + max(d for _, d, _ in NOTES)) * SR)
    mix = np.zeros(n, dtype=np.float64)
    for f0, delay, gain in NOTES:
        k = int(delay * SR)
        b = bell(f0, gain)
        mix[k:k + len(b)] += b

    # một lớp vọng rất nhẹ cho đỡ khô
    echo = np.zeros_like(mix)
    d = int(0.085 * SR)
    echo[d:] = mix[:-d] * 0.16
    mix += echo

    mix *= 0.5 / (np.abs(mix).max() or 1.0)
    pcm = (mix * 32767).astype("<i2")
    with wave.open(dst, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"{dst}  {len(mix)/SR:.2f}s")


if __name__ == "__main__":
    main()
