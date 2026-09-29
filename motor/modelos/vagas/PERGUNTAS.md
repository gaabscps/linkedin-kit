# Perguntas sem resposta

Pauta, e não banco. Cada entrada é uma pergunta de formulário que fez o
`/aplicar-vagas` pular uma vaga, porque a resposta não estava em
`eu/vagas/RESPOSTAS.md`, no `eu/cv/FATOS.yml` nem no `eu/PERFIL.md`, e a rotina
não inventa.

Ao fim de cada passada, as perguntas novas aparecem de uma vez. A resposta vai
para o `eu/vagas/RESPOSTAS.md`, a entrada sai daqui, e aquela pergunta nunca
mais pula uma vaga. Muitas perguntas nas primeiras passadas é o esperado: elas
diminuem sozinhas.

Formato de uma entrada:

```markdown
## AAAA-MM-DD

- **Pergunta literal:** o texto exato do campo, sem reescrever.
  **Vaga:** título, empresa e id.
```

---
