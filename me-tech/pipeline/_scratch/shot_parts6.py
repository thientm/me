import tempfile
from playwright.sync_api import sync_playwright
from PIL import Image
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

    for t in ("Accept all", "Accept", "I agree", "Got it", "Reject all"):
        try:
            b = p.get_by_role("button", name=t, exact=False)
            if b.count() and b.first.is_visible():
                b.first.click(); p.wait_for_timeout(1000); break
        except Exception:
            pass
    p.evaluate("window.scrollTo(0,0)")
    p.wait_for_timeout(1500)
    p.screenshot(path="_scratch/hero6.png")

    n = p.evaluate("""() => {
      let best=null;
      document.querySelectorAll('div,section,table,figure').forEach(e=>{
        const t=(e.innerText||'');
        if(t.includes('$4 \\u2192 $2') && t.includes('$0.20 \\u2192 $0.10') && t.includes('per 1 million')){
          if(!best || t.length < best.len) best={el:e, len:t.length};
        }
      });
      if(!best) return null;
      best.el.setAttribute('data-shot','price');
      best.el.scrollIntoView({block:'center'});
      return best.len;
    }""")
    print("price block len:", n)
    p.wait_for_timeout(1500)
    el = p.locator("[data-shot='price']").first
    el.screenshot(path="_scratch/price6.png")
    print("box", el.bounding_box())
    ctx.close()

a = Image.open("_scratch/hero6.png"); b = Image.open("_scratch/price6.png")
print("hero", a.size, "price", b.size)
W = max(a.width, b.width)
out = Image.new("RGB", (W, a.height + b.height), (0, 0, 0))
out.paste(a, ((W - a.width)//2, 0))
out.paste(b, ((W - b.width)//2, a.height))
out.save("shots/gpt6-sol-luna.png")
print("ghep ->", out.size, "| hero cao", a.height)
