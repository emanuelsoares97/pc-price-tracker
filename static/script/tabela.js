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

      const indexDiff = headers.indexOf("diferença");
      // antes de usar .replace, verifico se existe valor
      let diffValue = row[indexDiff];
      if (diffValue !== undefined) {
          diffValue = diffValue.replace(",", ".");
      } else {
          diffValue = ""; // se não houver valor, fica vazio
          console.log("Coluna diff não encontrada nesta linha:", row);
      }
      let diff = parseFloat(diffValue);
      
      if (!isNaN(diff)) {
        if (diff > 0) {
          tr.classList.add("aumentou");
        } else if (diff < 0) {
          tr.classList.add("diminuiu");
        } else {
          tr.classList.add("neutro");
        }
      }

      row.forEach(cell => {
        const td = tr.insertCell();
        td.textContent = cell;
      });

      dados.push({
        nome: row[headers.indexOf("nome")],
        preco_hoje: parseFloat(row[headers.indexOf("preco_hoje")].replace(",", ".")),
        preco_ontem: parseFloat(row[headers.indexOf("preco_ontem")].replace(",", ".")),
        diferenca: diff
      });
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
