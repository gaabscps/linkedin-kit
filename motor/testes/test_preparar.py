import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MOTOR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOTOR))
import privacidade

ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Teste", "GIT_AUTHOR_EMAIL": "teste@example.com",
    "GIT_COMMITTER_NAME": "Teste", "GIT_COMMITTER_EMAIL": "teste@example.com",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
}
TEMPLATE_GITHUB = "https://github.com/mantenedor/linkedin-kit.git"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, check=True, capture_output=True, text=True).stdout


def escreve(raiz, caminho, texto):
    arq = raiz / caminho
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding="utf-8")


class TestPreparar(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.kit = tmp / "kit"
        self.pasta = tmp / "pasta"
        self.kit.mkdir()
        git(self.kit, "init", "-q", "-b", "main")
        for nome in ("atualizar.py", "kit.py", "preparar.py", "privacidade.py"):
            escreve(self.kit, f"motor/{nome}", (MOTOR / nome).read_text(encoding="utf-8"))
        escreve(self.kit, "CLAUDE.md", "claude v1\n")
        escreve(self.kit, "README.md", "leia v1\n")
        escreve(self.kit, ".gitignore", "__pycache__/\n")
        escreve(self.kit, ".claude/skills/comecar/SKILL.md", "skill v1\n")
        escreve(self.kit, "motor/regras/a.md", "regra a v1\n")
        escreve(self.kit, "motor/VERSAO", "1.0.0\n")
        escreve(self.kit, "motor/ORIGEM", f"{TEMPLATE_GITHUB}\n")
        escreve(self.kit, "motor/NOVIDADES.md", "# Novidades\n\n## v1.0.0\n\n- Primeira versão.\n")
        escreve(self.kit, "eu/LEIA-ME.md", "sua pasta\n")
        git(self.kit, "add", "-A")
        git(self.kit, "commit", "-q", "-m", "v1")
        git(self.kit, "tag", "v1.0.0")

    def tearDown(self):
        self._tmp.cleanup()

    def baixar_zip(self):
        """A pasta do jeito que o Download ZIP entrega: os arquivos, sem .git."""
        shutil.copytree(self.kit, self.pasta, ignore=shutil.ignore_patterns(".git"))

    def clonar(self, url_do_origin):
        git(self.kit.parent, "clone", "-q", str(self.kit), str(self.pasta))
        git(self.pasta, "remote", "set-url", "origin", url_do_origin)

    def rodar(self, script, *args):
        r = subprocess.run([sys.executable, f"motor/{script}", *args],
                           cwd=self.pasta, env=ENV, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def remotes(self):
        return git(self.pasta, "remote").split()

    def test_zip_vira_repositorio_com_o_kit_assinado_pelo_kit(self):
        self.baixar_zip()
        codigo, saida = self.rodar("preparar.py")
        self.assertEqual(codigo, 0, saida)
        self.assertIn("repositório local", saida)
        self.assertEqual(git(self.pasta, "log", "--format=%an <%ae>|%s").strip(),
                         "linkedin-kit <kit@linkedin-kit.local>|motor: kit v1.0.0")
        self.assertEqual(git(self.pasta, "status", "--porcelain"), "")

    def test_commit_inicial_nao_leva_arquivo_solto(self):
        self.baixar_zip()
        escreve(self.pasta, "cv-antigo.txt", "telefone da pessoa\n")
        escreve(self.pasta, "rascunho/notas.md", "anotação\n")
        self.rodar("preparar.py")
        rastreados = git(self.pasta, "ls-files").split()
        self.assertIn("eu/LEIA-ME.md", rastreados)
        self.assertIn("motor/VERSAO", rastreados)
        self.assertNotIn("cv-antigo.txt", rastreados)
        self.assertNotIn("rascunho/notas.md", rastreados)

    def test_clone_do_template_vira_a_copia_da_pessoa(self):
        self.clonar("git@github.com:mantenedor/linkedin-kit.git")
        antes = git(self.pasta, "rev-parse", "HEAD")
        codigo, saida = self.rodar("preparar.py")
        self.assertEqual(codigo, 0, saida)
        self.assertIn("kit", saida)
        self.assertEqual(self.remotes(), ["kit"])
        self.assertEqual(git(self.pasta, "rev-parse", "HEAD"), antes)
        upstream = subprocess.run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"],
                                  cwd=self.pasta, env=ENV, capture_output=True, text=True)
        self.assertNotEqual(upstream.returncode, 0, upstream.stdout)
        chamadas = []
        codigo, _ = privacidade.checar(self.pasta, consulta=lambda d, r: chamadas.append(r) or 200)
        self.assertEqual((codigo, chamadas), (0, []))

    def test_clone_que_ja_tem_o_remote_kit_perde_so_o_origin(self):
        self.clonar(TEMPLATE_GITHUB)
        git(self.pasta, "remote", "add", "kit", TEMPLATE_GITHUB)
        self.rodar("preparar.py")
        self.assertEqual(self.remotes(), ["kit"])

    def test_copia_feita_pelo_use_this_template_fica_como_esta(self):
        self.baixar_zip()
        git(self.pasta, "init", "-q", "-b", "main")
        git(self.pasta, "add", "-A")
        git(self.pasta, "commit", "-q", "-m", "Initial commit")
        git(self.pasta, "remote", "add", "origin", "https://github.com/fulana/meu-linkedin.git")
        antes = git(self.pasta, "rev-parse", "HEAD")
        codigo, saida = self.rodar("preparar.py")
        self.assertEqual(codigo, 0, saida)
        self.assertIn("já estava pronta", saida)
        self.assertEqual(self.remotes(), ["origin"])
        self.assertEqual(git(self.pasta, "rev-parse", "HEAD"), antes)

    def test_rodar_de_novo_nao_muda_nada(self):
        self.baixar_zip()
        self.rodar("preparar.py")
        antes = git(self.pasta, "rev-parse", "HEAD")
        _, saida = self.rodar("preparar.py")
        self.assertIn("já estava pronta", saida)
        self.assertEqual(git(self.pasta, "rev-parse", "HEAD"), antes)

    def test_pasta_do_zip_recebe_atualizacao_sem_perder_eu(self):
        escreve(self.kit, "motor/ORIGEM", f"{self.kit}\n")
        git(self.kit, "commit", "-q", "-am", "origem local")
        git(self.kit, "tag", "-f", "v1.0.0")
        self.baixar_zip()
        self.rodar("preparar.py")
        escreve(self.pasta, "eu/VOZ.md", "o tom dela\n")
        git(self.pasta, "add", "eu")
        git(self.pasta, "commit", "-q", "-m", "eu: parte 2, voz", "--", "eu")
        escreve(self.kit, "motor/regras/a.md", "regra a v2\n")
        escreve(self.kit, "motor/VERSAO", "1.1.0\n")
        escreve(self.kit, "motor/NOVIDADES.md", "# Novidades\n\n## v1.1.0\n\n- Regra A nova.\n")
        git(self.kit, "commit", "-q", "-am", "v1.1")
        git(self.kit, "tag", "v1.1.0")
        codigo, saida = self.rodar("atualizar.py", "aplicar")
        self.assertEqual(codigo, 0, saida)
        self.assertTrue(saida.startswith("ESTADO: aplicado"), saida)
        self.assertEqual((self.pasta / "motor/regras/a.md").read_text(encoding="utf-8"), "regra a v2\n")
        self.assertEqual((self.pasta / "eu/VOZ.md").read_text(encoding="utf-8"), "o tom dela\n")


if __name__ == "__main__":
    unittest.main()
