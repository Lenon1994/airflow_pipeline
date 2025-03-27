## Execução Airflow

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
- Iniciar o Airflow:
```sh
astro dev start
```
- Parar o projeto:
```sh
astro dev stop
```


## Configurar conexão banco


Acesse o Airflow Web UI

No navegador, vá para: http://localhost:8082 (ou o endereço do seu Airflow)

Vá para "Admin" → "Connections"

No menu superior, clique em "Admin"

Depois, clique em "Connections"

Clique em "+ Add Connection"

Nomeie a conexão como postgres_conn (igual ao código)

Preencha os campos assim:

Exemplo:

| Campo      | Valor                   |
|------------|-------------------------|
| Conn Id    | postgres_conn           |
| Conn Type  | Postgres                |
| Host       | seu_host_do_postgres    |
| Schema     | seu_schema (ex: public) |
| Login      | seu_usuario             |
| Password   | sua_senha               |
| Port       | 5432 (se for padrão)    |

## Dag para teste de conexão

Em "hook" colocar o id da conexão criada do aiflow.
Exemplo: postgres_conn

```sh

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from pendulum import datetime

# Definição da DAG para teste de conexão

with DAG(
    dag_id="test_postgres_connection",
    start_date=datetime(2024, 3, 25),
    schedule=None,  # Execução manual apenas
    catchup=False,
) as dag:

    @task
    def test_connection():
        try:
            # Tenta se conectar ao PostgreSQL
            hook = PostgresHook(postgres_conn_id="postgres_conn")
            conn = hook.get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")  # Executa um teste simples
            result = cursor.fetchone()
            return f"Conexão bem-sucedida! Resultado: {result}"
        except Exception as e:
            return f"Erro na conexão: {str(e)}"

    test_connection()
```

## Execução Airflow com dbt (Dag)

Exemplo de DAG

```sh


import os
from pathlib import Path
from datetime import timedelta
from pendulum import datetime

# Importações do Airflow
from airflow.decorators import dag, task

# Importações do Cosmos para integração com DBT
from cosmos import (
    DbtTaskGroup,     # Grupo de tarefas para executar comandos DBT
    RenderConfig,     # Configuração de renderização para seleção de modelos
    ProjectConfig,    # Configuração do projeto DBT
    ProfileConfig,    # Configuração do perfil DBT
    ExecutionConfig,  # Configuração de execução do DBT
)

# Importação do Cosmos para configuração do Postgres
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.constants import TestBehavior  # Comportamento dos testes DBT

# Definição do caminho do projeto DBT
project_path = "/usr/local/airflow/my_project_dbt"  

# Definição da DAG do Airflow
@dag(
    dag_id="dbt_users_dag",  # Nome único da DAG no Airflow
    start_date=datetime(2024, 3, 25, tz="America/Sao_Paulo"),  # Data de início da DAG com timezone
    schedule_interval="0 * * * *",  # Executa a cada hora (cron schedule)
    tags=["dbt", "produto_a", "daily"],  # Tags para organização no Airflow
    catchup=False,  # Não executa tarefas passadas automaticamente
    max_active_runs=1,  # Limita a DAG para rodar apenas uma instância por vez
    concurrency=4,  # Número máximo de tarefas simultâneas
    default_args={"retries": 3, "retry_delay": timedelta(minutes=2)},  # Configuração de tentativas e atraso
)
def dbt_users_dag():  
    """Define a DAG e suas tarefas."""

    @task
    def init():
        """Tarefa inicial de inicialização, pode ser usada para verificações antes da execução do DBT."""
        return True

    # Configuração do grupo de tarefas DBT no Cosmos
    dbt_run = DbtTaskGroup(
        group_id="dbt_models",  # Identificador do grupo de tarefas no Airflow
        
        # Configuração do perfil DBT
        profile_config=ProfileConfig(
            profile_name="my_project_dbt",      # Nome do perfil definido no profiles.yml do DBT
            target_name="prd",                  # Ambiente de destino que esta configurado no profiles.yml do DBT
            profile_mapping=PostgresUserPasswordProfileMapping(
                conn_id="postgres_conn",  # Conexão PostgreSQL definida no Airflow
                profile_args={"schema": "dbt"},  # Definição do schema usado para as tabelas DBT
            ),
        ),
        
        # Configuração do projeto DBT
        project_config=ProjectConfig(
            project_path  # Caminho do diretório do projeto DBT
        ),

        # Configuração de execução dos modelos DBT
        render_config=RenderConfig(
            select=["tag:produto_a", "tag:daily"],  # Filtros para rodar apenas modelos com essas tags
            test_behavior=TestBehavior.NONE,  # Não executa testes DBT automaticamente
        ),

        # Configuração de execução
        execution_config=ExecutionConfig(
            dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"  # Caminho do executável DBT dentro do Airflow
        ),

        # Argumentos adicionais
        operator_args={"install_deps": True},  # Instala dependências automaticamente
    )

    @task()
    def finish():
        """Tarefa final, pode ser usada para logs ou verificações pós-processamento."""
        return True

    # Define a ordem de execução das tarefas dentro da DAG
    init() >> dbt_run >> finish()


# Instancia a DAG no Airflow
dbt_users_dag()
```