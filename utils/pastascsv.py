import os


caminho_projeto = os.path.dirname(os.path.abspath(__file__))

caminho_csv_diario = os.path.join(caminho_projeto, "..", "data/raw")

caminho_csv_analise = os.path.join(caminho_projeto, "..", "data/reports")

# função para encontrar o csv anterior ao mais recente
def obter_csv_anteriores(pasta, ficheiro_mais_recente):
    """Encontra o CSV anterior ao mais recente na pasta especificada.
    Args:
        pasta (str): Caminho da pasta onde os CSVs estão localizados.
        ficheiro_mais_recente (str): Nome do arquivo mais recente."""
    ficheiros = [f for f in os.listdir(pasta) if f.endswith('.csv')]
    ficheiros = [f for f in ficheiros if os.path.join(pasta, f) != ficheiro_mais_recente]
    if not ficheiros:
        return None
    ficheiros.sort(key=lambda x: os.path.getmtime(os.path.join(pasta, x)), reverse=True)
    return os.path.join(pasta, ficheiros[0])
