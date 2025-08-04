## importing the stuff I need
import sys
import os

## add the project root to the path, just in case
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.comparador import ComparadorPreco
from utils.csvrecente import obter_csv_mais_recente
from utils.pastascsv import obter_csv_anteriores
from utils.guardarcsv import guardar_csv
from utils.logger_util import get_logger
import pandas as pd
from datetime import datetime

logger = get_logger(__name__)

## main function to compare prices, does the heavy lifting
def main(nome_pesquisa=None, n_dias=5):
    ## pick the right folder, depends if searching by name or not
    if nome_pesquisa:
        pasta = 'data/raw/individual'
    else:
        pasta = 'data/raw/geral'
    todos_ficheiros = [f for f in os.listdir(pasta) if f.endswith('.csv')]
    todos_ficheiros.sort(reverse=True)
    ## get the last n days for the report columns
    ficheiros_ultimos = todos_ficheiros[:n_dias]
    datas_ultimos = [f.split('_')[-1].replace('.csv','') for f in ficheiros_ultimos]

    ## read all the CSVs, just in case
    todos_dfs = [pd.read_csv(os.path.join(pasta, f)) for f in todos_ficheiros]
    dfs_ultimos = [pd.read_csv(os.path.join(pasta, f)) for f in ficheiros_ultimos]

    ## call the comparador, let it do the magic
    df_final = ComparadorPreco.comparar_multidias(dfs_ultimos, datas_ultimos, nome_pesquisa)
    if nome_pesquisa:
        ## clean up the name, no weird characters in the filename
        nome_limpo = ''.join(c for c in nome_pesquisa if c.isalnum() or c in ('-', '_')).replace(' ', '_')
        nome_saida = f"comparacao_multidias_{datas_ultimos[0]}_{nome_limpo}.csv"
    else:
        nome_saida = f"comparacao_multidias_{datas_ultimos[0]}.csv"
    df_final.to_csv(os.path.join('data/reports', nome_saida), index=False)
    logger.info(f'Relatório multidias gerado: {nome_saida}')

## if you run this file directly, just call main and let it roll
if __name__ == "__main__":
    main()
