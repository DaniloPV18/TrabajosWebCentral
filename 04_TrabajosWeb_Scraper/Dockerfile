# 1. Usamos Python 3.11-slim
FROM python:3.11-slim

# 2. Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    --no-install-recommends

# 3. Descargar e instalar Google Chrome de forma directa (Método más estable)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# 4. Configurar directorio de trabajo
WORKDIR /app

# 5. Instalar librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código del proyecto
COPY . .

# 7. Comando para ejecutar
CMD ["python", "scraper.py"]