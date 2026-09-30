"""Đọc tài khoản YT/TT/FB đang đăng nhập ở Chrome cổng <port>; kèm --yt/--tt thì sai là thoát 1.

    python3 whois.py 9444 --yt UCvoMD_dBm8z1i-Zd8Pwu7mQ --tt thientranx
"""
import sys, re, json
import os
try:
    import playwright  # noqa: F401
except ModuleNotFoundError:  # chạy bằng python3 hệ thống → tự chuyển sang venv của me-tech
    _py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline", ".venv", "bin", "python")
    os.execv(_py, [_py] + sys.argv)
from playwright.sync_api import sync_playwright
port = sys.argv[1]
args = sys.argv[2:]
exp = dict(zip(args[0::2], args[1::2]))  # --yt UC... --tt user
with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
    ctx = b.contexts[0]
    p = ctx.new_page()
    p.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000); p.wait_for_timeout(9000)
    m = re.search(r"/channel/(UC[\w-]+)", p.url)
    yt = m.group(1) if m else ("CHƯA ĐĂNG NHẬP" if "accounts.google" in p.url else p.url[:80])
    ytname = ""
    if m:
        try: ytname = p.locator("#entity-name, ytcp-entity-page-header #channel-title").first.inner_text(timeout=5000)
        except Exception: pass
    p.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000); p.wait_for_timeout(8000)
    raw = p.evaluate("async()=>{try{const r=await fetch('/passport/web/account/info/?aid=1988',{credentials:'include'});return await r.text()}catch(e){return ''}}")
    try: tt = json.loads(raw).get("data", {}).get("username") or "CHƯA ĐĂNG NHẬP"
    except Exception: tt = "CHƯA ĐĂNG NHẬP"
    p.goto("https://www.facebook.com/me", wait_until="domcontentloaded", timeout=60000); p.wait_for_timeout(7000)
    fb = "CHƯA ĐĂNG NHẬP" if ("login" in p.url or p.url.rstrip("/").endswith("facebook.com")) else p.url
    print(f"YouTube : {yt} {ytname}\nTikTok  : {tt}\nFacebook: {fb}")
    p.goto("about:blank"); p.close()
bad = [k for k, v in (("--yt", yt), ("--tt", tt)) if k in exp and exp[k] != v]
if bad:
    sys.exit(f"[X] SAI TÀI KHOẢN ở cổng {port}: " + ", ".join(f"{k} mong {exp[k]}" for k in bad))
if exp: print("[OK] đúng tài khoản")
