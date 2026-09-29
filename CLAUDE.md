# linkedin-kit

Este repositório ajuda uma pessoa, de qualquer profissão, a manter um LinkedIn
que soa como ela: posts no tom dela, perfil montado a partir dos fatos dela, e
CV gerado para cada vaga. Ele fica mais preciso a cada post, porque registra o
que ela muda nos rascunhos.

---

## Antes de qualquer tarefa

Ler, nesta ordem:

1. `motor/regras/verdade.md`, sempre.
2. A regra do tipo de tarefa: `motor/regras/linkedin.md` e
   `motor/regras/escrita.md` para post e perfil; `motor/regras/cv.md` para CV.
3. `eu/EXCECOES.md`, que **vence qualquer regra de `motor/regras/`**. Se uma
   exceção dali contradiz uma regra do motor, vale a exceção.
4. `eu/VOZ.md`.

Se `eu/PROGRESSO.md` não existe, a pessoa ainda não começou. Sugira `/comecar`
e não improvise a entrevista fora da skill.

---

## Motor e conteúdo

O repositório tem duas partes:

- **O motor:** `CLAUDE.md`, `README.md`, `.gitignore`, `.claude/skills/` e
  `motor/`. É trocado inteiro pelo `/atualizar` quando sai versão nova.
- **O conteúdo:** `eu/`. É da pessoa, e nenhuma atualização mexe nele.

**Nunca edite o motor a pedido da pessoa.** Se ela quer mudar uma regra, o
pedido vira uma entrada em `eu/EXCECOES.md`. Explique por quê em uma frase: se
a mudança fosse feita no motor, a próxima atualização apagaria.

Exceção única: quando `eu/` tem só o `LEIA-ME.md` e a pessoa diz que está
mantendo o kit (e não usando), editar o motor é permitido, seguindo a seção
"Para quem mantém este kit" do `README.md`.

---

## Com quem você está falando

Pode ser alguém que nunca programou e nunca abriu um terminal.

- Explique todo termo técnico na primeira vez que ele aparecer, numa frase.
- Rode os comandos no lugar dela e conte o que foi feito, em vez de pedir que
  ela rode.
- Uma pergunta por vez.
- Quando pedir uma decisão, diga em uma linha por que ela importa.

---

## Fala por ditado

A pessoa pode estar falando por voz, com um programa que transcreve. Termo em
inglês chega aportuguesado ("fidibéque" é feedback) e a pontuação some.
Reconstrua o termo e a frase pelo som e pelo contexto, sem pedir para repetir.
Pergunte só quando as duas leituras possíveis levariam a ações diferentes.

---

## Nunca

- **Ler `motor/exemplo/`.** Ele existe para humanos e para teste. Um fato de lá
  poderia acabar no perfil de uma pessoa real.
- **Pedir documento** (CPF, RG, dado bancário, senha). Ver `verdade.md`.
- **Fazer push, criar repositório ou mudar a visibilidade do repositório** sem
  a pessoa pedir com essas palavras.
- **Commitar sem dizer os caminhos**, porque um commit sem caminhos leva junto
  tudo o que estiver preparado, inclusive o que não era para ir.

---

## Git

Commite ao fim de cada parte da entrevista, de cada post e de cada CV, sempre
com os caminhos explícitos:

```bash
git add eu
git commit -m "eu: post 003" -- eu
```

O `.gitignore` já deixa de fora o contato (`eu/cv/contato.yml`) e os PDFs
gerados.
