---
name: registrar-aprendizado
description: Use quando a pessoa disser que publicou um post, colar o texto publicado, ou pedir para o kit aprender com o que ela mudou. Compara o rascunho com o que foi ao ar e grava em eu/VOZ.md o que ela manteve, reescreveu e cortou.
---

# Registrar o aprendizado de um post

O que a pessoa muda no rascunho antes de publicar é a melhor amostra que existe
da voz dela. Esta skill guarda essa diferença, e é por ela que os próximos
rascunhos saem mais perto do jeito dela.

## Passos

Se ela já disse qual post foi e já colou o texto, pule os passos 1 e 2.

1. **Qual post.** Liste os posts de `eu/posts/` cujo `**Status:**` ainda não é
   "publicado", e pergunte qual foi ao ar.

2. **O texto publicado.** Peça que ela cole o texto **exatamente como foi ao
   ar**, copiado do próprio LinkedIn.

3. **Comparar** com o `-PARA-COLAR.txt` daquele post e mostrar numa tabela:

   | Tipo | Rascunho | Publicado |
   |---|---|---|
   | reescrito | o trecho antes | o trecho depois |
   | cortado | o trecho | |
   | acrescentado | | o trecho |

   E, numa linha, o que ela manteve igual.

4. **Fato antes de estilo.** Se um corte ou uma reescrita mexe num fato (um
   número, uma data, algo que deixou de ser verdade), pergunte primeiro. Se o
   fato mudou, corrija em todos os lugares onde ele está: `eu/MATERIA-PRIMA.md`,
   `eu/cv/FATOS.yml`, `eu/PERFIL.md` e as variantes do CV (ver "Auditar os dois
   lados" em `motor/regras/verdade.md`).

5. **Padrão ou caso isolado.** Para cada diferença de estilo, decida se é
   correção pontual (um erro) ou padrão da voz dela (um jeito de abrir, uma
   palavra que ela sempre troca). Pergunte só quando for ambíguo: "isso é
   sempre assim, ou foi só neste post?" Uma mudança de estilo que aparece uma
   vez só, sem ela dizer que é sempre assim, fica na entrada como observação;
   ela vira regra quando aparecer de novo numa entrada anterior de
   `## Aprendizados por post`.

6. **Gravar no `eu/VOZ.md`:**
   - uma entrada datada em `## Aprendizados por post`, com o número do post e
     a tabela resumida;
   - o que for padrão também atualiza a seção certa, com a citação do trecho
     publicado como prova: jeito de falar vai para `## Tom`, ordem das partes
     vai para `## Estrutura que ela usa`, o que ela não diria vai para
     `## Proibidos pessoais`. Nunca o mesmo traço em duas seções;
   - o que ela disser que foi caso isolado fica registrado na entrada como
     exceção daquele post, e **não vira regra**.

7. **Atualizar o post:** `**Status:** publicado em` com a data e o dia da
   semana, a `**Data alvo:**` trocada pela mesma data real, e o texto que ela
   colou em `## Versão publicada`. Se o dia saiu da
   `## Cadência` do `eu/VOZ.md`, diga em uma linha o que isso muda (por
   exemplo, o dia do próximo post que depende deste).

8. **Commitar**, antes de perguntar pelo resultado, para o aprendizado não se
   perder se a conversa parar aqui:
   ```bash
   git add eu
   git commit -m "eu: aprendizado do post 003" -- eu
   ```
   (com o número do post).

9. **Resultado.** Pergunte se aconteceu algo que valha registrar: comentário de
   alguém relevante, mensagem recebida, convite. Resultado costuma chegar dias
   depois: ela pode voltar com `/registrar-aprendizado` só para isso, e aí
   você abre o post já publicado e anota. Anote em `## Resultado` do arquivo
   do post e, se abrir assunto novo, em `## O que ainda rende post` do
   `eu/MATERIA-PRIMA.md`. Se houver comentário a responder, ofereça montar a
   resposta, em tom de conversa e só com fatos de `eu/` (o que ela contar de
   novo vai antes para a matéria-prima). Commite de novo:
   ```bash
   git add eu
   git commit -m "eu: resultado do post 003" -- eu
   ```
