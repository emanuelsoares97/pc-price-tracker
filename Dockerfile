FROM python:3.10-slim

# Instala dependências do sistema e Chrome
RUN apt-get update && \
    apt-get install -y \
        wget \
        unzip \
        curl \
        gnupg \
        fonts-liberation \
        libnss3 \
        libxss1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        --no-install-recommends && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -fy && \
    rm ./google-chrome-stable_current_amd64.deb

# Instala ChromeDriver compatível
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9.]+' | head -1) && \
    CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin/google-chrome:${PATH}"

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN which google-chrome || true
RUN google-chrome --version || true
RUN which chromedriver || true
RUN chromedriver --version || true

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
