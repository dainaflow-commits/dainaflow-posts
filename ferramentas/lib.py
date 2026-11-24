import asyncio
from playwright.async_api import async_playwright
S=1080;H=1350
def ff(n,w,f): return f'@font-face{{font-family:"{n}";font-weight:{w};src:url(fonts/{f})}}'
FONTS=ff("Anton",400,"anton-latin-400-normal.woff2")+''.join(ff("Outfit",w,f"outfit-latin-{w}-normal.woff2") for w in (400,700,800,900))+ff("Caveat",700,"caveat-latin-700-normal.woff2")
def phone(src,x,y,w,r=0,extra=""):
    h=int(w*2.1)
    return f'<div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg);{extra}"><img src="../{src}"></div>'
def arrow(x,y,w,h,d,rot=0,c="#FFB347"):
    return f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);overflow:visible" viewBox="0 0 {w} {h}"><path d="{d}" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def note(t,x,y,rot=-4,s=50,c="#FFB347"): return f'<div class="hand" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);font-size:{s}px;color:{c}">{t}</div>'
def chip(t,x,y,rot=0,cls="chip"): return f'<div class="{cls}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">{t}</div>'
def head(i,N):
    x=(i-1)*S
    d=''.join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(1,N+1))
    return f'<div class="logo" style="left:{x+70}px"><img src="../simbolo_crop.png">@daina_flow_</div><div class="dots" style="left:{x+S-70}px">{d}</div>'
CSS=FONTS+'''*{margin:0;padding:0;box-sizing:border-box}
body{height:1350px;position:relative;overflow:hidden;font-family:Outfit;color:#fff;
background:BGX}
body:after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:6px 6px;pointer-events:none}
.glow{position:absolute;border-radius:50%;pointer-events:none}
.big{position:absolute;font-family:Anton;text-transform:uppercase;letter-spacing:.005em;line-height:.95;text-shadow:0 10px 40px rgba(0,0,0,.4)}
.grad{background:linear-gradient(90deg,#3FC3FF,#1E6BFF 45%,#FFB347);-webkit-background-clip:text;color:transparent}
.grad2{background:linear-gradient(180deg,#FFD08A,#FFB347 50%,#F28C28);-webkit-background-clip:text;color:transparent}
.x{color:#FFB347;font-family:Outfit;font-weight:900;font-size:.6em;vertical-align:.2em}
.ghost{position:absolute;font-family:Anton;font-size:420px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(255,255,255,.08)}
.ghost.blue{-webkit-text-stroke:3px rgba(63,195,255,.22)}
.ph{position:absolute;border-radius:56px;border:11px solid #111;overflow:hidden;background:#fff;box-shadow:0 60px 120px rgba(0,0,0,.7),0 0 0 2px rgba(255,255,255,.15)}
.ph img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.hand{position:absolute;font-family:Caveat;font-weight:700;white-space:nowrap;line-height:1}
.chip{position:absolute;padding:14px 28px;border-radius:999px;font-weight:800;font-size:28px;letter-spacing:.08em;white-space:nowrap}
.chip.amber{background:#FFB347;color:#0a0f24}
.chip.white{background:#fff;color:#0a1440;font-size:32px;letter-spacing:0;box-shadow:0 14px 30px rgba(0,0,0,.35)}
.tag{position:absolute;padding:12px 36px;border-radius:14px;font-family:Anton;font-size:56px;letter-spacing:.08em}
.tag.gray{background:#3a3c42;color:#cfcfcf}.tag.blue{background:linear-gradient(90deg,#1E6BFF,#3FC3FF);box-shadow:0 0 60px rgba(63,195,255,.6)}
.txt{position:absolute;font-size:38px;line-height:1.35;font-weight:400}.txt b{font-weight:800;color:#fff}
.sticker{position:absolute;padding:22px 32px;font-weight:900;font-size:40px;line-height:1.1;border-radius:18px}
.sticker.red{background:#fff;color:#16181d;box-shadow:0 20px 40px rgba(0,0,0,.5)}
.num{position:absolute;width:92px;height:92px;border-radius:50%;background:#FFB347;color:#0a0f24;font-family:Anton;font-size:58px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.5);z-index:3}
.chat{position:absolute;width:380px;background:#0b141a;border-radius:28px;padding:18px;box-shadow:0 40px 80px rgba(0,0,0,.6),0 0 0 2px rgba(255,255,255,.12);z-index:2}
.chat-h{font-weight:700;font-size:24px;color:#8fe3a4;margin-bottom:12px}.wa{color:#53bdeb}
.bub{background:#005c4b;border-radius:18px 4px 18px 18px;padding:16px 20px;font-size:26px;line-height:1.4}
.card{position:absolute;width:450px;height:300px;border-radius:32px;padding:34px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.14);backdrop-filter:blur(10px);box-shadow:0 30px 60px rgba(0,0,0,.35)}
.ic{font-size:64px}.ct{white-space:nowrap;font-family:Anton;font-size:44px;text-transform:uppercase;margin:14px 0 8px;color:#FFB347}.cd{font-size:30px;line-height:1.3;color:#dfe6ff}
.tape{position:absolute;width:1400px;padding:18px 0;background:#fff;color:#000;font-family:Anton;font-size:40px;letter-spacing:.06em;white-space:nowrap;box-shadow:0 20px 40px rgba(0,0,0,.5)}
.price{position:absolute;width:420px;padding:36px 30px;border-radius:30px;background:linear-gradient(160deg,#fff,#dfe8ff);color:#0a1440;text-align:center;box-shadow:0 40px 80px rgba(0,0,0,.6),0 0 100px rgba(63,195,255,.5)}
.de{font-size:40px;text-decoration:line-through;color:#7a86a8;font-weight:700}.por{font-family:Anton;font-size:150px;line-height:1;color:#0B2A8A}.pg{font-size:24px;font-weight:700;color:#1E6BFF}
.cta{position:absolute;padding:30px 44px;border-radius:999px;background:#FF6A00;font-weight:900;font-size:42px;letter-spacing:.02em;box-shadow:0 20px 50px rgba(255,106,0,.45);white-space:nowrap}
.logo{position:absolute;top:66px;display:flex;align-items:center;gap:16px;font-size:30px;font-weight:700;letter-spacing:.04em;z-index:9}.logo img{height:58px}
.cnt{position:absolute;top:78px;width:170px;text-align:right;font-family:Anton;font-size:34px;color:rgba(255,255,255,.55);z-index:9}
.swipe{position:absolute;z-index:10;background:#0a0f24;padding:4px 26px 10px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.6);font-family:Caveat;font-weight:700;font-size:56px;color:#FFB347}
.qb{position:absolute;max-width:900px;padding:34px 44px;border-radius:44px 44px 44px 10px;background:#fff;color:#0a1440;font-family:Anton;font-size:86px;line-height:1;text-transform:uppercase;box-shadow:0 30px 70px rgba(0,0,0,.45)}
.ab{position:absolute;padding:40px 48px;border-radius:44px 44px 10px 44px;background:linear-gradient(135deg,#1E6BFF,#3FC3FF);font-size:40px;line-height:1.35;box-shadow:0 30px 80px rgba(30,107,255,.45)}.ab b{font-weight:900;color:#FFE2B8}
.av{position:absolute;width:86px;height:86px;border-radius:50%;background:#0a0f24;border:3px solid #3FC3FF;display:flex;align-items:center;justify-content:center}.av img{width:58px}
.off{position:absolute;width:190px;height:190px;border-radius:50%;background:#FFB347;color:#0a0f24;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Anton;font-size:76px;line-height:.9;box-shadow:0 20px 50px rgba(255,179,71,.4)}.off small{font-size:34px}
.cal{position:absolute;width:300px;border-radius:30px;overflow:hidden;background:#fff;color:#0a1440;text-align:center;box-shadow:0 40px 80px rgba(0,0,0,.6)}.cal .m{background:#FF6A00;color:#fff;font-weight:900;font-size:40px;padding:14px;letter-spacing:.15em}.cal .d{font-family:Anton;font-size:190px;line-height:1.1}
.dots{position:absolute;top:86px;transform:translateX(-100%);display:flex;gap:10px;z-index:9}.dots i{display:block;width:14px;height:14px;border-radius:9px;background:rgba(255,255,255,.28)}.dots i.on{width:46px;background:#FFB347}
'''
def render(name,B,N,bg,h=1350):
    for i in range(1,N+1): B+=(head(i,N) if N>1 else head(i,N).split('<div class="dots"')[0]) if h==1350 else ''
    css=CSS.replace("BGX",bg).replace("height:1350px","height:%dpx"%h)
    open(f'/home/claude/bf/v2/{name}.html','w').write(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body style="width:{N*S}px">{B}</body></html>')
    async def main():
        async with async_playwright() as p:
            b=await p.chromium.launch();pg=await b.new_page(viewport={'width':N*S,'height':h})
            await pg.goto(f'file:///home/claude/bf/v2/{name}.html');await pg.wait_for_timeout(800)
            for i in range(N): await pg.screenshot(path=f'/home/claude/bf/v2/{name}{i+1}.png',clip={'x':i*S,'y':0,'width':S,'height':h})
            await b.close()
    asyncio.run(main())
    from PIL import Image
    c=min(N,3);r=(N+c-1)//c;w=540;hh=int(w*h/S)
    pv=Image.new('RGB',(c*(w+10)+10,r*(hh+10)+10),'#111')
    for k in range(N): pv.paste(Image.open(f'/home/claude/bf/v2/{name}{k+1}.png').convert('RGB').resize((w,hh)),(10+(k%c)*(w+10),10+(k//c)*(hh+10)))
    pv.save(f'/home/claude/bf/v2/{name}_previa.jpg',quality=86)
