import pandas as pd
from utils.logger_util import get_logger

logger = get_logger(__name__)


class ComparadorPreco:
    def __init__(self, df_hoje: pd.DataFrame, df_ontem: pd.DataFrame):
        """
        Inicializa a classe ComparadorPreco com os dados de hoje e ontem.

        Args:
            df_hoje (pd.DataFrame): DataFrame com preços mais recentes.
            df_ontem (pd.DataFrame): DataFrame com preços anteriores.

        Raises:
            ValueError: Se os DataFrames não contiverem as colunas 'nome' e 'preco'.
        """
        self.df_hoje = df_hoje.copy()
        self.df_ontem = df_ontem.copy()
        self.df_comparado = pd.DataFrame()
        self.df_geral = pd.DataFrame()
        self.df_aumentaram = pd.DataFrame()
        self.df_diminuiram = pd.DataFrame()

        # Validação das colunas
        required_cols = {"nome", "preco"}
        for df, nome in [(self.df_hoje, "df_hoje"), (self.df_ontem, "df_ontem")]:
            if not required_cols.issubset(df.columns):
                raise ValueError(f"O DataFrame '{nome}' deve conter as colunas: {required_cols}")

    def _limpar_dados(self) -> None:
        """
        Limpa os dados de preço em ambos os DataFrames, convertendo para float.
        """
        try:
            for df, label in [(self.df_hoje, "hoje"), (self.df_ontem, "ontem")]:
                df["preco"] = (
                    df["preco"]
                    .str.replace("€", "", regex=False)
                    .str.replace(",", ".", regex=False)
                    .str.replace(" ", "", regex=False)
                    .str.strip()
                    .astype(float)
                )
                logger.info(f"Dados limpos com sucesso para df_{label}")
        except Exception as e:
            logger.error(f"Erro ao limpar dados: {e}")
            raise

    def comparar(self) -> pd.DataFrame:
        """
        Faz a comparação dos preços e calcula a diferença.

        Returns:
            pd.DataFrame: DataFrame com colunas de comparação e diferença de preços.
        """
        try:
            self._limpar_dados()

            self.df_comparado = pd.merge(
                self.df_ontem,
                self.df_hoje,
                on="nome",
                suffixes=("_ontem", "_hoje")
            )

            self.df_comparado["diferença"] = (
                self.df_comparado["preco_hoje"] - self.df_comparado["preco_ontem"]
            )

            logger.info("Comparação realizada com sucesso.")
            return self.df_comparado

        except Exception as e:
            logger.error(f"Erro ao fazer merge ou comparar dados: {e}")
            raise

    def gerar_relatorios(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Gera relatórios com os produtos que aumentaram, diminuíram e uma visão geral.

        Returns:
            tuple: (geral, aumentaram, diminuíram)
        """
        try:
            self.df_geral = self.df_comparado.sort_values(by="diferença", ascending=False).reset_index(drop=True)
            self.df_aumentaram = self.df_comparado[self.df_comparado["diferença"] > 0].reset_index(drop=True)
            self.df_diminuiram = self.df_comparado[self.df_comparado["diferença"] < 0].reset_index(drop=True)

            logger.info("Relatórios gerados com sucesso.")
            return self.df_geral, self.df_aumentaram, self.df_diminuiram

        except Exception as e:
            logger.error(f"Erro ao gerar relatórios: {e}")
            raise
