# PC Price Tracker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Sumário
- [Sobre](#sobre)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Como Executar Localmente](#como-executar-localmente)
- [Deploy com Docker (Render, Railway, etc.)](#deploy-com-docker-render-railway-etc)
- [Exemplo de Saída](#exemplo-de-saída)
- [Testes](#testes)
- [Futuras Melhorias](#futuras-melhorias)
- [Licença](#licença)

---

## Sobre

Este projeto faz a busca de preços de computadores gamer no site [Globaldata.pt](https://www.globaldata.pt), salva os dados em arquivos CSV e compara os preços entre diferentes dias. O objetivo é acompanhar a variação de preços de produtos ao longo do tempo de forma simples e visual.

---

## Tecnologias Utilizadas

- Python 3.10+
- Selenium
- WebDriver Manager
- Pandas
- Flask
- Chart.js
- Docker

---

## Estrutura do Projeto

```
pc-price-tracker/
│
├── data/
│   └── raw/                   # Dados crus obtidos via scraping
│   └── reports/               # Relatórios comparativos
│
├── models/
│   └── comparador.py          # Classe ComparadorPreco (análise entre dias)
│
├── scripts/
│   └── comparador_main.py     # Gera relatórios comparando dias
│   └── scraper_main.py        # Script de scraping
│
├── utils/                     # Utilitários
├── static/                    # Arquivos estáticos (CSS, JS)
├── templates/                 # HTML da interface web
├── tests/                     # Testes automatizados
├── Dockerfile                 # Ambiente pronto para deploy
├── requirements.txt           # Dependências Python
├── app.py                     # App Flask principal
└── README.md                  # Este ficheiro
```

---

## Funcionalidades

- Acede ao site da Globaldata e extrai:
  - Nome do produto
  - Preço atual
  - Estado de stock (Pré Reserva / Em Stock / Esgotado)
- Guarda os dados com data/hora em CSV
- Compara automaticamente os preços mais recentes com o dia anterior
- Gera 3 relatórios:
  - Comparação Geral
  - Produtos com aumento de preço
  - Produtos com diminuição de preço
- Interface web simples para visualizar os dados e gráficos
- Página de downloads para baixar os ficheiros gerados

---

## Como Executar Localmente

1. Certifique-se de ter o Python 3.10+ instalado.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o app Flask:
   ```bash
   python app.py
   ```
4. Abra o navegador e aceda a [http://localhost:5000](http://localhost:5000)

---

## Observação importante sobre o scraping

- O scraping deste projeto funciona normalmente **no seu computador**, pois o Chrome abre de forma visível (não headless).
- Em ambientes de deploy na nuvem (como Railway, Render, Heroku, etc.), o Chrome só roda em modo "headless" (sem interface gráfica), porque não existe tela nesses servidores.
- Alguns sites bloqueiam acesso de bots ou browsers em modo headless, então pode ser que o scraping não funcione nesses ambientes cloud.
- Se você quiser testar o scraping, recomendo rodar localmente no seu PC, onde o Chrome vai abrir normalmente e você consegue ver o processo funcionando.

### Como testar o scraping localmente

1. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script de scraping pelo terminal:
   ```bash
   python scripts/scraper_main.py
   ```
3. O Chrome vai abrir na sua tela e você verá o scraping acontecendo.

Se tiver dúvidas ou problemas, veja os comentários no código ou abra uma issue!

---

## Deploy com Docker (Render, Railway, etc.)

O projeto já está pronto para ser executado em qualquer serviço que suporte Docker (ex: Render, Railway, Google Cloud Run, etc.).

### Como fazer deploy:

1. Certifique-se de que o ficheiro `Dockerfile` está na raiz do projeto.
2. Faça commit e push de tudo para o GitHub.
3. No Railway (ou outro serviço que aceite Docker), escolha a opção de deploy pelo Dockerfile.
4. O serviço vai construir a imagem, instalar as dependências e rodar o app automaticamente.
5. A interface web vai funcionar normalmente. O scraping pode não funcionar em cloud se o site bloquear modo headless (veja a observação acima).

### Para executar localmente com Docker:

```bash
# Construir a imagem
docker build -t pc-price-tracker .

# Executar o container
# (Acede ao app em http://localhost:10000)
docker run -p 10000:10000 pc-price-tracker
```

---

## Exemplo de Saída

- Arquivos CSV em `data/raw/` com os preços coletados
- Relatórios em `data/reports/`:
  - `comparacao_geral_YYYY-MM-DD.csv`
  - `precos_aumentaram_YYYY-MM-DD.csv`
  - `precos_diminuiram_YYYY-MM-DD.csv`
- Interface web mostra tabela e gráfico de variação de preços
- Página de downloads com todos os ficheiros gerados

---

## Testes

Para correr os testes:
```bash
pytest tests/
```

---

## Futuras Melhorias

- Agendamento automático com `cron` ou `schedule`
- Melhorar gráficos e filtros na interface web
- Exportar gráficos como imagem

---

## Licença

MIT
