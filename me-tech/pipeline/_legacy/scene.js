// Mê Tech reel builder — timeline data + HTML generator
const fs=require('fs');

const DUR=32.0;
const S=[
 {id:'s1', in:0.0,  out:5.0},
 {id:'s2', in:4.8,  out:10.0},
 {id:'s3', in:9.8,  out:20.2},
 {id:'s4', in:20.0, out:26.8},
 {id:'s5', in:26.6, out:32.0},
];

const CSS=`
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#05070F}
body{font-family:'Be Vietnam Pro',sans-serif;color:#fff}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;
 background:radial-gradient(900px 800px at 12% 10%,rgba(79,156,255,.30),transparent 60%),
            radial-gradient(900px 900px at 92% 90%,rgba(124,92,255,.28),transparent 58%),
            linear-gradient(160deg,#0A1024 0%,#0E1430 55%,#080D1E 100%)}
#grid{position:absolute;inset:-200px;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:64px 64px}
#vig{position:absolute;inset:0;background:radial-gradient(120% 75% at 50% 45%,transparent 45%,rgba(0,0,0,.55) 100%);pointer-events:none}
.scene{position:absolute;inset:0;will-change:opacity,transform}
.el{position:absolute;will-change:opacity,transform}
.pill{display:inline-flex;align-items:center;gap:16px;background:rgba(79,156,255,.14);border:2px solid rgba(79,156,255,.45);color:#8FC2FF;font-weight:700;letter-spacing:.14em;border-radius:999px;padding:18px 38px;font-size:30px}
.dot{width:16px;height:16px;border-radius:50%;background:#4F9CFF;box-shadow:0 0 22px #4F9CFF}
.grad{background:linear-gradient(100deg,#7FC0FF,#B79BFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hl{color:#FFC978}
.rule{height:7px;border-radius:99px;background:linear-gradient(90deg,#4F9CFF,#7C5CFF,transparent);transform-origin:left center}
.card{background:rgba(255,255,255,.055);border:2px solid rgba(255,255,255,.10);border-radius:30px}
.num{font-weight:800;color:#FFC978;line-height:1;font-variant-numeric:tabular-nums}
.brand{display:flex;align-items:center;gap:20px;color:rgba(255,255,255,.55);font-weight:600;letter-spacing:.06em;font-size:30px}
.blogo{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#4F9CFF,#7C5CFF);display:flex;align-items:center;justify-content:center;font-weight:800;color:#0A0F22;font-size:26px}
#wave{position:absolute;display:flex;align-items:center;justify-content:space-between}
#wave i{display:block;width:16px;border-radius:99px;background:linear-gradient(180deg,#7FC0FF,#7C5CFF)}
#grain{position:absolute;inset:0;opacity:.055;pointer-events:none;mix-blend-mode:overlay}
`;

const BARS=26;
const body=`
<div id="stage">
 <div id="grid"></div>

 <div class="scene" id="s1">
   <div class="el" id="s1pill" style="left:90px;top:520px"><div class="pill"><span class="dot"></span>TIN AI · 16.09.2026</div></div>
   <div class="el" id="s1a" style="left:90px;top:640px;font-size:96px;font-weight:800;line-height:1.05;letter-spacing:-.02em">Trợ lý giọng nói</div>
   <div class="el" id="s1b" style="left:90px;top:760px;font-size:126px;font-weight:800;line-height:1.02;letter-spacing:-.03em"><span class="grad">hết im bặt<br>5 giây</span></div>
   <div id="wave" style="left:90px;top:1120px;width:900px;height:260px"></div>
 </div>

 <div class="scene" id="s2">
   <div class="el" id="s2a" style="left:90px;top:640px;font-size:52px;font-weight:600;color:rgba(255,255,255,.72)">Google vừa ra mắt</div>
   <div class="el" id="s2b" style="left:90px;top:720px;font-size:120px;font-weight:800;line-height:1.05;letter-spacing:-.02em"><span class="grad">Gemini 3.8 Live</span></div>
   <div class="el rule" id="s2r" style="left:90px;top:900px;width:320px"></div>
   <div class="el" id="s2c" style="left:90px;top:970px;width:900px;font-size:56px;font-weight:600;line-height:1.4;color:rgba(255,255,255,.85)">AI <span class="hl">vừa nghĩ vừa nói</span>.<br>Hỏi xong không còn im bặt —<br>nó nói “để mình kiểm tra nhé”<br>rồi tra cứu ngầm.</div>
 </div>

 <div class="scene" id="s3">
   <div class="el" id="s3t" style="left:90px;top:400px;font-size:76px;font-weight:800">4 con số <span class="grad">đáng nhớ</span></div>
   <div class="el rule" id="s3r" style="left:90px;top:510px;width:240px"></div>
   ${[0,1,2,3].map(i=>`<div class="el card" id="s3c${i}" style="left:90px;top:${620+i*240}px;width:900px;height:200px;display:flex;align-items:center;gap:40px;padding:0 44px">
      <div class="num" id="s3n${i}" style="font-size:${[86,86,80,64][i]}px;min-width:300px"></div>
      <div style="font-size:34px;color:rgba(255,255,255,.80);line-height:1.35;font-weight:500">${[
        '#1 bảng chất lượng<br>hội thoại giọng nói','ngôn ngữ, tự đổi<br>ngay giữa câu','điểm hiểu âm thanh<br>Big Bench Audio','cho 10 phút<br>hội thoại qua API'][i]}</div></div>`).join('')}
 </div>

 <div class="scene" id="s4">
   <div class="el" id="s4a" style="left:90px;top:560px;width:900px;font-size:44px;font-weight:600;color:rgba(255,255,255,.65)">Vậy thì sao?</div>
   <div class="el" id="s4b" style="left:90px;top:650px;width:900px;font-size:74px;font-weight:800;line-height:1.25">Một tổng đài CSKH<br>tiếng Việt chạy 24/7<br><span class="grad">rẻ hơn tiền điện</span></div>
   <div class="el rule" id="s4r" style="left:90px;top:1000px;width:260px"></div>
   <div class="el" id="s4c" style="left:90px;top:1090px;width:920px;font-size:44px;font-weight:600;line-height:1.45;color:rgba(255,255,255,.82)">Còn nếu bạn đang luyện nói tiếng Anh,<br>đây là <span class="hl">bạn tập kiên nhẫn nhất</span><br><span class="hl">quả đất</span> — nói sai bao nhiêu lần<br>cũng không cau mày.</div>
 </div>

 <div class="scene" id="s5">
   <div class="el" id="s5t" style="left:90px;top:480px;font-size:76px;font-weight:800">Dùng ở <span class="grad">đâu?</span></div>
   <div class="el rule" id="s5r" style="left:90px;top:590px;width:240px"></div>
   ${[['Search Live','miễn phí, có cả 2 bản'],['App Gemini &amp; Workspace','bản Extended Thinking, gói Pro/Ultra'],['Gemini API / AI Studio','cho anh em dev']].map((x,i)=>`
   <div class="el card" id="s5c${i}" style="left:90px;top:${690+i*180}px;width:900px;padding:34px 44px">
     <div style="font-size:46px;font-weight:700">${x[0]}</div>
     <div style="font-size:34px;color:rgba(255,255,255,.62);margin-top:10px;font-weight:500">${x[1]}</div></div>`).join('')}
   <div class="el" id="s5cta" style="left:90px;top:1280px;width:900px;font-size:52px;font-weight:800;line-height:1.3">Theo dõi <span class="grad">Mê Tech</span><br>để không lỡ tin AI.</div>
   <div class="el brand" id="s5b" style="left:90px;top:1460px"><div class="blogo">MT</div>MÊ TECH · AI dễ hiểu</div>
 </div>

 <div id="vig"></div>
 <canvas id="grain" width="270" height="480" style="width:1080px;height:1920px"></canvas>
</div>`;

const JS=`
const SC=${JSON.stringify(S)};
const E=id=>document.getElementById(id);
const cl=(v,a,b)=>Math.max(a,Math.min(b,v));
const easeOut=t=>1-Math.pow(1-t,3);
const easeInOut=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
// p(t, start, dur) -> eased 0..1
const P=(t,s,d)=>easeOut(cl((t-s)/d,0,1));

// build waveform bars
const wave=E('wave');
const BARS=${BARS};
for(let i=0;i<BARS;i++){const b=document.createElement('i');wave.appendChild(b);}
const waveEls=[...wave.children];

// grain
const g=E('grain'),gx=g.getContext('2d');
function grain(seed){const d=gx.createImageData(g.width,g.height);let s=seed*9301+49297;
 for(let i=0;i<d.data.length;i+=4){s=(s*9301+49297)%233280;const v=(s/233280)*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}
 gx.putImageData(d,0,0);}

function fadeUp(el,t,start,dur,dy){const p=P(t,start,dur);el.style.opacity=p;el.style.transform='translateY('+((1-p)*(dy||50))+'px)';}
function fmt(n,dec,suffix){return n.toLocaleString('vi-VN',{minimumFractionDigits:dec,maximumFractionDigits:dec})+(suffix||'');}

window.seek=function(t){
 // scene visibility with crossfade
 for(const s of SC){
   const el=E(s.id);
   const fi=cl((t-s.in)/0.45,0,1), fo=1-cl((t-(s.out-0.45))/0.45,0,1);
   const a=Math.min(fi,fo);
   el.style.opacity=a;
   el.style.transform='translateY('+((1-easeOut(fi))*40)+'px) scale('+(0.985+0.015*easeOut(fi))+')';
   el.style.display=a<=0.001?'none':'block';
 }
 // parallax grid
 E('grid').style.transform='translate('+(-t*10)+'px,'+(-t*6)+'px)';

 // S1
 let u=t-SC[0].in;
 fadeUp(E('s1pill'),t,0.15,0.6,40);
 fadeUp(E('s1a'),t,0.45,0.7,60);
 fadeUp(E('s1b'),t,0.75,0.8,70);
 const wp=P(t,1.15,0.7);
 waveEls.forEach((b,i)=>{
   const base=[.22,.45,.8,1,.72,.5,.3,.66,.9,1,.8,.42,.25,.55,.86,.7,.36,.22,.6,.95,.78,.44,.28,.2,.5,.72][i%26];
   const osc=0.55+0.45*Math.sin(t*6.2+i*0.55)*Math.sin(t*2.1+i*0.2);
   const h=26+base*osc*210*wp;
   b.style.height=h+'px';
   b.style.opacity=(0.30+base*0.7)*wp;
 });

 // S2
 fadeUp(E('s2a'),t,SC[1].in+0.20,0.5,40);
 fadeUp(E('s2b'),t,SC[1].in+0.38,0.6,55);
 const r2=P(t,SC[1].in+0.70,0.5);E('s2r').style.transform='scaleX('+r2+')';E('s2r').style.opacity=r2;
 fadeUp(E('s2c'),t,SC[1].in+0.95,0.7,45);

 // S3
 fadeUp(E('s3t'),t,SC[2].in+0.15,0.5,40);
 const r3=P(t,SC[2].in+0.45,0.45);E('s3r').style.transform='scaleX('+r3+')';E('s3r').style.opacity=r3;
 const TG=[82.6,97,97.7,6000], DEC=[1,0,1,0], SUF=['','','%','đ'], PRE=['','','','~'];
 for(let i=0;i<4;i++){
   const st=SC[2].in+0.75+i*0.85;
   fadeUp(E('s3c'+i),t,st,0.55,55);
   const cp=easeInOut(cl((t-st)/1.05,0,1));
   E('s3n'+i).textContent=PRE[i]+fmt(TG[i]*cp,DEC[i],SUF[i]);
 }

 // S4
 fadeUp(E('s4a'),t,SC[3].in+0.20,0.5,35);
 fadeUp(E('s4b'),t,SC[3].in+0.40,0.7,60);
 const r4=P(t,SC[3].in+0.85,0.5);E('s4r').style.transform='scaleX('+r4+')';E('s4r').style.opacity=r4;
 fadeUp(E('s4c'),t,SC[3].in+1.15,0.7,45);

 // S5
 fadeUp(E('s5t'),t,SC[4].in+0.15,0.5,40);
 const r5=P(t,SC[4].in+0.40,0.45);E('s5r').style.transform='scaleX('+r5+')';E('s5r').style.opacity=r5;
 for(let i=0;i<3;i++) fadeUp(E('s5c'+i),t,SC[4].in+0.60+i*0.28,0.5,45);
 fadeUp(E('s5cta'),t,SC[4].in+1.70,0.6,45);
 fadeUp(E('s5b'),t,SC[4].in+2.05,0.6,35);

 grain(Math.floor(t*30)%97+1);
 return true;
};
window.seek(0);
`;

fs.writeFileSync('video.html',`<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${body}<script>${JS}</script></body></html>`);
console.log('video.html written, duration', DUR);
