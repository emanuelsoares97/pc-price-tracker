function rodarScraping() {
      const btn = document.getElementById('scrapBtn');
      btn.disabled = true;
      btn.textContent = 'Processando...';
      fetch('/scrap', {method: 'POST'})
        .then(resp => resp.json())
        .then(data => {
          alert(data.mensagem);
        })
        .catch(() => {
          alert('Erro ao rodar scraping.');
        })
        .finally(() => {
          btn.disabled = false;
          btn.textContent = 'Rodar Scraping';
        });
    }