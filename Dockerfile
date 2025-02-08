# Usa a imagem oficial do Python como base
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo pyproject.toml e poetry.lock para o contêiner
COPY pyproject.toml poetry.lock* ./

# Instala o Poetry
RUN pip install poetry

# Copia todo o código do projeto para o contêiner
COPY . .

# Adiciona o diretório do projeto ao PYTHONPATH
ENV PYTHONPATH=/app

# Instala as dependências do projeto
RUN poetry install --no-root

# Comando padrão para rodar os testes
CMD ["poetry", "run", "pytest"]