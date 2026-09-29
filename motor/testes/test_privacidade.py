import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import privacidade

ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


class TestUrl(unittest.TestCase):
    def test_formatos_do_github(self):
        esperado = ("fulana", "meu-linkedin")
        for url in ("git@github.com:fulana/meu-linkedin.git",
                    "https://github.com/fulana/meu-linkedin",
                    "https://github.com/fulana/meu-linkedin.git",
                    "ssh://git@github.com/fulana/meu-linkedin.git"):
            self.assertEqual(privacidade.repo_github(url), esperado, url)

    def test_fora_do_github(self):
        self.assertIsNone(privacidade.repo_github("https://gitlab.com/a/b"))
        self.assertIsNone(privacidade.repo_github("/tmp/kit"))

    def test_classificar(self):
        self.assertEqual(privacidade.classificar(200), "publico")
        self.assertEqual(privacidade.classificar(404), "privado")
        self.assertEqual(privacidade.classificar(403), "desconhecido")
        self.assertEqual(privacidade.classificar(None), "desconhecido")


class TestChecar(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.raiz, env=ENV, check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def remote(self, nome, url):
        subprocess.run(["git", "remote", "add", nome, url], cwd=self.raiz, env=ENV, check=True)

    def test_sem_remote(self):
        codigo, mensagem = privacidade.checar(self.raiz, consulta=lambda d, r: 200)
        self.assertEqual(codigo, 0)
        self.assertIn("privado", mensagem)

    def test_publico(self):
        self.remote("origin", "https://github.com/fulana/meu-linkedin.git")
        codigo, mensagem = privacidade.checar(self.raiz, consulta=lambda d, r: 200)
        self.assertEqual(codigo, 1)
        self.assertIn("PÚBLICO", mensagem)
        self.assertIn("fulana/meu-linkedin", mensagem)

    def test_privado(self):
        self.remote("origin", "https://github.com/fulana/meu-linkedin.git")
        codigo, _ = privacidade.checar(self.raiz, consulta=lambda d, r: 404)
        self.assertEqual(codigo, 0)

    def test_sem_internet(self):
        self.remote("origin", "https://github.com/fulana/meu-linkedin.git")
        codigo, mensagem = privacidade.checar(self.raiz, consulta=lambda d, r: None)
        self.assertEqual(codigo, 2)
        self.assertIn("confirmar", mensagem)

    def test_ignora_o_remote_do_template(self):
        self.remote("kit", "https://github.com/mantenedor/linkedin-kit.git")
        codigo, _ = privacidade.checar(self.raiz, consulta=lambda d, r: 200)
        self.assertEqual(codigo, 0)


if __name__ == "__main__":
    unittest.main()
