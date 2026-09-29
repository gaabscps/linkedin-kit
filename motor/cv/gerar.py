#!/usr/bin/env python3
"""Gera o PDF do CV a partir dos fatos, do contato e de uma variante.

Uso:
    python3 motor/cv/gerar.py                    # gera todas as variantes
    python3 motor/cv/gerar.py base-pt            # gera uma variante pelo nome
    python3 motor/cv/gerar.py --checar           # diz o que falta para gerar
    python3 motor/cv/gerar.py --eu OUTRA/PASTA base-pt

Lê eu/cv/FATOS.yml (o conteúdo), eu/cv/contato.yml (email, telefone, cidade e
links, fora do git), eu/cv/variantes/*.yml (o que entra e em que ordem) e
motor/cv/template.html (a apresentação). Escreve em eu/cv/out/.

Dependências: PyYAML e o Google Chrome (ou Chromium), usado sem janela para
imprimir o PDF.
"""

import argparse
import datetime
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

MOTOR_CV = Path(__file__).resolve().parent
RAIZ = MOTOR_CV.parents[1]
TEMPLATE = MOTOR_CV / "template.html"

CAMINHOS_CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
NOMES_CHROME = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]

MSG_YAML = (
    "Falta o PyYAML, a biblioteca que lê os arquivos .yml.\n"
    "Para instalar, rode: python3 -m pip install --user pyyaml"
)
MSG_CHROME = (
    "Não achei o Google Chrome, que é usado para imprimir o PDF.\n"
    "Instale pelo site oficial (google.com/chrome) ou diga onde ele está na\n"
    "variável CHROME, por exemplo: CHROME=/caminho/do/chrome python3 motor/cv/gerar.py"
)
MSG_CONTATO = (
    "Falta o arquivo {caminho}, com email, telefone, cidade e links.\n"
    "Ele fica fora do git de propósito. Rode /comecar fatos, ou copie\n"
    "motor/modelos/contato.yml para lá e preencha."
)

LIMITE_RESUMO = 90
SINAIS_DE_EXEMPLO = ("example.com", "example.org", "exemplo", "90000-", "00000-")

MESES = {
    "pt": ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}

ROTULOS = {
    "pt": {"experiencia": "Experiência", "projetos": "Projetos", "skills": "Competências",
           "idiomas": "Idiomas", "formacao": "Formação", "ano": "a", "mes": "m",
           "atual": "atual", "ate": " a ", "certificacoes": "Certificações",
           "validade": "válida até"},
    "en": {"experiencia": "Experience", "projetos": "Projects", "skills": "Skills",
           "idiomas": "Languages", "formacao": "Education", "ano": "y", "mes": "m",
           "atual": "present", "ate": " to ", "certificacoes": "Certifications",
           "validade": "valid until"},
}


def acha_chrome(env=None, existe=os.path.exists, procura=shutil.which):
    """Devolve o caminho do Chrome: variável CHROME, caminho fixo ou PATH."""
    env = os.environ if env is None else env
    if env.get("CHROME"):
        return env["CHROME"]
    for caminho in CAMINHOS_CHROME:
        if existe(caminho):
            return caminho
    for nome in NOMES_CHROME:
        achado = procura(nome)
        if achado:
            return achado
    return None


def loc(valor, idioma):
    """Devolve a versão no idioma pedido, aceitando texto simples ou dict."""
    if isinstance(valor, dict):
        return valor.get(idioma) or valor.get("pt") or ""
    return "" if valor is None else valor


def e(texto):
    return html.escape("" if texto is None else str(texto).strip())


def eh_atual(valor):
    return str(valor).strip().lower() == "atual"


def partes_data(valor, hoje=None):
    """Aceita '2024-12', '2014', 2014 ou 'atual' e devolve (ano, mes|None)."""
    if eh_atual(valor):
        hoje = hoje or datetime.date.today()
        return hoje.year, hoje.month
    texto = str(valor)
    if "-" in texto:
        ano, mes = texto.split("-")[:2]
        return int(ano), int(mes)
    return int(texto), None


def formata_data(valor, idioma):
    if eh_atual(valor):
        return ROTULOS[idioma]["atual"]
    ano, mes = partes_data(valor)
    if mes is None:
        return str(ano)
    return f"{MESES[idioma][mes - 1]}/{ano}"


def formata_duracao(inicio, fim, idioma, hoje=None):
    """Meses inclusivos, na mesma contagem que o LinkedIn usa."""
    ano1, mes1 = partes_data(inicio, hoje)
    ano2, mes2 = partes_data(fim, hoje)
    if mes1 is None or mes2 is None:
        return ""
    total = (ano2 - ano1) * 12 + (mes2 - mes1) + 1
    anos, meses = divmod(total, 12)
    r = ROTULOS[idioma]
    pedacos = []
    if anos:
        pedacos.append(f"{anos}{r['ano']}")
    if meses:
        pedacos.append(f"{meses}{r['mes']}")
    return " ".join(pedacos)


def por_id(colecao):
    return {item["id"]: item for item in colecao or []}


def junta(pedacos):
    """Junta os pedaços não vazios com o separador do cabeçalho."""
    return '<span class="sep">·</span>'.join(p for p in pedacos if p)


def monta_cabecalho(fatos, contato, variante, idioma):
    ident = fatos.get("identidade") or {}
    disponibilidade = variante.get("disponibilidade") or ident.get("disponibilidade")
    linha1 = [e(loc(contato.get("local"), idioma)), e(loc(disponibilidade, idioma))]
    linha2 = [f'<a href="{e(link["url"])}">{e(link["texto"])}</a>' for link in contato.get("links") or []]
    if contato.get("email"):
        linha2.append(f'<a href="mailto:{e(contato["email"])}">{e(contato["email"])}</a>')
    if contato.get("telefone"):
        linha2.append(e(contato["telefone"]))
    if contato.get("registro"):
        linha2.append(e(contato["registro"]))
    linhas = "<br>".join(x for x in (junta(linha1), junta(linha2)) if x)
    return f"""<header class="cabecalho">
  <div class="nome">{e(ident.get("nome"))}</div>
  <div class="titulo">{e(loc(ident.get("titulo"), idioma))}</div>
  <div class="contato">{linhas}</div>
</header>"""


def texto_do_resumo(fatos, variante, idioma):
    escolha = variante.get("resumo", "base")
    base = (fatos.get("resumo") or {}).get("base")
    return loc(base, idioma) if escolha == "base" else loc(escolha, idioma)


def monta_resumo(fatos, variante, idioma):
    texto = texto_do_resumo(fatos, variante, idioma)
    return f'<p class="resumo">{e(texto)}</p>' if texto else ""


def monta_experiencias(fatos, variante, idioma):
    catalogo = por_id(fatos.get("experiencias"))
    r = ROTULOS[idioma]
    blocos = []
    for exp_id, ids_bullets in (variante.get("experiencias") or {}).items():
        exp = catalogo[exp_id]
        bullets = por_id(exp.get("bullets"))
        nota = loc(exp.get("empresa_nota"), idioma)
        nota_html = f' <span class="item-nota">({e(nota)})</span>' if nota else ""
        periodo = f'{formata_data(exp["inicio"], idioma)}{r["ate"]}{formata_data(exp["fim"], idioma)}'
        duracao = formata_duracao(exp["inicio"], exp["fim"], idioma)
        itens = "".join(f"<li>{e(loc(bullets[bid], idioma))}</li>" for bid in ids_bullets or [])
        contexto = loc(exp.get("contexto"), idioma)
        contexto_html = f'<div class="item-contexto">{e(contexto)}</div>' if contexto else ""
        cabecalho_item = (
            f'<span class="item-nome">{e(exp["empresa"])}</span>{nota_html}'
            f'<span class="item-cargo">, {e(loc(exp.get("cargo"), idioma))}</span>'
        )
        blocos.append(f"""<div class="item">
  <div class="item-topo">
    <div>{cabecalho_item}</div>
    <div class="item-datas">{e(periodo)}<br><span class="item-duracao">{e(duracao)}</span></div>
  </div>
  {contexto_html}
  <ul>{itens}</ul>
</div>""")
    if not blocos:
        return ""
    return f'<section class="secao"><h2>{r["experiencia"]}</h2>{"".join(blocos)}</section>'


def monta_projetos(fatos, variante, idioma):
    ids = variante.get("projetos") or []
    if not ids:
        return ""
    catalogo = por_id(fatos.get("projetos"))
    blocos = []
    for pid in ids:
        proj = catalogo[pid]
        ferramentas = ", ".join(str(f) for f in proj.get("ferramentas") or [])
        blocos.append(f"""<div class="projeto">
  <div class="projeto-topo">
    <span class="projeto-nome">{e(proj["nome"])}</span>
    <span class="projeto-ferramentas">{e(ferramentas)}</span>
  </div>
  <div class="projeto-texto">{e(loc(proj, idioma))}</div>
</div>""")
    return f'<section class="secao"><h2>{ROTULOS[idioma]["projetos"]}</h2>{"".join(blocos)}</section>'


def monta_skills(fatos, variante, idioma):
    ids = variante.get("skills") or []
    if not ids:
        return ""
    catalogo = por_id(fatos.get("skills"))
    linhas = []
    for sid in ids:
        grupo = catalogo[sid]
        itens = ", ".join(str(i) for i in grupo.get("itens") or [])
        linhas.append(f"""<div class="linha-skill">
  <div class="skill-rotulo">{e(loc(grupo.get("titulo"), idioma))}</div>
  <div class="skill-itens">{e(itens)}</div>
</div>""")
    return f'<section class="secao"><h2>{ROTULOS[idioma]["skills"]}</h2>{"".join(linhas)}</section>'


def monta_certificacoes(fatos, variante, idioma):
    """Certificações com instituição, ano e validade, quando a variante pede."""
    ids = variante.get("certificacoes") or []
    if not ids:
        return ""
    catalogo = por_id(fatos.get("certificacoes"))
    r = ROTULOS[idioma]
    linhas = []
    for cid in ids:
        cert = catalogo[cid]
        detalhes = [str(x) for x in (cert.get("instituicao"), cert.get("ano"), loc(cert.get("situacao"), idioma)) if x]
        if cert.get("validade"):
            detalhes.append(f'{r["validade"]} {formata_data(cert["validade"], idioma)}')
        linhas.append(f"""<div class="linha-skill">
  <div class="skill-rotulo">{e(loc(cert.get("nome"), idioma))}</div>
  <div class="skill-itens">{e(", ".join(detalhes))}</div>
</div>""")
    return f'<section class="secao"><h2>{r["certificacoes"]}</h2>{"".join(linhas)}</section>'


def vencida(validade, hoje=None):
    """Diz se a validade já passou. Validade só com o ano vale até dezembro."""
    hoje = hoje or datetime.date.today()
    ano, mes = partes_data(validade)
    return (ano, mes or 12) < (hoje.year, hoje.month)


def certificacoes_vencidas(fatos, variante, hoje=None):
    """Nomes das certificações escolhidas pela variante que já venceram."""
    catalogo = por_id(fatos.get("certificacoes"))
    return [
        loc(catalogo[cid].get("nome"), "pt")
        for cid in variante.get("certificacoes") or []
        if catalogo[cid].get("validade") and vencida(catalogo[cid]["validade"], hoje)
    ]


def avisos(fatos, contato, variante):
    """Problemas que não impedem gerar, mas que a pessoa precisa ver antes de enviar."""
    idioma = variante.get("idioma", "pt")
    lista = []
    palavras = len(str(texto_do_resumo(fatos, variante, idioma)).split())
    if palavras > LIMITE_RESUMO:
        lista.append(f"O resumo tem {palavras} palavras, acima do limite de {LIMITE_RESUMO}.")
    campos = [str(contato.get("email") or ""), str(contato.get("telefone") or "")]
    campos += [f'{link.get("texto", "")} {link.get("url", "")}' for link in contato.get("links") or []]
    if any(sinal in campo.lower() for campo in campos for sinal in SINAIS_DE_EXEMPLO):
        lista.append("O contato parece de exemplo (example.com, a palavra exemplo ou telefone 90000). "
                     "Confira eu/cv/contato.yml antes de enviar.")
    lista.extend(f"A certificação {nome} está vencida." for nome in certificacoes_vencidas(fatos, variante))
    lista.extend(f"A certificação {nome} vence nos próximos 3 meses." for nome in certificacoes_perto_de_vencer(fatos, variante))
    return lista


def paginas_do_pdf(caminho):
    """Número de páginas lido da árvore de páginas do PDF, ou None se não achar."""
    contagens = re.findall(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", Path(caminho).read_bytes())
    return max(int(c) for c in contagens) if contagens else None


def certificacoes_perto_de_vencer(fatos, variante, hoje=None, meses=3):
    """Nomes das certificações escolhidas que vencem nos próximos meses, ainda válidas."""
    hoje = hoje or datetime.date.today()
    limite_ano, limite_mes = divmod(hoje.year * 12 + hoje.month - 1 + meses, 12)
    limite = datetime.date(limite_ano, limite_mes + 1, 1)
    catalogo = por_id(fatos.get("certificacoes"))
    nomes = []
    for cid in variante.get("certificacoes") or []:
        validade = catalogo[cid].get("validade")
        if validade and not vencida(validade, hoje) and vencida(validade, limite):
            nomes.append(loc(catalogo[cid].get("nome"), "pt"))
    return nomes


def monta_rodape(fatos, variante, idioma):
    """Idiomas e formação lado a lado."""
    r = ROTULOS[idioma]
    linhas_idioma = "".join(
        f"""<div class="linha-skill">
  <div class="skill-rotulo">{e(loc(item.get("lingua"), idioma))}</div>
  <div class="skill-itens">{e(loc(item.get("nivel"), idioma))}</div>
</div>"""
        for item in fatos.get("idiomas") or []
    )
    catalogo = por_id(fatos.get("formacao"))
    linhas_formacao = "".join(
        f"""<div class="formacao-linha">
  <div>
    <div class="formacao-curso">{e(loc(catalogo[fid].get("curso"), idioma))}</div>
    <div class="formacao-inst">{e(catalogo[fid].get("instituicao"))}</div>
  </div>
  <div class="item-datas">{e(catalogo[fid].get("inicio"))}{r["ate"]}{e(formata_data(catalogo[fid].get("fim"), idioma))}</div>
</div>"""
        for fid in variante.get("formacao") or []
    )
    secoes = []
    if linhas_idioma:
        secoes.append(f'<section class="secao"><h2>{r["idiomas"]}</h2>{linhas_idioma}</section>')
    if linhas_formacao:
        secoes.append(f'<section class="secao"><h2>{r["formacao"]}</h2>{linhas_formacao}</section>')
    return f'<div class="rodape-secoes">{"".join(secoes)}</div>' if secoes else ""


def monta_documento(fatos, contato, variante, template, nome):
    """Monta o HTML completo do CV, sem escrever nada em disco."""
    idioma = variante.get("idioma", "pt")
    corpo = "".join([
        monta_cabecalho(fatos, contato, variante, idioma),
        monta_resumo(fatos, variante, idioma),
        monta_experiencias(fatos, variante, idioma),
        monta_projetos(fatos, variante, idioma),
        monta_skills(fatos, variante, idioma),
        monta_certificacoes(fatos, variante, idioma),
        monta_rodape(fatos, variante, idioma),
    ])
    return (template
            .replace("{{LANG}}", "pt-BR" if idioma == "pt" else "en")
            .replace("{{TITULO_DOC}}", e(nome))
            .replace("{{CONTEUDO}}", corpo))


def gerar(caminho_variante, fatos, contato, template, saida, chrome):
    """Escreve o HTML e imprime o PDF de uma variante. Devolve o caminho do PDF."""
    variante = yaml.safe_load(caminho_variante.read_text(encoding="utf-8")) or {}
    nome = variante.get("arquivo") or caminho_variante.stem
    for aviso in avisos(fatos, contato, variante):
        print(f"Aviso ({caminho_variante.name}): {aviso}", file=sys.stderr)
    saida.mkdir(parents=True, exist_ok=True)
    arquivo_html = saida / f"{nome}.html"
    arquivo_pdf = saida / f"{nome}.pdf"
    arquivo_html.write_text(monta_documento(fatos, contato, variante, template, nome), encoding="utf-8")
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={arquivo_pdf}", arquivo_html.as_uri(),
    ], check=True, capture_output=True)
    paginas = paginas_do_pdf(arquivo_pdf)
    if paginas and paginas > 1:
        print(f"Aviso ({caminho_variante.name}): o PDF saiu com {paginas} páginas. "
              "Corte o bullet mais fraco para esta vaga.", file=sys.stderr)
    return arquivo_pdf


def checar_colisao(caminhos):
    """Barra duas variantes que escreveriam no mesmo PDF."""
    destinos = {}
    for caminho in caminhos:
        variante = yaml.safe_load(caminho.read_text(encoding="utf-8")) or {}
        nome = variante.get("arquivo") or caminho.stem
        destinos.setdefault(nome, []).append(caminho.name)
    duplicados = {n: v for n, v in destinos.items() if len(v) > 1}
    if duplicados:
        linhas = [f"  {nome}.pdf  <-  {', '.join(vs)}" for nome, vs in duplicados.items()]
        sys.exit(
            "Duas variantes gerariam o mesmo arquivo:\n" + "\n".join(linhas)
            + "\n\nTroque o campo `arquivo:` de uma delas para um nome único da vaga."
        )


def carrega_contato(pasta_cv):
    caminho = pasta_cv / "contato.yml"
    if not caminho.exists():
        sys.exit(MSG_CONTATO.format(caminho=caminho))
    return yaml.safe_load(caminho.read_text(encoding="utf-8")) or {}


def checar(pasta_cv):
    """Lista o que falta para gerar o CV, vazia quando dá para gerar."""
    problemas = []
    if yaml is None:
        problemas.append(MSG_YAML)
    if acha_chrome() is None:
        problemas.append(MSG_CHROME)
    if not (pasta_cv / "FATOS.yml").exists():
        problemas.append(f"Falta {pasta_cv / 'FATOS.yml'}. Rode /comecar fatos.")
    if not (pasta_cv / "contato.yml").exists():
        problemas.append(MSG_CONTATO.format(caminho=pasta_cv / "contato.yml"))
    if not list((pasta_cv / "variantes").glob("*.yml")):
        problemas.append(f"Nenhuma variante em {pasta_cv / 'variantes'}. Rode /montar-cv.")
    return problemas


def resolve(argumento, pasta_variantes):
    caminho = Path(argumento)
    if caminho.exists():
        return caminho
    candidato = pasta_variantes / f"{argumento}.yml"
    if candidato.exists():
        return candidato
    sys.exit(f"Variante não encontrada: {argumento}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gera o PDF do CV.")
    parser.add_argument("--eu", default=str(RAIZ / "eu"), help="pasta com cv/FATOS.yml (padrão: eu/)")
    parser.add_argument("--checar", action="store_true", help="só diz o que falta para gerar")
    parser.add_argument("variantes", nargs="*")
    args = parser.parse_args(argv)
    pasta_cv = Path(args.eu).resolve() / "cv"

    if args.checar:
        problemas = checar(pasta_cv)
        print("\n\n".join(problemas) if problemas else "Tudo pronto para gerar o CV.")
        return 1 if problemas else 0

    if yaml is None:
        sys.exit(MSG_YAML)
    chrome = acha_chrome()
    if chrome is None:
        sys.exit(MSG_CHROME)
    fatos = yaml.safe_load((pasta_cv / "FATOS.yml").read_text(encoding="utf-8")) or {}
    contato = carrega_contato(pasta_cv)
    template = TEMPLATE.read_text(encoding="utf-8")
    todas = sorted((pasta_cv / "variantes").glob("*.yml"))
    checar_colisao(todas)
    alvos = [resolve(a, pasta_cv / "variantes") for a in args.variantes] or todas
    if not alvos:
        sys.exit(f"Nenhuma variante em {pasta_cv / 'variantes'}.")
    for alvo in alvos:
        print(gerar(alvo, fatos, contato, template, pasta_cv / "out", chrome))
    return 0


if __name__ == "__main__":
    sys.exit(main())
