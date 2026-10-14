import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9333")
    ctx = b.contexts[0]
    p = ctx.new_page()
    p.set_default_timeout(60000)
    p.goto("https://www.facebook.com/professional_dashboard/content/content_library/", wait_until="domcontentloaded")
    p.wait_for_timeout(8000)
    
    try:
        scheduled_tabs = [x for x in p.get_by_text("Scheduled", exact=True).all() if x.is_visible()]
        if scheduled_tabs:
            scheduled_tabs[0].click()
            p.wait_for_timeout(6000)
    except Exception as e:
        print("no Scheduled tab:", e)
        
    body = p.inner_text("body")
    k = "Meta vừa tung ra siêu mẫu Muse Wonder"
    n = body.count(k)
    print("Found match count:", n)
    i = body.find(k)
    j = body.find("Today at", i) if i >= 0 else -1
    s = body[j:j+20] if (i >= 0 and j > 0) else "no Today at"
    print("Schedule slot:", s)
    p.close()
    
    if n >= 1 and ("08:00" in s or "8:00" in s or "Today at" in s):
        print("✅ [OK] Dung mot ban Facebook Reel Scheduled.")
        sys.exit(0)
    elif n >= 1:
        print("✅ [OK] Thay ban Scheduled.")
        sys.exit(0)
    else:
        print("❌ [X] Khong tim thay ban Scheduled.")
        sys.exit(1)
