import contextlib
import datetime
import io
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cv"))
import gerar

FATOS = {
    "identidade": {
        "nome": "Ana Teste",
        "titulo": {"pt": "Enfermeira", "en": "Nurse"},
        "disponibilidade": {"pt": "Presencial em São Paulo"},
    },
    "resumo": {"base": {"pt": "Enfermeira desde 2015."}},
    "experiencias": [{
        "id": "hosp",
        "empresa": "Hospital Modelo",
        "cargo": {"pt": "Enfermeira", "en": "Nurse"},
        "inicio": "2021-03",
        "fim": "atual",
        "contexto": {"pt": "Hospital geral de 200 leitos."},
        "bullets": [{"id": "hosp-uti", "pt": "Coordenei a escala de 12 leitos."}],
    }],
    "projetos": [],
    "skills": [{"id": "clinica", "titulo": {"pt": "Clínica"}, "itens": ["Sepse", "Ventilação"]}],
    "idiomas": [{"lingua": {"pt": "Inglês"}, "nivel": {"pt": "Intermediário"}}],
    "formacao": [{"id": "grad", "curso": {"pt": "Enfermagem"}, "instituicao": "Faculdade Teste", "inicio": 2011, "fim": 2015}],
}
CONTATO = {
    "email": "ana@example.com",
    "telefone": "+55 11 90000-0000",
    "local": "São Paulo, SP",
    "links": [{"texto": "linkedin.com/in/ana", "url": "https://linkedin.com/in/ana"}],
}
VARIANTE = {
    "idioma": "pt", "arquivo": "Ana-CV", "resumo": "base",
    "experiencias": {"hosp": ["hosp-uti"]}, "skills": ["clinica"], "formacao": ["grad"],
}
TEMPLATE = "<html lang='{{LANG}}'><title>{{TITULO_DOC}}</title>{{CONTEUDO}}</html>"


class TestDatas(unittest.TestCase):
    def test_duracao_inclusiva(self):
        self.assertEqual(gerar.formata_duracao("2024-12", "2026-07", "pt"), "1a 8m")

    def test_fim_atual_conta_ate_hoje(self):
        hoje = datetime.date(2026, 9, 29)
        self.assertEqual(gerar.formata_duracao("2025-10", "atual", "pt", hoje=hoje), "1a")

    def test_data_atual_por_idioma(self):
        self.assertEqual(gerar.formata_data("atual", "pt"), "atual")
        self.assertEqual(gerar.formata_data("atual", "en"), "present")
        self.assertEqual(gerar.formata_data("2021-03", "pt"), "mar/2021")

    def test_loc_cai_para_pt_e_trata_vazio(self):
        self.assertEqual(gerar.loc({"pt": "x"}, "en"), "x")
        self.assertEqual(gerar.loc(None, "pt"), "")
        self.assertEqual(gerar.loc("texto", "en"), "texto")


class TestDocumento(unittest.TestCase):
    def test_documento_pt_tem_o_conteudo(self):
        doc = gerar.monta_documento(FATOS, CONTATO, VARIANTE, TEMPLATE, "Ana-CV")
        for trecho in ("Ana Teste", "ana@example.com", "linkedin.com/in/ana",
                       "Coordenei a escala de 12 leitos.", "mar/2021 a atual", "Sepse, Ventilação"):
            self.assertIn(trecho, doc)
        self.assertNotIn("{{", doc)
        self.assertNotIn("None", doc)

    def test_registro_profissional_do_contato_vai_no_cabecalho(self):
        contato = {**CONTATO, "registro": "COREN-SP 000000"}
        doc = gerar.monta_documento(FATOS, contato, VARIANTE, TEMPLATE, "x")
        self.assertIn("COREN-SP 000000", doc.split("</header>")[0])

    def test_certificacoes_entram_quando_a_variante_pede(self):
        fatos = {**FATOS, "certificacoes": [
            {"id": "acls", "nome": "ACLS", "instituicao": "Instituto Teste", "ano": 2023, "validade": 2025},
        ]}
        doc = gerar.monta_documento(fatos, CONTATO, {**VARIANTE, "certificacoes": ["acls"]}, TEMPLATE, "x")
        self.assertIn("Certificações", doc)
        self.assertIn("ACLS", doc)
        self.assertIn("Instituto Teste, 2023, válida até 2025", doc)

    def test_validade_com_mes(self):
        fatos = {**FATOS, "certificacoes": [{"id": "bls", "nome": "BLS", "ano": 2024, "validade": "2026-11"}]}
        doc = gerar.monta_documento(fatos, CONTATO, {**VARIANTE, "certificacoes": ["bls"]}, TEMPLATE, "x")
        self.assertIn("2024, válida até nov/2026", doc)

    def test_avisa_certificacao_vencida(self):
        hoje = datetime.date(2026, 9, 29)
        fatos = {**FATOS, "certificacoes": [
            {"id": "velha", "nome": "Vencida no mês", "validade": "2026-03"},
            {"id": "ano", "nome": "Vencida no ano", "validade": 2025},
            {"id": "boa", "nome": "Ainda vale", "validade": "2026-11"},
            {"id": "ano-atual", "nome": "Vale até dezembro", "validade": 2026},
            {"id": "sem", "nome": "Não vence"},
        ]}
        variante = {**VARIANTE, "certificacoes": ["velha", "ano", "boa", "ano-atual", "sem"]}
        self.assertEqual(gerar.certificacoes_vencidas(fatos, variante, hoje=hoje),
                         ["Vencida no mês", "Vencida no ano"])

    def test_certificacao_sem_validade(self):
        fatos = {**FATOS, "certificacoes": [{"id": "oab", "nome": "OAB/SP", "ano": 2016}]}
        doc = gerar.monta_documento(fatos, CONTATO, {**VARIANTE, "idioma": "en", "certificacoes": ["oab"]}, TEMPLATE, "x")
        self.assertIn("Certifications", doc)
        self.assertIn("2016", doc)
        self.assertNotIn("valid until", doc)

    def test_sem_certificacoes_na_variante_nao_ha_secao(self):
        doc = gerar.monta_documento(FATOS, CONTATO, VARIANTE, TEMPLATE, "x")
        self.assertNotIn("Certificações", doc)

    def test_documento_en_traduz_periodo(self):
        doc = gerar.monta_documento(FATOS, CONTATO, {**VARIANTE, "idioma": "en"}, TEMPLATE, "Ana-CV-EN")
        self.assertIn("Mar/2021 to present", doc)
        self.assertIn("lang='en'", doc)


class TestArquivos(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.pasta_cv = Path(self._tmp.name) / "cv"
        (self.pasta_cv / "variantes").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_colisao_de_arquivo_para(self):
        for nome in ("a", "b"):
            (self.pasta_cv / "variantes" / f"{nome}.yml").write_text("arquivo: Mesmo-CV\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            gerar.checar_colisao(sorted((self.pasta_cv / "variantes").glob("*.yml")))

    def test_contato_ausente_explica(self):
        with self.assertRaises(SystemExit) as ctx:
            gerar.carrega_contato(self.pasta_cv)
        self.assertIn("contato.yml", str(ctx.exception))

    def test_checar_lista_o_que_falta(self):
        problemas = "\n".join(gerar.checar(self.pasta_cv))
        self.assertIn("FATOS.yml", problemas)
        self.assertIn("contato.yml", problemas)
        self.assertIn("variante", problemas)


class TestChrome(unittest.TestCase):
    def test_variavel_de_ambiente_vence(self):
        self.assertEqual(gerar.acha_chrome(env={"CHROME": "/x/chrome"}), "/x/chrome")

    def test_procura_no_path_quando_nao_acha_caminho_fixo(self):
        achado = gerar.acha_chrome(
            env={}, existe=lambda p: False,
            procura=lambda n: "/usr/bin/chromium" if n == "chromium" else None,
        )
        self.assertEqual(achado, "/usr/bin/chromium")

    def test_nenhum_chrome(self):
        self.assertIsNone(gerar.acha_chrome(env={}, existe=lambda p: False, procura=lambda n: None))


@unittest.skipUnless(gerar.acha_chrome(), "Chrome não instalado")
class TestPdfDeVerdade(unittest.TestCase):
    def test_gera_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta_cv = Path(tmp) / "cv"
            (pasta_cv / "variantes").mkdir(parents=True)
            (pasta_cv / "FATOS.yml").write_text(yaml.safe_dump(FATOS, allow_unicode=True), encoding="utf-8")
            (pasta_cv / "contato.yml").write_text(yaml.safe_dump(CONTATO, allow_unicode=True), encoding="utf-8")
            (pasta_cv / "variantes" / "base.yml").write_text(yaml.safe_dump(VARIANTE, allow_unicode=True), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(gerar.main(["--eu", tmp, "base"]), 0)
            pdf = pasta_cv / "out" / "Ana-CV.pdf"
            self.assertTrue(pdf.exists())
            self.assertGreater(pdf.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
