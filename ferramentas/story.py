from lib import *
import lib,sys
lib.CSS+='.cover{position:absolute;left:150px;top:520px;width:780px;border-radius:22px;transform:rotate(-4deg);box-shadow:0 0 0 3px rgba(255,255,255,.2),0 0 140px rgba(30,107,255,.6),0 60px 120px rgba(0,0,0,.7)}'
X=[("st_ad","ad1.png","POST NOVO","antes x depois real"),("st_duv","duv1.png","POST NOVO","suas dúvidas respondidas"),("st_hoje","hoje1.png","É HOJE","os preços estão no ar"),("st_ult","ult1.png","ÚLTIMO DIA","termina hoje às 23:59")]
for n,img,t,h in X:
    B=f'''<div class="glow" style="left:-100px;top:400px;width:1300px;height:1300px;background:radial-gradient(circle,rgba(30,107,255,.7),transparent 60%)"></div>
<div class="logo" style="left:70px;top:120px"><img src="../simbolo_crop.png">@daina_flow_</div>
<div class="big" style="left:70px;top:230px;font-size:190px;padding-top:.15em;margin-top:-.15em">{t.split()[0]} <span class="grad2">{" ".join(t.split()[1:])}</span></div>
<img class="cover" src="{img}">
<div class="hand" style="right:70px;top:1530px;font-size:58px;color:#FFB347;transform:rotate(-5deg)">{h}</div>
<div class="cta" style="left:50%;transform:translateX(-50%);top:1690px">VER NO FEED ↓</div>'''
    lib.render(n,B,1,"linear-gradient(180deg,#060B22,#0B2A8A)",1920)
