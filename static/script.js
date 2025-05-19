async function consultar() {
  const serie = document.getElementById('serie').value;
  const bimestres = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                         .map(cb => cb.value);

  if (!serie || bimestres.length === 0) {
    alert("Selecione uma série e pelo menos um bimestre.");
    return;
  }

  const resposta = await fetch('/consulta', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ serie, bimestres })
  });

  const dados = await resposta.json();

  document.getElementById("total").textContent = `Total: R$ ${dados.total.toFixed(2)}`;
  const lista = document.getElementById("lista");
  lista.innerHTML = "";
  dados.apostilas.forEach(apostila => {
  const li = document.createElement("li");
  li.innerHTML = `${apostila.nome} - <strong>R$ ${apostila.preco.toFixed(2)}</strong>`;
  lista.appendChild(li);
});

}
