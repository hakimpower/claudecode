import numpy as np, wave
SR=44100; D=2.3; N=int(SR*D)
out=np.zeros(N)
rng=np.random.default_rng(42)
def coin(t0, f0, amp):
    n=int(0.35*SR); t=np.arange(n)/SR
    ratios=[1.0,1.47,2.09,2.56,3.42]; decs=[18,24,30,40,55]
    s=np.zeros(n)
    for r,d in zip(ratios,decs):
        s+=np.sin(2*np.pi*f0*r*t+rng.uniform(0,6.28))*np.exp(-d*t)*rng.uniform(.5,1)/r**0.5
    # strike transient
    k=int(0.004*SR); s[:k]+=rng.normal(0,0.8,k)*np.linspace(1,0,k)
    i=int(t0*SR); e=min(N,i+n); out[i:e]+=amp*s[:e-i]
# cascade: accelerating pour then thinning
t=0.02; times=[]
while t<1.25:
    times.append(t)
    gap=0.09-0.06*np.sin(np.pi*min(t/1.25,1))
    t+=gap*rng.uniform(.6,1.3)
for i,t0 in enumerate(times):
    coin(t0, rng.uniform(2300,3900), rng.uniform(.35,.7)*(1-0.4*t0/1.3))
    if rng.random()<.4: coin(t0+rng.uniform(.01,.03), rng.uniform(2600,4200), .3)
# "ka-ching" register bell
def bell(t0,f,amp,dec=3.5):
    n=int(1.1*SR); tt=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*h*tt)*np.exp(-dec*h**0.6*tt)/h for h in [1,2,3,4.2])
    i=int(t0*SR); e=min(N,i+n); out[i:e]+=amp*s[:e-i]
k=int(0.03*SR); i=int(0.02*SR); out[i:i+k]+=rng.normal(0,.5,k)*np.exp(-np.linspace(0,6,k))
bell(0.05,1568,.55); bell(0.17,2093,.6)
bell(1.05,2093,.35,2.6); bell(1.13,2637,.4,2.6)
# simple room: few taps
y=out.copy()
for dl,g in [(0.031,.25),(0.057,.18),(0.089,.12),(0.13,.08)]:
    d=int(dl*SR); y[d:]+=g*out[:-d]
fade=int(0.25*SR); y[-fade:]*=np.linspace(1,0,fade)
y/=np.max(np.abs(y))*1.12
w=wave.open(__import__('sys').argv[1],'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((y*32767).astype('<i2').tobytes()); w.close()
