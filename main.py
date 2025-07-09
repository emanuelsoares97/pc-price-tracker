# este ficheiro serve para correr o scraping e a comparação tudo de uma vez
from scripts import scraper_main, comparador_main
from utils.logger_util import get_logger

logger=get_logger(__name__)

def main():
    logger.info("Iniciando scraping...")
    scraper_main.main()

    logger.info("Iniciando comparação...")
    comparador_main.main()

    logger.info("Finalizado com sucesso!")

if __name__ == "__main__":
    # aqui faço o scraping
    scraper_main.main()
    # aqui faço a comparação dos preços
    comparador_main.main()
