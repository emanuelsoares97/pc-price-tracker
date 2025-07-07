import sys
import os

# diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas as pd
from models.comparador import ComparadorPreco
from utils.csvrecente import encontrar_csvs_mais_recentes
from utils.guardarcsv import guardar_csv
from utils.logger_util import get_logger

logger= get_logger(__name__)

def main():
    """
    Função principal que compara os preços dos dois arquivos CSV mais recentes e gera relatórios.
    Passos:
    1. Encontra os dois arquivos CSV mais recentes.
    2. Carrega os dados em DataFrames.
    3. Compara os preços usando a classe ComparadorPreco.
    4. Gera e salva relatórios de comparação.
    """
    try:
        # encontrar os ficheiros mais recentes
        caminho_hoje, caminho_ontem = encontrar_csvs_mais_recentes()

        # carregar os ficheiros em DataFrames
        df_hoje = pd.read_csv(caminho_hoje)
        df_ontem = pd.read_csv(caminho_ontem)

        # criar o comparador e preparar os dados
        comparador = ComparadorPreco(df_hoje, df_ontem)

        # Realiza a comparação e gera relatórios
        comparador.comparar()
        geral, aumentaram, diminuiram = comparador.gerar_relatorios()

        # Guardar CSVs dos relatórios
        guardar_csv(geral, "comparacao_geral", subpasta="reports")
        guardar_csv(aumentaram, "precos_aumentaram", subpasta="reports")
        guardar_csv(diminuiram, "precos_diminuiram", subpasta="reports")

        logger.info("Comparação realizada com sucesso!")
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatorios: {e}")
        raise Exception(f"Erro: {e}")

if __name__ == "__main__":
    main()
