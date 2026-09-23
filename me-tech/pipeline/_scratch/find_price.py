import tempfile
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
    p.goto("https://www.anthropic.com/claude-opus-5-5", wait_until="domcontentloaded")
    p.wait_for_timeout(6000)
    res = p.evaluate("""() => {
      const out=[];
      const want=['$4','$20','$0.20','40%','Pricing','pricing','cache'];
      document.querySelectorAll('p,li,td,th,h1,h2,h3,div').forEach(e=>{
        if(e.children.length>3) return;
        const t=(e.innerText||'').trim();
        if(t.length<3||t.length>400) return;
        if(!want.some(w=>t.includes(w))) return;
        const r=e.getBoundingClientRect();
        out.push({t:t.slice(0,160), x:Math.round(r.x+scrollX), y:Math.round(r.y+scrollY), w:Math.round(r.width), h:Math.round(r.height), tag:e.tagName});
      });
      return out;
    }""")
    seen=set()
    for r in res:
        k=(r['y'],r['t'][:40])
        if k in seen: continue
        seen.add(k)
        print(r['tag'], r['y'], r['h'], '|', r['t'].replace('\n',' / ')[:150])
    ctx.close()
