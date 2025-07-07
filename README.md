# PC Price Tracker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Sumário
- [Sobre](#sobre)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Como Executar](#como-executar)
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
- Logging
- Jupyter Notebooks (para análise)
- Estrutura modular com POO

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
│
├── utils/
│   └── logger_util.py         # Sistema de logs
│   └── guardarcsv.py          # Função genérica para salvar CSVs
│   └── csvrecente.py          # Encontra os dois arquivos mais recentes
│   └── pastascsv.py           # Criação de pastas se não existirem
│
├── static/                    # Arquivos estáticos (CSS, JS)
├── templates/                 # HTML da interface web
├── tests/                     # Testes automatizados
├── venv/                      # Ambiente virtual
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

---

## Como Executar

1. Clone o repositório
2. Ative o ambiente virtual (opcional, mas recomendado)
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o scraper para coletar dados:
   ```bash
   python scripts/scraper_main.py
   ```
5. Execute o comparador para gerar relatórios:
   ```bash
   python scripts/comparador_main.py
   ```
6. (Opcional) Inicie a interface web:
   ```bash
   python main.py
   ```
7. Abra o navegador e acesse: [http://localhost:5000](http://localhost:5000)

---

## Exemplo de Saída

- Arquivos CSV em `data/raw/` com os preços coletados
- Relatórios em `data/reports/`:
  - `comparacao_geral_YYYY-MM-DD.csv`
  - `precos_aumentaram_YYYY-MM-DD.csv`
  - `precos_diminuiram_YYYY-MM-DD.csv`
- Interface web mostra tabela e gráfico de variação de preços

---

## Testes

Para rodar os testes (exemplo):
```bash
python -m unittest discover tests
```

---

## Futuras Melhorias

- Agendamento automático com `cron` ou `schedule`
- Melhorar gráficos e filtros na interface web
- Exportar gráficos como imagem

---

## Licença

MIT

---

## Deploy no Render.com

1. Suba seu projeto para o GitHub.
2. Crie uma conta em [https://render.com/](https://render.com/).
3. Clique em "New +" > "Web Service".
4. Conecte seu GitHub e escolha o repositório do projeto.
5. Configure:
   - **Environment:** Python 3.x
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Clique em "Create Web Service".
7. Aguarde o deploy. O Render vai te dar uma URL pública.

**Dicas:**
- Certifique-se de que o arquivo `requirements.txt` contém `Flask` e `gunicorn`.
- O arquivo principal deve se chamar `app.py` e conter a variável `app` (como já está).
- Para logs/debug, use o painel do Render.

---
