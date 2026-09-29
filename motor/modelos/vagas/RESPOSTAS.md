# Respostas de formulário

As respostas que o `/aplicar-vagas` usa nos formulários de candidatura. Cada
uma vale para todas as vagas, até você mudar. Preenchidas na entrevista
(`/comecar vagas`) e completadas a cada passada: toda pergunta que pula uma
vaga vai para o `eu/vagas/PERGUNTAS.md`, e a sua resposta entra aqui.

Os textos são base: quando a vaga pedir algo específico, a rotina adapta a
partir daqui, sem começar da página em branco e sem inventar nada.

---

## Pretensão salarial

- **A vaga publicou faixa:** a pretensão é a média da faixa.
- **Não publicou:** o valor base abaixo.
- **Campo numérico:** só o número, sem moeda nem texto. Muitos campos recusam
  qualquer outra coisa.

<!-- Valor base mensal, valor por hora (se ela quiser um), e o regime que ela
aceita: CLT, PJ ou os dois. -->

## Qual CV anexar

**Pelo idioma de trabalho da vaga, e não pelo idioma do formulário.** O
formulário pode estar em inglês só porque o sistema da empresa é estrangeiro;
o que decide é o texto da vaga e se ela pede o idioma no dia a dia.

<!-- Uma linha por idioma: o PDF gerado pelo /montar-cv em eu/cv/out/, e o
nome do arquivo como ele aparece na lista de currículos do LinkedIn. -->

## Fale um pouco sobre você

<!-- Um parágrafo curto, derivado do resumo do eu/cv/FATOS.yml, com o número
de caracteres. Uma versão por idioma do público dela. -->

## Quer destacar mais alguma coisa

<!-- O que o CV não mostra bem, em poucas linhas. Campo opcional em branco é
lido como desinteresse, por isso ele tem resposta. -->

## Disponibilidade

<!-- Quando pode começar, modalidade, horário, se aceita mudar de cidade e se
pode viajar. -->

## Informações complementares

<!-- Perguntas comuns em formulário brasileiro: carteira de motorista,
veículo próprio. Só o que ela quiser responder. -->

## Diversidade

Preencher ou não é decisão sua. Se não quiser, a rotina escolhe "prefiro não
informar" quando a opção existe, e deixa em branco o campo opcional que não
tem essa opção.

<!-- A decisão dela e, se ela quiser preencher, as respostas. -->

## Consentimentos

<!-- As duas decisões dela: marcar a caixa obrigatória de aceite da política
de privacidade da empresa (sem ela, a candidatura não é enviada) e, se ela
respondeu diversidade, o consentimento de dados sensíveis. -->

## Formação

<!-- Curso, situação (completo, incompleto, cursando), instituição com o nome
igual ao do perfil do LinkedIn, e ano de conclusão. Coeficiente de curso
incompleto é "não se aplica". -->

## Idiomas

Nível honesto, e nunca um degrau acima: "fluente" num formulário vira
entrevista naquele idioma na conversa seguinte.

<!-- Um idioma por linha, com o nível nas escalas que aparecem (básico,
intermediário, avançado, fluente; e a do LinkedIn: None, Conversational,
Professional, Native or bilingual). -->

## Situação atual

<!-- Se está empregada no momento e o que responder no campo "empresa
atual". -->

## Por que esta empresa

Não tem texto pronto, de propósito: resposta genérica serve para qualquer
empresa, e quem lê percebe. A rotina escreve a partir do que a vaga descreve,
ligado a um fato do seu `eu/cv/FATOS.yml`, sem elogio. Se a vaga não der
material, a vaga é pulada.

## Perguntas de triagem

Perguntas que as empresas escrevem no formulário, com a resposta dela. **Anos
de experiência só saem daqui**, um número por competência, confirmado por ela:
a rotina nunca calcula durante a passada.

| Pergunta | Resposta |
|---|---|

## Dados que se repetem

<!-- Nome completo, nome usado, cidade e links. -->

**Email e telefone não moram aqui.** O formulário do LinkedIn já traz os da
conta; se um formulário pedir, eles estão no `eu/cv/contato.yml`, que fica fora
do git. Data de nascimento também não: se ela quiser que a rotina preencha,
ela mora no `eu/cv/contato.yml`, no campo `nascimento`. Sem ela, a vaga que
pedir é pulada.

**Documento nunca**, pela seção de mesmo nome do `motor/regras/verdade.md`.
