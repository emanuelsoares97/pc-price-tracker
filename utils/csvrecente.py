import os
from utils.pastascsv import caminho_csv_diario

def encontrar_csvs_mais_recentes(pasta= caminho_csv_diario):
    """Encontra os dois ficheiros CSV mais recentes na pasta especificada."""
    ficheiros = [f for f in os.listdir(pasta) if f.endswith(".csv")]
    ficheiros.sort(reverse=True)
    if len(ficheiros) < 2:
        raise Exception("É necessário pelo menos dois ficheiros CSV para comparar.")
    
    return os.path.join(pasta, ficheiros[0]), os.path.join(pasta, ficheiros[1])