# Tarefa 01

Este documento contém os links para os scripts utilizados na tarefa 01, sendo eles de criação e povoamento.

---

## 🗃️ Scripts do Esquema

- [Criação do esquema](create_script.sql)
- [Povoamento do esquema](inserts_script.sql)

---
## Modelo de dados

```mermaid
erDiagram
    ENDERECO ||--o{ PESSOA : possui
    PESSOA ||--|| ALUNO : é
    PESSOA ||--|| FUNCIONARIO : é
    FUNCIONARIO ||--o{ FUNCIONARIO_HORARIOS : possui
    FUNCIONARIO ||--o{ FUNCIONARIO_PERMISSOES : possui
    PLANO ||--o{ ALUNO : assina
    FUNCIONARIO ||--o{ AGENDAMENTO : ministra
    AGENDAMENTO ||--o{ AULA : gera
    AULA ||--o{ AULA_ALUNO : inclui
    AULA ||--o{ AULA_SERVICOS : oferece
    AULA_ALUNO ||--|| ALUNO : participa
    AULA_SERVICOS ||--|| SERVICOS : usa
    ALUNO ||--o{ CONTA_RECEBER : tem
    CONTA_RECEBER ||--o{ PAGAMENTO : recebe

    ENDERECO {
        int id PK
        string rua
        int numero
        string cep
        string bairro
        string cidade
    }

    PESSOA {
        string cpf
        string rg
        string nome
        string telefone
        string email
        date data_nascimento
        boolean status
        int endereco_id FK
    }

    ALUNO {
        string cpf FK
        string profissao
        string historico_saude
        int plano_codigo FK
        date data_inicio_plano
        date data_vencimento_plano
        boolean plano_ativo
        string evolucao
    }

    FUNCIONARIO {
        string cpf FK
        string funcao
        decimal salario
        decimal carga_horaria
        string login
        string senha_hash
        boolean is_admin
        datetime ultimo_acesso
    }

    FUNCIONARIO_HORARIOS {
        string funcionario_cpf FK
        string horario
    }

    FUNCIONARIO_PERMISSOES {
        string funcionario_cpf FK
        string permissao
    }

    PLANO {
        int codigo PK
        string nome
        int qtd_aulas
        decimal valor_aula
        boolean status
        date limite_vigencia
    }

    SERVICOS {
        int codigo PK
        char modalidade
        char niveis_dificuldade
    }

    AGENDAMENTO {
        int codigo PK
        datetime data
        string horario
        string local
        int vagas_totais
        int vagas_disponiveis
        string instrutor_cpf FK
    }

    AULA {
        int codigo PK
        int agendamento_codigo FK
        datetime data
        boolean frequencia
    }

    AULA_ALUNO {
        int aula_codigo FK
        string aluno_cpf FK
    }

    AULA_SERVICOS {
        int aula_codigo FK
        int servicos_codigo FK
    }

    CONTA_RECEBER {
        int codigo PK
        string aluno_cpf FK
        decimal valor
        date vencimento
        boolean status
    }

    PAGAMENTO {
        int codigo PK
        int conta_receber_codigo FK
        datetime data
        string metodo
        decimal valor
        boolean status
    }
```