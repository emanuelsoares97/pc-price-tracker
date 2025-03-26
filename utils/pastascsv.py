import os


caminho_projeto = os.path.dirname(os.path.abspath(__file__))

caminho_csv_diario = os.path.join(caminho_projeto, "..", "data/raw")

caminho_csv_analise = os.path.join(caminho_projeto, "..", "data/reports")
