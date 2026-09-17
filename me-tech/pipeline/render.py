#!/usr/bin/env python3
"""Dựng video từ timing.json — timeline suy ra từ giọng đọc, không đoán.

    python render.py <timing.json> <vo.wav> [outdir]
"""
import json, sys, os, subprocess, math, shutil

W, H, FPS = 1080, 1920, 30
ACCENT_A, ACCENT_B, GOLD = "#4F9CFF", "#7C5CFF", "#FFC978"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#05070F}
body{font-family:'Be Vietnam Pro',sans-serif;color:#fff}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;
 background:radial-gradient(900px 800px at 12% 10%,rgba(79,156,255,.30),transparent 60%),
            radial-gradient(900px 900px at 92% 90%,rgba(124,92,255,.28),transparent 58%),
            linear-gradient(160deg,#0A1024 0%,#0E1430 55%,#080D1E 100%)}
#grid{position:absolute;inset:-240px;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:64px 64px}
#vig{position:absolute;inset:0;background:radial-gradient(120% 75% at 50% 45%,transparent 45%,rgba(0,0,0,.55) 100%)}
.scene{position:absolute;inset:0}
.el{position:absolute;left:90px;width:900px;will-change:opacity,transform}
.pill{display:inline-flex;align-items:center;gap:16px;background:rgba(79,156,255,.14);border:2px solid rgba(79,156,255,.45);color:#8FC2FF;font-weight:700;letter-spacing:.14em;border-radius:999px;padding:18px 38px;font-size:30px}
.dot{width:16px;height:16px;border-radius:50%;background:#4F9CFF;box-shadow:0 0 22px #4F9CFF}
em{font-style:normal;background:linear-gradient(100deg,#7FC0FF,#B79BFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
b{color:#FFC978;font-weight:600}
.rule{height:7px;border-radius:99px;background:linear-gradient(90deg,#4F9CFF,#7C5CFF,transparent);transform-origin:left center}
.card{background:rgba(255,255,255,.055);border:2px solid rgba(255,255,255,.10);border-radius:30px}
.num{font-weight:800;color:#FFC978;line-height:1;font-variant-numeric:tabular-nums}
.brand{position:absolute;left:90px;display:flex;align-items:center;gap:20px;color:rgba(255,255,255,.55);font-weight:600;letter-spacing:.06em;font-size:30px}
.blogo{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#4F9CFF,#7C5CFF);display:flex;align-items:center;justify-content:center;font-weight:800;color:#0A0F22;font-size:26px}
#wave{position:absolute;left:90px;width:900px;display:flex;align-items:center;justify-content:space-between}
#wave i{display:block;width:16px;border-radius:99px;background:linear-gradient(180deg,#7FC0FF,#7C5CFF)}
"""

SEEK_JS = """
const TL = __TIMELINE__;
const E = id => document.getElementById(id);
const cl = (v,a,b) => Math.max(a, Math.min(b, v));
const easeOut = t => 1 - Math.pow(1-t, 3);
const easeInOut = t => t<.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2;
const P = (t,s,d) => easeOut(cl((t-s)/d, 0, 1));
const waveEls = [...document.querySelectorAll('#wave i')];
const g = document.getElementById('grain'), gx = g.getContext('2d');
function grain(seed){const d=gx.createImageData(g.width,g.height);let s=seed*9301+49297;
 for(let i=0;i<d.data.length;i+=4){s=(s*9301+49297)%233280;const v=(s/233280)*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}
 gx.putImageData(d,0,0);}
function fmt(n,dec){return n.toLocaleString('vi-VN',{minimumFractionDigits:dec,maximumFractionDigits:dec});}

window.seek = function(t){
  // --- scenes: hiện từ khi beat đầu bắt đầu tới khi beat cuối kết thúc
  for(const sc of TL.scenes){
    const el = E('sc-'+sc.id);
    const fi = cl((t - (sc.in - TL.pre))/0.40, 0, 1);
    const fo = 1 - cl((t - (sc.out + TL.post - 0.40))/0.40, 0, 1);
    const a = Math.min(fi, fo);
    el.style.display = a <= .001 ? 'none' : 'block';
    el.style.opacity = a;
    el.style.transform = 'translateY(' + ((1-easeOut(fi))*34) + 'px)';
  }
  E('grid').style.transform = 'translate(' + (-t*9) + 'px,' + (-t*5) + 'px)';

  // --- beats: mỗi phần tử hiện đúng lúc câu của nó bắt đầu được đọc
  for(const b of TL.beats){
    const el = E('el-'+b.id); if(!el) continue;
    const st = b.start - TL.pre;
    const p = P(t, st, 0.42);
    el.style.opacity = p;
    el.style.transform = 'translateY(' + ((1-p)*52) + 'px)';
    if(b.kind === 'rule'){ el.style.transform = 'scaleX(' + p + ')'; }
    if(b.kind === 'num'){
      const n = E('n-'+b.id);
      const cp = easeInOut(cl((t - st)/Math.min(1.15, Math.max(0.5, b.dur*0.55)), 0, 1));
      n.textContent = b.prefix + fmt(b.value*cp, b.dec) + b.suffix;
    }
  }

  // --- waveform chỉ sống trong cảnh hook
  const hs = TL.scenes.find(s=>s.id==='hook');
  if(hs){
    const on = cl((t - hs.in + TL.pre)/0.6, 0, 1) * (1 - cl((t - hs.out - TL.post + 0.4)/0.4, 0, 1));
    waveEls.forEach((el,i)=>{
      const base=[.22,.45,.8,1,.72,.5,.3,.66,.9,1,.8,.42,.25,.55,.86,.7,.36,.22,.6,.95,.78,.44,.28,.2,.5,.72][i%26];
      const osc=0.55+0.45*Math.sin(t*6.4+i*0.55)*Math.sin(t*2.2+i*0.2);
      el.style.height = (24 + base*osc*200*on) + 'px';
      el.style.opacity = (0.30 + base*0.7) * on;
    });
  }
  grain(Math.floor(t*30)%97 + 1);
  return true;
};
window.seek(0);
"""

def build_html(tl, date_label):
    scenes, beats, html = {}, [], []
    for s in tl["segments"]:
        scenes.setdefault(s["scene"], []).append(s)

    body = ['<div id="stage"><div id="grid"></div>']
    # layout cursors per scene
    for sid, segs in scenes.items():
        inner = []
        y = 560
        if sid == "hook":
            inner.append(f'<div class="el" id="el-_pill" style="top:470px"><div class="pill"><span class="dot"></span>{date_label}</div></div>')
            beats.append({"id":"_pill","start":segs[0]["start"],"dur":.5,"kind":"el"})
        for s in segs:
            sh, bid = s["show"], s["id"]
            t = sh["type"]
            if t == "hook":
                inner.append(f'<div class="el" id="el-{bid}" style="top:600px;font-size:100px;font-weight:800;line-height:1.04;letter-spacing:-.02em">{sh["line1"]}<br><em>{sh["line2"]}</em></div>')
                inner.append('<div id="wave" style="top:1130px;height:250px">' + '<i></i>'*26 + '</div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"el"})
            elif t == "title":
                inner.append(f'<div class="el" id="el-{bid}" style="top:600px"><div style="font-size:50px;font-weight:600;color:rgba(255,255,255,.72)">{sh["kicker"]}</div><div style="font-size:112px;font-weight:800;line-height:1.05;letter-spacing:-.02em;margin-top:10px"><em>{sh["title"]}</em></div></div>')
                inner.append(f'<div class="el rule" id="el-{bid}_r" style="top:800px;width:320px"></div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"el"})
                beats.append({"id":bid+"_r","start":s["start"]+0.5,"dur":.5,"kind":"rule"})
            elif t == "body":
                inner.append(f'<div class="el" id="el-{bid}" style="top:870px;font-size:54px;font-weight:600;line-height:1.42;color:rgba(255,255,255,.86)">{sh["text"]}</div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"el"})
            elif t == "header":
                inner.append(f'<div class="el" id="el-{bid}" style="top:430px;font-size:76px;font-weight:800">{sh["title"]}</div>')
                inner.append(f'<div class="el rule" id="el-{bid}_r" style="top:540px;width:240px"></div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"el"})
                beats.append({"id":bid+"_r","start":s["start"]+0.35,"dur":.4,"kind":"rule"})
                y = 620
            elif t == "num":
                inner.append(f'<div class="el card" id="el-{bid}" style="top:{y}px;height:200px;display:flex;align-items:center;gap:36px;padding:0 44px">'
                             f'<div class="num" id="n-{bid}" style="font-size:{72 if sh["value"]>=1000 else 84}px;min-width:300px"></div>'
                             f'<div style="font-size:34px;color:rgba(255,255,255,.80);line-height:1.35;font-weight:500">{sh["label"]}</div></div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"num",
                              "value":sh["value"],"dec":sh["dec"],"prefix":sh.get("prefix",""),"suffix":sh.get("suffix","")})
                y += 240
            elif t == "bullet":
                inner.append(f'<div class="el card" id="el-{bid}" style="top:{y}px;padding:32px 44px">'
                             f'<div style="font-size:46px;font-weight:700">{sh["name"]}</div>'
                             f'<div style="font-size:33px;color:rgba(255,255,255,.62);margin-top:10px;font-weight:500">{sh["sub"]}</div></div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"el"})
                y += 190
            elif t == "cta":
                inner.append(f'<div class="el" id="el-{bid}" style="top:760px;font-size:74px;font-weight:800;line-height:1.3">{sh["text"]}</div>')
                inner.append(f'<div class="el brand" id="el-{bid}_b" style="top:1060px;position:absolute"><div class="blogo">MT</div>MÊ TECH · AI dễ hiểu</div>')
                beats.append({"id":bid,"start":s["start"],"dur":s["dur"],"kind":"el"})
                beats.append({"id":bid+"_b","start":s["start"]+0.6,"dur":.5,"kind":"el"})
        body.append(f'<div class="scene" id="sc-{sid}">' + "".join(inner) + '</div>')

    body.append('<div id="vig"></div><canvas id="grain" width="270" height="480" style="position:absolute;inset:0;opacity:.055;mix-blend-mode:overlay;width:1080px;height:1920px"></canvas></div>')

    timeline = {"pre": 0.45, "post": 0.35, "beats": beats,
                "scenes": [{"id": k, "in": v[0]["start"], "out": v[-1]["end"]} for k, v in scenes.items()]}
    js = SEEK_JS.replace("__TIMELINE__", json.dumps(timeline, ensure_ascii=False))
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(body)}<script>{js}</script></body></html>', timeline


def main():
    tpath, vopath = sys.argv[1], sys.argv[2]
    outdir = sys.argv[3] if len(sys.argv) > 3 else "."
    tl = json.load(open(tpath, encoding="utf-8"))
    html, timeline = build_html(tl, tl.get("date_label", ""))
    WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".work")
    os.makedirs(WORK, exist_ok=True)
    open(os.path.join(WORK, "video.html"), "w", encoding="utf-8").write(html)
    total = tl["total"]
    print(f"scenes={len(timeline['scenes'])} beats={len(timeline['beats'])} total={total:.2f}s")
    json.dump(timeline, open(os.path.join(WORK,"timeline.debug.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

    # --- frames
    from playwright.sync_api import sync_playwright
    FR = os.path.join(WORK, "frames")
    os.makedirs(FR, exist_ok=True)
    for f in os.listdir(FR): os.remove(os.path.join(FR, f))
    n = int(round(total * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto("file://" + os.path.join(WORK, "video.html"))
        pg.wait_for_function("window.seek")
        pg.wait_for_timeout(500)
        for i in range(n):
            pg.evaluate("t => window.seek(t)", i / FPS)
            pg.screenshot(path=os.path.join(FR, f"f{i:05d}.jpg"), type="jpeg", quality=90)
            if i % 150 == 0: print("  frame", i, "/", n, flush=True)
        b.close()
    print("frames done", n)

if __name__ == "__main__":
    main()
