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
    caminho = os.path.join(pasta, f"{nome}_{df['data'].iloc[0]}.csv")
    df.to_csv(caminho, index=False)