import psycopg2
from faker import Faker

# Configuração da conexão com o PostgreSQL
DB_CONFIG = {
    "host": "dpg-cvmtnt8dl3ps73d7ner0-a.oregon-postgres.render.com",
    "user": "dbt_projeto_user",
    "password": "f6QufNx7NSKerljnBGGPNKF3A7sTivU7",
    "port": "5432",
    "dbname": "dbt_modelos"
    
}

# Criar conexão com o banco
def conectar_banco():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

# Criar tabela (caso não exista)
def criar_tabela():
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_info (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                idade INT,
                cidade VARCHAR(100)
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Gerar dados fictícios
def gerar_dados(qtd=1000):
    fake = Faker("pt_BR")
    dados = [(fake.name(), fake.email(), fake.random_int(min=18, max=80), fake.city()) for _ in range(qtd)]
    return dados

# Inserir dados no banco
def inserir_dados(dados):
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO users_info (nome, email, idade, cidade) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING;"
        cursor.executemany(query, dados)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{len(dados)} registros inseridos com sucesso!")

# Executando os passos
if __name__ == "__main__":
    criar_tabela()
    dados = gerar_dados(1000)  # Gerar 1000 usuários fictícios
    inserir_dados(dados)
