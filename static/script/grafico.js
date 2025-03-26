let chart;

function atualizarGrafico(dados) {
    const ctx = document.getElementById('graficoVariação').getContext('2d');
  
    if (chart) {
      chart.destroy();
    }
  
    const labels = dados.map(item => item.nome.length > 30 ? item.nome.slice(0, 30) + '...' : item.nome);
    const diferencaValores = dados.map(item => item.diferenca); // Usando 'diferenca' do CSV
  
    const data = {
      labels: labels,
      datasets: [{
        label: 'Diferença de Preço',
        data: diferencaValores,
        borderColor: 'green',
        fill: false
      }]
    };
  
    const config = {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        scales: {
          x: { 
            beginAtZero: true,
            ticks: {
              maxRotation: 90,
              minRotation: 45,
            },
          },
          y: { 
            beginAtZero: true 
          }
        }
      }
    };
  
    chart = new Chart(ctx, config);
  }
  
