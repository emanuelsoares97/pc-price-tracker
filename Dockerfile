FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y wget unzip curl gnupg && \
    # Instala Google Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -fy && \
    # Instala ChromeDriver compatível
    CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9.]+' | head -1 | cut -d. -f1) && \
    CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /var/lib/apt/lists/*

# Copia o código do projeto
WORKDIR /app
COPY . .

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta padrão do Render
EXPOSE 10000

# Comando para rodar o app
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"] 