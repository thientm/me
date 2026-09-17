import numpy as np, wave, struct, sys, os
WORK=os.path.join(os.path.dirname(os.path.abspath(__file__)),'.work'); os.makedirs(WORK,exist_ok=True)
SR=48000; DUR=float(sys.argv[1]) if len(sys.argv)>1 else 33.0; BPM=84.0
n=int(SR*DUR); t=np.arange(n)/SR
beat=60.0/BPM

def env_at(times, attack, decay, curve=2.0):
    e=np.zeros(n)
    for ts in times:
        i0=int(ts*SR)
        if i0>=n: continue
        L=int((attack+decay)*SR); L=min(L,n-i0)
        x=np.arange(L)/SR
        a=np.clip(x/max(attack,1e-4),0,1)
        d=np.exp(-np.maximum(x-attack,0)/max(decay/4,1e-4))
        e[i0:i0+L]=np.maximum(e[i0:i0+L], (a*d)**1.0)
    return e

def lp(x, cutoff):
    a=np.exp(-2*np.pi*cutoff/SR); y=np.zeros_like(x); prev=0.0
    # vectorised-ish one-pole via lfilter
    from scipy.signal import lfilter
    return lfilter([1-a],[1,-a],x)
try:
    from scipy.signal import lfilter
    HAVE_SCIPY=True
except Exception:
    HAVE_SCIPY=False
    def lp(x,cutoff):
        a=np.exp(-2*np.pi*cutoff/SR); y=np.empty_like(x); p=0.0
        for i in range(len(x)):
            p=(1-a)*x[i]+a*p; y[i]=p
        return y

def hp(x,cutoff):
    return x-lp(x,cutoff)

NOTE=lambda m: 440.0*2**((m-69)/12)
# Am7 - Fmaj7 - Cmaj7 - G  (4 beats each)
CH=[[45,57,60,64,67],[41,53,57,60,65],[48,52,55,60,64],[43,55,59,62,67]]
bar=4*beat
pad=np.zeros(n)
for k in range(int(DUR/bar)+1):
    ch=CH[k%len(CH)]; s=k*bar
    i0=int(s*SR); i1=min(int((s+bar+0.6)*SR),n)
    if i0>=n: break
    L=i1-i0; x=np.arange(L)/SR
    a=np.clip(x/0.35,0,1)*np.exp(-np.maximum(x-bar*0.7,0)/0.45)
    seg=np.zeros(L)
    for j,m in enumerate(ch):
        f=NOTE(m); amp=[0.55,0.30,0.26,0.22,0.16][j]
        for det in (-0.0025,0.0,0.0025):
            seg+=amp*np.sin(2*np.pi*f*(1+det)*(x+s))/3
        seg+=amp*0.12*np.sin(2*np.pi*f*2*(x+s))
    pad[i0:i1]+=seg*a
pad=lp(pad,1400)
lfo=0.85+0.15*np.sin(2*np.pi*0.12*t)
pad*=lfo

# bass on beats 1 and 3
bt=[k*bar for k in range(int(DUR/bar)+1)]+[k*bar+2*beat for k in range(int(DUR/bar)+1)]
bass=np.zeros(n)
for k in range(int(DUR/bar)+1):
    root=CH[k%len(CH)][0]-12
    for off in (0.0,2*beat):
        s=k*bar+off; i0=int(s*SR)
        if i0>=n: continue
        L=min(int(1.1*beat*SR),n-i0); x=np.arange(L)/SR
        e=np.clip(x/0.02,0,1)*np.exp(-x/0.28)
        bass[i0:i0+L]+=0.42*np.sin(2*np.pi*NOTE(root)*(x+s))*e
bass=lp(bass,220)

# kick
kick=np.zeros(n)
for k in range(int(DUR/beat)+1):
    if k%2: continue
    s=k*beat; i0=int(s*SR)
    if i0>=n: continue
    L=min(int(0.22*SR),n-i0); x=np.arange(L)/SR
    f=95*np.exp(-x/0.035)+46
    ph=2*np.pi*np.cumsum(f)/SR
    kick[i0:i0+L]+=0.55*np.sin(ph)*np.exp(-x/0.075)

# hats on offbeats
rng=np.random.default_rng(7); noise=rng.standard_normal(n)
hats=np.zeros(n)
for k in range(int(DUR/(beat/2))+1):
    if k%2==0: continue
    s=k*beat/2; i0=int(s*SR)
    if i0>=n: continue
    L=min(int(0.06*SR),n-i0); x=np.arange(L)/SR
    hats[i0:i0+L]+=0.11*noise[i0:i0+L]*np.exp(-x/0.012)
hats=hp(hats,5500)

kenv=np.minimum(1.0,np.convolve(np.abs(kick),np.ones(int(0.05*SR))/(0.05*SR),mode='same')*6)
mix=pad*(1-0.30*kenv)*0.62 + bass*0.75 + kick*0.85 + hats*0.9

# simple stereo widening + short reverb tail
def delay(x,ms,g):
    d=int(SR*ms/1000); y=np.zeros_like(x); y[d:]=x[:-d]*g; return y
rev=delay(mix,63,0.22)+delay(mix,97,0.17)+delay(mix,131,0.12)
rev=lp(rev,2600)
L=mix+rev*0.9+delay(mix,11,0.25)
R=mix+rev*0.75+delay(mix,17,0.25)

fi=np.clip(t/1.8,0,1); fo=np.clip((DUR-t)/2.6,0,1)
L*=fi*fo; R*=fi*fo
peak=max(np.abs(L).max(),np.abs(R).max())
L=L/peak*0.82; R=R/peak*0.82
st=np.empty(n*2); st[0::2]=L; st[1::2]=R
pcm=(np.clip(st,-1,1)*32767).astype('<i2')
with wave.open(os.path.join(WORK,'bed.wav'),'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('bed.wav written', DUR, 's, scipy=', HAVE_SCIPY)
