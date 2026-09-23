import tempfile, re
from playwright.sync_api import sync_playwright
prof = tempfile.mkdtemp(prefix="metech-capture-")
with sync_playwright() as pw:
    ctx = pw.chromium.launch_persistent_context(
        user_data_dir=prof, headless=True,
        viewport={"width":430,"height":932}, device_scale_factor=3,
        is_mobile=True, has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
    p = ctx.pages[0] if ctx.pages else ctx.new_page()
    p.set_default_timeout(60000)
    p.goto("https://openai.com/index/introducing-gpt-6-sol-and-luna/", wait_until="domcontentloaded")
    p.wait_for_timeout(7000)
    t = p.evaluate("document.body.innerText")
    print("LEN", len(t))
    for i, line in enumerate(t.split("\n")):
        if "$" in line or "1M" in line or "pric" in line.lower() or "Pric" in line:
            print(i, repr(line[:160]))
    ctx.close()
