---
name: atualizar
description: Use quando a pessoa pedir para atualizar o kit, disser que saiu versão nova, ou digitar /atualizar. Troca o motor pela versão mais nova sem tocar em eu/, e mostra o que mudou.
---

# Atualizar o kit

Traz as melhorias do kit para esta cópia. Só o motor muda (`CLAUDE.md`,
`README.md`, `.gitignore`, `.claude/skills/` e `motor/`); a pasta `eu/` fica
intacta.

## Passos

1. **Situar**, em uma frase: vou buscar a versão nova do kit; só as regras e os
   comandos mudam, e nada da pasta `eu/` é tocado.

2. **Verificar.** Rode `python3 motor/atualizar.py verificar` e aja pela
   primeira linha da saída:

   | Primeira linha | O que fazer |
   |---|---|
   | `ESTADO: atualizado` | Diga que ela já está na versão mais nova e pare. |
   | `ESTADO: sem-origem` | Explique que esta cópia não sabe de onde baixar as atualizações, e que quem passou o kit precisa informar o endereço. Pare. |
   | `ESTADO: erro-rede` | Diga que não deu para falar com a origem do kit e sugira conferir a internet. Pare. |
   | `ESTADO: sem-referencia` | Explique que não foi possível achar a versão de referência, e que trocar o motor às cegas poderia apagar algo dela. Pare e sugira falar com quem passou o kit. |
   | `ESTADO: nao-salvo` | Mostre os arquivos listados e explique que há mudanças não salvas em arquivos do motor. Pergunte se ela quer salvar (commit). Depois de salvar, rode `verificar` de novo: a mudança vai aparecer como edição. |
   | `ESTADO: editado` | Veja o passo 3. |
   | `ESTADO: disponivel` | Diga qual é a versão nova e vá para o passo 4. |

3. **Edições no motor.** Mostre o que foi editado, em linguagem simples (qual
   arquivo, o que mudou). Para cada edição, proponha o texto de uma entrada em
   `eu/EXCECOES.md` que preserve a intenção dela, no formato daquele arquivo.
   Com o ok dela, grave, commite:
   ```bash
   git add eu
   git commit -m "eu: excecoes antes de atualizar" -- eu
   ```
   e rode `python3 motor/atualizar.py aplicar --ignorar-edicoes`.

4. **Aplicar.** Rode `python3 motor/atualizar.py aplicar`. Com
   `ESTADO: aplicado`, resuma as novidades que o script mostrou, em português
   simples, dizendo o que muda para ela no dia a dia.

5. **Sanidade.** Rode `python3 motor/verificar.py` e confirme que saiu `ok`.

Nunca faça push sem ela pedir.
