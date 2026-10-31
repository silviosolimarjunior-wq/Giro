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
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b131e; color: #e0e0e0; padding: 12px; max-width: 450px; margin: auto; }
        
        /* Cartão de Métricas Superior (Estilo GigU) */
        .metrics-card { background: #121c2c; border: 2px solid #f39c12; border-radius: 16px; padding: 15px; margin-bottom: 15px; box-shadow: 0 6px 15px rgba(0,0,0,0.4); }
        .metrics-grid { display: flex; justify-content: space-between; text-align: center; margin-bottom: 10px; }
        .metric-item div:first-child { font-size: 0.75rem; color: #95a5a6; text-transform: uppercase; }
        .metric-val { font-size: 1.3rem; font-weight: bold; margin-top: 2px; }
        
        .metrics-sub { display: flex; justify-content: space-around; font-size: 0.85rem; color: #bdc3c7; border-top: 1px solid #1f2c3f; padding-top: 8px; }

        /* Cartão do Pedido de Corrida */
        .ride-card { background: #121c2c; border-radius: 16px; padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 15px; }
        .platform-badge { display: inline-block; background: #fff; color: #000; font-weight: bold; font-size: 0.75rem; padding: 3px 10px; border-radius: 6px; margin-bottom: 8px; }
        .ride-value { font-size: 1.8rem; font-weight: bold; color: #fff; margin-bottom: 5px; }
        
        .rating-badge { background: #1f2c3f; color: #f39c12; padding: 2px 8px; border-radius: 6px; font-size: 0.8rem; display: inline-flex; align-items: center; gap: 4px; }

        /* Linha de trajeto (Origem e Destino) */
        .route-line { margin-top: 12px; border-left: 2px solid #4f5d73; margin-left: 6px; padding-left: 15px; position: relative; }
        .route-point { margin-bottom: 10px; font-size: 0.85rem; }
        .route-point::before { content: ''; position: absolute; left: -5px; width: 8px; height: 8px; border-radius: 50%; background: #fff; }
        .route-point.dest::before { background: #f39c12; }
        .point-title { font-weight: bold; color: #fff; }
        .point-sub { color: #95a5a6; font-size: 0.75rem; }

        /* Formulário de Entrada Rápida */
        .form-card { background: #162235; padding: 15px; border-radius: 12px; }
        label { display: block; margin-top: 10px; font-size: 0.8rem; color: #95a5a6; }
        input, select { width: 100%; padding: 10px; margin-top: 4px; background: #0b131e; border: 1px solid #2c3e50; color: white; border-radius: 8px; box-sizing: border-box; font-size: 0.95rem; }
        
        button { width: 100%; background: #e67e22; color: white; border: none; padding: 12px; margin-top: 15px; border-radius: 8px; font-weight: bold; font-size: 1rem; cursor: pointer; }
        button:hover { background: #d35400; }

        .row { display: flex; gap: 10px; }
        .row > div { flex: 1; }

        /* Cores de indicador */
        .txt-green { color: #2ecc71; }
        .txt-yellow { color: #f39c12; }
        .txt-red { color: #e74c3c; }
    </style>
</head>
<body>

    <!-- PAINEL DE MÉTRICAS (Estilo GigU) -->
    {% if resultado %}
    <div class="metrics-card">
        <div class="metrics-grid">
            <div class="metric-item">
                <div>R$/km</div>
                <div class="metric-val txt-green">R$ {{ "%.2f"|format(resultado.ganho_km) }}</div>
            </div>
            <div class="metric-item">
                <div>R$/Hora</div>
                <div class="metric-val txt-yellow">R$ {{ "%.2f"|format(resultado.ganho_hora) }}</div>
            </div>
            <div class="metric-item">
                <div>Lucro Líquido</div>
                <div class="metric-val txt-green">R$ {{ "%.2f"|format(resultado.lucro) }}</div>
            </div>
        </div>
        <div class="metrics-sub">
            <span>⏱️ {{ minutos }} mins</span>
            <span>📍 {{ km }} Km</span>
            <span>⛽ Custo: R$ {{ "%.2f"|format(resultado.custo) }}</span>
        </div>
    </div>

    <!-- CARTÃO DO PEDIDO -->
    <div class="ride-card">
        <span class="platform-badge">{{ plataforma }}</span>
        <div class="ride-value">R$ {{ "%.2f"|format(valor) }}</div>
        <div class="rating-badge">⭐ {{ nota }}</div>

        <div class="route-line">
            <div class="route-point">
                <div class="point-title">Embarque</div>
                <div class="point-sub">{{ origem }}</div>
            </div>
            <div class="route-point dest">
                <div class="point-title">Destino</div>
                <div class="point-sub">{{ destino }}</div>
            </div>
        </div>
        <p style="text-align: center; margin-top: 12px; margin-bottom: 0; font-weight: bold; font-size: 0.9rem;" class="{{ resultado.classe }}">
            {{ resultado.veredito }}
        </p>
    </div>
    {% endif %}

    <!-- FORMULÁRIO DE ENTRADA -->
    <div class="form-card">
        <h2 style="color: #e67e22; font-size: 1.1rem; text-align: center; margin-top: 0;">GIRO 🚖 Copiloto</h2>
        <form method="POST">
            <div class="row">
                <div>
                    <label>Plataforma:</label>
                    <select name="plataforma">
                        <option value="Uber" {% if plataforma == 'Uber' %}selected{% endif %}>Uber</option>
                        <option value="99App" {% if plataforma == '99App' %}selected{% endif %}>99 App</option>
                    </select>
                </div>
                <div>
                    <label>Nota Passageiro:</label>
                    <input type="text" name="nota" value="{{ nota or '4.75' }}">
                </div>
            </div>

            <div class="row">
                <div>
                    <label>Valor (R$):</label>
                    <input type="text" name="valor" placeholder="Ex: 25.11" required value="{{ valor_str or '' }}">
                </div>
                <div>
                    <label>Distância (KM):</label>
                    <input type="text" name="km" placeholder="Ex: 11.65" required value="{{ km_str or '' }}">
                </div>
            </div>

            <div class="row">
                <div>
                    <label>Tempo (min):</label>
                    <input type="number" name="minutos" placeholder="Ex: 30" required value="{{ minutos_str or '' }}">
                </div>
                <div>
                    <label>Trânsito:</label>
                    <select name="transito">
                        <option value="normal">🟢 Fluido</option>
                        <option value="moderado">🟡 Moderado</option>
                        <option value="pesado">🔴 Lento / Pico</option>
                    </select>
                </div>
            </div>

            <label>Endereço de Embarque:</label>
            <input type="text" name="origem" placeholder="Ex: Estrada da Descoberta, 4896" value="{{ origem or 'Estrada da Descoberta, 4896' }}">

            <label>Endereço de Destino:</label>
            <input type="text" name="destino" placeholder="Ex: Ribeirão da Paixão, 5291" value="{{ destino or 'Ribeirão da Paixão, 5291' }}">

            <button type="submit">ANALISAR CORRIDA</button>
        </form>
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
    valor = 0.0
    km = 0.0
    minutos = 0
    nota = "4.75"
    plataforma = "Uber"
    origem = "Estrada da Descoberta, 4896"
    destino = "Ribeirão da Paixão, 5291"
    
    if request.method == "POST":
        try:
            plataforma = request.form.get("plataforma", "Uber")
            nota = request.form.get("nota", "4.75")
            valor_str = request.form.get("valor", "").replace(",", ".")
            km_str = request.form.get("km", "").replace(",", ".")
            minutos_str = request.form.get("minutos", "")
            transito = request.form.get("transito", "normal")
            origem = request.form.get("origem", "")
            destino = request.form.get("destino", "")
            
            valor = float(valor_str)
            km = float(km_str)
            minutos = int(minutos_str) if minutos_str else 0
            
            if km > 0:
                fator = 1.35 if transito == "pesado" else (1.15 if transito == "moderado" else 1.0)
                custo = km * (0.75 * fator)
                lucro = valor - custo
                ganho_km = valor / km
                ganho_hora = (lucro / minutos) * 60 if minutos > 0 else 0
                
                if ganho_km >= 2.00:
                    veredito = "🟢 EXCELENTE! Vale muito a pena."
                    classe = "txt-green"
                elif ganho_km >= 1.30:
                    veredito = "🟡 BOA. Razoável para o momento."
                    classe = "txt-yellow"
                else:
                    veredito = "🔴 RUIM! Prejuízo ou ganho baixo."
                    classe = "txt-red"
                    
                resultado = {
                    "lucro": lucro,
                    "ganho_km": ganho_km,
                    "ganho_hora": ganho_hora,
                    "custo": custo,
                    "veredito": veredito,
                    "classe": classe
                }
        except ValueError:
            pass
            
    return render_template_string(
        HTML_TEMPLATE,
        resultado=resultado,
        valor=valor,
        km=km,
        minutos=minutos,
        nota=nota,
        plataforma=plataforma,
        origem=origem,
        destino=destino,
        valor_str=valor_str,
        km_str=km_str,
        minutos_str=minutos_str
    )

if __name__ == "__main__":
    app.run(debug=True)
