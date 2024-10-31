import jwt
import datetime
import psycopg2
from dotenv import load_dotenv
import os
import yfinance as yf

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('POSTGRES_DB')
DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')

def conectar_banco():
    return psycopg2.connect(
        host=DATABASE_HOST,  
        database=DATABASE_NAME, 
        user=DATABASE_USER,  
        password=DATABASE_PASSWORD  
    )

def criar_tabela_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def gerar_jwt(dados_usuario):
    payload = {
        "nome": dados_usuario["nome"],
        "email": dados_usuario["email"],
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def email_existe(email: str):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def salvar_usuario(nome: str, email: str, senha_hash: str):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
        (nome, email, senha_hash)
    )
    conn.commit()
    cursor.close()
    conn.close()

def buscar_usuario_por_email(email: str):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, senha FROM usuarios WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return {"nome": result[0], "email": result[1], "senha": result[2]}
    return None

def get_data_yfinance():
    # Baixa dados de cotação do USD/BRL para os últimos 10 dias
    ticker = "NVDA"
    data = yf.download(ticker, period="5d", interval="1d")
    

    # Organiza os dados em formato de lista de dicionários, extraindo o valor numérico dos pd.Series
    info_data = []
    for index, row in data.iterrows():
        info_data.append({
            "Date": index.strftime("%Y-%m-%d"),
            "Open": row["Open"].values[0] if hasattr(row["Open"], 'values') else row["Open"],
            "High": row["High"].values[0] if hasattr(row["High"], 'values') else row["High"],
            "Low": row["Low"].values[0] if hasattr(row["Low"], 'values') else row["Low"],
            "Close": row["Close"].values[0] if hasattr(row["Close"], 'values') else row["Close"],
            "Volume": row["Volume"].values[0] if hasattr(row["Volume"], 'values') else row["Volume"]
        })

    return info_data