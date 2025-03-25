import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas as pd
from models.comparador import ComparadorPreco
from utils.csvrecente import encontrar_csvs_mais_recentes
from utils.guardarcsv import guardar_csv
from utils.logger_util import get_logger

logger= get_logger(__name__)

def main():
    try:
        # Passo 1: Encontrar os ficheiros mais recentes
        caminho_hoje, caminho_ontem = encontrar_csvs_mais_recentes()

        # Passo 2: Carregar os ficheiros em DataFrames
        df_hoje = pd.read_csv(caminho_hoje)
        df_ontem = pd.read_csv(caminho_ontem)

        # Passo 3: Criar o comparador e preparar os dados
        comparador = ComparadorPreco(df_hoje, df_ontem)

        comparador.comparar()
        
        comparador.gerar_relatorios()

        # Passo 4: Gerar relatórios
        geral, aumentaram, diminuiram = comparador.gerar_relatorios()

        # Passo 5: Guardar CSVs dos relatórios
        guardar_csv(geral, "comparacao_geral", subpasta="reports")
        guardar_csv(aumentaram, "precos_aumentaram", subpasta="reports")
        guardar_csv(diminuiram, "precos_diminuiram", subpasta="reports")

        logger.info("Comparação realizada com sucesso!")
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatorios: {e}")
        raise f"Erro: {e}"

if __name__ == "__main__":
    main()
