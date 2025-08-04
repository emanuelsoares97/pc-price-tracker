function pesquisarPorNome() {
    const nome = document.getElementById('filtroNome').value;
    if (!nome) {
        alert('Digite o nome do computador para pesquisar.');
        return;
    }
    fetch('/scrap_nome', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome })
    })
    .then(resp => resp.json())
    .then(data => {
        if (data.status === 'ok') {
            alert(data.mensagem);
            // Aqui pode chamar uma função para atualizar o gráfico/tabela com os dados filtrados
        } else {
            alert(data.mensagem);
        }
    })
    .catch(() => {
        alert('Erro ao pesquisar por nome.');
    });
}
