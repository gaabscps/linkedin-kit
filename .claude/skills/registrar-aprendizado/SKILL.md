---
name: registrar-aprendizado
description: Use quando a pessoa disser que publicou um post, colar o texto publicado, ou pedir para o kit aprender com o que ela mudou. Compara o rascunho com o que foi ao ar e grava em eu/VOZ.md o que ela manteve, reescreveu e cortou.
---

# Registrar o aprendizado de um post

O que a pessoa muda no rascunho antes de publicar é a melhor amostra que existe
da voz dela. Esta skill guarda essa diferença, e é por ela que os próximos
rascunhos saem mais perto do jeito dela.

## Passos

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

4. **Padrão ou caso isolado.** Para cada diferença, decida se é correção
   pontual (um erro, um fato ajustado) ou padrão da voz dela (um jeito de abrir,
   uma palavra que ela sempre troca). Pergunte só quando for ambíguo: "isso é
   sempre assim, ou foi só neste post?"

5. **Gravar no `eu/VOZ.md`:**
   - uma entrada datada em `## Aprendizados por post`, com o número do post e
     a tabela resumida;
   - o que for padrão também atualiza `## Tom`, `## Estrutura que ela usa` ou
     `## Proibidos pessoais`, com a citação do trecho publicado como prova;
   - o que ela disser que foi caso isolado fica registrado na entrada como
     exceção daquele post, e **não vira regra**.

6. **Atualizar o post:** `**Status:** publicado em` com a data, e o texto que
   ela colou em `## Versão publicada`.

7. **Resultado.** Pergunte se aconteceu algo que valha registrar: comentário de
   alguém relevante, mensagem recebida, convite. Anote no arquivo do post e,
   se abrir assunto novo, em `## O que ainda rende post` do
   `eu/MATERIA-PRIMA.md`.

8. **Commitar:**
   ```bash
   git add eu
   git commit -m "eu: aprendizado do post 003" -- eu
   ```
   (com o número do post).
