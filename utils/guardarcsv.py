from utils.logger_util import get_logger
import os
from datetime import datetime
import pandas as pd

logger= get_logger(__name__)


def guardar_csv(df, nome, subpasta="raw"):
    # cria a pasta se não existir
    pasta = os.path.join('data', subpasta)
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    # guarda o ficheiro csv
    if 'data' in df.columns and not df['data'].empty:
        data_str = str(df['data'].iloc[0])
    else:
        # Usa a data atual se não houver coluna 'data'
        data_str = datetime.now().strftime('%Y-%m-%d')
        logger.warning("Coluna 'data' não encontrada no DataFrame. Usando data atual para nome do arquivo.")
    caminho = os.path.join(pasta, f"{nome}_{data_str}.csv")
    df.to_csv(caminho, index=False)