import pandas as pd
from models.comparador import ComparadorPreco
import pytest

def test_comparar_multidias_basic():
    # monta dataframes simulados
    df1 = pd.DataFrame({
        'nome': ['PC Gamer A', 'PC Gamer B'],
        'preco': [1000, 1500],
        'stock': ['Em stock', 'Esgotado'],
        'data': ['2025-08-03', '2025-08-03']
    })
    df2 = pd.DataFrame({
        'nome': ['PC Gamer A', 'PC Gamer B'],
        'preco': [950, 1600],
        'stock': ['Em stock', 'Esgotado'],
        'data': ['2025-08-04', '2025-08-04']
    })
    dfs = [df1, df2]
    datas = ['2025-08-03', '2025-08-04']
    df_final = ComparadorPreco.comparar_multidias(dfs, datas)
    assert 'PC Gamer A' in df_final['nome'].values
    assert '2025-08-03' in df_final.columns
    assert '2025-08-04' in df_final.columns
    assert df_final.loc[df_final['nome']=='PC Gamer A', '2025-08-03'].values[0] == 1000
    assert df_final.loc[df_final['nome']=='PC Gamer A', '2025-08-04'].values[0] == 950

def test_comparar_multidias_nome_pesquisa():
    df1 = pd.DataFrame({
        'nome': ['PC Gamer A', 'PC Gamer B'],
        'preco': [1000, 1500],
        'stock': ['Em stock', 'Esgotado'],
        'data': ['2025-08-03', '2025-08-03']
    })
    df2 = pd.DataFrame({
        'nome': ['PC Gamer A', 'PC Gamer B'],
        'preco': [950, 1600],
        'stock': ['Em stock', 'Esgotado'],
        'data': ['2025-08-04', '2025-08-04']
    })
    dfs = [df1, df2]
    datas = ['2025-08-03', '2025-08-04']
    df_final = ComparadorPreco.comparar_multidias(dfs, datas, nome_pesquisa='Gamer A')
    assert len(df_final) == 1
    assert df_final['nome'].iloc[0] == 'PC Gamer A'

def test_comparar_multidias_nome_inexistente():
    df1 = pd.DataFrame({
        'nome': ['PC Gamer A', 'PC Gamer B'],
        'preco': [1000, 1500],
        'stock': ['Em stock', 'Esgotado'],
        'data': ['2025-08-03', '2025-08-03']
    })
    df2 = pd.DataFrame({
        'nome': ['PC Gamer A', 'PC Gamer B'],
        'preco': [950, 1600],
        'stock': ['Em stock', 'Esgotado'],
        'data': ['2025-08-04', '2025-08-04']
    })
    dfs = [df1, df2]
    datas = ['2025-08-03', '2025-08-04']
    with pytest.raises(ValueError):
        ComparadorPreco.comparar_multidias(dfs, datas, nome_pesquisa='Inexistente')
