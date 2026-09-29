---
name: escrever-post
description: Use quando a pessoa quiser escrever, rascunhar ou revisar um post do LinkedIn. Escreve no tom de eu/VOZ.md, confere contra as regras do motor e grava o post com o arquivo para colar.
---

# Escrever um post

Do assunto ao arquivo pronto para colar, no tom da pessoa.

## Passos

1. **Ler**, nesta ordem: `motor/regras/verdade.md`, `motor/regras/escrita.md`,
   `motor/regras/linkedin.md`, `eu/EXCECOES.md` (vence as regras),
   `eu/VOZ.md`, `eu/MATERIA-PRIMA.md`, e os três posts mais recentes de
   `eu/posts/`. Os posts servem para não repetir assunto e para achar o próximo
   número.

2. **Pauta.** Se a pessoa trouxe o assunto, use. Se não, sugira duas ou três
   pautas de `## O que ainda rende post`, cada uma com uma linha dizendo por
   que rende.

3. **Peso e idioma.** Pergunte se o post é pesado (vitrine do trabalho, pode ter
   imagem) ou leve (curto, um detalhe só). O idioma sai da seção `## Idioma` do
   `eu/VOZ.md` para aquele peso.

4. **Fatos que faltam.** Se a pauta precisa de um fato que não está em `eu/`,
   pergunte antes de escrever, uma pergunta por vez, e grave a resposta do jeito
   que ela falou em `eu/MATERIA-PRIMA.md`.

5. **Rascunho.** Escreva na língua em que a pessoa pensa, no tom de `## Tom` e
   na ordem de `## Estrutura que ela usa`. Se o post sai em outra língua,
   traduza perto do literal, pela seção "Idioma dos posts" de
   `motor/regras/escrita.md`.

6. **Conferir, e mostrar o resultado de cada item:**
   - **Tamanho:** grave o texto num arquivo temporário e conte com `wc -w`.
     Teto de 250 palavras.
   - **Corte do "ver mais":** mostre os primeiros 210 caracteres e confirme que
     eles se sustentam sozinhos.
   - **Nada da seção "O que denuncia texto de IA ou de copywriter"** de
     `motor/regras/escrita.md`, nem dos `## Proibidos pessoais` do `eu/VOZ.md`,
     a não ser o que o `eu/EXCECOES.md` liberar.
   - **Nenhum travessão nem meia-risca**: procure os dois caracteres com
     `grep` no texto.
   - **Todo fato tem origem**: liste cada fato do post com o arquivo de `eu/`
     de onde ele veio. Fato sem origem sai do texto ou vira pergunta.

7. **Gravar.** Descubra o próximo número (três dígitos, sequencial, contando
   os posts que já existem em `eu/posts/`) e um nome curto do assunto, sem
   acento e com hífens. Copie `motor/modelos/post.md` para
   `eu/posts/NNN-assunto.md`, preencha o cabeçalho e as seções `## Texto`,
   `## Correções feitas` e `## Decisões`. Crie ao lado
   `eu/posts/NNN-assunto-PARA-COLAR.txt`, pela seção "Formato na hora de
   colar" de `motor/regras/linkedin.md`: um parágrafo por linha, linha em
   branco entre parágrafos, só o corpo.

8. **Mostrar e ajustar.** Mostre o texto e pergunte o que ela mudaria. Aplique
   o que ela pedir no `.md` e no `.txt`, e confira de novo o passo 6.

9. **Commitar** e lembrar do próximo passo:
   ```bash
   git add eu
   git commit -m "eu: post 003" -- eu
   ```
   (com o número do post). Diga que, depois de publicar, ela roda
   `/registrar-aprendizado` e cola o texto que foi ao ar.
