# Escolhe a imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte para dentro do container
COPY datathon/ ./datathon

# Expõe a porta que a API vai rodar
EXPOSE 8000

# Comando para iniciar a API usando uvicorn
CMD ["uvicorn", "datathon.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]