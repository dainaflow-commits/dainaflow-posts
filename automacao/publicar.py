"""Publicador da Daina Flow: lê automacao/agenda.json e publica no Instagram
pela API oficial o que já chegou no horário. Roda no GitHub Actions.

Nunca imprime chaves. A chave fica criptografada em automacao/token.enc
(senha = segredo IG_APP_SECRET), gerada pelo workflow "Configurar chave".
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
AGENDA = os.path.join(AQUI, "agenda.json")
FEITOS = os.path.join(AQUI, "publicados.json")
TOKEN_ENC = os.path.join(AQUI, "token.enc")
VERSAO = "v23.0"
BR = timezone(timedelta(hours=-3))
TOLERANCIA_H = 6  # não publica algo que atrasou mais que isso (ex.: workflow parado)


# ---------- utilidades ----------
def http(metodo, url, dados=None):
    corpo = urllib.parse.urlencode(dados).encode() if dados else None
    req = urllib.request.Request(url, data=corpo, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:600]
        raise RuntimeError(f"HTTP {e.code}: {msg}") from None


def mascarar(valor):
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::add-mask::{valor}")


def senha():
    s = os.environ.get("IG_APP_SECRET", "")
    if not s:
        sys.exit("Falta o segredo IG_APP_SECRET no GitHub.")
    return s


def cifrar(texto):
    p = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-salt", "-a", "-A",
                        "-pass", "env:IG_APP_SECRET"], input=texto.encode(), capture_output=True, check=True)
    return p.stdout.decode()


def decifrar(texto):
    p = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-a", "-A",
                        "-pass", "env:IG_APP_SECRET"], input=texto.encode(), capture_output=True, check=True)
    return p.stdout.decode()


def salvar_cred(cred):
    senha()
    open(TOKEN_ENC, "w").write(cifrar(json.dumps(cred)) + "\n")


def ler_cred():
    senha()
    if not os.path.exists(TOKEN_ENC):
        sys.exit("Chave ainda não configurada: rode o workflow 'Configurar chave do Instagram'.")
    cred = json.loads(decifrar(open(TOKEN_ENC).read().strip()))
    mascarar(cred["token"])
    return cred


def base(cred):
    return "https://graph.instagram.com" if cred["tipo"] == "instagram" else "https://graph.facebook.com"


# ---------- configuração (roda uma vez) ----------
def configurar():
    curto = os.environ.get("INSTAGRAM_TOKEN", "").strip()
    app_id = os.environ.get("IG_APP_ID", "").strip()
    secret = senha()
    if not curto:
        sys.exit("Falta o segredo INSTAGRAM_TOKEN no GitHub.")
    mascarar(curto)
    if curto.startswith("IG"):
        # Login do Instagram: troca por chave de 60 dias (renovada sozinha depois)
        r = http("GET", "https://graph.instagram.com/access_token?" + urllib.parse.urlencode(
            {"grant_type": "ig_exchange_token", "client_secret": secret, "access_token": curto}))
        longo = r["access_token"]; mascarar(longo)
        me = http("GET", f"https://graph.instagram.com/{VERSAO}/me?" + urllib.parse.urlencode(
            {"fields": "user_id,username", "access_token": longo}))
        cred = {"tipo": "instagram", "token": longo, "ig_id": str(me["user_id"]), "usuario": me.get("username"),
                "renovado_em": datetime.now(BR).isoformat()}
    else:
        # Login do Facebook: chave longa do usuário -> chave da página (não vence)
        if not app_id:
            sys.exit("Falta o segredo IG_APP_ID no GitHub.")
        r = http("GET", f"https://graph.facebook.com/{VERSAO}/oauth/access_token?" + urllib.parse.urlencode(
            {"grant_type": "fb_exchange_token", "client_id": app_id, "client_secret": secret,
             "fb_exchange_token": curto}))
        longo = r["access_token"]; mascarar(longo)
        pags = http("GET", f"https://graph.facebook.com/{VERSAO}/me/accounts?" + urllib.parse.urlencode(
            {"fields": "name,access_token,instagram_business_account{id,username}", "access_token": longo}))
        alvo = None
        for p in pags.get("data", []):
            mascarar(p["access_token"])
            ig = p.get("instagram_business_account")
            if ig and (alvo is None or ig.get("username") == "daina_flow_"):
                alvo = (p, ig)
        if not alvo:
            sys.exit("Nenhuma página do Facebook com Instagram ligado foi encontrada para essa chave.")
        p, ig = alvo
        cred = {"tipo": "facebook", "token": p["access_token"], "ig_id": ig["id"], "usuario": ig.get("username"),
                "pagina": p.get("name"), "renovado_em": datetime.now(BR).isoformat()}
    salvar_cred(cred)
    print(f"Chave configurada para @{cred.get('usuario')} ({cred['tipo']}).")


def renovar_se_preciso(cred):
    """Chaves do login do Instagram valem 60 dias: renova a cada 7."""
    if cred["tipo"] != "instagram":
        return cred
    quando = datetime.fromisoformat(cred["renovado_em"])
    if datetime.now(BR) - quando < timedelta(days=7):
        return cred
    r = http("GET", "https://graph.instagram.com/refresh_access_token?" + urllib.parse.urlencode(
        {"grant_type": "ig_refresh_token", "access_token": cred["token"]}))
    mascarar(r["access_token"])
    cred.update(token=r["access_token"], renovado_em=datetime.now(BR).isoformat())
    salvar_cred(cred)
    print("Chave renovada.")
    return cred


# ---------- publicação ----------
def criar(cred, dados):
    dados = dict(dados, access_token=cred["token"])
    return http("POST", f"{base(cred)}/{VERSAO}/{cred['ig_id']}/media", dados)["id"]


def esperar(cred, cid, limite=600):
    ini = time.time()
    while time.time() - ini < limite:
        r = http("GET", f"{base(cred)}/{VERSAO}/{cid}?" + urllib.parse.urlencode(
            {"fields": "status_code,status", "access_token": cred["token"]}))
        st = r.get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram recusou a mídia: {r.get('status')}")
        time.sleep(10)
    raise RuntimeError("Tempo esgotado processando o vídeo.")


def publicar_container(cred, cid):
    r = http("POST", f"{base(cred)}/{VERSAO}/{cred['ig_id']}/media_publish",
             {"creation_id": cid, "access_token": cred["token"]})
    return r["id"]


def e_video(url):
    return url.lower().split("?")[0].endswith((".mp4", ".mov"))


def publicar(cred, item):
    tipo = item["tipo"].upper()
    midias = item["midias"]
    legenda = item.get("legenda", "")
    if tipo == "CARROSSEL":
        filhos = []
        for u in midias:
            d = {"is_carousel_item": "true"}
            d.update({"media_type": "VIDEO", "video_url": u} if e_video(u) else {"image_url": u})
            cid = criar(cred, d)
            if e_video(u):
                esperar(cred, cid)
            filhos.append(cid)
        cid = criar(cred, {"media_type": "CAROUSEL", "children": ",".join(filhos), "caption": legenda})
        esperar(cred, cid)
    elif tipo == "IMAGEM":
        cid = criar(cred, {"image_url": midias[0], "caption": legenda})
        esperar(cred, cid)
    elif tipo == "REEL":
        d = {"media_type": "REELS", "video_url": midias[0], "caption": legenda, "share_to_feed": "true"}
        if item.get("capa"):
            d["cover_url"] = item["capa"]
        cid = criar(cred, d)
        esperar(cred, cid)
    elif tipo == "STORY":
        u = midias[0]
        cid = criar(cred, {"media_type": "STORIES", **({"video_url": u} if e_video(u) else {"image_url": u})})
        esperar(cred, cid)
    else:
        raise RuntimeError(f"Tipo desconhecido: {tipo}")
    return publicar_container(cred, cid)


def rodar():
    agenda = json.load(open(AGENDA))
    feitos = json.load(open(FEITOS)) if os.path.exists(FEITOS) else {}
    agora = datetime.now(BR)
    pendentes = []
    for it in agenda:
        if not it.get("ativo", False) or it["id"] in feitos:
            continue
        quando = datetime.fromisoformat(it["quando"])
        if quando <= agora:
            pendentes.append((quando, it))
    if not pendentes:
        print("Nada para publicar agora.")
        return
    if not os.path.exists(TOKEN_ENC) and os.environ.get("INSTAGRAM_TOKEN"):
        configurar()  # primeira vez: troca a chave sozinha, sem botão
    cred = renovar_se_preciso(ler_cred())
    for quando, it in sorted(pendentes, key=lambda x: x[0]):
        if agora - quando > timedelta(hours=TOLERANCIA_H):
            feitos[it["id"]] = {"status": "pulado (atrasou mais de %dh)" % TOLERANCIA_H, "em": agora.isoformat()}
            print(f"[{it['id']}] pulado: atrasado demais.")
            continue
        try:
            mid = publicar(cred, it)
            feitos[it["id"]] = {"status": "publicado", "media_id": mid, "em": datetime.now(BR).isoformat()}
            print(f"[{it['id']}] publicado.")
        except Exception as e:  # registra e segue para o próximo
            tent = feitos.setdefault("_tentativas", {})
            tent[it["id"]] = n = tent.get(it["id"], 0) + 1
            if n >= 3:  # depois de 3 tentativas, desiste e registra o erro
                feitos[it["id"]] = {"status": "erro", "erro": str(e)[:400], "em": datetime.now(BR).isoformat()}
            print(f"[{it['id']}] ERRO: {str(e)[:400]}")
    json.dump(feitos, open(FEITOS, "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    configurar() if (len(sys.argv) > 1 and sys.argv[1] == "configurar") else rodar()
