FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]