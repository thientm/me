const {chromium}=require('playwright');
const fs=require('fs');
(async()=>{
 const mode=process.argv[2]||'full';
 const FPS=30, DUR=32.0;
 const b=await chromium.launch({args:['--no-sandbox','--font-render-hinting=none','--disable-lcd-text']});
 const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('file://'+__dirname+'/video.html');
 await p.waitForFunction(()=>window.seek);
 await p.waitForTimeout(600);
 if(mode==='preview'){
   const ts=process.argv.slice(3).map(Number);
   for(const t of ts){ await p.evaluate(x=>window.seek(x),t);
     await p.screenshot({path:`prev_${String(t).replace('.','_')}.jpg`,type:'jpeg',quality:88}); }
 } else {
   fs.mkdirSync('frames',{recursive:true});
   const N=Math.round(DUR*FPS);
   for(let i=0;i<N;i++){ const t=i/FPS;
     await p.evaluate(x=>window.seek(x),t);
     await p.screenshot({path:`frames/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:90});
     if(i%120===0) console.log('frame',i,'/',N);
   }
   console.log('done',N,'frames');
 }
 await b.close();
})();
