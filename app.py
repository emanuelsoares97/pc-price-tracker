from flask import Flask, render_template, jsonify, send_from_directory
import traceback
from scripts import scraper_main, comparador_main
from utils.logger_util import get_logger
import os

# crio a app flask
app = Flask(__name__)
logger = get_logger(__name__)

# rota principal, mostra a página inicial
@app.route('/')
def index():
    """renderiza a interface principal do visualizador"""
    return render_template('index.html')

# rota para downloads, mostra os ficheiros disponíveis
@app.route('/downloads')
def downloads():
    """renderiza a página de downloads de ficheiros"""
    raw_dir = os.path.join('data', 'raw')
    reports_dir = os.path.join('data', 'reports')
    raw_files = sorted(os.listdir(raw_dir)) if os.path.exists(raw_dir) else []
    reports_files = sorted(os.listdir(reports_dir)) if os.path.exists(reports_dir) else []
    return render_template('downloads.html', raw_files=raw_files, reports_files=reports_files)

# rota para fazer scraping e comparação quando carrego no botão
@app.route('/scrap', methods=['POST'])
def scrap():
    """executa o scraping e a comparação, como o main.py"""
    try:
        logger.info("iniciando scraping via frontend...")
        scraper_main.main()
        logger.info("iniciando comparação via frontend...")
        comparador_main.main()
        logger.info("finalizado com sucesso!")
        return jsonify({'status': 'ok', 'mensagem': 'scraping e comparação concluídos!'}), 200
    except Exception as e:
        logger.error(f"erro: {e}")
        traceback.print_exc()
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

# rota para fazer download dos ficheiros raw
@app.route('/download/raw/<filename>')
def download_raw(filename):
    """permite baixar ficheiros csv da pasta data/raw"""
    return send_from_directory(os.path.join('data', 'raw'), filename, as_attachment=True)

# rota para fazer download dos ficheiros de relatórios
@app.route('/download/reports/<filename>')
def download_reports(filename):
    """permite baixar ficheiros csv da pasta data/reports"""
    return send_from_directory(os.path.join('data', 'reports'), filename, as_attachment=True)

# aqui arranco a app se correr localmente
if __name__ == '__main__':
    app.run(debug=True) 