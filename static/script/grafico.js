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
      type: 'bar', // Troca para barra para melhor visualização de ponto único
      data: data,
      options: {
        responsive: true,
        scales: {
          x: {
            ticks: {
              maxRotation: 90,
              minRotation: 45,
            },
          },
          y: {
            // Ajusta os limites do eixo Y para incluir negativos e positivos
            beginAtZero: false,
            suggestedMin: Math.min(...diferencaValores, 0) - 50,
            suggestedMax: Math.max(...diferencaValores, 0) + 50
          }
        }
      }
    };

    chart = new Chart(ctx, config);
  }
  
