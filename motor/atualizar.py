#!/usr/bin/env python3
"""Troca o motor do kit pela versão mais nova, sem tocar em eu/.

Uso:
    python3 motor/atualizar.py verificar
    python3 motor/atualizar.py aplicar [--ignorar-edicoes]
    python3 motor/atualizar.py avisar

Em verificar e aplicar, a primeira linha da saída é sempre "ESTADO: <estado>".
O avisar é o do início de sessão (.claude/settings.json): imprime um aviso só
quando há versão nova, e fica calado em qualquer outro caso. O endereço do template
vem de motor/ORIGEM e vira o remote "kit". Cada versão do template é uma tag
vX.Y.Z, e a tag da versão atual da cópia é a referência para saber se a pessoa
editou algum arquivo do motor.
"""

import argparse
import os
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
TEMPO_DO_AVISO = 5
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


def maior_versao(saida_ls_remote):
    """A maior versão entre as tags vX.Y.Z listadas, ou None."""
    versoes = [m.group(1) for linha in saida_ls_remote.splitlines() if (m := TAG_REMOTA.search(linha))]
    return max(versoes, key=versao_tupla) if versoes else None


def ultima_versao_remota(raiz):
    r = git(raiz, "ls-remote", "--tags", REMOTE, checar=False)
    if r.returncode != 0:
        raise Parada("erro-rede", f"Não consegui falar com a origem do kit.\n{r.stderr.strip()}")
    return maior_versao(r.stdout)


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


def arquivos_em(raiz, ref, caminhos):
    """Arquivos rastreados em `ref` dentro dos caminhos dados."""
    saida = git(raiz, "ls-tree", "-r", "--name-only", ref, "--", *caminhos).stdout
    return {linha for linha in saida.splitlines() if linha}


def trocar_motor(raiz, de, para):
    """Troca os arquivos do kit pela versão nova e commita só os caminhos do motor.

    Só sai o que pertence ao kit (existe na versão antiga ou na nova). Um
    arquivo que só a pessoa criou, como uma skill dela, fica.
    """
    antiga, nova = f"v{de}", f"v{para}"
    do_kit = arquivos_em(raiz, antiga, CAMINHOS_MOTOR) | arquivos_em(raiz, nova, CAMINHOS_MOTOR)
    remover = sorted(arquivos_em(raiz, "HEAD", CAMINHOS_MOTOR) & do_kit)
    if remover:
        git(raiz, "rm", "-q", "--", *remover)
    novos = [c for c in CAMINHOS_MOTOR if existe_em(raiz, nova, c)]
    if novos:
        git(raiz, "checkout", nova, "--", *novos)
    presentes = [c for c in CAMINHOS_MOTOR if existe_em(raiz, "HEAD", c) or existe_em(raiz, nova, c)]
    git(raiz, "commit", "-q", "-m", f"motor: atualiza de v{de} para v{para}", "--", *presentes)


def completar(raiz, versao):
    """Traz de volta os arquivos do motor da versão atual que faltam na pasta.

    Acontece quando a atualização foi feita pelo script de uma versão anterior,
    que não conhecia um caminho novo do motor. Devolve os caminhos trazidos.
    """
    tag = f"v{versao}"
    if git(raiz, "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}", checar=False).returncode != 0:
        return []
    faltando = sorted(
        caminho
        for caminho in arquivos_em(raiz, tag, CAMINHOS_MOTOR) - arquivos_em(raiz, "HEAD", CAMINHOS_MOTOR)
        if not (raiz / caminho).exists()
    )
    if faltando:
        git(raiz, "checkout", tag, "--", *faltando)
        git(raiz, "commit", "-q", "-m", f"motor: completa a {tag}", "--", *faltando)
    return faltando


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
    completados = completar(raiz, local)
    ultima = ultima_versao_remota(raiz)
    if ultima is None or versao_tupla(ultima) <= versao_tupla(local):
        mensagem = f"Você já está na versão mais nova (v{local})."
        if completados:
            mensagem += "\nCompletei arquivos do motor que faltavam: " + ", ".join(completados) + "."
        return "atualizado", mensagem
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


def avisar(raiz):
    """Devolve o aviso de versão nova para o início da sessão, ou "" se não há.

    Só lista as tags da origem: não cria remote nem baixa nada. Qualquer falha
    (sem internet, sem git, origem fora do ar, demora) vira silêncio.
    """
    url = ler_origem(raiz)
    if not url:
        return ""
    try:
        local = versao_local(raiz)
        r = subprocess.run(["git", "ls-remote", "--tags", url], cwd=raiz, capture_output=True, text=True,
                           timeout=TEMPO_DO_AVISO, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        ultima = maior_versao(r.stdout) if r.returncode == 0 else None
        if ultima is None or versao_tupla(ultima) <= versao_tupla(local):
            return ""
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return ""
    return (f"Aviso do linkedin-kit: saiu a versão v{ultima} do kit, e esta cópia está na v{local}. "
            "Na sua primeira resposta, conte isso à pessoa em uma frase e diga que ela pode digitar "
            "/atualizar quando quiser. Não atualize sem ela pedir.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Atualiza o motor do kit.")
    parser.add_argument("acao", choices=["verificar", "aplicar", "avisar"])
    parser.add_argument("--ignorar-edicoes", action="store_true",
                        help="troca o motor mesmo com edições locais já commitadas")
    args = parser.parse_args(argv)
    if args.acao == "avisar":
        aviso = avisar(RAIZ)
        if aviso:
            print(aviso)
        return 0
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
