#!/usr/bin/env python3
"""Confere se esta cópia do kit está num repositório público do GitHub.

Uso:
    python3 motor/privacidade.py

Pergunta à API do GitHub pelo repositório sem estar logado: se ela responde,
qualquer pessoa vê. O remote "kit" aponta para o template, que é público de
propósito, e por isso é ignorado.

Saída: 0 quando é privado ou não tem remote no GitHub, 1 quando é público, 2
quando não deu para confirmar.
"""

import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import RAIZ  # noqa: E402

REMOTE_DO_TEMPLATE = "kit"
PADRAO_GITHUB = re.compile(r"github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$")


def repo_github(url):
    marca = PADRAO_GITHUB.search(url.strip())
    return (marca.group(1), marca.group(2)) if marca else None


def consulta_api(dono, repo):
    """Devolve o status HTTP da API do GitHub para o repo, ou None sem rede."""
    pedido = urllib.request.Request(
        f"https://api.github.com/repos/{dono}/{repo}",
        headers={"User-Agent": "linkedin-kit", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(pedido, timeout=10) as resposta:
            return resposta.status
    except urllib.error.HTTPError as erro:
        return erro.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def classificar(status):
    if status == 200:
        return "publico"
    if status == 404:
        return "privado"
    return "desconhecido"


def remotes_do_github(raiz):
    """Devolve (dono, repo) de cada remote no GitHub, fora o do template."""
    r = subprocess.run(["git", "remote", "-v"], cwd=raiz, capture_output=True, text=True)
    achados = []
    for linha in r.stdout.splitlines():
        partes = linha.split()
        if len(partes) < 2 or partes[0] == REMOTE_DO_TEMPLATE:
            continue
        repo = repo_github(partes[1])
        if repo and repo not in achados:
            achados.append(repo)
    return achados


def checar(raiz, consulta=consulta_api):
    repos = remotes_do_github(raiz)
    if not repos:
        return 0, ("Sem remote no GitHub. Se um dia subir esta pasta para o GitHub, "
                   "crie o repositório como privado.")
    codigo, linhas = 0, []
    for dono, repo in repos:
        estado = classificar(consulta(dono, repo))
        nome = f"{dono}/{repo}"
        if estado == "publico":
            codigo = 1
            linhas.append(f"O repositório {nome} está PÚBLICO: qualquer pessoa vê seus arquivos. "
                          f"Torne privado em https://github.com/{nome}/settings, na seção "
                          f"Danger Zone, em Change visibility.")
        elif estado == "privado":
            linhas.append(f"O repositório {nome} é privado.")
        else:
            codigo = codigo or 2
            linhas.append(f"Não deu para confirmar se {nome} é privado (sem internet ou limite da "
                          f"API do GitHub). Confira em https://github.com/{nome}.")
    return codigo, "\n".join(linhas)


def main():
    codigo, mensagem = checar(RAIZ)
    print(mensagem)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
