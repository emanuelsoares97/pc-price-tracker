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

# Instala ChromeDriver universal (compatível com Chrome 115+)
RUN set -ex \
    && export CHROME_VERSION=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])") \
    && wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

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

CMD ["gunicorn", "-b", "0.0.0.0:10000", "-w", "1", "app:app"]