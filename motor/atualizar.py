#!/usr/bin/env python3
"""Troca o motor do kit pela versão mais nova, sem tocar em eu/.

Uso:
    python3 motor/atualizar.py verificar
    python3 motor/atualizar.py aplicar [--ignorar-edicoes]

A primeira linha da saída é sempre "ESTADO: <estado>". O endereço do template
vem de motor/ORIGEM e vira o remote "kit". Cada versão do template é uma tag
vX.Y.Z, e a tag da versão atual da cópia é a referência para saber se a pessoa
editou algum arquivo do motor.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import CAMINHOS_MOTOR, RAIZ  # noqa: E402

REMOTE = "kit"
CODIGOS = {
    "atualizado": 0, "disponivel": 0, "aplicado": 0, "sem-origem": 2,
    "nao-salvo": 3, "sem-referencia": 4, "editado": 5, "erro-rede": 6,
}
TAG_REMOTA = re.compile(r"refs/tags/v(\d+\.\d+\.\d+)$")
CABECALHO_VERSAO = re.compile(r"(\d+\.\d+\.\d+)")


class Parada(Exception):
    """Interrompe a atualização com um estado e uma explicação."""

    def __init__(self, estado, mensagem):
        super().__init__(mensagem)
        self.estado = estado
        self.mensagem = mensagem


def git(raiz, *args, checar=True):
    r = subprocess.run(["git", *args], cwd=raiz, capture_output=True, text=True)
    if checar and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} falhou: {r.stderr.strip()}")
    return r


def versao_tupla(texto):
    return tuple(int(p) for p in texto.strip().lstrip("v").split("."))


def ler_origem(raiz):
    arq = raiz / "motor" / "ORIGEM"
    return arq.read_text(encoding="utf-8").strip() if arq.exists() else ""


def versao_local(raiz):
    return (raiz / "motor" / "VERSAO").read_text(encoding="utf-8").strip()


def garantir_remote(raiz, url):
    atual = git(raiz, "remote", "get-url", REMOTE, checar=False)
    if atual.returncode != 0:
        git(raiz, "remote", "add", REMOTE, url)
    elif atual.stdout.strip() != url:
        git(raiz, "remote", "set-url", REMOTE, url)


def ultima_versao_remota(raiz):
    r = git(raiz, "ls-remote", "--tags", REMOTE, checar=False)
    if r.returncode != 0:
        raise Parada("erro-rede", f"Não consegui falar com a origem do kit.\n{r.stderr.strip()}")
    versoes = [m.group(1) for linha in r.stdout.splitlines() if (m := TAG_REMOTA.search(linha))]
    return max(versoes, key=versao_tupla) if versoes else None


def buscar(raiz):
    r = git(raiz, "fetch", "--quiet", "--force", "--tags", REMOTE, checar=False)
    if r.returncode != 0:
        raise Parada("erro-rede", f"Não consegui baixar a versão nova.\n{r.stderr.strip()}")


def nao_salvos(raiz):
    return git(raiz, "status", "--porcelain", "--", *CAMINHOS_MOTOR).stdout.rstrip()


def edicoes_locais(raiz, versao):
    """Devolve o diff entre o motor da cópia e a versão que ela recebeu."""
    tag = f"v{versao}"
    if git(raiz, "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}", checar=False).returncode != 0:
        raise Parada("sem-referencia",
                     f"Não achei a versão {tag} na origem, então não dá para saber o que foi editado aqui.")
    return git(raiz, "diff", tag, "HEAD", "--", *CAMINHOS_MOTOR).stdout


def existe_em(raiz, ref, caminho):
    return bool(git(raiz, "ls-tree", "-r", "--name-only", ref, "--", caminho).stdout.strip())


def trocar_motor(raiz, de, para):
    """Apaga os caminhos do motor, traz os da versão nova e commita só eles."""
    tag = f"v{para}"
    presentes = [c for c in CAMINHOS_MOTOR if existe_em(raiz, "HEAD", c) or existe_em(raiz, tag, c)]
    git(raiz, "rm", "-r", "-q", "--ignore-unmatch", "--", *presentes)
    novos = [c for c in presentes if existe_em(raiz, tag, c)]
    if novos:
        git(raiz, "checkout", tag, "--", *novos)
    git(raiz, "commit", "-q", "-m", f"motor: atualiza de v{de} para v{para}", "--", *presentes)


def novidades_entre(texto, de, ate):
    """Devolve as seções do NOVIDADES.md com versão maior que `de` e até `ate`."""
    blocos = re.split(r"(?m)^## v", texto)
    escolhidos = []
    for bloco in blocos[1:]:
        marca = CABECALHO_VERSAO.match(bloco)
        if marca and versao_tupla(de) < versao_tupla(marca.group(1)) <= versao_tupla(ate):
            escolhidos.append("## v" + bloco.rstrip())
    return "\n\n".join(escolhidos)


def verificar(raiz):
    url = ler_origem(raiz)
    if not url:
        raise Parada("sem-origem",
                     "Este kit ainda não tem endereço de origem (motor/ORIGEM vazio), então não há de onde atualizar.")
    garantir_remote(raiz, url)
    local = versao_local(raiz)
    ultima = ultima_versao_remota(raiz)
    if ultima is None or versao_tupla(ultima) <= versao_tupla(local):
        return "atualizado", f"Você já está na versão mais nova (v{local})."
    buscar(raiz)
    pendentes = nao_salvos(raiz)
    if pendentes:
        raise Parada("nao-salvo", "Há mudanças não salvas em arquivos do motor:\n" + pendentes)
    diff = edicoes_locais(raiz, local)
    if diff:
        raise Parada("editado", f"Estes arquivos do motor foram editados nesta cópia desde a v{local}:\n{diff}")
    return "disponivel", f"Versão nova disponível: v{ultima} (você está na v{local})."


def aplicar(raiz, ignorar_edicoes=False):
    try:
        estado, mensagem = verificar(raiz)
    except Parada as parada:
        if not (ignorar_edicoes and parada.estado == "editado"):
            raise
        estado = "disponivel"
    if estado == "atualizado":
        return estado, mensagem
    local = versao_local(raiz)
    ultima = ultima_versao_remota(raiz)
    trocar_motor(raiz, local, ultima)
    texto = (raiz / "motor" / "NOVIDADES.md").read_text(encoding="utf-8")
    return "aplicado", f"Motor atualizado de v{local} para v{ultima}.\n\n{novidades_entre(texto, local, ultima)}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Atualiza o motor do kit.")
    parser.add_argument("acao", choices=["verificar", "aplicar"])
    parser.add_argument("--ignorar-edicoes", action="store_true",
                        help="troca o motor mesmo com edições locais já commitadas")
    args = parser.parse_args(argv)
    try:
        if args.acao == "verificar":
            estado, mensagem = verificar(RAIZ)
        else:
            estado, mensagem = aplicar(RAIZ, args.ignorar_edicoes)
    except Parada as parada:
        estado, mensagem = parada.estado, parada.mensagem
    print(f"ESTADO: {estado}\n{mensagem}")
    return CODIGOS[estado]


if __name__ == "__main__":
    sys.exit(main())
