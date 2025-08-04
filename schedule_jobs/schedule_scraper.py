import schedule
import time
from scripts.scraper_main import main as run_scraper
from utils.logger_util import get_logger

logger = get_logger(__name__)


def job():
    """Função agendada para rodar o scraping geral todos os dias."""
    logger.info('Iniciar scraping geral...')
    run_scraper()
    logger.info('Scraping geral finalizado.')

# agenda para correr todos os dias às 8h
schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    logger.info("Scheduler ativo. Vai correr o scraping todos os dias às 8h.")
    while True:
        schedule.run_pending()
        time.sleep(60)
