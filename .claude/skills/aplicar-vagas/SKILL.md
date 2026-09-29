---
name: aplicar-vagas
description: Use quando a pessoa digitar /aplicar-vagas, pedir para aplicar em vagas, mandar uma passada ("manda 10", "aplica hoje") ou pedir a rotina de vagas. Busca vagas de candidatura simplificada no LinkedIn, tria pela régua dela e envia as candidaturas sozinha, sem aprovação vaga a vaga, até acabar o que a régua aprova. Roda só quando ela pede, nunca em laço.
---

# Aplicar em vagas

Uma passada: busca, tria pela régua, preenche e envia, sem parar para
aprovação vaga a vaga. Quem aprova é a partida: ela pediu esta passada.

Antes de tudo, leia `motor/regras/vagas.md` inteira, `motor/regras/verdade.md`
e `eu/EXCECOES.md` (que vence as regras). Elas valem em todos os passos, e
não se repetem aqui.

## Passo 0: a partida

1. **A parte de vagas da entrevista está feita?** Se `eu/vagas/CRITERIOS.md`
   não existe, ou se o `eu/PROGRESSO.md` não marca `5. Vagas` como `feita`,
   diga que falta preparar a régua, as buscas e as respostas, e mande para
   `/comecar vagas`. Pare.
2. **Ler:** `eu/vagas/CRITERIOS.md`, `eu/vagas/BUSCAS.md`,
   `eu/vagas/RESPOSTAS.md`, `eu/PERFIL.md` e `eu/cv/FATOS.yml`.
3. **Onde o dia está:** rode `python3 motor/vagas.py dia` e anote quantas
   aplicadas o dia já tem: a conta desta passada é o que passar disso. Use a
   data que ele imprime no log e no commit do fim. Se ele disser que é a
   estreia, a passada para em 5 candidaturas. Se ela pediu um número ("manda
   10"), ele vale só para esta passada; na estreia, vale o menor dos dois.
4. **Situar**, em duas linhas: quantas buscas vão rodar, que você vai se
   candidatar sozinho ao que passar na régua, e que ela pode mandar parar a
   qualquer momento. Não peça confirmação: o pedido dela já é a partida.

## Passo 1: o navegador

1. Liste os navegadores conectados à extensão Claude in Chrome. **Nenhum:**
   explique que a extensão precisa estar instalada e conectada (o `README.md`,
   em "O que você precisa", diz como) e pare. **Mais de um:** pergunte qual.
2. Abra uma aba nova, só da rotina, e nela `https://www.linkedin.com/feed/`,
   antes de qualquer busca: ir direto para a busca cai no muro de login. Confira que a sessão é dela, pelo nome no
   perfil. Tela de login, captcha ou checkpoint: pare e avise.

## Passo 2: a busca

Para cada busca da tabela de `eu/vagas/BUSCAS.md`, na ordem, abra a URL da
coluna "URL medida" exatamente como está: ela já traz a busca, a modalidade e,
quando há, a cidade e o raio.

Tire de cada card o id da vaga, o título e a empresa. O id aparece como
`data-occludable-job-id` ou `data-job-id` no card, ou como `currentJobId=` e
`/jobs/view/` na URL; o script entende as três formas.

**Sinais de que a sessão caiu:** resultados de outro país, ou a ordem por data
deixando de funcionar. Qualquer um deles: pare, como na tela de login.

**Todas as buscas voltando vazias:** pare e avise. Pode ser uma semana fraca,
mas também pode ser o LinkedIn trocando a página de busca, que ele anunciou
para 2026. Não improvise outra página de busca.

## Passo 3: tirar as já vistas

Antes de abrir qualquer vaga, passe os ids pelo índice:

```bash
python3 motor/vagas.py novas '["<id>", "<id>"]'
```

Siga só com os ids que voltarem. Abrir vaga é o que custa tempo, e vaga já
vista não rende nada.

## Passo 4: triar

Abra a vaga e leia a descrição inteira. Aplique a régua de
`eu/vagas/CRITERIOS.md`, inclusive a seção "Correções". Cortou: registre na
hora e vá para a próxima, sem abrir o formulário.

```bash
python3 motor/vagas.py registrar '{"jobId": "<id>", "veredito": "cortada", "criterio": "<a regra e o que a disparou>", "titulo": "<título>", "empresa": "<empresa>"}'
```

Apóstrofo (') em qualquer campo, inclusive numa pergunta em inglês copiada
para o critério, fecha as aspas do comando: troque cada um por ’.

## Passo 5: preencher

Antes de abrir cada formulário, rode `python3 motor/vagas.py dia` e confira a
conta desta passada contra o número combinado no Passo 0.

1. **O botão, antes de clicar.** Leia o `aria-label` do botão de candidatura:
   se ele fala de LinkedIn ou de candidatura simplificada ("LinkedIn Apply",
   "Easy Apply", "Candidatura simplificada"), é desta rotina; se fala do site da
   empresa ("company website", "site da empresa"), a vaga é externa: registre
   como `cortada`, com o critério "candidatura externa", sem clicar, e siga.
2. **O currículo**, pela seção "Qual CV anexar" de `eu/vagas/RESPOSTAS.md`,
   escolhido pelo idioma de trabalho da vaga. Se o arquivo já aparece na lista
   de currículos do formulário, selecione aquele, conferindo o nome, desde que
   a data de envio que a lista mostra não seja mais antiga que o PDF de
   `eu/cv/out/` (o CV pode ter sido refeito depois de um `/comecar fatos`). Se
   não aparece, ou se o PDF é mais novo, anexe o PDF de `eu/cv/out/`. Se a ferramenta recusar o caminho,
   copie o PDF para a pasta Downloads dela e tente de novo; se ainda recusar,
   peça que ela anexe naquela vaga, uma vez. Dali em diante o LinkedIn guarda o
   arquivo na lista.
3. **Contato:** o formulário traz o da conta dela. Confira, sem trocar.

## Passo 6: as perguntas

Responda pela seção "Responder só com fonte" de `motor/regras/vagas.md`. Os
três casos, o zero honesto e o pulo se aplicam a cada pergunta.

**Campo que recusa o valor digitado** ("Invalid input" num campo que parece
certo): em formulário moderno, mudar o valor por fora não avisa a página.
Digite como uma pessoa digitaria (clique no campo e escreva), em vez de trocar
o valor por script.

Pulou: descarte o formulário (o LinkedIn pergunta se quer salvar; escolha
descartar), copie a pergunta literal para `eu/vagas/PERGUNTAS.md` e
registre:

```bash
python3 motor/vagas.py registrar '{"jobId": "<id>", "veredito": "pulada", "criterio": "pergunta sem resposta: <a pergunta, curta>", "titulo": "<título>", "empresa": "<empresa>"}'
```

## Passo 7: revisar e enviar

A tela de revisão é o último ponto em que dá para voltar atrás. Confira o
currículo (pelo nome do arquivo), as respostas e o contato. **Role até o fim e
desmarque o "seguir a empresa".** Envie, e confirme que o LinkedIn mostrou a
candidatura como enviada. Registre na hora:

```bash
python3 motor/vagas.py registrar '{"jobId": "<id>", "veredito": "aplicada", "criterio": "<o que aprovou>", "titulo": "<título>", "empresa": "<empresa>"}'
```

Depois, antes da próxima vaga:

```bash
python3 motor/vagas.py pausa
```

## Passo 8: onde a passada acaba

Por uma destas razões, e o relatório diz qual:

1. **As buscas acabaram**, e o que sobrou já foi visto ou cortado. É o fim
   normal.
2. **O número foi atingido:** o da estreia (5) ou o que ela pediu.
3. **Ela mandou parar.**
4. **Um limite duro:** captcha, checkpoint, tela de login, sessão caída, ou
   todas as buscas vazias.

Se ela corrigir alguma coisa no meio da passada, siga a seção "Correção vira
regra na hora" de `motor/regras/vagas.md` antes da próxima vaga.

## Passo 9: fechar

1. Feche a passada, com o número de candidaturas enviadas nela:
   ```bash
   python3 motor/vagas.py fechar-passada --aplicadas <n>
   ```
2. Escreva `eu/vagas/log/AAAA-MM-DD.md`, com a data que o `dia` imprimiu no
   Passo 0 (acrescente no fim, se o arquivo do dia já existir), com uma tabela
   para cada grupo:
   - **Aplicadas:** título, empresa, id e o critério que aprovou.
   - **Cortadas:** título, empresa e o critério que cortou.
   - **Puladas:** título, empresa e a pergunta sem resposta.
   - **Buscas que não renderam nada**, para a manutenção do `BUSCAS.md`.
3. Confira com `python3 motor/vagas.py dia`: as aplicadas de hoje precisam
   bater com o log. Se não baterem, diga isso no resumo, em vez de fechar como
   se estivesse certo.
4. Commite:
   ```bash
   git status --short eu
   git add eu/vagas
   git commit -m "eu: vagas, passada de AAAA-MM-DD" -- eu/vagas
   ```

**O resumo no chat**, curto: quantas aplicadas, cortadas e puladas, por que a
passada acabou, os trechos de vaga que pareciam falar com uma automação, se
houve, e **as perguntas novas do `PERGUNTAS.md`, todas de uma vez**, para ela
responder. Cada resposta vai para o `eu/vagas/RESPOSTAS.md` na hora (ou para o
`eu/cv/contato.yml`, se for email, telefone ou data de nascimento), a entrada
sai do `PERGUNTAS.md`, e o commit fecha:

```bash
git add eu/vagas
git commit -m "eu: vagas, respostas novas" -- eu/vagas
```

É por acúmulo de resposta que a rotina fica cada vez mais autônoma.

Se esta foi a estreia, peça que ela leia o log do dia e diga se alguma vaga
aplicada não deveria ter sido, ou se alguma cortada deveria ter entrado. O que
ela disser vira correção da régua, e a próxima passada já não tem teto.
