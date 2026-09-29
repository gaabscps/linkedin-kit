import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MOTOR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOTOR))
import atualizar

ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Teste", "GIT_AUTHOR_EMAIL": "teste@example.com",
    "GIT_COMMITTER_NAME": "Teste", "GIT_COMMITTER_EMAIL": "teste@example.com",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
}
NOVIDADES_V1 = "# Novidades\n\n## v1.0.0\n\n- Primeira versão.\n"
NOVIDADES_V11 = "# Novidades\n\n## v1.1.0\n\n- Regra A reescrita.\n\n## v1.0.0\n\n- Primeira versão.\n"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, check=True, capture_output=True, text=True).stdout


def escreve(raiz, caminho, texto):
    arq = raiz / caminho
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding="utf-8")


class TestNovidades(unittest.TestCase):
    def test_pega_so_o_intervalo(self):
        texto = "# N\n\n## v1.2.0 (2026-11-01)\n\n- c\n\n## v1.1.0\n\n- b\n\n## v1.0.0\n\n- a\n"
        saida = atualizar.novidades_entre(texto, "1.0.0", "1.2.0")
        self.assertIn("- c", saida)
        self.assertIn("- b", saida)
        self.assertNotIn("- a", saida)


class TestAtualizar(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.kit = tmp / "kit"
        self.copia = tmp / "copia"
        self.kit.mkdir()
        git(self.kit, "init", "-q", "-b", "main")
        for nome in ("atualizar.py", "kit.py"):
            escreve(self.kit, f"motor/{nome}", (MOTOR / nome).read_text(encoding="utf-8"))
        escreve(self.kit, "CLAUDE.md", "claude v1\n")
        escreve(self.kit, "README.md", "leia v1\n")
        escreve(self.kit, ".gitignore", "__pycache__/\n")
        escreve(self.kit, ".claude/skills/comecar/SKILL.md", "skill v1\n")
        escreve(self.kit, "motor/regras/a.md", "regra a v1\n")
        escreve(self.kit, "motor/regras/velho.md", "regra velha\n")
        escreve(self.kit, "motor/VERSAO", "1.0.0\n")
        escreve(self.kit, "motor/ORIGEM", f"{self.kit}\n")
        escreve(self.kit, "motor/NOVIDADES.md", NOVIDADES_V1)
        escreve(self.kit, "eu/LEIA-ME.md", "sua pasta\n")
        git(self.kit, "add", "-A")
        git(self.kit, "commit", "-q", "-m", "v1")
        git(self.kit, "tag", "v1.0.0")
        # Cópia do jeito que o "Use this template" faz: os arquivos, sem o histórico.
        shutil.copytree(self.kit, self.copia, ignore=shutil.ignore_patterns(".git"))
        git(self.copia, "init", "-q", "-b", "main")
        escreve(self.copia, "eu/VOZ.md", "o tom dela\n")
        git(self.copia, "add", "-A")
        git(self.copia, "commit", "-q", "-m", "copia")

    def tearDown(self):
        self._tmp.cleanup()

    def publicar_v110(self):
        escreve(self.kit, "motor/regras/a.md", "regra a v2\n")
        (self.kit / "motor/regras/velho.md").unlink()
        escreve(self.kit, ".claude/skills/nova/SKILL.md", "skill nova\n")
        escreve(self.kit, "motor/VERSAO", "1.1.0\n")
        escreve(self.kit, "motor/NOVIDADES.md", NOVIDADES_V11)
        git(self.kit, "add", "-A")
        git(self.kit, "commit", "-q", "-m", "v1.1")
        git(self.kit, "tag", "v1.1.0")

    def rodar(self, *args):
        r = subprocess.run([sys.executable, "motor/atualizar.py", *args],
                           cwd=self.copia, env=ENV, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def ler(self, caminho):
        return (self.copia / caminho).read_text(encoding="utf-8")

    def test_sem_origem(self):
        escreve(self.copia, "motor/ORIGEM", "")
        codigo, saida = self.rodar("verificar")
        self.assertEqual(codigo, 2)
        self.assertTrue(saida.startswith("ESTADO: sem-origem"))

    def test_ja_atualizado(self):
        codigo, saida = self.rodar("verificar")
        self.assertEqual(codigo, 0)
        self.assertTrue(saida.startswith("ESTADO: atualizado"))

    def test_verificar_anuncia_versao_nova(self):
        self.publicar_v110()
        codigo, saida = self.rodar("verificar")
        self.assertEqual(codigo, 0)
        self.assertTrue(saida.startswith("ESTADO: disponivel"))
        self.assertIn("v1.1.0", saida)
        self.assertEqual(self.ler("motor/regras/a.md"), "regra a v1\n")

    def test_aplica_e_preserva_eu(self):
        self.publicar_v110()
        voz_antes = (self.copia / "eu/VOZ.md").read_bytes()
        codigo, saida = self.rodar("aplicar")
        self.assertEqual(codigo, 0, saida)
        self.assertTrue(saida.startswith("ESTADO: aplicado"))
        self.assertEqual(self.ler("motor/regras/a.md"), "regra a v2\n")
        self.assertFalse((self.copia / "motor/regras/velho.md").exists())
        self.assertTrue((self.copia / ".claude/skills/nova/SKILL.md").exists())
        self.assertEqual((self.copia / "eu/VOZ.md").read_bytes(), voz_antes)
        self.assertIn("Regra A reescrita", saida)
        self.assertNotIn("Primeira versão", saida)
        self.assertIn("v1.1.0", git(self.copia, "log", "-1", "--format=%s"))
        self.assertEqual(git(self.copia, "status", "--porcelain"), "")

    def test_edicao_commitada_no_motor_bloqueia(self):
        self.publicar_v110()
        escreve(self.copia, "motor/regras/a.md", "minha mudança\n")
        git(self.copia, "commit", "-q", "-am", "mexi no motor")
        codigo, saida = self.rodar("aplicar")
        self.assertEqual(codigo, 5)
        self.assertTrue(saida.startswith("ESTADO: editado"))
        self.assertIn("motor/regras/a.md", saida)
        self.assertEqual(self.ler("motor/regras/a.md"), "minha mudança\n")

    def test_ignorar_edicoes_segue(self):
        self.publicar_v110()
        escreve(self.copia, "motor/regras/a.md", "minha mudança\n")
        git(self.copia, "commit", "-q", "-am", "mexi no motor")
        codigo, saida = self.rodar("aplicar", "--ignorar-edicoes")
        self.assertEqual(codigo, 0, saida)
        self.assertEqual(self.ler("motor/regras/a.md"), "regra a v2\n")

    def test_skill_propria_da_pessoa_sobrevive_a_atualizacao(self):
        self.publicar_v110()
        escreve(self.copia, ".claude/skills/minha/SKILL.md", "skill dela\n")
        git(self.copia, "add", ".claude/skills/minha/SKILL.md")
        git(self.copia, "commit", "-q", "-m", "skill dela")
        codigo, saida = self.rodar("aplicar", "--ignorar-edicoes")
        self.assertEqual(codigo, 0, saida)
        self.assertEqual(self.ler(".claude/skills/minha/SKILL.md"), "skill dela\n")
        self.assertIn(".claude/skills/minha/SKILL.md", git(self.copia, "ls-files"))
        self.assertEqual(self.ler("motor/regras/a.md"), "regra a v2\n")

    def test_mudanca_nao_salva_bloqueia_mesmo_ignorando(self):
        self.publicar_v110()
        escreve(self.copia, "motor/regras/a.md", "rascunho\n")
        codigo, saida = self.rodar("aplicar", "--ignorar-edicoes")
        self.assertEqual(codigo, 3)
        self.assertTrue(saida.startswith("ESTADO: nao-salvo"))
        self.assertEqual(self.ler("motor/regras/a.md"), "rascunho\n")

    def test_trabalho_em_eu_nao_salvo_nao_entra_no_commit(self):
        self.publicar_v110()
        escreve(self.copia, "eu/VOZ.md", "rascunho dela\n")
        git(self.copia, "add", "eu/VOZ.md")
        codigo, saida = self.rodar("aplicar")
        self.assertEqual(codigo, 0, saida)
        arquivos_do_commit = git(self.copia, "show", "--name-only", "--format=", "HEAD")
        self.assertNotIn("eu/VOZ.md", arquivos_do_commit)
        self.assertEqual(self.ler("eu/VOZ.md"), "rascunho dela\n")

    def test_aplica_traz_o_settings_do_claude(self):
        escreve(self.kit, ".claude/settings.json", "{}\n")
        self.publicar_v110()
        codigo, saida = self.rodar("aplicar")
        self.assertEqual(codigo, 0, saida)
        self.assertEqual(self.ler(".claude/settings.json"), "{}\n")

    def atualizada_por_script_antigo(self):
        """Deixa a cópia como o script de uma versão anterior deixaria: na v1.1.0,
        mas sem o .claude/settings.json, um caminho do motor que ele não conhecia."""
        escreve(self.kit, ".claude/settings.json", "{}\n")
        self.publicar_v110()
        self.rodar("aplicar")
        git(self.copia, "rm", "-q", ".claude/settings.json")
        git(self.copia, "commit", "-q", "-m", "motor: atualiza de v1.0.0 para v1.1.0")

    def test_completa_arquivo_que_um_script_antigo_nao_trouxe(self):
        self.atualizada_por_script_antigo()
        codigo, saida = self.rodar("verificar")
        self.assertEqual(codigo, 0, saida)
        self.assertTrue(saida.startswith("ESTADO: atualizado"), saida)
        self.assertIn(".claude/settings.json", saida)
        self.assertEqual(self.ler(".claude/settings.json"), "{}\n")
        self.assertEqual(git(self.copia, "log", "-1", "--format=%s").strip(), "motor: completa a v1.1.0")
        self.assertEqual(git(self.copia, "status", "--porcelain"), "")

    def test_arquivo_que_faltava_nao_vira_edicao_na_versao_seguinte(self):
        self.atualizada_por_script_antigo()
        escreve(self.kit, "motor/regras/a.md", "regra a v3\n")
        escreve(self.kit, "motor/VERSAO", "1.2.0\n")
        escreve(self.kit, "motor/NOVIDADES.md", "# Novidades\n\n## v1.2.0\n\n- Regra A de novo.\n\n" + NOVIDADES_V11[len("# Novidades\n\n"):])
        git(self.kit, "commit", "-q", "-am", "v1.2")
        git(self.kit, "tag", "v1.2.0")
        codigo, saida = self.rodar("aplicar")
        self.assertEqual(codigo, 0, saida)
        self.assertTrue(saida.startswith("ESTADO: aplicado"), saida)
        self.assertEqual(self.ler("motor/regras/a.md"), "regra a v3\n")

    def test_avisar_fica_calado_na_versao_mais_nova(self):
        codigo, saida = self.rodar("avisar")
        self.assertEqual((codigo, saida), (0, ""))

    def test_avisar_conta_da_versao_nova_sem_mexer_na_pasta(self):
        self.publicar_v110()
        codigo, saida = self.rodar("avisar")
        self.assertEqual(codigo, 0, saida)
        self.assertIn("v1.1.0", saida)
        self.assertIn("v1.0.0", saida)
        self.assertIn("/atualizar", saida)
        self.assertEqual(git(self.copia, "remote"), "")
        self.assertEqual(git(self.copia, "tag"), "")
        self.assertEqual(self.ler("motor/regras/a.md"), "regra a v1\n")

    def test_avisar_fica_calado_sem_conexao(self):
        escreve(self.copia, "motor/ORIGEM", f"{self.kit.parent / 'nao-existe'}\n")
        codigo, saida = self.rodar("avisar")
        self.assertEqual((codigo, saida), (0, ""))


class TestHookDoKit(unittest.TestCase):
    def test_inicio_de_sessao_roda_o_aviso(self):
        settings = json.loads((MOTOR.parent / ".claude" / "settings.json").read_text(encoding="utf-8"))
        [grupo] = settings["hooks"]["SessionStart"]
        [hook] = grupo["hooks"]
        self.assertEqual(grupo["matcher"], "startup")
        self.assertIn("motor/atualizar.py\" avisar", hook["command"])
        self.assertLessEqual(hook["timeout"], 15)


if __name__ == "__main__":
    unittest.main()
