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
    p.goto("https://www.anthropic.com/claude-opus-5-5", wait_until="domcontentloaded")
    p.wait_for_timeout(6000)

    # 1) khoi anh hero: ngay + tieu de
    p.evaluate("window.scrollTo(0,0)")
    p.wait_for_timeout(1200)
    p.screenshot(path="_scratch/hero.png")

    # 2) bang gia: tim div chua ca 'Pricing' va '$0.20'
    h = p.evaluate("""() => {
      let best=null;
      document.querySelectorAll('div,section,table').forEach(e=>{
        const t=(e.innerText||'');
        if(t.includes('Cache reads') && t.includes('$0.20') && t.includes('$20')){
          if(!best || t.length < best.len) best={el:e, len:t.length};
        }
      });
      if(!best) return null;
      best.el.setAttribute('data-shot','price');
      best.el.scrollIntoView({block:'center'});
      return best.len;
    }""")
    print("price block len:", h)
    p.wait_for_timeout(1500)
    el = p.locator("[data-shot='price']").first
    el.screenshot(path="_scratch/price.png")
    print("box", el.bounding_box())
    ctx.close()

a = Image.open("_scratch/hero.png"); b = Image.open("_scratch/price.png")
print("hero", a.size, "price", b.size)
