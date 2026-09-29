import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

MOTOR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOTOR))
import vagas

HOJE = date.today().isoformat()


class TestIdDaVaga(unittest.TestCase):
    def test_as_formas_em_que_o_id_aparece(self):
        for entrada in ("https://www.linkedin.com/jobs/search/?currentJobId=4463524867&f_AL=true",
                        "https://www.linkedin.com/jobs/view/4463524867/",
                        "urn:li:jobPosting:4463524867",
                        "4463524867",
                        4463524867):
            self.assertEqual(vagas.id_da_vaga(entrada), "4463524867", entrada)

    def test_sem_id(self):
        for entrada in ("", None, "vaga boa", "123", "https://www.linkedin.com/feed/"):
            self.assertIsNone(vagas.id_da_vaga(entrada), entrada)


class TestIndice(unittest.TestCase):
    def test_novas_tira_as_vistas_e_as_repetidas_mas_devolve_a_pulada(self):
        indice = vagas.registrar(vagas.indice_vazio(), [
            {"jobId": "1000001", "veredito": "aplicada", "criterio": "c"},
            {"jobId": "1000002", "veredito": "cortada", "criterio": "c"},
            {"jobId": "1000003", "veredito": "pulada", "criterio": "c"},
        ])
        entradas = ["1000001", "1000002", "1000003", "/jobs/view/1000004/", "1000004"]
        self.assertEqual(vagas.novas(indice, entradas), ["1000003", "1000004"])

    def test_novas_recusa_o_que_nao_tem_id_em_vez_de_descartar(self):
        for entradas in (["1000001", "vaga boa"], [{"jobId": "1000001"}]):
            with self.assertRaises(ValueError, msg=entradas):
                vagas.novas(vagas.indice_vazio(), entradas)

    def test_registrar_recusa_item_que_nao_e_objeto(self):
        with self.assertRaises(ValueError):
            vagas.registrar(vagas.indice_vazio(), ["1000001"])

    def test_registrar_poe_a_data_de_hoje_quando_falta(self):
        indice = vagas.registrar(vagas.indice_vazio(), [{"jobId": "1000001", "veredito": "cortada",
                                                         "criterio": "fora da área"}])
        self.assertEqual(indice["vagas"]["1000001"]["visto_em"], HOJE)

    def test_registrar_aceita_um_objeto_so(self):
        indice = vagas.registrar(vagas.indice_vazio(), {"jobId": "1000001", "veredito": "aplicada",
                                                        "criterio": "c", "titulo": "t", "empresa": "e"})
        self.assertEqual(indice["vagas"]["1000001"]["empresa"], "e")

    def test_registrar_recusa_entrada_incompleta(self):
        for entrada in ({"veredito": "aplicada", "criterio": "c"},
                        {"jobId": "1000001", "veredito": "enviada", "criterio": "c"},
                        {"jobId": "1000001", "veredito": "cortada", "criterio": "  "}):
            with self.assertRaises(ValueError, msg=entrada):
                vagas.registrar(vagas.indice_vazio(), [entrada])

    def test_situacao_do_dia_e_a_estreia(self):
        indice = vagas.registrar(vagas.indice_vazio(), [
            {"jobId": "1000001", "veredito": "aplicada", "criterio": "c", "visto_em": "2026-10-01"},
            {"jobId": "1000002", "veredito": "cortada", "criterio": "c", "visto_em": "2026-10-01"},
            {"jobId": "1000003", "veredito": "aplicada", "criterio": "c", "visto_em": "2026-10-02"},
        ])
        self.assertIn("estreia", vagas.situacao(indice, "2026-10-01"))
        indice = vagas.fechar_passada(indice, "2026-10-01", 0)
        self.assertIn("estreia", vagas.situacao(indice, "2026-10-01"))
        indice = vagas.fechar_passada(indice, "2026-10-01", 1)
        texto = vagas.situacao(indice, "2026-10-01")
        self.assertIn("1 aplicadas em 2 passadas", texto)
        self.assertNotIn("estreia", texto)

    def test_pausa_fica_entre_20_e_60_segundos(self):
        dormiu = []
        segundos = vagas.pausa(dormir=dormiu.append, sortear=lambda a, b: b)
        self.assertEqual((segundos, dormiu), (60, [60]))
        self.assertEqual(vagas.pausa(dormir=lambda s: None, sortear=lambda a, b: a), 20)


class TestLinhaDeComando(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        (self.raiz / "motor").mkdir()
        for nome in ("vagas.py", "kit.py"):
            shutil.copy(MOTOR / nome, self.raiz / "motor" / nome)

    def tearDown(self):
        self._tmp.cleanup()

    def rodar(self, *args):
        return subprocess.run([sys.executable, "motor/vagas.py", *args], cwd=self.raiz,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)

    def test_registrar_e_novas_usam_o_indice_de_eu_vagas(self):
        r = self.rodar("registrar", json.dumps([{"jobId": "1000001", "veredito": "cortada",
                                                  "criterio": "fora da área"}]))
        self.assertEqual(r.returncode, 0, r.stderr)
        indice = json.loads((self.raiz / "eu/vagas/aplicadas.json").read_text(encoding="utf-8"))
        self.assertEqual(indice["vagas"]["1000001"]["criterio"], "fora da área")
        r = self.rodar("novas", '["1000001", "1000002"]')
        self.assertEqual(r.stdout.split(), ["1000002"])
        self.assertIn("1 novas de 2", r.stderr)

    def test_json_pode_vir_como_argumento(self):
        r = self.rodar("registrar", '{"jobId": "1000001", "veredito": "cortada", "criterio": "c"}')
        self.assertEqual(r.returncode, 0, r.stderr)
        r = self.rodar("novas", '["1000001", "1000002"]')
        self.assertEqual(r.stdout.split(), ["1000002"])

    def test_fechar_passada_e_dia(self):
        self.rodar("registrar", '{"jobId": "1000001", "veredito": "aplicada", "criterio": "c"}')
        r = self.rodar("fechar-passada", "--aplicadas", "1")
        self.assertEqual(r.returncode, 0, r.stderr)
        r = self.rodar("dia")
        self.assertIn(f"Hoje ({HOJE}): 1 aplicadas em 1 passadas", r.stdout)

    def sai_sem_esperar_entrada(self, *args):
        """Roda com a entrada aberta, como num terminal: quem espera por ela trava aqui."""
        processo = subprocess.Popen([sys.executable, "motor/vagas.py", *args],
                                    cwd=self.raiz, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        try:
            codigo = processo.wait(timeout=5)
        finally:
            processo.kill()
            processo.stdin.close()
            processo.stdout.close()
            processo.stderr.close()
        return codigo

    def test_opcao_inventada_falha_na_hora_sem_esperar_entrada(self):
        self.assertNotEqual(self.sai_sem_esperar_entrada("registrar", "--status=aplicada"), 0)
        self.assertFalse((self.raiz / "eu/vagas/aplicadas.json").exists())

    def test_sem_json_falha_na_hora_sem_esperar_entrada(self):
        for comando in ("registrar", "novas"):
            self.assertNotEqual(self.sai_sem_esperar_entrada(comando), 0, comando)
        self.assertFalse((self.raiz / "eu/vagas/aplicadas.json").exists())

    def test_json_invalido_explica_o_formato(self):
        r = self.rodar("registrar", "aplicada na vaga 1000001")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("JSON", r.stderr)


if __name__ == "__main__":
    unittest.main()
