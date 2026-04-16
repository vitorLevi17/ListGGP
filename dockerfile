# Usa uma imagem oficial do Python (que é baseada em Linux)
FROM python:3.12-slim

# Define a pasta de trabalho lá dentro
WORKDIR /app

# Copia e instala as bibliotecas (Certifique-se de que 'gunicorn' está no seu requirements.txt)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o resto do seu projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# O COMANDO MÁGICO: Liga o Gunicorn apontando para o seu wsgi.py
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]