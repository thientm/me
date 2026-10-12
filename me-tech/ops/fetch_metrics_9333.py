import sys, re, json, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, "me-tech/pipeline/publish")
from _conn import quiet

results = {}

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9333")
    ctx = b.contexts[0]
    quiet(b, ctx)
    p = ctx.new_page()
    p.set_default_timeout(60000)

    # 1. YouTube Analytics Mê Tech
    try:
        p.goto("https://studio.youtube.com/channel/UCnElgDX9q_AYGdFc2oDuWUA/analytics", wait_until="domcontentloaded")
        p.wait_for_timeout(8000)
        body = p.inner_text("body")
        # Extract metrics
        results["yt_metech"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": body[:1200]
        }
    except Exception as e:
        results["yt_metech_err"] = str(e)

    # 2. TikTok Studio Mê Tech
    try:
        p.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded")
        p.wait_for_timeout(8000)
        body = p.inner_text("body")
        results["tt_metech_content"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": body[:1500]
        }
        
        # Check TikTok Studio Analytics overview
        p.goto("https://www.tiktok.com/tiktokstudio/analytics", wait_until="domcontentloaded")
        p.wait_for_timeout(8000)
        results["tt_metech_analytics"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": p.inner_text("body")[:1500]
        }
    except Exception as e:
        results["tt_metech_err"] = str(e)

    # 3. Facebook Business Suite Insights (Mê Tech)
    try:
        p.goto("https://business.facebook.com/latest/insights/overview?asset_id=403727472998689", wait_until="domcontentloaded")
        p.wait_for_timeout(9000)
        results["fb_metech"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": p.inner_text("body")[:1500]
        }
    except Exception as e:
        results["fb_metech_err"] = str(e)

    # 4. Facebook Business Suite Insights (Tâm An Lạc)
    try:
        p.goto("https://business.facebook.com/latest/insights/overview?asset_id=686899491163120", wait_until="domcontentloaded")
        p.wait_for_timeout(9000)
        results["fb_tamanlac"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": p.inner_text("body")[:1500]
        }
    except Exception as e:
        results["fb_tamanlac_err"] = str(e)

    # 5. Facebook Profile thientm
    try:
        p.goto("https://www.facebook.com/thientm/reels", wait_until="domcontentloaded")
        p.wait_for_timeout(7000)
        results["fb_thientm"] = {
            "title": p.title(),
            "url": p.url,
            "snippet": p.inner_text("body")[:1500]
        }
    except Exception as e:
        results["fb_thientm_err"] = str(e)

    p.close()

with open("me-tech/ops/metrics_9333.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved metrics_9333.json successfully!")
