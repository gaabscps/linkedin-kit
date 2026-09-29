# Regras do CV

Como o currículo é montado neste kit, e por quê. O CV é um artefato gerado, e
não um PDF editado à mão: os fatos moram num lugar só, e cada PDF é derivado
deles. Se você discorda de alguma regra daqui, registre a exceção em
`eu/EXCECOES.md`, que vence qualquer regra deste arquivo.

---

## Fonte única

| Arquivo | O que é |
|---|---|
| `eu/cv/FATOS.yml` | Todo o conteúdo: bullets nas duas línguas, projetos, competências, formação. |
| `eu/cv/contato.yml` | Email, telefone, cidade e links. Fora do git. |
| `eu/cv/variantes/*.yml` | Só seleção: o que entra, em que ordem e em que idioma. Zero conteúdo. |
| `eu/cv/out/` | Os PDFs gerados. Saída, fora do git. |

CV editado à mão envelhece em silêncio: continua dizendo que a pessoa está num
emprego meses depois da saída, ou dá três números diferentes para o tempo de
carreira. Com uma fonte só, quando um fato muda, todas as versões acompanham na
próxima geração.

---

## As quatro lentes

Todo bullet carrega pelo menos uma destas quatro coisas:

| Lente | Pergunta | Exemplo |
|---|---|---|
| **Escala** | Quanto, quantos, que volume? | Enfermagem: "Coordenei a escala de 20 leitos de UTI." |
| **Posse** | O que era seu, e não do time? | Vendas: "Assumi sozinho a carteira de 40 clientes da região Sul." |
| **Resultado** | O que ficou de pé depois? | Docência: "Levei a turma de 3º ano de 60% para 85% de aprovação." |
| **Dificuldade** | O que tornava aquilo difícil? | Direito: "Protocolei a defesa em 48 horas, com o processo recebido na véspera do prazo." |

Sem nenhuma das quatro, o bullet é descrição de cargo ("Responsável pelo
atendimento ao cliente") e sai do CV.

---

## Forma do bullet

- **Começa pelo verbo, sem sujeito.** "Implantei", "Coordenei", "Reduzi".
- **Não pendura explicação de contexto** que o cabeçalho da experiência já dá.
  Se a experiência já diz que é um hospital, o bullet não repete "dentro de um
  hospital de grande porte".
- **Não troca de sujeito no meio da lista.** "Entregamos o projeto, comigo à
  frente" mistura "nós" e "eu"; escolha um.
- **Descrição de projeto é outro gênero:** prosa curta, e ali a primeira pessoa
  pode ficar.

---

## Resumo

O resumo é o único texto reescrito por vaga, e por isso é onde o tom mais
oscila. Três movimentos, nesta ordem, e nada além deles:

1. **Quem a pessoa é e desde quando.** Uma frase, com o ano de início.
2. **A posse principal**, com o que a vaga pede citado dentro dela.
3. **A peça que mais conversa com esta vaga**, com o número que a sustenta.

Limites:

- **Máximo de 90 palavras.** Acima disso o leitor pula direto para a
  experiência.
- **Nenhum fato que não exista no `FATOS.yml`.** O resumo não é lugar de
  estrear informação.
- **Nada de palavra-chave solta no fim** ("Domínio de Excel."). Se importa,
  entra dentro do movimento 2 ou do 3.
- **Sem autoelogio** (ver `motor/regras/escrita.md`).

---

## Tags

As tags de cada bullet existem para filtrar rápido, e **não escolhem nada
sozinhas**. Quem escolhe os bullets de uma vaga é gente. Um seletor automático
produziria um CV que bate no checklist da vaga e não conta história nenhuma.

---

## Variante de vaga

1. Copiar a base do idioma da vaga (`base-pt.yml` ou `base-en.yml`).
2. Nome do arquivo: `AAAA-MM-DD-empresa-cargo.yml`.
3. **Trocar o `arquivo:`** para um nome único da vaga. Ele dá nome ao PDF, e
   uma cópia que o mantenha sobrescreveria o PDF de outra variante. O gerador
   barra isso, mas o erro custa uma execução.
4. Reescrever o resumo pelos três movimentos.
5. Reordenar os bullets, com o que mais conversa com a vaga primeiro.

---

## Forma do PDF

- **Uma coluna.** O ATS (o sistema que várias empresas usam para ler currículos
  automaticamente) lê o PDF na ordem do texto, e duas colunas embaralham tudo.
- **Sem foto, por padrão.** Em vaga internacional ela costuma ser sinal
  negativo. Se a sua área espera foto, registre isso em `eu/EXCECOES.md`.
- **Títulos de seção padrão** (Experiência, Formação), que o ATS reconhece.
- **Duração ao lado do período** ("2a 3m"), porque boa permanência não se
  percebe lendo datas cruas.
- **Certificações antes da formação**, quando existem: curso com certificado,
  registro profissional, habilitação. Certificado que vence leva o ano da
  validade, porque vencido ele conta contra.
- **Formação no fim.**

---

## Idioma do CV

O CV é exceção à tradução literal dos posts. Em inglês ele segue a convenção de
currículo: verbo no passado, sem "I" no começo de cada linha. No post o leitor
avalia se aquilo soa como você; no CV ele avalia rapidez, e a convenção é o que
deixa o texto rápido de ler.

O texto nasce em português. Se um bullet mudar, mude o `pt` primeiro e refaça o
`en` a partir dele.
