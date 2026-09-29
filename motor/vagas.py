#!/usr/bin/env python3
"""Índice das vagas que o /aplicar-vagas já viu, em eu/vagas/aplicadas.json.

Uso:
    python3 motor/vagas.py novas '["<url ou id>", ...]'
    python3 motor/vagas.py registrar '{"jobId": "...", "veredito": "cortada", "criterio": "..."}'
    python3 motor/vagas.py dia [--data AAAA-MM-DD]
    python3 motor/vagas.py fechar-passada --aplicadas N [--data AAAA-MM-DD]
    python3 motor/vagas.py pausa

novas imprime, um por linha, os ids que ainda não estão no índice (a vaga
pulada volta, porque a pergunta que a pulou pode ter ganhado resposta).
Entrada sem id é erro, e não descarte. registrar aceita um objeto ou uma
lista, com veredito aplicada, cortada ou pulada, e critério sempre preenchido;
sem visto_em, vale a data de hoje. dia resume o dia e diz se é a estreia, que
dura até uma passada fechar com alguma candidatura. pausa dorme entre 20 e 60
segundos, sorteados. O JSON vai sempre como argumento: o script nunca lê a
entrada padrão, para não ficar esperando por ela.
"""

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import RAIZ  # noqa: E402

VERSAO = 1
VEREDITOS = {"aplicada", "cortada", "pulada"}
PAUSA_MINIMA, PAUSA_MAXIMA = 20, 60
FORMAS_DO_ID = [
    re.compile(r"currentJobId=(\d+)"),
    re.compile(r"/jobs/view/(\d+)"),
    re.compile(r"urn:li:jobPosting:(\d+)"),
    re.compile(r"^\s*(\d{6,})\s*$"),
]


def id_da_vaga(entrada):
    """O id da vaga em qualquer forma que o LinkedIn mostra, ou None."""
    texto = "" if entrada is None else str(entrada)
    for forma in FORMAS_DO_ID:
        achado = forma.search(texto)
        if achado:
            return achado.group(1)
    return None


def indice_vazio():
    return {"versao": VERSAO, "vagas": {}, "passadas": []}


def caminho_do_indice(raiz):
    return raiz / "eu" / "vagas" / "aplicadas.json"


def ler_indice(caminho):
    if not caminho.exists():
        return indice_vazio()
    bruto = json.loads(caminho.read_text(encoding="utf-8"))
    return {"versao": VERSAO, "vagas": bruto.get("vagas", {}), "passadas": bruto.get("passadas", [])}


def gravar_indice(caminho, indice):
    """Grava num arquivo temporário e troca, para uma queda no meio não corromper o índice."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_suffix(".tmp")
    temporario.write_text(json.dumps(indice, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporario, caminho)


def novas(indice, entradas):
    """Os ids ainda não vistos, na ordem de chegada e sem repetir; recusa entrada sem id."""
    sem_id = [entrada for entrada in entradas if not id_da_vaga(entrada)]
    if sem_id:
        raise ValueError(f"sem id de vaga: {json.dumps(sem_id, ensure_ascii=False)} (mande urls ou ids)")
    saida = []
    for entrada in entradas:
        vaga_id = id_da_vaga(entrada)
        registro = indice["vagas"].get(vaga_id)
        if not vaga_id or vaga_id in saida or (registro and registro["veredito"] != "pulada"):
            continue
        saida.append(vaga_id)
    return saida


def registrar(indice, entradas):
    """Devolve o índice com as entradas gravadas; recusa entrada incompleta."""
    if isinstance(entradas, dict):
        entradas = [entradas]
    vagas = dict(indice["vagas"])
    for entrada in entradas:
        if not isinstance(entrada, dict):
            raise ValueError(f"cada vaga é um objeto com jobId, veredito e criterio, e não {entrada!r}")
        vaga_id = id_da_vaga(entrada.get("jobId"))
        if not vaga_id:
            raise ValueError(f"entrada sem id de vaga: {json.dumps(entrada, ensure_ascii=False)}")
        if entrada.get("veredito") not in VEREDITOS:
            raise ValueError(f"veredito desconhecido: {entrada.get('veredito')!r} (use aplicada, cortada ou pulada)")
        criterio = str(entrada.get("criterio") or "").strip()
        if not criterio:
            raise ValueError(f"a vaga {vaga_id} está sem critério: diga qual regra aprovou, cortou ou pulou")
        vagas[vaga_id] = {
            "visto_em": entrada.get("visto_em") or date.today().isoformat(),
            "veredito": entrada["veredito"],
            "criterio": criterio,
            "titulo": entrada.get("titulo", ""),
            "empresa": entrada.get("empresa", ""),
        }
    return {**indice, "vagas": vagas}


def fechar_passada(indice, data, aplicadas):
    return {**indice, "passadas": [*indice["passadas"], {"data": data, "aplicadas": aplicadas}]}


def situacao(indice, data):
    """O resumo do dia, com o aviso de estreia até uma passada fechar com candidatura."""
    aplicadas = sum(1 for v in indice["vagas"].values() if v["visto_em"] == data and v["veredito"] == "aplicada")
    passadas = sum(1 for p in indice["passadas"] if p["data"] == data)
    linhas = [f"Hoje ({data}): {aplicadas} aplicadas em {passadas} passadas.",
              f"Passadas fechadas no total: {len(indice['passadas'])}."]
    if not any(p.get("aplicadas", 0) > 0 for p in indice["passadas"]):
        linhas.append("Esta é a estreia: a passada para em 5 candidaturas.")
    return "\n".join(linhas)


def pausa(dormir=time.sleep, sortear=random.randint):
    segundos = sortear(PAUSA_MINIMA, PAUSA_MAXIMA)
    dormir(segundos)
    return segundos


def carregar_json(texto):
    if texto is None:
        raise ValueError("falta o JSON, como argumento: python3 motor/vagas.py novas '[\"4012345678\"]'")
    try:
        return json.loads(texto)
    except json.JSONDecodeError as erro:
        raise ValueError(f"a entrada não é JSON válido ({erro})") from erro


def main(argv=None):
    parser = argparse.ArgumentParser(description="Índice das vagas do /aplicar-vagas.")
    comandos = parser.add_subparsers(dest="comando", required=True)
    comandos.add_parser("novas").add_argument("json", nargs="?")
    comandos.add_parser("registrar").add_argument("json", nargs="?")
    comandos.add_parser("pausa")
    dia = comandos.add_parser("dia")
    dia.add_argument("--data", default=date.today().isoformat())
    fechar = comandos.add_parser("fechar-passada")
    fechar.add_argument("--aplicadas", type=int, required=True)
    fechar.add_argument("--data", default=date.today().isoformat())
    args = parser.parse_args(argv)

    caminho = caminho_do_indice(RAIZ)
    try:
        if args.comando == "novas":
            entradas = carregar_json(args.json)
            ids = novas(ler_indice(caminho), entradas)
            print("\n".join(ids))
            print(f"{len(ids)} novas de {len(entradas)} recebidas.", file=sys.stderr)
        elif args.comando == "registrar":
            gravar_indice(caminho, registrar(ler_indice(caminho), carregar_json(args.json)))
        elif args.comando == "fechar-passada":
            gravar_indice(caminho, fechar_passada(ler_indice(caminho), args.data, args.aplicadas))
        elif args.comando == "dia":
            print(situacao(ler_indice(caminho), args.data))
        else:
            print(f"Pausa de {pausa()} segundos.")
    except ValueError as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
