import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}

FICAM_FORA = [
    "eu/cv/contato.yml",
    "eu/cv/out/Fulana-CV.pdf",
    "eu/cv-antigo.pdf",
    "eu/Perfil.PDF",
    "eu/cv-antigo.docx",
    "eu/cv-antigo.doc",
    "eu/Connections.csv",
    "eu/Basic_LinkedInDataExport.zip",
]
ENTRAM = [
    "eu/VOZ.md",
    "eu/cv/FATOS.yml",
    "eu/cv/variantes/base-pt.yml",
    "eu/posts/001-assunto-PARA-COLAR.txt",
    "eu/posts/assets/imagem.png",
    "eu/.gitignore",
]


class TestGitignore(unittest.TestCase):
    """Confere o .gitignore do motor como o git de cada cópia vai ler."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, env=ENV, check=True)
        shutil.copy(RAIZ / ".gitignore", self.repo / ".gitignore")

    def tearDown(self):
        self._tmp.cleanup()

    def ignorado(self, caminho):
        r = subprocess.run(
            ["git", "-c", "core.ignorecase=false", "check-ignore", "-q", caminho],
            cwd=self.repo, env=ENV,
        )
        return r.returncode == 0

    def test_dado_pessoal_fica_fora(self):
        for caminho in FICAM_FORA:
            self.assertTrue(self.ignorado(caminho), caminho)

    def test_conteudo_dela_entra(self):
        for caminho in ENTRAM:
            self.assertFalse(self.ignorado(caminho), caminho)


if __name__ == "__main__":
    unittest.main()
