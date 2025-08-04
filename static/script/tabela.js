// Gera tabela de comparação multidias simples (nome + datas)
function gerarTabelaComparacaoMultidias(dados) {
    const tabela = document.getElementById('tabela-comparacao');
    tabela.innerHTML = '';

    if (!dados || dados.length === 0) {
        tabela.innerHTML = '<tr><td>Nenhum dado disponível</td></tr>';
        return;
    }

    // Cabeçalho dinâmico: nome + datas
    const colunas = Object.keys(dados[0]).filter(col => col === 'nome' || /^\d{4}-\d{2}-\d{2}$/.test(col));
    const thead = document.createElement('thead');
    const trHead = document.createElement('tr');
    colunas.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        trHead.appendChild(th);
    });
    thead.appendChild(trHead);
    tabela.appendChild(thead);

    // Corpo da tabela
    const tbody = document.createElement('tbody');
    dados.forEach(linha => {
        const tr = document.createElement('tr');
        colunas.forEach(col => {
            const td = document.createElement('td');
            td.textContent = linha[col];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    tabela.appendChild(tbody);
}
function carregarCSV() {
  const input = document.getElementById("csvFile");
  const file = input.files[0];

  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    const content = e.target.result;
    // Detecta se o delimitador é ';' ou ','
    const delimiter = content.indexOf(";") > -1 ? ";" : ",";
    const lines = content.split("\n").filter(line => line.trim() !== "");
    // Removendo espaços extras nos cabeçalhos
    const headers = lines[0].split(delimiter).map(header => header.trim());
    console.log("Headers:", headers);

    const table = document.createElement("table");
    const thead = table.createTHead();
    const headerRow = thead.insertRow();

    headers.forEach(header => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });

    const tbody = table.createTBody();
    const dados = [];

    // Função para dividir linha CSV respeitando aspas
    function splitCSVLine(line, delimiter) {
      const regex = new RegExp(
        `(?:"([^"]*)"|([^"${delimiter}]+))(?:${delimiter}|$)`,
        'g'
      );
      const result = [];
      let match;
      while ((match = regex.exec(line)) !== null) {
        // match[1] é o campo entre aspas, match[2] é o campo sem aspas
        result.push(match[1] !== undefined ? match[1] : match[2]);
      }
      return result;
    }

    // Processa cada linha (exceto a de cabeçalho)
    for (let i = 1; i < lines.length; i++) {
      const row = splitCSVLine(lines[i], delimiter);
      const tr = tbody.insertRow();

      // Destacar menor valor em verde e mostrar o dia
      let menorValor = row[headers.indexOf("menor_preco")];
      let menorValorNum = parseFloat(menorValor);
      let diaMenor = "";
      // Descobre o dia do menor valor
      headers.forEach((h, idx) => {
        if (h !== "nome" && h !== "menor_preco") {
          let valorNum = parseFloat(row[idx]);
          if (!isNaN(valorNum) && valorNum === menorValorNum) {
            diaMenor = h;
          }
        }
      });

      row.forEach((cell, idx) => {
        const td = tr.insertCell();
        // Se for a coluna menor_preco, mostra valor + dia
        if (headers[idx] === "menor_preco") {
          td.textContent = menorValor + (diaMenor ? ` (${diaMenor})` : "");
        } else {
          td.textContent = cell;
        }
        // Destaca o menor valor nas colunas de preço (exceto nome e menor_preco)
        if (headers[idx] !== "nome" && headers[idx] !== "menor_preco") {
          let valorNum = parseFloat(cell);
          if (!isNaN(valorNum) && valorNum === menorValorNum) {
            td.style.background = "#d4f7d4"; // verde claro
            td.style.fontWeight = "bold";
          }
        }
      });

      // Adiciona ao array dados para uso no gráfico se quiser
      let obj = { nome: row[headers.indexOf("nome")], menor_preco: menorValorNum, dia_menor: diaMenor };
      // Adiciona os preços por data
      headers.forEach((h, idx) => {
        if (h !== "nome" && h !== "menor_preco") {
          obj[h] = row[idx];
        }
      });
      dados.push(obj);
    }

    const container = document.getElementById("tabelaContainer");
    container.innerHTML = "";
    container.appendChild(table);

    // Loop de log para depuração de cada linha
    for (let i = 1; i < lines.length; i++) {
      const row = lines[i].split(delimiter);
      const indexDiff = headers.indexOf("diferença");
      console.log("Linha bruta:", lines[i]);    // Exibe a linha inteira
      console.log("Linha dividida:", row);        // Exibe a linha dividida em array
      console.log("Index de diferença:", indexDiff, "->", row[indexDiff]);
    }

    console.log("Dados lidos:", dados);
    atualizarGrafico(dados);
  };

  reader.readAsText(file);
}

function filtrarTabela() {
  const nomeFiltro = document.getElementById("filtroNome").value.toLowerCase();
  const filtroDiferenca = document.getElementById("filtroDiferenca").value;
  // Remove acentos e transforma em minúsculas para evitar problemas de comparação
  const filtro = filtroDiferenca.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const linhas = document.querySelectorAll("#tabelaContainer table tbody tr");

  linhas.forEach((linha) => {
    // Verifique se o índice da coluna "nome" está correto; aqui estou assumindo que é a segunda coluna.
    const nome = linha.children[1]?.textContent.toLowerCase();
    // Supondo que a coluna "diferença" seja a última coluna da linha
    const diferenca = parseFloat(linha.lastElementChild?.textContent) || 0;

    let mostrar = true;

    // Filtra pelo nome
    if (nomeFiltro && !nome.includes(nomeFiltro)) {
      mostrar = false;
    }

    // Se o filtro for "aumentaram", exibe somente se a diferença for positiva (> 0)
    if (filtro === "aumentaram" && diferenca <= 0) {
      mostrar = false;
    }
    // Se o filtro for "diminuiram", exibe somente se a diferença for negativa (< 0)
    else if (filtro === "diminuiram" && diferenca >= 0) {
      mostrar = false;
    }

    linha.style.display = mostrar ? "" : "none";
  });
}
