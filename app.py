from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("dados/apostilas.csv")
df['valor'] = df['valor'].str.replace(',', '.').astype(float)

def mapear_periodo(p):
    if isinstance(p, str) and p.lower() == "anual":
        return "Anual"
    try:
        return f"{int(p)}º Bimestre"
    except:
        return "Outro"

df['periodo_formatado'] = df['período'].apply(mapear_periodo)

@app.route('/')
def index():
    ordem_desejada = ['INFANTIL 1', 'INFANTIL 2', 'INFANTIL 3', 'INFANTIL 4', '1º ANO', '2º ANO', '3º ANO', '4º ANO', '5º ANO', '6º ANO', '7º ANO', '8º ANO', '9º ANO', '1º EM', '2º EM', '3º EM']
    series_disponiveis = df['Série'].dropna().unique().tolist()
    series = [s for s in ordem_desejada if s in series_disponiveis]
    return render_template("index.html", series=series)

@app.route('/consulta', methods=['POST'])
def consulta():
    dados = request.json
    serie = dados.get('serie')
    bimestres = dados.get('bimestres', [])

    filtrado = df[
        (df['Série'] == serie) &
        (df['periodo_formatado'].isin(bimestres))
    ]

    total = round(filtrado['valor'].sum(), 2)
    apostilas = [
        {"nome": row["descrição"], "preco": round(row["valor"], 2)}
        for _, row in filtrado.iterrows()
    ]

    return jsonify({
        "total": total,
        "apostilas": apostilas
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
