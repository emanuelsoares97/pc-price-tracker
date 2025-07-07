from flask import Flask, render_template, jsonify
import traceback
from scripts import scraper_main, comparador_main
from utils.logger_util import get_logger

app = Flask(__name__)
logger = get_logger(__name__)

@app.route('/')
def index():
    """Renderiza a página principal com o frontend."""
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap():
    """Executa o scraping e a comparação, como o main.py."""
    try:
        logger.info("Iniciando scraping via frontend...")
        scraper_main.main()
        logger.info("Iniciando comparação via frontend...")
        comparador_main.main()
        logger.info("Finalizado com sucesso!")
        return jsonify({'status': 'ok', 'mensagem': 'Scraping e comparação concluídos!'}), 200
    except Exception as e:
        logger.error(f"Erro: {e}")
        traceback.print_exc()
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 