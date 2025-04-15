## Utilização

- Ativar WSL:
```sh
wsl
```
- Ativar o ambiente virtual:
```sh
source airflow-dbt-env/bin/activate
```
- Entrar no ambiente criado:
```sh
cd airflow-dbt-env
```


### DBT

Entrar na pasta dbt:
```sh
cd my_project_dbt
```

### 1. Na pasta "models" criar a estrutura deseja
Exemplo de pastas criadas
models/
│── raw/            # Dados brutos extraídos (equivalente ao raw)
│── staging/        # Padronização, limpeza e tipagem
│── intermediate/   # Transformações intermediárias, enriquecimento
│── marts/          #Modelos finais prontos para análise



### 2. Após a criação das pastas  entrar em "dbt_project.yml" e adicionar a estrutura
```sh
models:
  my_project_dbt:
    raw:
      +schema: raw  #Define o nome do schema que será criado no banco
      +materialized: table
    
    staging:
      +schema: staging
      +materialized: table

    intermediate:
      +schema: intermediate
      +materialized: table

    marts:
      +schema: marts
      +materialized: table

```

Modelos aceitos
- view: Cria uma visão no banco de dados, sem armazenamento físico. Ideal para dados dinâmicos.
- table: Cria uma tabela física, com dados persistidos. Ideal para dados estáticos ou de leitura frequente.
- incremental: Atualiza ou insere apenas novos dados, sem recriar a tabela inteira. Bom para grandes volumes.
- ephemeral: Não armazena dados fisicamente, cria CTEs temporárias. Útil para transformações intermediárias.
- snapshot: Armazena versões históricas dos dados, permitindo auditoria.



### 3. Após realizar procedimentos acima criar os arquivos slq para trabalhar os dados em cada camada
Exemplo:
raw:
arquivo: raw_dbt_users_info.sql
```sh
SELECT * FROM public.users_info  LIMIT 10
```

staging:
arquivo: staging_dbt_users.sql

#Este modelo referência com a raw usando o nome da tabela {{ ref('raw_dbt_users_info') }}
```sh
select *
from {{ ref('raw_dbt_users_info') }}
limit 2
```


### 4. Após executar os processos acima realizar um debug para avaliar se tem erros
Executar no terminal
```sh
dbt debug
```

### 5. Execução dos modelos
#### Rodar um modelo especifico no terminal
Exemplo
```sh
dbt run --models nome_do_modelo
dbt run --models raw.raw_dbt_users_info
```

#### Rodar modelos por zonas
Exemplo
```sh
dbt run --select raw  #isso executa todos os modelos da zona raw
dbt run --select staging  #isso executa todos os modelos da zona staging
```

#### Rodar todos os modelos
```sh
dbt run
```

#### Documentação das tabelas
Dentro de cada pasta "raw", "staging" ,etc...  colocar um arquivo
```sh
schema.yml
```

Dentro deste arquivo **schema.yml** a estrutura para documentação será
```sh
version: 2

models:
  - name: dbt_users_info
    description: "Tabela com informações referente a usuários - dados brutos"
    config:
      tags:
        - produto_a    #tags para rodar os modelos e tambem utilizado como filtro no docs
        - contains_pii
    meta:
      is_pii: true        # Indica que a tabela contém informações pessoais identificáveis
      is_phi: false       # Indica que a tabela não contém informações de saúde protegida
      data_classification: "sensível"
      data_type: "dados_pessoais"

    columns:
      - name: nome
        description: "Nome do usuário"
        type: "text"
        meta:
          is_pii: true
          data_classification: "sensível"

      - name: email
        description: "Email do usuário"
        type: "text"
        meta:
          is_pii: true
          data_classification: "sensível"

      - name: idade
        description: "Idade do usuário"
        type: "int"
        meta:
          is_pii: false
          data_classification: "sensível"

      - name: cidade
        description: "Cidade do usuário"
        type: "text"
        meta:
          is_pii: false
          data_classification: "sensível"

```
### Gerar documentação das tabelas
```sh
dbt docs generate
```

Visualizar a documentação
```sh
dbt docs serve --port 9000
```

Isso iniciará um servidor local (geralmente em http://localhost:9000), onde você pode navegar pela documentação do seu projeto dbt.



