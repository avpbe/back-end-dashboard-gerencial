# Define a imagem base do Python
FROM python:3.8-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia primeiro o requirements.txt para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte da aplicação para o container
COPY . .

# Expõe a porta em que o Flask roda
EXPOSE 5000

# Executa a aplicação via comando flask run conforme o README
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]