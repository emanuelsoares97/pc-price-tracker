import os
import tempfile
from utils import csvrecente

def test_encontrar_csvs_mais_recentes():
    with tempfile.TemporaryDirectory() as tempdir:
        # Cria arquivos CSV simulados
        nomes = [
            'precos_computadores_2025-03-25.csv',
            'precos_computadores_2025-03-26.csv',
            'precos_computadores_2025-03-27.csv',
        ]
        for nome in nomes:
            with open(os.path.join(tempdir, nome), 'w') as f:
                f.write('teste')
        # Chama a função utilitária
        mais_recentes = csvrecente.encontrar_csvs_mais_recentes(tempdir)
        # Espera os dois arquivos mais recentes (ordem alfabética reversa)
        esperado = (
            os.path.join(tempdir, 'precos_computadores_2025-03-27.csv'),
            os.path.join(tempdir, 'precos_computadores_2025-03-26.csv')
        )
        assert mais_recentes == esperado 