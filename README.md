# pc price tracker

este projeto serve para acompanhar os preços de computadores gamer na globaldata.pt. faço scraping dos preços, guardo tudo em csv e depois comparo os preços de dias diferentes para ver o que subiu ou desceu. também tem uma interface web simples para veres os dados e fazer download dos ficheiros.

---

## sumário
- sobre o projeto
- tecnologias usadas
- estrutura das pastas
- como usar no pc
- deploy na cloud (railway, render, etc)
- exemplos de saída
- testes
- melhorias futuras
- licença

---

## sobre o projeto

- vai buscar os preços dos computadores gamer na globaldata.pt
- guarda os dados em csv (um ficheiro por dia)
- compara os preços de hoje com os de ontem
- gera relatórios: comparação geral, produtos que subiram e produtos que desceram de preço
- tem uma página web para veres os dados e fazer download dos ficheiros

---

## tecnologias usadas
- python 3.10+
- selenium
- pandas
- flask
- chart.js
- docker

---

## estrutura das pastas
```
pc-price-tracker/
├── data/
│   └── raw/         # csvs com os preços de cada dia
│   └── reports/     # relatórios das comparações
├── models/          # lógica de comparação de preços
├── scripts/         # scripts de scraping e comparação
├── utils/           # funções auxiliares
├── static/          # css e js da página web
├── templates/       # html da página web
├── tests/           # testes automáticos
├── Dockerfile       # para deploy
├── requirements.txt # dependências
├── app.py           # app flask
└── README.md        # este ficheiro
```

---

## como usar no pc
1. instala o python 3.10 ou superior
2. instala as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. corre o app flask:
   ```bash
   python app.py
   ```
4. abre o navegador e vai a [http://localhost:5000](http://localhost:5000)

### para fazer scraping e comparar preços
1. corre o script principal:
   ```bash
   python main.py
   ```
2. os ficheiros csv vão aparecer em `data/raw/` e os relatórios em `data/reports/`

---

## atenção ao scraping
- o scraping só funciona no teu computador, porque o site bloqueia bots em modo headless (sem janela do chrome)
- na cloud (railway, render, etc) só dá para correr headless, por isso o scraping não funciona lá
- o deploy cloud serve só para veres os dados, relatórios e gráficos
- se quiseres atualizar os dados, faz o scraping no pc e mete os csvs na pasta certa

---

## deploy na cloud (railway, render, etc)
1. garante que o ficheiro `Dockerfile` está na raiz
2. faz commit e push para o github
3. no railway (ou outro serviço que aceite docker), faz deploy pelo dockerfile
4. o serviço vai construir a imagem e arrancar o app
5. a interface web vai funcionar, mas o scraping não (ver aviso acima)

### para correr localmente com docker
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
  - comparacao_geral_YYYY-MM-DD.csv
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

---

⚠️ atenção: o scraping só funciona localmente, porque o site bloqueia headless e a cloud só deixa correr assim. o deploy cloud é só para veres os dados e relatórios. se quiseres dados novos, faz scraping no pc e mete os csvs na pasta.
