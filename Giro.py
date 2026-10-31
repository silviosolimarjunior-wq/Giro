from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIRO - Copiloto de Corridas</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: #e0e0e0; padding: 15px; max-width: 420px; margin: auto; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        h1 { color: #4CAF50; font-size: 1.6rem; text-align: center; margin-bottom: 5px; }
        label { display: block; margin-top: 12px; font-size: 0.85rem; color: #bbb; }
        input, select { width: 100%; padding: 10px; margin-top: 4px; background: #2d2d2d; border: 1px solid #444; color: white; border-radius: 6px; box-sizing: border-box; font-size: 1rem; }
        button { width: 100%; background: #4CAF50; color: white; border: none; padding: 12px; margin-top: 18px; border-radius: 6px; font-weight: bold; font-size: 1.05rem; cursor: pointer; }
        button:hover { background: #45a049; }
        .grid { display: flex; gap: 10px; }
        .grid > div { flex: 1; }
        .result { margin-top: 20px; padding: 15px; border-radius: 8px; background: #252525; border-left: 5px solid #4CAF50; }
        .result-ruim { border-left-color: #F44336; }
        .result-boa { border-left-color: #FFEB3B; }
        .excelente { color: #4CAF50; font-weight: bold; }
        .boa { color: #FFEB3B; font-weight: bold; }
        .ruim { color: #F44336; font-weight: bold; }
        .stat-val { font-size: 1.1rem; font-weight: bold; color: #fff; }
    </style>
</head>
<body>
    <div class="card">
        <h1>GIRO 🚖</h1>
        <p style="text-align: center; font-size: 0.8rem; color: #888; margin-top: 0;">Copiloto Inteligente de Corridas</p>
        
        <form method="POST">
            <div class="grid">
                <div>
                    <label>Valor Corrida (R$):</label>
                    <input type="text" name="valor" placeholder="Ex: 28.50" required value="{{ valor or '' }}">
                </div>
                <div>
                    <label>Distância Total (KM):</label>
                    <input type="text" name="km" placeholder="Ex: 12.0" required value="{{ km or '' }}">
                </div>
            </div>

            <div class="grid">
                <div>
                    <label>Tempo Estimado (min):</label>
                    <input type="number" name="minutos" placeholder="Ex: 25" value="{{ minutos or '' }}">
                </div>
                <div>
                    <label>Condição do Trânsito:</label>
                    <select name="transito">
                        <option value="normal" {% if transito == 'normal' %}selected{% endif %}>🟢 Livre / Fluido</option>
                        <option value="moderado" {% if transito == 'moderado' %}selected{% endif %}>🟡 Moderado</option>
                        <option value="pesado" {% if transito == 'pesado' %}selected{% endif %}>🔴 Pico / Lento</option>
                    </select>
                </div>
            </div>
            
            <button type="submit">Analisar Corrida</button>
        </form>

        {% if resultado %}
        <div class="result result-{{ resultado.classe }}">
            <p><strong>Veredito:</strong> <span class="{{ resultado.classe }}">{{ resultado.veredito }}</span></p>
            <hr style="border-color: #333; margin: 10px 0;">
            <p>💰 <strong>Lucro Líquido Est.:</strong> <span class="stat-val">R$ {{ "%.2f"|format(resultado.lucro) }}</span></p>
            <p>📍 <strong>Ganho por KM:</strong> <span class="stat-val">R$ {{ "%.2f"|format(resultado.ganho_km) }} / km</span></p>
            {% if resultado.ganho_hora %}
            <p>⏱️ <strong>Estimativa por Hora:</strong> <span class="stat-val">R$ {{ "%.2f"|format(resultado.ganho_hora) }} / hora</span></p>
            {% endif %}
            <p style="font-size: 0.8rem; color: #888; margin-bottom: 0;">Custo operacional considerado: R$ {{ "%.2f"|format(resultado.custo) }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    valor_str = ""
    km_str = ""
    minutos_str = ""
    transito = "normal"
    
    if request.method == "POST":
        try:
            valor_str = request.form.get("valor", "").replace(",", ".")
            km_str = request.form.get("km", "").replace(",", ".")
            minutos_str = request.form.get("minutos", "")
            transito = request.form.get("transito", "normal")
            
            valor = float(valor_str)
            km = float(km_str)
            minutos = float(minutos_str) if minutos_str else 0
            
            if km > 0:
                fator_custo = 1.0
                if transito == "moderado":
                    fator_custo = 1.15
                elif transito == "pesado":
                    fator_custo = 1.35
                    
                custo_km = 0.75 * fator_custo
                custo = km * custo_km
                lucro = valor - custo
                ganho_km = valor / km
                
                ganho_hora = None
                if minutos > 0:
                    ganho_hora = (lucro / minutos) * 60

                if ganho_km >= 2.00 and (not ganho_hora or ganho_hora >= 35.0):
                    veredito = "🟢 EXCELENTE! Aceita na hora."
                    classe = "excelente"
                elif ganho_km >= 1.30 and (not ganho_hora or ganho_hora >= 22.0):
                    veredito = "🟡 BOA / RAZOÁVEL. Vale a pena."
                    classe = "boa"
                else:
                    veredito = "🔴 RUIM! Vais pagar para trabalhar ou perder tempo."
                    classe = "ruim"
                    
                resultado = {
                    "valor": valor,
                    "custo": custo,
                    "lucro": lucro,
                    "ganho_km": ganho_km,
                    "ganho_hora": ganho_hora,
                    "veredito": veredito,
                    "classe": classe
                }
        except ValueError:
            pass
            
    return render_template_string(
        HTML_TEMPLATE, 
        resultado=resultado, 
        valor=valor_str, 
        km=km_str, 
        minutos=minutos_str,
        transito=transito
    )

if __name__ == "__main__":
    app.run(debug=True)
