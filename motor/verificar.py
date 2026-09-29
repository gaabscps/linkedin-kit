#!/usr/bin/env python3
"""Confere a integridade do motor do kit.

Uso:
    python3 motor/verificar.py             # confere o motor
    python3 motor/verificar.py --template  # e também que eu/ está vazia

Procura travessão, meia-risca e colchete de placeholder nos arquivos do motor,
e skill que cite motor/exemplo/. A pasta eu/ é da pessoa e só entra no modo
--template, que confere se ela está vazia.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import CAMINHOS_MOTOR, RAIZ  # noqa: E402

TRACOS = {chr(0x2014): "travessão", chr(0x2013): "meia-risca"}
PALAVRAS_PLACEHOLDER = "seu|sua|nome|preencher|inserir|exemplo|empresa|cargo|data|telefone|email|xxx"
PLACEHOLDER = re.compile(
    r"\[(?:[A-ZÀ-Ý][A-ZÀ-Ý _]{2,}|(?i:" + PALAVRAS_PLACEHOLDER + r")\b[^\]\n]*)\](?!\()"
)
PASTAS_IGNORADAS = {"__pycache__", "out", ".git"}
ARQUIVO_LIVRE_NO_TEMPLATE = "eu/LEIA-ME.md"


def arquivos_do_motor(raiz):
    """Devolve os arquivos dos caminhos do motor, sem saída gerada nem cache."""
    for caminho in CAMINHOS_MOTOR:
        alvo = raiz / caminho
        if alvo.is_file():
            yield alvo
        elif alvo.is_dir():
            for arq in sorted(alvo.rglob("*")):
                partes = arq.relative_to(raiz).parts
                if arq.is_file() and not PASTAS_IGNORADAS.intersection(partes):
                    yield arq


def ler_texto(arq):
    """Devolve o texto do arquivo, ou None quando ele não é texto UTF-8."""
    try:
        return arq.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def problemas_da_linha(rel, numero, linha):
    """Lista os problemas de uma linha de um arquivo do motor."""
    achados = []
    for caractere, nome in TRACOS.items():
        if caractere in linha:
            achados.append(f"{rel}:{numero}: {nome}")
    marca = PLACEHOLDER.search(linha)
    if marca:
        achados.append(f"{rel}:{numero}: colchete de placeholder {marca.group(0)}")
    if rel.startswith(".claude/skills/") and "motor/exemplo" in linha:
        achados.append(f"{rel}:{numero}: skill citando motor/exemplo/")
    return achados


def arquivos_pessoais(raiz):
    """Lista os arquivos de eu/ que não deveriam existir num template."""
    eu = raiz / "eu"
    if not eu.exists():
        return []
    return [
        f"{arq.relative_to(raiz).as_posix()}: arquivo pessoal dentro do template"
        for arq in sorted(eu.rglob("*"))
        if arq.is_file()
        and arq.name != ".DS_Store"
        and arq.relative_to(raiz).as_posix() != ARQUIVO_LIVRE_NO_TEMPLATE
    ]


def achar_problemas(raiz, modo_template=False):
    """Devolve a lista de problemas do motor, vazia quando está tudo certo."""
    problemas = []
    for arq in arquivos_do_motor(raiz):
        texto = ler_texto(arq)
        if texto is None:
            continue
        rel = arq.relative_to(raiz).as_posix()
        for numero, linha in enumerate(texto.splitlines(), 1):
            problemas.extend(problemas_da_linha(rel, numero, linha))
    if modo_template:
        problemas.extend(arquivos_pessoais(raiz))
    return problemas


def main(argv=None):
    parser = argparse.ArgumentParser(description="Confere a integridade do motor do kit.")
    parser.add_argument("--template", action="store_true", help="confere também que eu/ está vazia")
    args = parser.parse_args(argv)

    problemas = achar_problemas(RAIZ, modo_template=args.template)
    if problemas:
        print("\n".join(problemas))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
