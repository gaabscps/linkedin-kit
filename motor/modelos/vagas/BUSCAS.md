# Buscas de vagas

As buscas que o `/aplicar-vagas` roda, na ordem da tabela: da mais estreita
para a mais larga. Montadas na entrevista (`/comecar vagas`) e medidas no seu
Chrome, logado.

---

## Onde a busca roda

```
https://www.linkedin.com/jobs/search/?keywords=<busca>&f_AL=true&f_WT=<modalidade>&f_TPR=r604800&sortBy=DD
```

| Parâmetro | Papel |
|---|---|
| `f_AL=true` | só vaga de candidatura simplificada, dentro do LinkedIn |
| `f_WT` | modalidade: `1` presencial, `2` remoto, `3` híbrido; mais de uma separadas por `%2C` (vírgula), como `1%2C3` |
| `f_TPR=r604800` | publicadas nos últimos 7 dias |
| `sortBy=DD` | mais recentes primeiro |
| `location` e `distance` | cidade e raio em quilômetros, para presencial e híbrido; confira na medição se os resultados respeitam |

**A busca é booleana, com aspas e AND**, como `"enfermeira" AND "uti"`. Sem
isso, o LinkedIn casa palavra solta e devolve vaga de tudo, e a régua passa a
fazer o trabalho que a busca deveria ter feito.

**Logado, a região vem da conta**, e por isso a busca remota não leva
`location`.

---

## Buscas

<!-- Uma linha por busca, da mais estreita para a mais larga. A URL medida é
a URL inteira, como foi aberta na medição, com a busca, a modalidade e, quando
há, a cidade e o raio: o /aplicar-vagas abre essa URL exatamente como está. A
medição diz a data, quantos resultados vieram e se os títulos batiam com o que
ela procura. Busca que não rende nada em três passadas seguidas sai da
tabela. -->

| # | Busca | URL medida | Medição |
|---|---|---|---|
