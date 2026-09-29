#!/usr/bin/env python3
"""Deixa esta pasta pronta para ser a cópia da pessoa, sem passar pelo GitHub.

Uso:
    python3 motor/preparar.py

Cobre os três jeitos de chegar ao kit:
- Download ZIP (pasta sem git): cria o repositório local e uma primeira versão
  com os arquivos do kit, assinada pelo kit;
- clone direto do template: o remote que aponta para o template vira "kit", o
  mesmo que o /atualizar usa, e a pasta deixa de seguir o template;
- cópia feita com "Use this template": nada a fazer.

Imprime uma linha por passo feito. Rodar de novo não muda nada.
"""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import CAMINHOS_MOTOR, RAIZ  # noqa: E402
from privacidade import REMOTE_DO_TEMPLATE, repo_github  # noqa: E402

AUTOR_DO_KIT = {
    "GIT_AUTHOR_NAME": "linkedin-kit", "GIT_AUTHOR_EMAIL": "kit@linkedin-kit.local",
    "GIT_COMMITTER_NAME": "linkedin-kit", "GIT_COMMITTER_EMAIL": "kit@linkedin-kit.local",
}
ARQUIVOS_DA_PRIMEIRA_VERSAO = [*CAMINHOS_MOTOR, "eu/LEIA-ME.md"]


def git(raiz, *args, env=None, checar=True):
    r = subprocess.run(["git", *args], cwd=raiz, capture_output=True, text=True, env=env)
    if checar and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} falhou: {r.stderr.strip()}")
    return r


def ler_origem(raiz):
    arq = raiz / "motor" / "ORIGEM"
    return arq.read_text(encoding="utf-8").strip() if arq.exists() else ""


def mesmo_repo(a, b):
    """Diz se dois endereços apontam para o mesmo repositório."""
    no_github = repo_github(a), repo_github(b)
    if any(no_github):
        return no_github[0] == no_github[1]
    return a.strip().rstrip("/") == b.strip().rstrip("/")


def remotes(raiz):
    """Devolve {nome: endereço} dos remotes da pasta."""
    achados = {}
    for linha in git(raiz, "remote", "-v").stdout.splitlines():
        partes = linha.split()
        if len(partes) >= 2:
            achados.setdefault(partes[0], partes[1])
    return achados


def criar_repositorio(raiz):
    git(raiz, "init", "-q", "-b", "main")
    return "Criei o repositório local nesta pasta."


def adotar_clone(raiz, origem):
    """Troca o remote que aponta para o template pelo "kit"; devolve o que foi feito."""
    atuais = remotes(raiz)
    tem_kit = REMOTE_DO_TEMPLATE in atuais
    feito = []
    for nome, url in atuais.items():
        if nome == REMOTE_DO_TEMPLATE or not mesmo_repo(url, origem):
            continue
        if tem_kit:
            git(raiz, "remote", "remove", nome)
        else:
            git(raiz, "remote", "rename", nome, REMOTE_DO_TEMPLATE)
            git(raiz, "branch", "--unset-upstream", checar=False)
            tem_kit = True
        feito.append(f'Esta pasta era um clone do template: o remote "{nome}" virou "{REMOTE_DO_TEMPLATE}", '
                     "que só serve para buscar atualizações, e a pasta agora é sua.")
    return feito


def tem_commit(raiz):
    return git(raiz, "rev-parse", "--verify", "--quiet", "HEAD", checar=False).returncode == 0


def primeira_versao(raiz):
    """Commita só os arquivos do kit, assinados pelo kit."""
    caminhos = [c for c in ARQUIVOS_DA_PRIMEIRA_VERSAO if (raiz / c).exists()]
    versao = (raiz / "motor" / "VERSAO").read_text(encoding="utf-8").strip()
    git(raiz, "add", "--", *caminhos)
    git(raiz, "commit", "-q", "-m", f"motor: kit v{versao}", "--", *caminhos,
        env={**os.environ, **AUTOR_DO_KIT})
    return f"Salvei a primeira versão, com os arquivos do kit v{versao}."


def preparar(raiz):
    feito = []
    if not (raiz / ".git").exists():
        feito.append(criar_repositorio(raiz))
    origem = ler_origem(raiz)
    if origem:
        feito.extend(adotar_clone(raiz, origem))
    if not tem_commit(raiz):
        feito.append(primeira_versao(raiz))
    return feito


def main():
    feito = preparar(RAIZ)
    print("\n".join(feito) if feito else "A pasta já estava pronta: nada a fazer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
