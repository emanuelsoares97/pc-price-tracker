# importo as bibliotecas que vou usar
import sys
import os

# adiciono o diretório raiz do projeto ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.comparador import ComparadorPreco
from utils.csvrecente import obter_csv_mais_recente
from utils.pastascsv import obter_csv_anteriores
from utils.guardarcsv import guardar_csv
from utils.logger_util import get_logger
import pandas as pd
from datetime import datetime

logger = get_logger(__name__)

# função principal para comparar preços
def main():
    # aqui vou buscar o csv mais recente
    caminho_hoje = obter_csv_mais_recente('data/raw')
    # aqui vou buscar o csv anterior
    caminho_ontem = obter_csv_anteriores('data/raw', caminho_hoje)

    if not caminho_hoje or not caminho_ontem:
        logger.warning('não há ficheiros suficientes para comparar preços')
        return

    # leio os ficheiros csv
    df_hoje = pd.read_csv(caminho_hoje)
    df_ontem = pd.read_csv(caminho_ontem)

    # crio o comparador de preços
    comparador = ComparadorPreco(df_hoje, df_ontem)

    # gero os relatórios
    comparador.gerar_relatorio_comparacao_geral()
    comparador.gerar_relatorio_precos_aumentaram()
    comparador.gerar_relatorio_precos_diminuiram()

    logger.info('relatórios gerados com sucesso')

# se correr este ficheiro diretamente, chama a função main
if __name__ == "__main__":
    main()
