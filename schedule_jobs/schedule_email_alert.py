import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os
from utils.logger_util import get_logger
import dotenv

dotenv.load_dotenv()

logger = get_logger(__name__)

def email_config():
    sender = os.getenv('EMAIL_USER')
    receiver = os.getenv('EMAIL_RECEIVER')
    password = os.getenv('EMAIL_PASS')
    return sender, receiver, password

def job():
    """Função agendada para rodar o scraping e comparar preços.
    Se a diferença de preço for maior que 300€, envia um email único de alerta com todos."""
    try:
        pasta = 'data/reports'
        files = [f for f in os.listdir(pasta) if f.startswith('comparacao_multidias_') and f.endswith('.csv')]
        files.sort(reverse=True) 

        if not files:
            logger.warning('Nenhum comparacao_multidias encontrado.')
            return
        
        df = pd.read_csv(os.path.join(pasta, files[0]))

        datas = [col for col in df.columns if col != 'nome']
        if len(datas) < 2:
            logger.warning('Preciso de pelo menos 2 datas para comparar.')
            return
        
        datas = sorted(datas, reverse=True)[:2]
        data_hoje, data_ontem = datas[0], datas[1]

        # Lista para acumular as diferenças significativas
        alertas = []

        for idx, row in df.iterrows():
            preco_hoje = row[data_hoje]
            preco_ontem = row[data_ontem]
            if pd.notna(preco_hoje) and pd.notna(preco_ontem):
                diff = preco_ontem - preco_hoje
                if diff >= 300:
                    alertas.append((row['nome'], diff))
                else:
                    logger.info(f'Nenhuma diferença significativa para {row["nome"]}: {diff:.2f}€')


        # Se achou algum alerta, envia um email único para todos
        if alertas:
            send_alert_email_multiplos(alertas)
        else:
            logger.info('Nenhuma alteração significativa encontrada para envio de alertas.')

    except Exception as e:
        logger.error(f'Erro ao executar o job de alerta: {e}')
        raise

def send_alert_email_multiplos(alertas):
    """Envia um email com a lista de computadores que tiveram alterações significativas de preço.
    Cada computador com diferença maior que 300€ é listado no email."""
    sender, receiver, password = email_config()

    subject = f'ALERTA: {len(alertas)} computadores mudaram mais de 300€'

    # Monta a lista de computadores e diferenças em HTML
    linhas = "".join(
        f"<li><strong>{nome}</strong> com diferença de <strong>{diff:.2f}€</strong></li>"
        for nome, diff in alertas
    )

    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #d9534f;">Alerta de Preço</h2>
            <p>Os seguintes computadores tiveram alterações significativas de preço hoje:</p>
            <ul>
                {linhas}
            </ul>
            <p>Por favor, verifique as alterações para possíveis ações.</p>
            <br>
            <hr style="border:none; border-top:1px solid #eee;">
            <p style="font-size: 0.9em; color: #777;">
                Atenciosamente,<br>
                <strong>PC Price Tracker</strong><br>
                Quinta do Conde<br>
                <a href="mailto:pricetracker@gmail.com" style="color:#1a73e8;">pricetracker@gmail.com</a>
            </p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        logger.info(f'Email de alerta enviado para {receiver} com {len(alertas)} computadores.')
    except Exception as e:
        logger.error(f'Erro ao enviar email: {e}')
        raise


schedule.every().day.at('09:00').do(job)

if __name__ == '__main__':
    logger.info('Scheduler de alertas ativo. Vai validar diferenças todos os dias às 9h.')
    while True:
        
        schedule.run_pending()
        time.sleep(60)
