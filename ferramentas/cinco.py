from lib import *
import lib
lib.CSS+='''body{color:#0a1440}.big{text-shadow:none}.txt{color:#33406b}.txt b{color:#0a1440}
.dots i{background:rgba(10,20,64,.18)}.dots i.on{background:#1E6BFF}.logo{color:#0a1440}
.ig{position:absolute;width:560px;padding:40px;border-radius:40px;background:#fff;box-shadow:0 40px 90px rgba(10,30,90,.18),0 0 0 1px rgba(10,20,64,.06);font-size:28px;line-height:1.4;color:#111}
.ig .av2{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#FFB347,#1E6BFF);display:flex;align-items:center;justify-content:center;font-family:Anton;font-size:56px;color:#fff;float:left;margin-right:28px}
.ig .st{display:flex;gap:28px;padding-top:24px;font-size:24px;color:#555}.ig .st b{display:block;font-size:32px;color:#111}
.ig .nm{clear:both;padding-top:26px;font-weight:800;font-size:30px}.ig .lk{color:#00376b;font-weight:700}
.sheet{position:absolute;width:520px;border-radius:36px 36px 0 0;background:#fff;padding:26px 36px;box-shadow:0 -10px 80px rgba(10,30,90,.2);font-size:28px}
.sheet .h{width:70px;height:8px;border-radius:9px;background:#ddd;margin:0 auto 20px}.sheet .t{font-weight:800;text-align:center;margin-bottom:12px}
.sheet .r{padding:20px 0;border-top:1px solid #eee;color:#00376b}.sheet .r small{display:block;color:#999;font-size:22px}
.circle{position:absolute;border:6px solid #FF6A00;border-radius:50%;transform:rotate(-6deg)}
.app{position:absolute;padding:22px 30px;border-radius:24px;background:#fff;font-weight:800;font-size:32px;box-shadow:0 20px 50px rgba(10,30,90,.15);white-space:nowrap}
.ck2{position:absolute;width:450px;padding:30px 34px;border-radius:30px;background:#fff;box-shadow:0 24px 60px rgba(10,30,90,.12);font-size:30px;line-height:1.3}.ck2 b{display:block;font-family:Anton;font-size:44px;font-weight:400;color:#1E6BFF;text-transform:uppercase;margin-bottom:6px}
.grad{background:linear-gradient(90deg,#1E6BFF,#3FC3FF);-webkit-background-clip:text;color:transparent}.app{font-size:42px!important}
.chip.navy{background:#0a1440;color:#fff}
'''
N=6;o=lambda i:(i-1)*S;B=''
def IG(x,y,rot):
    return f'''<div class="ig" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="av2">L</div>
<div class="st"><div><b>312</b>posts</div><div><b>4.890</b>seguidores</div><div><b>402</b>seguindo</div></div>
<div class="nm">Ateliê Lumi · Nail Designer</div>Unhas que duram 💅 Igarapé/MG<br>Agenda aberta para dezembro<br><span class="lk">🔗 wa.me/5531… e mais 4</span></div>'''
x=o(1)
B+=f'''<div class="glow" style="left:{x+400}px;top:300px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(30,107,255,.25),transparent 62%)"></div>
{chip("SEU PERFIL",x+70,190,-2,"chip navy")}
<div class="big" style="left:{x+66}px;top:270px;font-size:165px;line-height:.86">5 LINKS<br>NA BIO.<br><span class="grad">ZERO<br>CLIQUE?</span></div>
{IG(x+420,880,-4)}
<div class="circle" style="left:{x+440}px;top:1170px;width:480px;height:110px"></div>
{note("ninguém toca aqui",x+80,1220,-6,52,"#FF6A00")}
<div class="swipe" style="left:{x+S-300}px;top:200px;color:#FFB347">arrasta →</div>'''
x=o(2)
B+=f'''<div class="glow" style="left:{x+300}px;top:500px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(255,179,71,.25),transparent 62%)"></div>
<div class="big" style="left:{x+70}px;top:190px;font-size:130px;line-height:.9">O INSTAGRAM<br>MOSTRA <span class="grad">SÓ 1.</span></div>
<div class="txt" style="left:{x+72}px;top:470px;width:400px">Os outros 4 ficam escondidos em <b>"e mais 4"</b>. Quem toca vê uma lista crua: sem foto, sem preço, sem explicação.</div>
<div class="sheet" style="left:{x+500}px;top:560px;transform:rotate(3deg)"><div class="h"></div><div class="t">Links</div>
<div class="r">wa.me/5531999…<small>wa.me</small></div><div class="r">agenda.app/lumi<small>agenda.app</small></div><div class="r">drive.google.com/…<small>drive.google.com</small></div><div class="r">maps.app.goo.gl/…<small>maps.app.goo.gl</small></div><div class="r">linktr…/lumi<small>linktr…</small></div></div>
{note("qual eu toco??",x+110,880,-5,64,"#FF6A00")}
{arrow(x+300,960,200,160,"M10 20 C 80 30, 150 70, 180 140 M150 118 L182 142 L190 102",0,"#FF6A00")}'''
x=o(3)
apps=[("💬 WhatsApp",60,480,-4),("📅 Agenda",640,470,5),("📁 Drive",50,820,3),("📍 Maps",720,800,-3),("🔗 Outro app",360,1000,-2)]
B+=f'''<div class="big" style="left:{x+70}px;top:190px;font-size:130px;line-height:.9">CADA LINK,<br><span class="grad">UM LUGAR.</span></div>'''
for t,ax,ay,r in apps: B+=f'<div class="app" style="left:{x+ax}px;top:{ay}px;transform:rotate({r}deg)">{t}</div>'
B+=f'''<svg style="position:absolute;left:{x}px;top:0;width:1080px;height:1350px">{''.join(f'<line x1="540" y1="790" x2="{ax+150}" y2="{ay+40}" stroke="#1E6BFF" stroke-width="4" stroke-dasharray="12 12" opacity=".5"/>' for t,ax,ay,r in apps)}</svg>
<div class="ig" style="left:{x+430}px;top:700px;width:220px;padding:24px;text-align:center;border-radius:50%;height:220px;display:flex;align-items:center;justify-content:center;font-family:Anton;font-size:38px;color:#0a1440">SEU<br>PERFIL</div>
<div class="txt" style="left:{x+72}px;top:1120px;width:900px">A cliente sai do seu perfil, se perde no caminho… <b>e desiste.</b></div>'''
x=o(4)
B+=f'''<div class="glow" style="left:{x-200}px;top:200px;width:1200px;height:1200px;background:radial-gradient(circle,rgba(30,107,255,.35),transparent 60%)"></div>
{phone("jamy_0.png",x+70,200,450,-5,"box-shadow:0 0 0 3px rgba(63,195,255,.7),0 0 120px rgba(30,107,255,.45),0 50px 100px rgba(10,30,90,.3)")}
{chip("A SOLUÇÃO",x+590,200,2,"chip amber")}
<div class="big" style="left:{x+584}px;top:290px;font-size:140px;line-height:.9">1 LINK.<br><span class="grad">TUDO<br>NELE.</span></div>
<div class="txt" style="left:{x+590}px;top:760px;width:420px">Uma página com a cara da sua marca, onde a cliente <b>vê, entende e chama</b> sem sair do caminho.</div>
{note("exemplo real 👆",x+620,1100,-5,52,"#FF6A00")}'''
x=o(5)
cks=[("WhatsApp","com a mensagem pronta"),("Agenda","para marcar sozinha"),("Portfólio","seus melhores trabalhos"),("Preços","sem precisar perguntar"),("Endereço","com o mapa num toque"),("Avaliações","de quem já foi")]
B+=f'''<div class="big" style="left:{x+70}px;top:180px;font-size:120px;line-height:.9">O QUE CABE<br><span class="grad">NESSE 1 LINK:</span></div>'''
for k,(t,d) in enumerate(cks):
    B+=f'<div class="ck2" style="left:{x+70+(k%2)*490}px;top:{450+(k//2)*250}px">✓ <b style="display:inline">{t}</b><br>{d}</div>'
x=o(6)
B+=f'''<div class="glow" style="left:{x+100}px;top:250px;width:1100px;height:1100px;background:radial-gradient(circle,rgba(30,107,255,.3),transparent 60%)"></div>
<div class="big" style="left:{x+70}px;top:200px;font-size:130px;line-height:.9">TROCA OS 5<br>POR <span class="grad">1 QUE<br>FUNCIONA.</span></div>
<div class="price" style="left:{x+600}px;top:590px;transform:rotate(5deg)"><div class="de">de R$ 450</div><div class="por">R$ 250</div><div class="pg">Flow Bio · pagamento único<br>sem mensalidade</div></div>
<div class="txt" style="left:{x+74}px;top:700px;width:480px">Feito do zero, com a cara da sua marca. <b>Black Friday só até 28/11.</b></div>
<div class="cta" style="left:{x+70}px;top:1030px">TOQUE NO LINK DA BIO ↑</div>
<div class="txt" style="left:{x+80}px;top:1160px;width:900px;font-size:34px">ou envie uma mensagem no <b>direct</b> 💬</div>'''
render('cinco',B,N,"linear-gradient(90deg,#F4F8FF 0,#E6F0FF 2160px,#FFF4E8 3240px,#EAF2FF 4320px,#DCE8FF 6480px)")
