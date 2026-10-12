import sys, re, json, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, "me-tech/pipeline/publish")
from _conn import quiet

results = {}

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9555")
    ctx = b.contexts[0]
    quiet(b, ctx)
    p = ctx.new_page()
    p.set_default_timeout(60000)

    # 1. YouTube Analytics Tâm An Lạc
    try:
        p.goto("https://studio.youtube.com/channel/UCjEteQMJ4zzFV9_iKvChpvA/analytics", wait_until="domcontentloaded")
        p.wait_for_timeout(8000)
        body = p.inner_text("body")
        sub_match = re.search(r"Current subscribers[\s\n]+([0-9,.]+)", body, re.IGNORECASE)
        results["yt_tamanlac"] = {
            "title": p.title(),
            "url": p.url,
            "subscribers": sub_match.group(1) if sub_match else "N/A",
            "snippet": body[:1500]
        }
    except Exception as e:
        results["yt_tamanlac_err"] = str(e)

    # 2. TikTok Studio Tâm An Lạc
    try:
        p.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded")
        p.wait_for_timeout(8000)
        results["tt_tamanlac_content"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": p.inner_text("body")[:1500]
        }
        
        p.goto("https://www.tiktok.com/tiktokstudio/analytics", wait_until="domcontentloaded")
        p.wait_for_timeout(8000)
        results["tt_tamanlac_analytics"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": p.inner_text("body")[:1500]
        }
    except Exception as e:
        results["tt_tamanlac_err"] = str(e)

    p.close()

with open("me-tech/ops/metrics_9555.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved metrics_9555.json successfully!")
