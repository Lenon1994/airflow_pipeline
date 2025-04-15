
# Integração Airflow + Airbyte com Porta Personalizada 

## 🎯 Objetivo

Executar uma sincronização de dados (sync) do Airbyte a partir de uma DAG no Airflow, utilizando uma porta personalizada (9300) para evitar conflitos com outras aplicações.

---

## 🔧 1. Configuração do Airbyte (Docker Compose)

Altere a porta no arquivo `docker-compose.yaml` do Airbyte para expor a API HTTP em uma porta diferente:

```yaml
services:
  airbyte-server:
    ports:
      - 9300:8000  # Porta externa personalizada (9300)
```

> Isso faz com que o Airbyte seja acessível em `http://localhost:9300`.

---

## 🧪 2. Teste da API do Airbyte (PowerShell)

```powershell
# Codifica as credenciais padrão do Airbyte
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("airbyte:password"))

# Verifica a saúde da API
Invoke-RestMethod -Uri "http://localhost:9300/api/v1/health" -Method GET

# Esperado:
# available
# ---------
#     True
```

---

## 📥 3. Obter o ID da conexão do Airbyte

Você pode listar as conexões existentes via API:

```powershell
Invoke-RestMethod -Uri "http://localhost:9300/api/v1/connections/list" `
  -Method POST `
  -Headers @{
    "Content-Type" = "application/json"
    "Authorization" = "Basic $base64AuthInfo"
  } `
  -Body '{}'
```

Exemplo de resposta (resumido):

```json
{
  "connections": [
    {
      "connectionId": "e4a9c226-81d4-4a39-8548-572b102ad68b",
      "name": "pokeapi_to_postgres"
    }
  ]
}
```

Copie o valor de `connectionId` — ele será usado na DAG do Airflow.

---

## 🔗 4. Criar conexão HTTP no Airflow

No Airflow (via interface ou código), crie uma conexão com os seguintes dados:

- **ID da Conexão**: `airbyte_conn`
- **Tipo**: HTTP
- **Host**: `http://host.docker.internal`
- **Porta**: `9300`
- **Login**: `airbyte`
- **Senha**: `password`

> `host.docker.internal` permite que o container do Airflow se comunique com serviços rodando no host local (válido em Windows/macOS).

---

## 🛠️ 5. DAG de Sincronização Airflow → Airbyte

```python
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='airbyte_sync_pokeapi_to_postgres',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['airbyte'],
) as dag:

    trigger_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id='airbyte_sync_task',
        airbyte_conn_id='airbyte_conn',
        connection_id='e4a9c226-81d4-4a39-8548-572b102ad68b',
        asynchronous=False,
        timeout=3600,
        wait_seconds=10,
    )
```

---

## ✅ Checklist Final

- [x] Airbyte rodando na porta 9300 (`docker-compose.yaml` ajustado).
- [x] Conexão `airbyte_conn` criada no Airflow com `host.docker.internal:9300`.
- [x] `connectionId` da conexão obtido via API.
- [x] DAG do Airflow configurada e funcionando.

---

## 📎 Referências

- [Documentação do Airbyte API](https://docs.airbyte.com/api/)
- [Operadores Airbyte no Airflow](https://airflow.apache.org/docs/apache-airflow-providers-airbyte/stable/operators/index.html)
 