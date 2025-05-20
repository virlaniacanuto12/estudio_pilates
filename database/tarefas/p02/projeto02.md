# Tarefa 02 – Funções e Procedimentos

Este documento reúne as descrições e os links dos arquivos SQL criados por cada membro da equipe referentes à Tarefa 02 da disciplina de Projeto de Banco de Dados. Cada membro foi responsável por desenvolver duas funções e dois procedimentos relacionados ao projeto do estúdio de pilates.

---

## 👤 Aron

### 🔧 Função 1: Retorna o nome do plano com maior número de alunos vinculados

Retorna o nome do plano com o maior número de alunos vinculados. A função faz um JOIN entre as tabelas studio_aluno e studio_plano, agrupa pelos planos existentes e seleciona aquele com maior quantidade de alunos associados. Útil para análises de popularidade e marketing.

- [Função 1](projeto02-aronslv-q01.sql)

---

### 🔧 Função 2: Verifica se um aluno está inadimplente (tem conta vencida e não paga)

Verifica se um aluno, identificado por seu CPF, está inadimplente. Um aluno é considerado inadimplente se tiver pelo menos uma conta a receber que esteja vencida e ainda não paga. A função retorna um valor booleano (TRUE ou FALSE) com base nessa condição.

- [Função 2](projeto02-aronslv-q02.sql)

---

### ⚙️ Procedimento 1: Desativa todos os alunos com planos vencidos

Desativa automaticamente todos os alunos cujo plano venceu. O procedimento atualiza a coluna plano_ativo para FALSE na tabela studio_aluno quando a data de vencimento do plano (data_vencimento_plano) for anterior à data atual e o plano ainda estiver ativo. É útil para manter a integridade dos dados e o controle de acesso a serviços.

- [Procedimento 1](projeto02-aronslv-q03.sql)

---

### ⚙️ Procedimento 2: Atualiza status de contas para "pago" com base nos pagamentos existentes

Atualiza o status das contas a receber (studio_contareceber) para 'pago' com base nos registros encontrados na tabela studio_pagamento. Ele verifica quais contas possuem um pagamento associado e marca automaticamente essas contas como quitadas. Garante a sincronização entre os módulos de cobrança e pagamento do sistema.

- [Procedimento 2](projeto02-aronslv-q04.sql)

---

## 👤 Beatriz

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---

## 👤 Eloisa

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---

## 👤 Giovanna

### 🔧 Função 1: Soma dos pagamentos de um plano específico

Esta função recebe o código de um plano como parâmetro e retorna a soma total de todos os pagamentos realizados por alunos vinculados a esse plano. A função realiza junções entre as tabelas `pagamento`, `conta_receber` e `aluno`, considerando o campo `plano_codigo`.

- [Função 1](projeto02-giovanna-melo-q01.sql)

---

### 🔧 Função 2: Número de alunos vinculados a um plano

Esta função retorna a quantidade de alunos que estão atualmente vinculados a um determinado plano. É útil para fins administrativos, como verificar a popularidade de diferentes planos ofertados.

- [Função 2](projeto02-giovanna-melo-q02.sql)

---

### ⚙️ Procedimento 1: Registro de novo pagamento

Este procedimento registra um novo pagamento para uma conta a receber existente. Ele insere os dados do pagamento na tabela `pagamento` e atualiza o status da conta correspondente para `TRUE`, indicando que a conta foi quitada.

- [Procedimento 1](projeto02-giovanna-melo-q03.sql)

---

### ⚙️ Procedimento 2: Cancelamento de plano de um aluno

Este procedimento desativa o plano ativo de um aluno, limpando os campos de vínculo (`plano_codigo`, `data_inicio_plano`, `data_vencimento_plano`) e marcando o plano como inativo (`plano_ativo = FALSE`). É útil em casos de cancelamento ou suspensão do serviço.

- [Procedimento 2](projeto02-giovanna-melo-q04.sql)

---

## 👤 Mariana

### 🔧 Função 1: Calcular Valor Cheio do Plano

Esta função recebe o código de um plano da tabela `studio_plano` e retorna seu valor total. O cálculo é feito multiplicando a quantidade de aulas (`qtd_aulas`) pelo valor individual da aula (`valor_aula`) definidos para o plano. É útil para saber o preço integral de um plano.

- [Função 1](projeto02-maricaico-q01.sql)

---

### 🔧 Função 2: Obter Data de Vencimento do Plano do Aluno

Esta função recebe o CPF de um aluno como parâmetro e retorna a data de vencimento registrada para o plano atualmente associado a esse aluno. É útil para verificações rápidas sobre a validade do plano de um cliente.

- [Função 2](projeto02-maricaico-q02.sql)

---

### ⚙️ Procedimento 1: Registrar Novo Serviço Oferecido

Este procedimento permite cadastrar um novo serviço ou modalidade de aula no estúdio. Ele recebe a modalidade, o nível de dificuldade e uma descrição opcional como parâmetros, e insere um novo registro na tabela `studio_servico`. O nível de dificuldade deve corresponder aos valores pré-definidos ('Iniciante', 'Intermediário', 'Avançado').

- [Procedimento 1](projeto02-maricaico-q03.sql)

---

### ⚙️ Procedimento 2: Alterar Função e Salário de Funcionário

Este procedimento atualiza a função e o salário de um funcionário específico, identificado pelo seu CPF. Recebe o CPF do funcionário, a nova designação da função e o novo valor salarial como parâmetros, e modifica os respectivos campos na tabela `studio_funcionario`. É útil para registrar promoções ou reajustes salariais.

- [Procedimento 2](projeto02-maricaico-q04.sql)

---

## 👤 Virlânia

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---
