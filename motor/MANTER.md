# Para quem mantém este kit

Este arquivo é para quem publica as versões do kit. Quem só usa o kit não
precisa ler: o que importa para o uso está no `README.md`.

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
   `/atualizar` das cópias não tem com o que comparar. Todo push para o `main`
   vai junto com versão nova, `NOVIDADES.md` e tag: uma cópia criada de um
   `main` que mudou sem subir a versão enxerga a mudança como edição dela.
5. **Publique** os commits e depois a tag: `git push` e em seguida
   `git push --tags`.

Na primeira publicação, antes da primeira tag: preencha `motor/ORIGEM` com o
endereço do repositório no GitHub (é de lá que as cópias baixam as
atualizações) e marque o repositório como template nas configurações do GitHub.

Um caminho novo no motor (acrescentado em `motor/kit.py`) só é conhecido pelo
script novo. Uma cópia que atualiza com o script antigo fica sem o arquivo
novo, e o `/atualizar` seguinte, já com o script novo, completa o que falta.
Por isso a entrada do `NOVIDADES.md` dessa versão pede para rodar
`/atualizar` duas vezes.

Não rode `/comecar` na pasta de manutenção: ele trocaria o nome do seu remote
`origin` para `kit`, como faz com quem clona o template. Para desfazer:
`git remote rename kit origin`.

## As imagens do README

Ficam em `motor/imagens/`. A capa (`capa.png`) e a ilustração das vagas
(`vagas.png`) são geradas fora do kit. O `cv-exemplo.png` é a primeira página
do CV da pessoa fictícia de `motor/exemplo/`, e precisa ser refeito quando o
modelo do CV mudar:

```bash
qlmanage -t -s 1600 -o motor/imagens motor/exemplo/cv/out/Marina-Lopes-Teixeira-CV-Hospital-Horizonte.pdf
mv motor/imagens/Marina-Lopes-Teixeira-CV-Hospital-Horizonte.pdf.png motor/imagens/cv-exemplo.png
```
