import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verificar

TRAVESSAO = chr(0x2014)
MEIA_RISCA = chr(0x2013)
# Montados por concatenação para este arquivo não acusar a si mesmo.
PLACEHOLDER_CAIXA_ALTA = "[" + "SEU NOME" + "]"
PLACEHOLDER_MINUSCULO = "[" + "seu email aqui" + "]"


class TestVerificar(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        self.escreve("CLAUDE.md", "Leia as regras.\n")
        self.escreve("motor/regras/a.md", "Regra limpa.\n")

    def tearDown(self):
        self._tmp.cleanup()

    def escreve(self, caminho, texto):
        arq = self.raiz / caminho
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(texto, encoding="utf-8")

    def test_motor_limpo_nao_tem_problema(self):
        self.assertEqual(verificar.achar_problemas(self.raiz), [])

    def test_acusa_travessao_com_linha(self):
        self.escreve("motor/regras/a.md", "linha boa\nlinha " + TRAVESSAO + " ruim\n")
        self.assertEqual(verificar.achar_problemas(self.raiz), ["motor/regras/a.md:2: travessão"])

    def test_acusa_meia_risca(self):
        self.escreve("README.md", "de 13 " + MEIA_RISCA + " 19\n")
        self.assertEqual(verificar.achar_problemas(self.raiz), ["README.md:1: meia-risca"])

    def test_acusa_placeholder_caixa_alta_e_minusculo(self):
        self.escreve("motor/modelos/x.md", PLACEHOLDER_CAIXA_ALTA + "\n" + PLACEHOLDER_MINUSCULO + "\n")
        problemas = verificar.achar_problemas(self.raiz)
        self.assertEqual(len(problemas), 2)
        self.assertTrue(all("colchete de placeholder" in p for p in problemas))

    def test_nao_confunde_link_lista_yaml_e_checkbox(self):
        self.escreve(
            "motor/modelos/x.md",
            "[Exemplo](https://example.com)\ntags: [escala, posse]\n- [ ] item\n- [x] feito\n",
        )
        self.assertEqual(verificar.achar_problemas(self.raiz), [])

    def test_acusa_skill_que_cita_exemplo(self):
        self.escreve(".claude/skills/comecar/SKILL.md", "Leia motor/exemplo/VOZ.md\n")
        self.assertEqual(
            verificar.achar_problemas(self.raiz),
            [".claude/skills/comecar/SKILL.md:1: skill citando motor/exemplo/"],
        )

    def test_acusa_caminho_do_motor_citado_que_nao_existe(self):
        self.escreve("motor/modelos/post.md", "modelo\n")
        self.escreve(
            ".claude/skills/escrever-post/SKILL.md",
            "Copie `motor/modelos/post.md` e depois `motor/modelos/sumiu.md`.\n",
        )
        self.assertEqual(
            verificar.achar_problemas(self.raiz),
            [".claude/skills/escrever-post/SKILL.md:1: caminho citado não existe: motor/modelos/sumiu.md"],
        )

    def test_caminho_com_padrao_nao_e_conferido(self):
        self.escreve("CLAUDE.md", "Os arquivos `motor/modelos/*` e `motor/regras/`.\n")
        self.escreve("motor/regras/a.md", "Regra limpa.\n")
        self.assertEqual(verificar.achar_problemas(self.raiz), [])

    def test_ignora_eu_fora_do_modo_template(self):
        self.escreve("eu/VOZ.md", "texto dela " + TRAVESSAO + " com travessão\n")
        self.assertEqual(verificar.achar_problemas(self.raiz), [])

    def test_modo_template_exige_eu_vazia(self):
        self.escreve("eu/LEIA-ME.md", "sua pasta\n")
        self.assertEqual(verificar.achar_problemas(self.raiz, modo_template=True), [])
        self.escreve("eu/VOZ.md", "tom\n")
        self.assertEqual(
            verificar.achar_problemas(self.raiz, modo_template=True),
            ["eu/VOZ.md: arquivo pessoal dentro do template"],
        )

    def test_ignora_saida_gerada_e_binario(self):
        self.escreve("motor/exemplo/cv/out/x.html", "gerado " + TRAVESSAO + "\n")
        (self.raiz / "motor/img.png").write_bytes(b"\x89PNG\x00\xff\xfe")
        self.assertEqual(verificar.achar_problemas(self.raiz), [])


if __name__ == "__main__":
    unittest.main()
