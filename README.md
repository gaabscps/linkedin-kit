# linkedin-kit

Um jeito de manter o seu LinkedIn sem gastar uma hora por post e sem soar como
robô. Você conversa com o Claude, e ele escreve post no seu tom, monta o seu
perfil a partir dos seus fatos e gera um CV sob medida para cada vaga. E ele
fica melhor a cada post, porque registra o que você mudou no rascunho antes de
publicar.

Serve para qualquer profissão. O vocabulário da sua área entra pela entrevista,
com as suas palavras.

---

## O que você precisa

- **Assinatura do Claude** num plano pago (o Claude Code, que roda este kit,
  não está no plano gratuito).
- **O app do Claude no computador**, na aba Code.
- **Uma conta no GitHub**, para ter a sua cópia e receber as atualizações do
  kit.
- **Para o CV em PDF:** Python 3 e Google Chrome. O `/montar-cv` confere se
  eles estão instalados e explica como instalar o que faltar.

---

## Como começar

1. No GitHub, abra a página deste kit e clique em **Use this template**.
   Escolha um nome para a sua cópia e marque **Private**. Isso é importante:
   você vai contar a sua trajetória aqui.
2. Baixe a sua cópia para o computador. O jeito mais simples é o GitHub
   Desktop, com a opção "Clone".
3. Abra a pasta no app do Claude, na aba Code.
4. Digite `/comecar`.

A entrevista leva de 1 a 2 horas e pode ser feita em partes: dá para parar e
voltar outro dia. Dá para fazer sozinha ou com alguém do lado conduzindo; o
caminho é o mesmo.

---

## Os comandos

| Comando | Quando usar |
|---|---|
| `/comecar` | Na primeira vez, e para refazer uma parte quando algo mudar (`/comecar fatos` depois de um emprego novo, por exemplo). |
| `/escrever-post` | Quando quiser postar. |
| `/registrar-aprendizado` | Depois de publicar: você cola o que foi ao ar e o kit aprende com o que você mudou. |
| `/montar-cv` | Quando for se candidatar: você cola a vaga e sai o PDF. |
| `/atualizar` | Quando avisarem que saiu versão nova do kit. |

---

## Onde mexer

- **A pasta `eu/` é sua.** Tudo o que é seu mora ali, e nenhuma atualização
  mexe nela.
- **Não edite o motor:** `CLAUDE.md`, `README.md`, `.gitignore`,
  `.claude/skills/` e `motor/`. A próxima atualização apagaria a sua mudança.
- **Discorda de uma regra?** Peça ao Claude para registrar a exceção em
  `eu/EXCECOES.md`. Ela vence a regra do motor, e a atualização não apaga.

---

## Privacidade

- O repositório precisa ser **privado**. O `/comecar` confere isso antes de
  começar.
- Telefone, email e os PDFs do CV ficam **fora do git**, só no seu computador.
- Nenhum documento (CPF, RG, dado bancário, senha) é pedido, em nenhum momento.

---

## Para quem mantém este kit

Se você recebeu melhorias de uso (uma regra nova do LinkedIn, um jeito melhor
de perguntar) e quer passá-las adiante:

1. **Porte a regra à mão**, julgando o que vale para todo mundo e o que é gosto
   de uma pessoa só. Gosto pessoal não entra no motor.
2. **Confira antes de publicar:**
   ```bash
   python3 -m unittest discover -s motor/testes
   python3 motor/verificar.py --template
   ```
   E confira que nenhum dado seu (nome, contato, empresas) entrou em nenhum
   arquivo.
3. **Suba a versão** em `motor/VERSAO` e escreva a entrada nova no topo de
   `motor/NOVIDADES.md`, em português simples, dizendo o que muda para quem usa.
4. **Commite e crie a tag** com o mesmo número: `git tag v1.1.0`. Sem a tag, o
   `/atualizar` das cópias não tem com o que comparar.
5. **Publique** os commits e depois a tag: `git push` e em seguida
   `git push --tags`.

Na primeira publicação, antes da primeira tag: preencha `motor/ORIGEM` com o
endereço do repositório no GitHub (é de lá que as cópias baixam as
atualizações) e marque o repositório como template nas configurações do GitHub.
