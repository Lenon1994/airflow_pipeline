## Configurações e Instalações

### 1. Instalar o WSL (Windows Subsystem for Linux)
Abra o CMD como Administrador e execute:
```sh
wsl --install
```
Reinicie o PC quando solicitado. Após a reinicialização, abra o Ubuntu e siga as instruções de configuração.

### 2. Instalar o Docker Desktop
🔗 [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 3. Habilitar a integração com WSL
1. Abra o Docker Desktop
2. Vá em **Settings > Resources > WSL Integration**
3. Ative a opção para a sua distribuição Linux (ex: Ubuntu)
4. Reinicie o Docker para garantir que as configurações sejam aplicadas.

### 4. Instalar o Astro CLI
Abra o CMD como Administrador e execute:
```sh
wsl
```
Agora, dentro do Ubuntu (WSL), execute os comandos:
```sh
curl -sSL https://install.astronomer.io | sudo bash
```
Verifique a instalação com:
```sh
astro version
```

## Criar e Configurar o Ambiente

### 5. Criar um ambiente virtual
```sh
python3 -m venv airflow-dbt-env
```
- Ativar o ambiente virtual:
```sh
source airflow-dbt-env/bin/activate
```
- Instalar os pacotes necessários:
```sh
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
pip install dbt-core==1.7.5
pip install protobuf==3.20.3 #Para funcionar a executção dbt
pip install dbt-postgres==1.7.5  # Opcional, se for usar PostgreSQL
```
- Entrar no ambiente criado:
```sh
cd airflow-dbt-env
```

### 6. Inicializar um novo projeto Airflow
```sh
astro dev init
```
Aceitar a criação do novo projeto (**Y**). Isso criará um novo diretório com os arquivos necessários.

### 7. Instalar bibliotecas do arquivo `requirements.txt`
```sh
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```
Para forçar a instalação sem cache (opcional):
```sh
pip install --no-cache-dir -r requirements.txt
```

## Bibliotecas Utilizadas (Opcional)
```sh
requests==2.32.3
xlrd==2.0.1
msoffcrypto-tool==5.4.2
pandas==2.1.4
openpyxl==3.1.5
delta-sharing==1.1.1
Office365-REST-Python-Client==2.5.12
dbt-redshift==1.7.5
sqlfluff==2.3.5
astronomer-cosmos==1.6.0
astronomer-providers[amazon]==1.19.4
apache-airflow-providers-amazon==8.19.0
apache-airflow-providers-airbyte==3.9.0
apache-airflow-providers-slack==8.9.0
apache-airflow-providers-postgres==5.12.0
apache-airflow-providers-google==10.15.0
apache-airflow-providers-imap==3.7.0
google-api-python-client==2.142.0
Unidecode==1.3.8
reportlab==4.2.2
psycopg2-binary==2.9.9
```
Para verificar a instalação:
```sh
pip freeze
```

### 8. Inicializar um novo projeto dbt
```sh
dbt init
```
Após iniciar, é possível alterar o nome da pasta criada.
exemplo: my_project_dbt

### 9. Criar um arquivo `profiles.yml`
Para configuração do dbt com PostgreSQL, siga o exemplo:
🔗 [Documentação Oficial](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup)
```yaml
my_project_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: seu_usuario
      password: sua_senha
      port: 5432
      dbname: seu_banco
      schema: public
      threads: 3

my_project_dbt:
  target: prd
  outputs:
    prd:
      type: postgres
      host: localhost
      user: seu_usuario
      password: sua_senha
      port: 5432
      dbname: seu_banco
      schema: dbt
      threads: 3
```
Após configurar o acesso, teste a conexão do banco com o dbt:
```sh
cd my_project_dbt
```
```sh
dbt debug
```
Saída esperada:
```
Connection test: [OK connection ok]
```

### 10. Criar um Banco de Dados para Testes
🔗 [Render](https://render.com/docs/postgresql)

### 11. Inicializar o Airflow
```sh
astro dev start
```
Acesse a interface do Airflow no navegador:
🔗 [http://localhost:8080](http://localhost:8080)
- **Usuário:** admin
- **Senha:** admin

## Possíveis Erros e Soluções

### Erro de Porta em Uso
Se ao iniciar o Airflow ocorrer o erro:
```
Ports are not available: exposing port TCP 127.0.0.1:5432 -> 127.0.0.1:0
```
Isso indica que a porta já está sendo utilizada por outro programa (geralmente PostgreSQL).

Para verificar a porta em uso:
```sh
netstat -ano | findstr :5432
```
Para identificar o processo que está utilizando a porta:
```sh
tasklist | findstr 6932
```
Para alterar a porta do Airflow, edite o arquivo `config.yaml` dentro de `.astro`:
```yaml
project:
  name: airflow-dbt-env
webserver:
  port: 8081  # Alterado de 8080 para 8081
postgres:
  port: 5435  # Alterado de 5432 para 5435
```
Para finalizar o processo que está utilizando a porta:
```sh
taskkill /PID 6804 /F
```

## Execução no Dia a Dia Após Configuração

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
- Testar conexão dbt (na pasta dbt):
```sh
dbt debug
```

## Vídeos Úteis
- [Introdução ao Airflow e dbt](https://www.youtube.com/watch?v=NWbazIW0XIU&t=6473s) *(44:53 min)*
- [Configuração e Execução do dbt](https://www.youtube.com/watch?v=rBsfUiHoNdc)
- [dbt com Cosmos](https://www.youtube.com/watch?v=BI5HsgviSRQ) *(07:41 min)*
