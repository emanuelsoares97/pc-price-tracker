from utils.logger_util import get_logger
import os
from datetime import datetime
import pandas as pd

logger= get_logger(__name__)


def guardar_csv(df, nome_ficheiro, subpasta="raw"):
    """
    Guarda CSV numa subpasta de `data/` (por padrão, 'csv').
    """
    try:
        caminho_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_data = os.path.join(caminho_projeto, "..", "data", subpasta)

        os.makedirs(caminho_data, exist_ok=True)

        data_atual = datetime.today().strftime('%Y-%m-%d')
        nome_completo = os.path.join(caminho_data, f"{nome_ficheiro}_{data_atual}.csv")

        if isinstance(df, pd.Series):
            df = df.reset_index()

        df.to_csv(nome_completo, index=False)
        logger.info(f"Ficheiro guardado com sucesso: {nome_completo}")
    except Exception as e:
        logger.error(f"Erro ao guardar ficheiro: {e}")
        raise f"Erro: {e}"