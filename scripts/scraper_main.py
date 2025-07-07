import sys
import os

# diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.guardarcsv import guardar_csv
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

def main():
    from selenium.webdriver.chrome.options import Options
    import shutil

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    if sys.platform.startswith('linux'):
        chrome_options.add_argument('--headless')
        chrome_path = shutil.which('google-chrome')
        print('google-chrome path:', chrome_path)
        print('chromedriver path:', shutil.which('chromedriver'))
        if chrome_path:
            chrome_options.binary_location = chrome_path
        else:
            raise Exception('Google Chrome não encontrado no sistema!')

    driver = webdriver.Chrome(
        service=Service(shutil.which('chromedriver')),
        options=chrome_options
    )
    driver.get("https://www.globaldata.pt/computadores/desktop/computadores-gamer")

    sleep(2)

    try:
        aceitar_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        aceitar_cookies.click()
        logger.info("Popup de cookies fechado com sucesso.")
    except:
        logger.info("Não apareceu popup de cookies.")
        


    dados = []

    produtos = driver.find_elements(By.CLASS_NAME, "col")

    for produto in produtos:
        try:
            linhas = produto.text.split("\n")

            # Procurar linha com a palavra "Computador"
            nome = next((linha for linha in linhas if "Computador" in linha), None)

            # Procurar última linha com "€"
            precos = [linha for linha in linhas if "€" in linha]
            preco_final = precos[-1] if precos else None

            validar= ["Pré Reserva", "Em stock", "Esgotado"]

            # Verifica se alguma palavra da lista "validar" aparece na linha
            stock = [linha for linha in linhas if any(palavra in linha for palavra in validar)]
            stock_final = stock[-1] if stock else None


            if nome and preco_final and stock_final:
                dados.append({
                    "nome": nome,
                    "preco": preco_final,
                    "stock": stock_final,
                    "data": datetime.today().strftime("%Y-%m-%d")
                })
                logger.info(f"Dados recolhidos: {dados}")

        except Exception as e:
            logger.error("Erro ao extrair produto:", e)

    df = pd.DataFrame(dados)

    guardar_csv(df, "precos_computadores")

    driver.quit()

if __name__ == "__main__":
    main()