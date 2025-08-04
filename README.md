# pc price tracker

este projeto serve para acompanhar os preços de computadores gamer na globaldata.pt. faço scraping dos preços, guardo tudo em csv e depois comparo os preços de dias diferentes para ver o que subiu ou desceu. também tem uma interface web simples para veres os dados e fazer download dos ficheiros.

## sobre o projeto

- O scraping só funciona localmente, pois o site bloqueia bots em modo headless (sem janela do navegador)
- O deploy na cloud (Render, Railway etc.) é apenas para consulta dos dados
- Para atualizar os dados na cloud, é necessário fazer scraping local e subir os novos ficheiros

## tecnologias usadas
- Python 3.10+
- Flask
- Pandas
- Selenium
- HTML/CSS/JavaScript
- Docker
- GitHub Actions
- Pytest

## estrutura das pastas
```
pc-price-tracker/
├── .github/workflows      # Workflows CI (GitHub Actions)
├── data/
│   ├── raw/
│   │   ├── geral/         # todos os csvs gerais, um por dia
│   │   ├── individual/    # csvs filtrados por nome (pesquisas)
│   └── reports/           # relatórios das comparações, aumentos, quedas
├── models/                # lógica de comparação de preços
├── notebooks/             # Análises manuais, testes exploratórios
├── scripts/               # scripts de scraping e comparação
├── utils/                 # funções auxiliares
├── static/
│   ├── css/               # estilos da página web
│   └── script/            # js para gráficos, tabelas, pesquisa, etc
├── templates/             # html da página web
├── tests/                 # testes automáticos
├── Dockerfile             # para deploy
├── requirements.txt       # dependências
├── app.py                 # app flask
└── README.md              


## como usar no pc
1. instala o python 3.10 ou superior
2. instala as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. corre o app flask:
   ```bash
   ```
4. abre o navegador e vai a [http://localhost:5000](http://localhost:5000)
   ```bash
   ```
2. os ficheiros csv vão aparecer em `data/raw/` e os relatórios em `data/reports/`
- o scraping só funciona no teu computador, porque o site bloqueia bots em modo headless (sem janela do chrome)
- o deploy cloud serve só para veres os dados, relatórios e gráficos
- se quiseres atualizar os dados, faz o scraping no pc e mete os csvs na pasta certa
---
## deploy na cloud (railway, render, etc)
1. garante que o ficheiro `Dockerfile` está na raiz

```bash
# construir a imagem
docker build -t pc-price-tracker .
# correr o container
docker run -p 10000:10000 pc-price-tracker
```

---

## exemplos de saída
- csvs em `data/raw/` com os preços
- relatórios em `data/reports/`:
  - comparacao_multidias_YYYY-MM-DD.csv
  - precos_aumentaram_YYYY-MM-DD.csv
  - precos_diminuiram_YYYY-MM-DD.csv
- página web mostra tabela e gráfico
- página de downloads com todos os ficheiros

---

## testes
para correr os testes:
```bash
pytest tests/
```

---

## melhorias futuras
- agendar scraping automático
- melhorar gráficos e filtros na web
- exportar gráficos como imagem

---

## licença
mit
