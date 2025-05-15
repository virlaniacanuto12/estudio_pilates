# Documento Lista de User Stories

Documento construído a partir do **Modelo BSI - Doc 004 - Lista de User Stories** que pode ser encontrado no
link: https://docs.google.com/document/d/1Ns2J9KTpLgNOpCZjXJXw_RSCSijTJhUx4zgFhYecEJg/edit?usp=sharing

## Descrição

Este documento descreve os User Stories criados a partir da Lista de Requisitos no [Documento 001 - Documento de Visão](DocumentodeVisão.md). Este documento também pode ser adaptado para descrever Casos de Uso. Modelo de documento baseado nas características do processo easYProcess (YP).

## Histórico de revisões

| Data       | Versão  | Descrição                          | Autor                          |
| :--------- | :-----: | :--------------------------------: | :----------------------------- |
| 28/03/2025 | 0.0.1   | Template e descrição do documento  | Virlânia |
| 01/04/2025 | 0.0.2   | Detalhamento do User Story US01    | Virlânia |
| 01/04/2025 | 0.0.3   | Detalhamento do User Story US02    | Aron     |
| 01/04/2025 | 0.0.4   | Detalhamento do User Story US03    | Giovanna |
| 01/04/2025 | 0.0.5   | Detalhamento do User Story US04    | Giovanna |
| 02/04/2025 | 0.0.6   | Detalhamento do User Story US05    | Eloisa   |
| 02/04/2025 | 0.0.7   | Detalhamento do User Story US06    | Mariana  |
| 02/04/2025 | 0.0.8   | Detalhamento do User Story US07    | Beatriz  |
| 02/04/2025 | 0.0.9   | Detalhamento do User Story US08    | Eloisa   |
| 05/04/2025 | 1.0.0   | Documento completo com o detalhamento de todos os User Stories | Virlânia     |
| 07/04/2025 | 1.0.1   | Adição das informações da equipe: Analista, Desenvolvedor, Revisor e Testador. | Mariana |



### User Story US01 - Manter Aluno

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | No procedimento de cadastro, o funcionário deve acessar o sistema através de login e senha, entrar na aba de cadastro de aluno, e inserir as informações de identificação do aluno: nome, cpf, endereço e data de nascimento; e as informações médicas: exames, indicações, anamnese, etc.                                                                       O funcionário salva as informações no sistema, e aguarda a aprovação do cadastro pelo administrador, para que a matrícula possa ser efetuada. Para realizar a pesquisa, o funcionário deve acessar o sistema através de login e senha, acessar o Banco de Dados na aba consulta, e digitar o cpf que deseja pesquisar e clicar em pesquisar, em seguida, o sistema mostrará as todas as informações referentes ao aluno. No que tange a alteração, o funcionário deve realizar o mesmo procedimento de Pesquisa, e em seguida, digitar as informações nos campos que deseja alterar e salvar no sistema, e a operação ficará pendente de aprovação do administrador.Para efetuar a exclusão, o funcionário deve realizar o mesmo procedimento de Pesquisa, e em seguida, o funcionário seleciona e confirma a exclusão(lógica) do cadastro do aluno. O procedimento fica pendente de aprovação do administrador.|

**Requisitos envolvidos**                                                   
|             |           |  
| ----------- | --------- |
| RF01          | Cadastrar Aluno |
| RF02          | Alterar Aluno  |
| RF03          | Pesquisar Aluno|
| RF04          | Excluir Aluno |

|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Giovanna                            | 
| **Desenvolvedor**         | Aron                                |
| **Revisor**               | Beatriz                             | 
| **Testador**              | Eloisa                              | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA01.01** |O funcionário informa, na tela de Cadastro, os dados do aluno para cadastrá-lo corretamente, ao clicar em Salvar o sistema apresenta uma mensagem de sucesso. Mensagem: Cadastro realizado com sucesso, aguardando aprovação do administrador. |
| **TA01.02** | O funcionário informa, na tela de Cadastro, os dados do aluno para cadastrá-lo incorretamente, ao clicar em Salvar ele é notificado com uma mensagem de erro. Mensagem: Cadastro não realizado, o campo “xxxx” não foi informado corretamente.|
| **TA01.03** | O funcionário informa, na tela de Pesquisa, os dados do aluno para fazer a pesquisa corretamente, ao clicar em Pesquisar o sistema apresenta os dados do aluno pesquisado.|
| **TA01.04** | O funcionário informa, na tela de Pesquisa, os dados do aluno para fazer a pesquisa incorretamente, ao clicar em Pesquisar o sistema apresenta uma mensagem de erro. Mensagem: Cadastro não localizado no sistema.|
| **TA01.05** | O funcionário informa, na tela de pesquisa, os dados do aluno que deseja fazer a alteração, preenche corretamente os dados e ao clicar em Alterar, o sistema apresenta uma mensagem de sucesso. Mensagem: Alteração realizada com sucesso, aguardando aprovação do administrador.|
| **TA01.06** | O funcionário informa, na tela de pesquisa, os dados do aluno que deseja fazer a alteração, ao digitar os dados deixa de preencher um campo obrigatório, e ao clicar em Alterar o sistema apresenta uma mensagem de erro. Mensagem: Alteração não realizada, o campo “xxxx” não foi informado corretamente.|
| **TA01.07** | O funcionário informa corretamente, na tela de pesquisa, os dados do aluno que deseja fazer a exclusão do cadastro, o funcionário seleciona o cadastro, e ao clicar em Excluir o sistema apresenta uma mensagem de sucesso. Mensagem: Cadastro excluído com sucesso, aguardando aprovação do administrador.|
| **TA01.08** | O administrador informa, na tela de pesquisa, os dados do administrador que deseja fazer a exclusão do cadastro, o sistema apresenta uma mensagem de erro. Mensagem: Exclusão não permitida: Não é possível excluir o único administrador cadastrado no sistema. Por favor, cadastre outro administrador antes de realizar esta ação. |

### User Story US02 - Manter Funcionário

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | Para realizar o cadastro, o administrador deve acessar o sistema através de login e senha, entrar na aba de cadastro de funcionário, e inserir as informações de identificação do funcionário: nome, cpf, email, endereço e telefone, informações profissionais e os horários de trabalho. O administrador salva as informações no sistema. Na pesquisa, o administrador deve acessar o sistema através de login e senha, acessar o Banco de Dados na aba consulta, e digitar o cpf/nome do funcionário que deseja pesquisar e clicar em pesquisar, em seguida, o sistema mostrará todas as informações referentes ao aluno. No processo de alteração, o administrador deve realizar o mesmo procedimento de Pesquisa, e em seguida, digitar as informações nos campos que deseja alterar, e então salvar no sistema. Para efetivar a exclusão, o Administrador deve realizar o mesmo procedimento de Pesquisa, e em seguida, selecionar e confirmar a exclusão do cadastro do funcionário.|

**Requisitos envolvidos**                                                    
|             |           |  
| ----------- | --------- |
| RF01          | Cadastrar Funcionário |
| RF02          | Alterar Funcionário  |
| RF03          | Pesquisar Funcionário|
| RF04          | Excluir Funcionário |

|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Mariana                             | 
| **Desenvolvedor**         | Virlânia                            |
| **Revisor**               | Aron                                | 
| **Testador**              | Giovanna                            | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA02.01** | O administrador informa, na tela de Cadastro, os dados do funcionário para cadastrá-lo corretamente, ao clicar em Salvar o sistema apresenta uma mensagem de sucesso. Mensagem: Cadastro realizado com sucesso, aguardando aprovação do administrador. |
| **TA02.02** | O administrador informa, na tela de Cadastro, os dados do funcionário para cadastrá-lo incorretamente, ao clicar em Salvar ele é notificado com uma mensagem de erro. Mensagem: Cadastro não realizado, o campo “xxxx” não foi informado corretamente. |
| **TA02.03** | O administrador informa, na tela de Pesquisa, os dados do funcionário para fazer a pesquisa corretamente, ao clicar em Pesquisar o sistema apresenta os dados do funcionário pesquisado. |
| **TA02.04** | O administrador informa, na tela de Pesquisa, os dados do funcionário para fazer a pesquisa incorretamente, ao clicar em Pesquisar o sistema apresenta uma mensagem de erro. Mensagem: Cadastro não localizado no sistema. |
| **TA02.05** | O administrador informa, na tela de pesquisa, os dados do funcionário que deseja fazer a alteração, preenche corretamente os dados e ao clicar em Alterar, o sistema atualiza os dados do funcionário com sucesso. |
| **TA02.06** | O administrador informa, na tela de pesquisa, os dados do funcionário que deseja fazer a alteração, ao digitar os dados, deixa de preencher um campo obrigatório, e ao clicar em Alterar o sistema apresenta uma mensagem de erro. Mensagem: Alteração não realizada, o campo “xxxx” não foi informado corretamente. |
| **TA02.07** | O administrador informa corretamente, na tela de pesquisa, os dados do funcionário que deseja fazer a exclusão do cadastro, o administrador seleciona o cadastro, e ao clicar em Excluir o sistema exclui o cadastro do funcionário. |
| **TA02.08** | O administrador informa, na tela de Login, os dados incorretos para logar, ao clicar em Entrar ele é notificado com uma mensagem de erro. Mensagem: Dados incorretos, informe os dados novamente. |

### User Story US03 - Manter Serviço

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | O administrador/ funcionário acessa o sistema através de login e senha, e cadastra as informações sobre os serviços oferecidos: nome, tipo, código, perfil dos alunos e máquinas/ objetos utilizados. Em seguida, as informações são salvas no sistema. O administrador/ funcionário acessa a aba de pesquisar serviço, e informa o código/ nome do serviço que deseja pesquisar, o sistema exibe as informações do serviço. O administrador/ funcionário realiza o mesmo procedimento de pesquisa, e edita os campos que deseja alterar, clica em salvar e o sistema atualiza as informações.
O administrador/ funcionário realiza o mesmo procedimento de pesquisa, seleciona o serviço e confirma a exclusão do serviço.|

**Requisitos envolvidos**                                                    
|             |           |  
| ----------- | --------- |
| RF01          | Cadastrar Serviço |
| RF02          | Alterar Serviço  |
| RF03          | Pesquisar Serviço |
| RF04          | Excluir Serviço  |

|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Beatriz                             | 
| **Desenvolvedor**         | Mariana                             |
| **Revisor**               | Eloisa                              | 
| **Testador**              | Aron                                | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA04.01** | O administrador/ funcionário acessa o sistema através de login e senha, acessa a aba Cadastrar serviços, e insere corretamente todas as informações inerentes ao serviço oferecido, clica em Salvar e as informações são salvas no sistema. |
| **TA04.02** | O administrador/ funcionário acessa o sistema através de login e senha, acessa a aba Cadastrar serviços, e insere as informações inerentes ao serviço oferecido, ao clicar em Salvar o sistema detecta incoerência no preenchimento de um ou mais campos, e emite uma mensagem de erro. Mensagem: Erro no(s) tipo(s) de dado(s) “x”, cadastro não realizado. |
| **TA04.03** | O administrador/ funcionário acessa a aba de pesquisar serviço, e informa corretamente o código/ nome do serviço que deseja pesquisar, clica em Pesquisar e o sistema exibe as informações do serviço. |
| **TA04.04** | O administrador/ funcionário acessa a aba de pesquisar serviço, e informa incorretamente o código/ nome do serviço que deseja pesquisar, clica em Pesquisar e o sistema exibe uma mensagem de erro. Mensagem: Serviço não localizado. |
| **TA04.05** | O administrador/ funcionário realiza o mesmo procedimento de pesquisa, e edita os campos que deseja alterar, clica em salvar e o sistema atualiza as informações. |
| **TA04.06** | O administrador/ funcionário realiza o mesmo procedimento de pesquisa, e ao editar os campos, deixa de preencher um campo obrigatório, clica em salvar e o sistema exibe uma mensagem de erro: Cadastro não realizado, o campo “xxxx” não foi informado corretamente |
| **TA04.07** | O administrador/ funcionário realiza o mesmo procedimento de pesquisa, seleciona o serviço e confirma a exclusão do serviço. |
| **TA04.08** | O administrador/ funcionário realiza o mesmo procedimento de pesquisa, seleciona o serviço e quando clica em Confirmar exclusão aparece uma mensagem de erro. Mensagem: Exclusão não permitida: O serviço está vinculado a matrículas ativas. |

### User Story US04 - Registrar Aula

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | O funcionário informa as aulas que ele ministrou e insere as informações essenciais da aula: os alunos presentes, ausentes e os que terão direito a reposição (se for o caso). Registra a evolução de cada aluno. Salva a evolução dos alunos e as horas trabalhadas pelo instrutor.|

**Requisitos envolvidos**                                                    
|             |           |  
| ----------- | --------- |
| RF01          | Registrar Aula |
| RF02          | Alterar Aula |
| RF03          | Pesquisar Aula |

|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Eloisa                              | 
| **Desenvolvedor**         | Giovanna                            |
| **Revisor**               | Virlânia                            | 
| **Testador**              | Beatriz                             | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA05.01** | O administrador/funcionário acessa o campo de registrar aula, seleciona qual aula ele ministrou e insere as informações essenciais da aula. Depois vai para a opção registrar a evolução do aluno, seleciona o aluno para registro e registra sua evolução naquela aula e repete isso para todos os alunos presentes na aula. O funcionário salva o registro e o sistema confirma com a mensagem: aula registrada com sucesso. |
| **TA05.02** | O administrador/funcionário acessa o campo de registrar aula, seleciona qual aula ele ministrou e insere as informações essenciais da aula: funcionário que ministrou a aula, frequência e reposições. Depois vai para a opção registrar a evolução do aluno, e seleciona um aluno ausente para registro e o sistema exibe uma mensagem de erro. Mensagem: aluno não disponível para registro. |
| **TA05.03** | O administrador/ funcionário acessa a aba de pesquisar aula, informa a aula que ele deseja pesquisar com base na modalidade, horário e data e o sistema exibe as informações detalhadas sobre a aula. |
| **TA05.04** | O administrador/funcionário acessa a aba de pesquisar aula, informa a aula que ele deseja pesquisar com base na modalidade, horário e data e o sistema exibe uma mensagem de erro. Mensagem: aula não encontrada. |

### User Story US05 - Agendamento

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | O funcionário/administrador, insere o aluno em um dos horários que estejam disponíveis, a disponibilidade desses horários será definida a partir da quantidade de alunos naquele horário, que tem como limite 5 alunos. Também será possível a alteração de agendamento e o cancelamento do agendamento, liberando consequentemente a vaga para novos agendamentos.|

**Requisitos envolvidos**                                                   
|             |           |  
| ----------- | --------- |
| RF01          | Cadastrar agendamento|
| RF02          | Alterar agendamento |
| RF03          | Pesquisar agendamento |
| RF03          | Cancelar agendamento |


|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Aron                                | 
| **Desenvolvedor**         | Beatriz                             |
| **Revisor**               | Giovanna                            | 
| **Testador**              | Mariana                             | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA07.01** | O administrador/funcionário acessa o sistema na funcionalidade de agendamentos de alunos, seleciona um horário que tenha disponibilidade, seleciona o horário disponível e realiza o agendamento. O sistema confirma o agendamento. |
| **TA07.02** | O administrador/funcionário acessa o sistema na funcionalidade de agendamentos de alunos, seleciona uma data e horário de atendimento e o sistema exibe uma mensagem de erro. Mensagem: horário indisponível. Vagas esgotadas. |
| **TA07.03** | O administrador/funcionário acessa o sistema na funcionalidade de agendamentos de alunos, seleciona uma data de atendimento e pesquisa o aluno que deseja cancelar a aula naquele dia. O sistema confirma o cancelamento e atualiza os alunos agendados para aquela aula. |
| **TA07.04** | O administrador/funcionário acessa o sistema na funcionalidade de agendamentos de alunos, seleciona uma data de atendimento e pesquisa o aluno que deseja cancelar a aula. O sistema exibe uma mensagem de erro: aluno não encontrado. |

### User Story US06 - Registrar pagamento

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | O funcionário/administrador, quando cadastra um aluno em um plano, acaba por gerar uma ou mais contas a receber vinculadas ao aluno. Quando esse, realizar o pagamento de tais, será realizado um registro de pagamento inserindo as informações essenciais, como valor, data e método.|

**Requisitos envolvidos**                                                    
|             |           |  
| ----------- | --------- |
| RF01          | Cadastrar pagamento|
| RF02          | Pesquisar agendamento |

|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Virlânia                            | 
| **Desenvolvedor**         | Eloisa                              |
| **Revisor**               | Mariana                             | 
| **Testador**              | Giovanna                            | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA07.01** | O administrador/funcionário acessa o sistema na funcionalidade de pagamentos, insere o valor, a data e o método do pagamento e salva o pagamento. O sistema confirma que o registro foi salvo com sucesso. |
| **TA07.02** | O administrador/funcionário acessa o sistema na funcionalidade de pagamentos, seleciona uma data de pagamento ou/e um aluno, e acessa os horários disponíveis naquele dia, mas o sistema não encontra nenhum registro para os dados informados, exibindo uma mensagem de aviso. Mensagem: Pagamentos para a data/aluno não encontrados. |

### User Story US07 - Cadastrar Plano 

|               |                                                                |
| ------------- | :------------------------------------------------------------- |
| **Descrição** | O funcionário/administrador, cadastra opções de plano de aulas para o aluno que varia entre as modalidades: 1 dia a 3 dias por semana, tendo as variações de plano mensal, trimestral e semestral. Ao escolher um plano, automaticamente é gerado uma conta a receber vinculada ao aluno. |

**Requisitos envolvidos**                                                    
|             |           |  
| ----------- | --------- |
| RF01          | Cadastrar plano|
| RF02          | Pesquisar plano |
| RF03          | Editar plano |
| RF04          | Excluir plano |


|                           |                                     |
| ------------------------- | ----------------------------------- | 
| **Prioridade**            | Essencial                           | 
| **Estimativa**            | 8 h                                 | 
| **Tempo Gasto (real):**   |                                     | 
| **Tamanho Funcional**     | 7 PF                                | 
| **Analista**              | Beatriz                             | 
| **Desenvolvedor**         | Aron                                |
| **Revisor**               | Virlânia                            | 
| **Testador**              | Eloisa                              | 
|                           |                                     |

**Testes de Aceitação (TA)**
|             |           |  
| ----------- | --------- |
| **Código**      | **Descrição** |
| **TA07.01** | O administrador/funcionário acessa o sistema na funcionalidade de plano, insere o valor, a modalidade do plano(um, dois ou três dias na semana), o tipo do plano(mensal, trimestral ou semestral) e salva as informações de cadastro. O sistema confirma que o cadastro foi salvo com sucesso. |
| **TA07.02** | O administrador/funcionário acessa o sistema na funcionalidade de plano, insere o valor, a modalidade do plano(um, dois ou três dias na semana), o tipo do plano(mensal, trimestral ou semestral) e apertar em salvar mas o sistema apresenta uma mensagem de erro. Mensagem: Já existe um plano com  as mesmas informações que deseja cadastrar.|
| **TA07.03** | O administrador/funcionário acessa o sistema na funcionalidade de plano, seleciona o nome de um plano e o sistema exibe as informações do plano selecionado. |
| **TA07.04** | O administrador/funcionário acessa o sistema na funcionalidade de plano, seleciona o nome de um plano e o sistema exibe uma mensagem de erro. Mensagem de erro: plano não encontrado. |
| **TA07.05** | O administrador/funcionário acessa o sistema na funcionalidade de plano, seleciona o nome do plano que deseja editar, o sistema exibe o plano selecionado e todos os seus campos para serem editados. O usuário edita as informações desejadas, salva as informações editadas e o sistema confirma as alteraçõe salvas. |
| **TA07.06** | O administrador/funcionário acessa o sistema na funcionalidade de plano, seleciona o nome do plano que deseja editar, o sistema exibe o plano selecionado e todos os seus campos para serem editados. O usuário aperta em salvar as informações editadas mas o sistema exibe uma mensagem de erro. Mensagem de erro: você já possui um plano com essas informações. |
| **TA07.07** | O administrador/funcionário acessa o sistema na funcionalidade de plano, seleciona o nome do plano que deseja excluir, o sistema exibe o plano selecionado. O usuário aperta em excluir e o sistema exibe uma mensagem de erro: Mensagem: existe alunos ativos vinculados a este plano.|
| **TA07.08** | O administrador/funcionário acessa o sistema na funcionalidade de plano, seleciona o nome do plano que deseja excluir, o sistema exibe o plano selecionado. O usuário aperta em excluir e o sistema exibe uma mensagem confirmando a exclusão.|
