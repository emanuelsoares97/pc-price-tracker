import os
from utils.pastascsv import caminho_csv_diario
from datetime import datetime

# aqui ficam funções para encontrar o csv mais recente e o anterior

# devolve o caminho do csv mais recente numa pasta
def obter_csv_mais_recente(pasta):
    ficheiros = [f for f in os.listdir(pasta) if f.endswith('.csv')]
    if not ficheiros:
        return None
    ficheiros.sort(key=lambda x: os.path.getmtime(os.path.join(pasta, x)), reverse=True)
    return os.path.join(pasta, ficheiros[0])

def encontrar_csvs_mais_recentes(pasta= caminho_csv_diario):
    """
    Encontra os dois ficheiros CSV mais recentes na pasta especificada.
    Os arquivos são ordenados por nome (espera-se que contenham datas no nome).
    Retorna os caminhos completos dos dois arquivos mais recentes.
    """
    ficheiros = [f for f in os.listdir(pasta) if f.endswith(".csv")]
    ficheiros.sort(reverse=True)
    if len(ficheiros) < 2:
        raise Exception("É necessário pelo menos dois ficheiros CSV para comparar.")
    
    return os.path.join(pasta, ficheiros[0]), os.path.join(pasta, ficheiros[1])