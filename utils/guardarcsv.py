from utils.logger_util import get_logger
import os
from datetime import datetime
import pandas as pd

logger= get_logger(__name__)


def guardar_analise_csv(df, nome_ficheiro):
    """
    Guarda um DataFrame ou Series como CSV dentro da pasta `data/analisescsv`, garantindo que os ficheiros não sejam sobrescritos.

    :param df: DataFrame ou Series do Pandas com os dados a guardar.
    :param nome_ficheiro: Nome base do ficheiro CSV (sem extensão).
    """
    try:
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            logger.error("Parâmetro 'df' inválido. Esperado DataFrame ou Series.")
            raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame ou Series.")
        
        # Obtém o caminho do diretório base do projeto
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_data = os.path.join(caminho_projeto, "..", "data/csv")

        # Criar a pasta "csv" se não existir
        os.makedirs(caminho_data, exist_ok=True)

        # Adicionar a data e hora ao nome do ficheiro (formato YYYY-MM-DD_HH-MM-SS)
        data_atual = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.csv")

        # Se for uma Series, converte para DataFrame
        if isinstance(df, pd.Series):
            df = df.reset_index()

        # Guarda o ficheiro CSV
        df.to_csv(nome_completo, index=False)
        logger.info(f"Ficheiro guardado com sucesso: {nome_completo}")
    
    except Exception as e:
        logger.error(f"Erro ao tentar guardar o ficheiro: {e}")