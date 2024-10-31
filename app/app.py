from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
import bcrypt
from app.classes import *
from app.functions import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_in_threadpool(criar_tabela_usuarios)
    yield 

app = FastAPI(lifespan=lifespan)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# Endpoint /registrar
@app.post("/registrar")
def registrar_usuario(user: UserRegister):
    if email_existe(user.email):
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    senha_hash = bcrypt.hashpw(user.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    salvar_usuario(user.nome, user.email, senha_hash)
    token = gerar_jwt(user.model_dump())
    return {"jwt": token}

# Endpoint /login
@app.post("/login")
def login_usuario(login: UserLogin):
    usuario = buscar_usuario_por_email(login.email)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    senha_valida = bcrypt.checkpw(login.senha.encode('utf-8'), usuario["senha"].encode('utf-8'))
    if not senha_valida:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = gerar_jwt({"nome": usuario["nome"], "email": usuario["email"]})
    return {"jwt": token}

def verificar_jwt(token: str = Depends(api_key_header)):
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token inválido ou ausente")
    token = token[7:]  # Remove "Bearer " do início
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

# Endpoint /consultar
@app.get("/consultar")
def consultar_dados(token: str = Depends(verificar_jwt)):
    dados = get_data_yfinance()   
    return dados
