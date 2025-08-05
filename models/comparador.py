import pandas as pd
from utils.logger_util import get_logger

logger = get_logger(__name__)


# classe para comparar preços entre dois dataframes
class ComparadorPreco:
    """Classe para comparar preços entre dois dataframes de computadores.
    Recebe dois dataframes: um de hoje e outro de ontem.
    Pode comparar preços de múltiplos dias, filtrando por nome do computador."""
    
    def __init__(self, df_hoje: pd.DataFrame, df_ontem: pd.DataFrame):
        # guardo os dataframes de hoje e de ontem
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


    # ...existing code...
    @staticmethod
    def comparar_multidias(dfs, datas, nome_pesquisa=None):
        """
        Recebe lista de DataFrames (um por dia) e lista de datas.
        Retorna DataFrame: cada linha um computador, cada coluna um preço por data, traço se não houver.
        Se nome_pesquisa for passado, filtra só esse computador.
        """
        # Limpa preços e monta dict: {data: df}
        dfs_dict = {}
        for df, data in zip(dfs, datas):
            df = df.copy()
            df['preco'] = df['preco'].astype(str)
            df['preco'] = df['preco'].str.replace('€','', regex=False)
            df['preco'] = df['preco'].str.replace(r'\s','', regex=True)
            df['preco'] = df['preco'].str.replace(',','.', regex=False)
            df['preco'] = df['preco'].replace(['Esgotado','Indisponível','-',''], pd.NA)
            df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
            dfs_dict[data] = df

        # Monta lista de todos os nomes únicos
        nomes = set()
        for df in dfs_dict.values():
            nomes.update(df['nome'].unique())
        import unicodedata
        def normalizar(texto):
            return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8').lower()
        if nome_pesquisa:
            termo = normalizar(nome_pesquisa)
            nomes_filtrados = {n for n in nomes if termo in normalizar(n)}
            if not nomes_filtrados:
                raise ValueError(f"Nenhum computador encontrado com o nome: '{nome_pesquisa}'.")
            nomes = nomes_filtrados

        # Monta tabela: cada linha um computador, cada coluna um preço por data
        relatorio = []
        for nome in sorted(nomes):
            linha = {'nome': nome}
            for data in datas:
                df = dfs_dict[data]
                preco = df.loc[df['nome'] == nome, 'preco']
                if not preco.empty and pd.notnull(preco.values[0]):
                    valor = preco.values[0]
                    linha[data] = valor
                else:
                    linha[data] = '-'
            relatorio.append(linha)

        # Cria DataFrame final
        colunas = ['nome'] + datas
        df_final = pd.DataFrame(relatorio)[colunas]
        return df_final


    # função para gerar relatório geral de comparação
    def gerar_relatorio_comparacao_geral(self):
        """Gera um relatório geral comparando os preços de hoje e ontem."""
        # aqui junto os dois dataframes pelo nome do produto
        df_merged = pd.merge(self.df_hoje, self.df_ontem, on='nome', suffixes=('_hoje', '_ontem'))
        # guardo o csv com a comparação geral
        df_merged.to_csv('data/reports/comparacao_geral_' + self.df_hoje['data'].iloc[0] + '.csv', index=False)

    # função para gerar relatório de produtos que aumentaram de preço
    def gerar_relatorio_precos_aumentaram(self):
        """Gera um relatório de produtos que aumentaram de preço comparando hoje e ontem."""
        # junto os dataframes e filtro os que aumentaram
        df_merged = pd.merge(self.df_hoje, self.df_ontem, on='nome', suffixes=('_hoje', '_ontem'))
        df_aumentaram = df_merged[df_merged['preco_hoje'] > df_merged['preco_ontem']]
        # guardo o csv dos que aumentaram
        df_aumentaram.to_csv('data/reports/precos_aumentaram_' + self.df_hoje['data'].iloc[0] + '.csv', index=False)

    # função para gerar relatório de produtos que diminuíram de preço
    def gerar_relatorio_precos_diminuiram(self):
        """Gera um relatório de produtos que diminuíram de preço comparando hoje e ontem."""
        # junto os dataframes e filtro os que diminuíram
        df_merged = pd.merge(self.df_hoje, self.df_ontem, on='nome', suffixes=('_hoje', '_ontem'))
        df_diminuiram = df_merged[df_merged['preco_hoje'] < df_merged['preco_ontem']]
        # guardo o csv dos que diminuíram
        df_diminuiram.to_csv('data/reports/precos_diminuiram_' + self.df_hoje['data'].iloc[0] + '.csv', index=False)