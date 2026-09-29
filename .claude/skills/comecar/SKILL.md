---
name: comecar
description: Use quando a pessoa digitar /comecar, disser que quer começar, montar o perfil, fazer a entrevista, ou quando eu/PROGRESSO.md não existir. Entrevista a pessoa em partes (objetivo, fatos, voz, perfil, primeiro post) e preenche a pasta eu/. Também refaz uma parte só, com /comecar fatos, /comecar voz, /comecar perfil, /comecar objetivo ou /comecar post.
---

# Começar: a entrevista

A entrevista que transforma a trajetória da pessoa nos arquivos de `eu/`. É
dividida em partes, e cada parte termina gravando arquivos e marcando
`eu/PROGRESSO.md`, para que dê para parar e voltar outro dia.

Funciona igual com a pessoa sozinha ou com alguém do lado conduzindo: quem
digita as respostas não muda nada.

## Argumento

- **Sem argumento:** retoma a primeira parte que não está `feita` no
  `eu/PROGRESSO.md`.
- **`objetivo`, `fatos`, `voz`, `perfil` ou `post`:** refaz só aquela parte.
  É assim que a pessoa atualiza tudo depois de um emprego novo ou um curso
  novo.
- **`vagas`:** responda que essa parte ainda não existe no kit e que vai chegar
  por uma atualização.

## Preparação (toda vez, antes de qualquer pergunta)

1. **Criar `eu/` na primeira vez.** Se `eu/PROGRESSO.md` não existe, copie de
   `motor/modelos/`:
   - `VOZ.md`, `MATERIA-PRIMA.md`, `PERFIL.md`, `EXCECOES.md` e
     `PROGRESSO.md` para `eu/`;
   - `FATOS.yml` e `contato.yml` para `eu/cv/`;
   - e crie as pastas `eu/cv/variantes/` e `eu/posts/`.

   Nunca sobrescreva um arquivo que já existe.

2. **Conferir a privacidade.** Rode `python3 motor/privacidade.py`.
   - **Saída 1 (público):** pare. Mostre a mensagem do script e explique em uma
     frase: num repositório público, qualquer pessoa na internet lê tudo o que
     for contado aqui. Só siga depois que ela tornar o repositório privado e o
     script sair com 0.
   - **Saída 2 (não deu para confirmar):** avise, peça que ela confira pelo
     link da mensagem, e siga.
   - **Saída 0:** siga.

3. **Identidade do git.** Se `git config --local user.name` estiver vazio
   (repare no `--local`: o que importa é a identidade deste repositório, e não
   a do computador, que pode ser de outra pessoa ou ter o email pessoal dela),
   pergunte o nome dela e configure só neste repositório:
   ```bash
   git config --local user.name "o nome que ela disser"
   git config --local user.email "eu@linkedin-kit.local"
   ```
   Explique: o git assina cada versão salva com um nome e um email, e o email
   genérico evita que um email pessoal fique gravado no histórico. Isso vale
   também quando alguém conduz a entrevista no próprio computador: sem este
   passo, as versões dela sairiam assinadas por quem conduz.

4. **Situar a pessoa** em até três linhas: o que vai acontecer, que leva de 1 a
   2 horas no total, que dá para parar quando quiser. Mostre a tabela do
   `eu/PROGRESSO.md`.

## Regras de condução (valem para todas as partes)

- **Uma pergunta por vez.** Espere a resposta antes da próxima.
- **Comece pela cena, não pela categoria.** Não "quais eram suas
  responsabilidades?", e sim "me conta um dia de trabalho que você lembra bem"
  ou "me conta uma vez em que deu errado e o que você fez".
- **Adapte a pergunta à profissão dela**, com as palavras da área dela.
- **Grave o bruto logo depois de cada resposta**, em `eu/MATERIA-PRIMA.md`, do
  jeito que ela falou, e não no fim da parte. É o que permite retomar sem
  repetir pergunta se a conversa for interrompida.
- **Ao retomar ou refazer uma parte**, leia primeiro o que já existe nos
  arquivos daquela parte e pergunte só o que falta. Nunca repita uma pergunta
  que já tem resposta gravada.
- **Número que ela não confirma** entra com `verificar: true` e não vai para
  nenhum texto publicado.
- **Nunca peça documento.** Ver `motor/regras/verdade.md`, seção "Documento
  nunca".
- **Quando a razão da pergunta não for óbvia**, diga em uma frase por que está
  perguntando.
- **Ao fim de cada parte:** mostre o que foi gravado, peça o ok dela, marque a
  parte como `feita` com a data no `eu/PROGRESSO.md` e commite:
  ```bash
  git add eu
  git commit -m "eu: parte 1, fatos" -- eu
  ```
  (com o número e o nome da parte que terminou). Ao começar uma parte, marque
  `em andamento`.

## Parte 0: Objetivo

Perguntas, uma por vez:

1. Para que você quer o LinkedIn agora? (recolocação, mudar de área, conseguir
   clientes, mostrar o trabalho, manter contato com a área)
2. Quem precisa encontrar o seu perfil? (que tipo de recrutador, cliente ou
   colega)
3. Em que idioma está esse público?
4. Quando essa pessoa abrir o seu perfil, o que você quer que ela pense?
5. O que você NÃO quer parecer?

O bruto de cada resposta vai para `## Objetivo` do `eu/MATERIA-PRIMA.md`.
Grave o resumo em `eu/VOZ.md`, nas seções `## Posicionamento` e `## Idioma`. No
posicionamento, registre também a regra de `motor/regras/escrita.md`,
"Reposicionamento se deduz, não se declara", aplicada ao objetivo dela.

## Parte 1: Fatos

1. **Documentos de partida.** Peça o CV antigo em PDF (ela pode arrastar o
   arquivo para a conversa) e o PDF do perfil do LinkedIn (no LinkedIn: abrir
   o próprio perfil, botão "Mais", "Salvar como PDF"). Aceite um, os dois ou
   nenhum. O que vier desses documentos é ponto de partida, e não verdade: tudo
   é confirmado com ela.
2. **Linha do tempo.** Monte a lista de experiências com empresa, cargo, mês e
   ano de início e de fim, e **confirme cada data com ela**. A linha do tempo é
   o que mais envelhece errado num currículo. Emprego atual tem fim `atual`.
   Pergunte também se houve trabalho que não está no documento de partida:
   antes do primeiro emprego, entre dois deles, ou ao mesmo tempo (segundo
   emprego, plantão extra, aula, trabalho por conta própria). Documento velho
   esquece exatamente isso.
   Mantenha no topo de `## Trajetória` duas listas, atualizadas a cada
   resposta: **"Confirmado com ela"** e **"A confirmar"**. É por elas que uma
   conversa retomada sabe o que falta perguntar.
3. **Cada experiência, da mais recente para a mais antiga:**
   - o contexto: o que a empresa faz e o porte dela;
   - uma cena: um momento de trabalho que ela lembra bem. **Antes de pedir,
     avise** que a história se conta sem nome nem detalhe que identifique quem
     foi atendido (ver "Sigilo de terceiros" em `motor/regras/verdade.md`). Se
     um nome aparecer mesmo assim, grave a resposta já sem ele: nunca grave
     para limpar depois, porque o que foi commitado fica no histórico;
   - primeiro, firme os números que a própria cena trouxe: de onde veio cada
     um, e se houve ação dela ligada ao resultado (ver "Número" em
     `motor/regras/verdade.md`);
   - depois, as quatro lentes de `motor/regras/cv.md` **só para o que a cena
     não cobriu**, uma pergunta por vez, na língua da área dela: escala
     (quanto, quantos), posse (o que era dela e não do time), resultado (o
     que ficou de pé depois), dificuldade (o que tornava aquilo difícil).

   Grave cada resposta em `eu/MATERIA-PRIMA.md`, seção `## Trajetória`, numa
   subseção por experiência. Se uma história render post, anote também em
   `## Histórias` e em `## O que ainda rende post`.
4. **Formação, idiomas e competências**, nas palavras da área dela.
5. **Topo do CV**, uma pergunta por vez:
   - o nome profissional, que precisa ser igual no CV e no LinkedIn (é por ele
     que o recrutador procura o perfil);
   - o título: proponha o cargo atual dela, sem nível que ela não teve e sem
     anunciar a área para onde ela quer ir (ver "Título" em `verdade.md` e
     "Reposicionamento se deduz" em `escrita.md`);
   - a disponibilidade: presencial, híbrido ou remoto, e em que região;
   - o contato: email, telefone, cidade e os links que ela quer no CV. Grave
     em `eu/cv/contato.yml` e explique que esse arquivo fica fora do git, só
     no computador dela. Esta é a única resposta que não vai para a
     matéria-prima: telefone e email não se repetem em nenhum outro arquivo.

   Nome, título e disponibilidade vão para `identidade` no `eu/cv/FATOS.yml`.
6. **Bullets.** Converta o bruto em bullets no `eu/cv/FATOS.yml`, seguindo
   `motor/regras/cv.md` (as quatro lentes, a forma do bullet, com `tags`,
   `lente` e `verificar` quando couber). Escreva o `resumo.base` pelos três
   movimentos. Mostre os bullets para ela aprovar, e ajuste o que ela pedir.
7. **Variante base.** Copie `motor/modelos/variante.yml` para
   `eu/cv/variantes/base-pt.yml`, com `arquivo:` formado pelo nome dela sem
   acento, com hífens no lugar dos espaços, seguido de `-CV-PT`, e com todos os
   bullets aprovados na ordem da linha do tempo, menos os marcados
   `verificar: true`. Se o público dela é em inglês,
   crie também `base-en.yml` com `idioma: en` e `arquivo:` terminando em
   `-CV-EN`.

## Parte 2: Voz

1. Peça **dois ou três textos que ela escreveu sozinha**, para colegas ou
   amigos: uma mensagem, um email, um post antigo. Explique por quê: texto
   revisado por outra pessoa, ou escrito em tom de documento oficial, não
   mostra como ela escreve. Antes de ela colar, avise que nome e detalhe de
   terceiros (paciente, cliente, aluno, colega) e telefone ou email de outras
   pessoas saem do texto, e a assinatura dela também (email e telefone dela
   moram só no `contato.yml`). Se algo assim vier mesmo assim, guarde o texto com o
   trecho trocado por uma descrição em palavras, como "o paciente do leito",
   sem colchete.
2. Analise nos textos: como cumprimenta, se fala em primeira pessoa e como
   trata o leitor, tamanho e ritmo das frases, pontuação característica,
   expressões que são dela, humor, o que ela evita.
3. Pergunte, uma por vez: que tipo de post de LinkedIn você detesta ler? Que
   palavra você nunca usaria? Respostas de entrevista (desta parte ou da Parte
   0) podem confirmar um traço que apareceu nos textos, mas não criam um traço
   sozinhas; a exceção são os proibidos, que ela declara.
4. Guarde os textos colados, inteiros, e as respostas brutas em `## Voz` do
   `eu/MATERIA-PRIMA.md`. Grave a análise em `eu/VOZ.md`: `## Tom`,
   `## Estrutura que ela usa`,
   `## Proibidos pessoais` e `## Ortografia`. **Cada traço com uma citação
   curta de um texto dela**, como prova.
5. Mostre o resumo e confirme.

A voz sai dos textos dela, e não das respostas da entrevista: ninguém responde
entrevista no mesmo tom em que escreve para os colegas.

## Parte 3: Perfil

Leia `motor/regras/linkedin.md` antes.

1. **Headline:** proponha duas ou três opções no idioma do público dela, cada
   uma com a razão em uma linha. Registre a escolhida e as descartadas, com a
   razão.
2. **Sobre (About):** curto, com as duas primeiras linhas carregando o
   diferencial, e não a biografia. Se o perfil é num idioma diferente da
   língua dela, escreva primeiro na língua dela (o rascunho-fonte) e traduza a
   partir dele.
3. **Experiências:** a descrição de cada uma, a partir dos bullets aprovados.
4. **Onde cada coisa vai:** a tabela dela.
5. **Configuração:** os lembretes da seção "Configuração, não texto", como
   caixas para ela marcar. Uma delas pede decisão: os cargos que ela procura,
   que vão no "Open to Work" só para recrutadores. Pergunte, e grave os cargos
   na própria caixa. Eles nunca entram no texto do perfil.

Todo texto que vai ser colado fica **sem quebra de linha dentro do parágrafo**.
Grave em `eu/PERFIL.md`, com as decisões. Crie também
`eu/PERFIL-PARA-COLAR.txt`, só com o que vai para o LinkedIn: headline, Sobre
e a descrição de cada experiência, cada bloco com um rótulo de uma linha, sem
decisões nem comentários. É dele que ela copia.

## Parte 4: Primeiro post

1. Siga os passos de `.claude/skills/escrever-post/SKILL.md`, com uma história
   de `## O que ainda rende post`. O post tem o commit dele (passo 9 daquela
   skill), e o fechamento da Parte 4 tem outro, depois da cadência.
2. Pergunte quantos posts por semana ela consegue manter sem virar obrigação, e
   em que dias. Grave em `## Cadência` do `eu/VOZ.md`.
3. Explique o ciclo: depois de publicar, ela roda `/registrar-aprendizado` e
   cola o texto que foi ao ar. É isso que faz o kit aprender o jeito dela.

## Fim

Quando a Parte 4 estiver feita, resuma em três linhas o que existe agora,
ofereça salvar tudo no GitHub (ver "Salvar fora do computador" no
`CLAUDE.md`) e mostre os comandos:

| Comando | Quando usar |
|---|---|
| `/escrever-post` | Quando quiser postar. |
| `/registrar-aprendizado` | Depois de publicar. |
| `/montar-cv` | Quando for se candidatar a uma vaga. |
| `/comecar fatos` | Quando mudar de emprego ou fizer um curso. |
| `/atualizar` | Quando avisarem que saiu versão nova do kit. |
