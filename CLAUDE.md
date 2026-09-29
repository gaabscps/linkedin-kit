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

- As skills e as regras chamam a pessoa de "ela" porque concordam com "a
  pessoa". Ao falar com ela, não deduza gênero pelo nome nem pela profissão:
  use a forma que ela usa para si nas próprias respostas, e, na dúvida, uma
  forma neutra ("que bom que deu certo", e não "obrigada" ou "cansada").
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
- **Fazer push sem o ok dela**, criar repositório ou mudar a visibilidade do
  repositório sem ela pedir com essas palavras. Oferecer o push é permitido
  (ver "Salvar fora do computador").
- **Commitar sem dizer os caminhos**, porque um commit sem caminhos leva junto
  tudo o que estiver preparado, inclusive o que não era para ir.

---

## Git

Commite ao fim de cada parte da entrevista, de cada post e de cada CV, sempre
com os caminhos explícitos. Antes de todo `git add eu`, rode
`git status --short eu` e confira que só entram arquivos esperados: um CV
antigo, um print ou um export de dados salvo em `eu/` não pode entrar.

```bash
git status --short eu
git add eu
git commit -m "eu: post 003" -- eu
```

Regra de ignore pessoal (uma pasta dela que não deve entrar no git) vai em
`eu/.gitignore`, e nunca no `.gitignore` da raiz, que é do motor.

**Salvar fora do computador.** Os commits ficam só no computador dela até
alguém enviar para o GitHub. O que fazer depende de a pasta ter um remote no
GitHub além do `kit` (o `python3 motor/privacidade.py` diz "Sem remote no
GitHub" quando não tem):

- **Com remote:** ao fim de cada parte da entrevista e de cada post, ofereça
  enviar (`git push`, ou o botão "Push origin" do GitHub Desktop). Só envie
  com o ok dela, e só depois de o `privacidade.py` confirmar que o
  repositório é privado.
- **Sem remote:** não ofereça a cada parte nem a cada post. Uma vez só, no fim
  da entrevista, avise que tudo mora só neste computador, e que um computador
  perdido leva junto o trabalho. Se ela quiser uma cópia de segurança, o
  caminho é o GitHub Desktop, com uma conta no GitHub: "Add Local Repository"
  com esta pasta, e depois "Publish repository" com "Keep this code private"
  marcado. Guie o passo a passo; quem clica é ela. Se ela não quiser, não
  volte ao assunto.

O `.gitignore` já deixa de fora o contato (`eu/cv/contato.yml`) e os PDFs
gerados.
