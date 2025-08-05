import sys
import os

# adiciono o diretório raiz do projeto ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.save_csv import save_csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
import pandas as pd
from utils.logger_util import get_logger
import shutil

logger= get_logger(__name__)

# função principal do scraping
def main(nome_pesquisa=None):
    """ Função principal do scraper de computadores gamer.
    Se nome_pesquisa for fornecido, filtra os resultados pelo nome do computador."""

    import shutil
    import tempfile
    import uuid

    # defino variáveis de ambiente para garantir que o chrome use /tmp
    os.environ["XDG_CONFIG_HOME"] = "/tmp"
    os.environ["HOME"] = "/tmp"


    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')  # tamanho da janela

    if sys.platform.startswith('linux'):
        # estes argumentos só fazem sentido em cloud/linux
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--remote-debugging-port=9222')
        # aqui defino o caminho do chrome se for linux
        chrome_path = shutil.which('google-chrome')
        print('google-chrome path:', chrome_path)
        print('chromedriver path:', shutil.which('chromedriver'))
        if chrome_path:
            chrome_options.binary_location = chrome_path
        else:
            raise Exception('google chrome não encontrado no sistema!')
    # no windows não adiciono argumentos extra, só o tamanho da janela

    # forço o chrome a usar um diretório temporário único para o perfil
    profile_dir = tempfile.mkdtemp(prefix="chrome_profile_")
    chrome_options.add_argument(f'--user-data-dir={profile_dir}')

    # crio o driver do chrome
    driver = webdriver.Chrome(
        service=Service(shutil.which('chromedriver')),
        options=chrome_options
    )
    # abro a página dos computadores gamer
    driver.get("https://www.globaldata.pt/computadores/desktop/computadores-gamer")

    sleep(2)  # espero 2 segundos para garantir que a página carregou

    try:
        # tento aceitar os cookies se aparecer o popup
        aceitar_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        aceitar_cookies.click()
        logger.info("popup de cookies fechado com sucesso.")
    except:
        logger.info("não apareceu popup de cookies.")
        

    dados = []  # aqui vou guardar os dados dos produtos

    produtos = driver.find_elements(By.CLASS_NAME, "col")

    for produto in produtos:
        try:
            linhas = produto.text.split("\n")

            
            nome = next((linha for linha in linhas if "Computador" in linha), None)

            # procuro última linha com "€"
            precos = [linha for linha in linhas if "€" in linha]
            preco_final = precos[-1] if precos else None

            validar= ["Pré Reserva", "Em stock", "Esgotado"]

            # verifica se alguma palavra da lista "validar" aparece na linha
            stock = [linha for linha in linhas if any(palavra in linha for palavra in validar)]
            stock_final = stock[-1] if stock else None

            # se encontrar nome, preço e stock, guardo o produto
            if nome and preco_final and stock_final:
                # se nome_pesquisa foi passado, só adiciona se corresponder
                if nome_pesquisa:
                    if nome_pesquisa.lower() in nome.lower():
                        dados.append({
                            "nome": nome,
                            "preco": preco_final,
                            "stock": stock_final,
                            "data": datetime.today().strftime("%Y-%m-%d")
                        })
                        logger.info(f"dados recolhidos: {dados}")
                else:
                    dados.append({
                        "nome": nome,
                        "preco": preco_final,
                        "stock": stock_final,
                        "data": datetime.today().strftime("%Y-%m-%d")
                    })
                    logger.info(f"dados recolhidos: {dados}")

        except Exception as e:
            logger.error("erro ao extrair produto:", e)

    # crio o dataframe com os dados recolhidos
    df = pd.DataFrame(dados)

    # Se não encontrou nenhum produto, retorna feedback e não salva
    if df.empty:
        logger.warning("Nenhum produto encontrado para o termo de pesquisa.")
        # fecho o chrome
        driver.quit()
        return False

    # guarda o csv na pasta correta
    if nome_pesquisa:
        nome_limpo = ''.join(c for c in nome_pesquisa if c.isalnum() or c in ('-', '_')).replace(' ', '_')
        save_csv(df, f"precos_computadores_{nome_limpo}", subpasta="raw/individual")
    else:
        save_csv(df, "precos_computadores", subpasta="raw/geral")

    # fecho o chrome
    driver.quit()
    return True

    

# se correr este ficheiro diretamente, chama a função main
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scraper de computadores")
    parser.add_argument('--nome', type=str, help='Nome do computador para pesquisar', default=None)
    args = parser.parse_args()
    main(nome_pesquisa=args.nome)