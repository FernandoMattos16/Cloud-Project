# Usando uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY app/requirements.txt .

# Instala as dependências dentro do contêiner
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da API para o contêiner
COPY . .

# Expõe a porta 8000 (porta padrão do Uvicorn)
EXPOSE 8000

# Comando para rodar o servidor FastAPI quando o contêiner iniciar
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
