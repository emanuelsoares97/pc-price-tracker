# PC Price Tracker

Este projeto tem como objetivo fazer a procura de preços de computadores gamer no site [Globaldata.pt](https://www.globaldata.pt), guarda os dados em arquivos CSV e compara os preços entre diferentes dias.

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
│   └── analisescsv/          # Relatórios comparativos
│
├── models/
│   └── comparador.py         # Classe ComparadorPreco (análise entre dias)
│   └── globaldata_scraper.py # (a criar) Classe GlobaldataScraper
│
├── scripts/
│   └── comparador_main.py    # Gera relatórios comparando dias
│   └── globaldata_scraper.py # Script atual de scraping
│
├── utils/
│   └── logger_util.py        # Sistema de logs
│   └── guardarcsv.py         # Função genérica para salvar CSVs
│   └── csvrecente.py         # Encontra os dois arquivos mais recentes
│   └── pastascsv.py          # Criação de pastas se não existirem
│
├── venv/                     # Ambiente virtual
└── README.md                 # Este ficheiro
```

---

## Funcionalidades

- Acede ao site da Globaldata e extrai:
  - Nome do produto
  - Preço atual
  - Estado de stock (Pré Reserva / Em Stock / Esgotado)
- Guarda os dados com timestamp em CSV
- Compara automaticamente os preços mais recentes com o dia anterior
- Gera 3 relatórios:
  - Comparação Geral
  - Produtos com aumento de preço
  - Produtos com diminuição de preço

---

## Como executar

1. Clonar o repositório
2. Ativar o ambiente virtual
3. Instalar dependências:
   ```
   pip install -r requirements.txt
   ```
4. Executar o scraper:
   ```
   python sites/globaldata_scraper.py
   ```
5. Executar o comparador:
   ```
   python scripts/comparador_main.py
   ```

---

## Futuras melhorias

- Agendamento automático com `cron` ou `schedule`
- Geração de gráficos
