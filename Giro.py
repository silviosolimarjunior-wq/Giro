<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIRO - Copiloto de Corridas</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b131e; color: #e0e0e0; padding: 12px; max-width: 450px; margin: auto; }
        .metrics-card { background: #121c2c; border: 2px solid #f39c12; border-radius: 16px; padding: 15px; margin-bottom: 15px; box-shadow: 0 6px 15px rgba(0,0,0,0.4); display: none; }
        .metrics-grid { display: flex; justify-content: space-between; text-align: center; margin-bottom: 10px; }
        .metric-item div:first-child { font-size: 0.75rem; color: #95a5a6; text-transform: uppercase; }
        .metric-val { font-size: 1.3rem; font-weight: bold; margin-top: 2px; }
        .metrics-sub { display: flex; justify-content: space-around; font-size: 0.85rem; color: #bdc3c7; border-top: 1px solid #1f2c3f; padding-top: 8px; }
        .ride-card { background: #121c2c; border-radius: 16px; padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 15px; display: none; }
        .platform-badge { display: inline-block; background: #fff; color: #000; font-weight: bold; font-size: 0.75rem; padding: 3px 10px; border-radius: 6px; margin-bottom: 8px; }
        .ride-value { font-size: 1.8rem; font-weight: bold; color: #fff; margin-bottom: 5px; }
        .rating-badge { background: #1f2c3f; color: #f39c12; padding: 2px 8px; border-radius: 6px; font-size: 0.8rem; display: inline-flex; align-items: center; gap: 4px; }
        .route-line { margin-top: 12px; border-left: 2px solid #4f5d73; margin-left: 6px; padding-left: 15px; position: relative; }
        .route-point { margin-bottom: 10px; font-size: 0.85rem; }
        .route-point::before { content: ''; position: absolute; left: -5px; width: 8px; height: 8px; border-radius: 50%; background: #fff; }
        .route-point.dest::before { background: #f39c12; }
        .point-title { font-weight: bold; color: #fff; }
        .point-sub { color: #95a5a6; font-size: 0.75rem; }
        .form-card { background: #162235; padding: 15px; border-radius: 12px; }
        label { display: block; margin-top: 10px; font-size: 0.8rem; color: #95a5a6; }
        input, select { width: 100%; padding: 10px; margin-top: 4px; background: #0b131e; border: 1px solid #2c3e50; color: white; border-radius: 8px; box-sizing: border-box; font-size: 0.95rem; }
        button { width: 100%; background: #e67e22; color: white; border: none; padding: 12px; margin-top: 15px; border-radius: 8px; font-weight: bold; font-size: 1rem; cursor: pointer; }
        button:hover { background: #d35400; }
        .row { display: flex; gap: 10px; }
        .row > div { flex: 1; }
        .txt-green { color: #2ecc71; }
        .txt-yellow { color: #f39c12; }
        .txt-red { color: #e74c3c; }
    </style>
</head>
<body>

    <!-- PAINEL DE MÉTRICAS -->
    <div id="metricsCard" class="metrics-card">
        <div class="metrics-grid">
            <div class="metric-item">
                <div>R$/km</div>
                <div id="resKm" class="metric-val txt-green">R$ 0,00</div>
            </div>
            <div class="metric-item">
                <div>R$/Hora</div>
                <div id="resHora" class="metric-val txt-yellow">R$ 0,00</div>
            </div>
            <div class="metric-item">
                <div>Lucro Líquido</div>
                <div id="resLucro" class="metric-val txt-green">R$ 0,00</div>
            </div>
        </div>
        <div class="metrics-sub">
            <span id="resTempo">⏱️ 0 mins</span>
            <span id="resDistancia">📍 0 Km</span>
            <span id="resCusto">⛽ Custo: R$ 0,00</span>
        </div>
    </div>

    <!-- CARTÃO DO PEDIDO -->
    <div id="rideCard" class="ride-card">
        <span id="resPlat" class="platform-badge">Uber</span>
        <div id="resValorTotal" class="ride-value">R$ 0,00</div>
        <div class="rating-badge">⭐ <span id="resNota">4.75</span></div>
        <div class="route-line">
            <div class="route-point">
                <div class="point-title">Embarque</div>
                <div id="resOrigem" class="point-sub">-</div>
            </div>
            <div class="route-point dest">
                <div class="point-title">Destino</div>
                <div id="resDestino" class="point-sub">-</div>
            </div>
        </div>
        <p id="resVeredito" style="text-align: center; margin-top: 12px; margin-bottom: 0; font-weight: bold; font-size: 0.9rem;"></p>
    </div>

    <!-- FORMULÁRIO DE ENTRADA -->
    <div class="form-card">
        <h2 style="color: #e67e22; font-size: 1.1rem; text-align: center; margin-top: 0;">GIRO 🚖 Copiloto</h2>
        <div class="row">
            <div>
                <label>Plataforma:</label>
                <select id="plataforma">
                    <option value="Uber">Uber</option>
                    <option value="99App">99 App</option>
                </select>
            </div>
            <div>
                <label>Nota Passageiro:</label>
                <input type="text" id="nota" value="4.75">
            </div>
        </div>

        <div class="row">
            <div>
                <label>Valor (R$):</label>
                <input type="text" id="valor" placeholder="Ex: 25.11">
            </div>
            <div>
                <label>Distância (KM):</label>
                <input type="text" id="km" placeholder="Ex: 11.65">
            </div>
        </div>

        <div class="row">
            <div>
                <label>Tempo (min):</label>
                <input type="number" id="minutos" placeholder="Ex: 30">
            </div>
            <div>
                <label>Trânsito:</label>
                <select id="transito">
                    <option value="normal">🟢 Fluido</option>
                    <option value="moderado">🟡 Moderado</option>
                    <option value="pesado">🔴 Lento / Pico</option>
                </select>
            </div>
        </div>

        <label>Endereço de Embarque:</label>
        <input type="text" id="origem" value="Estrada da Descoberta, 4896">

        <label>Endereço de Destino:</label>
        <input type="text" id="destino" value="Ribeirão da Paixão, 5291">

        <button onclick="analisarCorrida()">ANALISAR CORRIDA</button>
    </div>

    <script>
        function analisarCorrida() {
            let plataforma = document.getElementById('plataforma').value;
            let nota = document.getElementById('nota').value;
            let valor = parseFloat(document.getElementById('valor').value.replace(',', '.')) || 0;
            let km = parseFloat(document.getElementById('km').value.replace(',', '.')) || 0;
            let minutos = parseInt(document.getElementById('minutos').value) || 0;
            let transito = document.getElementById('transito').value;
            let origem = document.getElementById('origem').value;
            let destino = document.getElementById('destino').value;

            if (km <= 0 || valor <= 0) {
                alert('Por favor, insira valores válidos para o valor e a distância.');
                return;
            }

            let fator = transito === 'pesado' ? 1.35 : (transito === 'moderado' ? 1.15 : 1.0);
            let custo = km * (0.75 * fator);
            let lucro = valor - custo;
            let ganho_km = valor / km;
            let ganho_hora = minutos > 0 ? (lucro / minutos) * 60 : 0;

            let veredito = "";
            let classe = "";
            if (ganho_km >= 2.00) {
                veredito = "🟢 EXCELENTE! Vale muito a pena.";
                classe = "txt-green";
            } else if (ganho_km >= 1.30) {
                veredito = "🟡 BOA. Razoável para o momento.";
                classe = "txt-yellow";
            } else {
                veredito = "🔴 RUIM! Prejuízo ou ganho baixo.";
                classe = "txt-red";
            }

            // Atualizar UI
            document.getElementById('resKm').innerText = `R$ ${ganho_km.toFixed(2)}`;
            document.getElementById('resHora').innerText = `R$ ${ganho_hora.toFixed(2)}`;
            document.getElementById('resLucro').innerText = `R$ ${lucro.toFixed(2)}`;
            document.getElementById('resTempo').innerText = `⏱️ ${minutos} mins`;
            document.getElementById('resDistancia').innerText = `📍 ${km} Km`;
            document.getElementById('resCusto').innerText = `⛽ Custo: R$ ${custo.toFixed(2)}`;

            document.getElementById('resPlat').innerText = plataforma;
            document.getElementById('resValorTotal').innerText = `R$ ${valor.toFixed(2)}`;
            document.getElementById('resNota').innerText = nota;
            document.getElementById('resOrigem').innerText = origem;
            document.getElementById('resDestino').innerText = destino;
            
            let elemVeredito = document.getElementById('resVeredito');
            elemVeredito.innerText = veredito;
            elemVeredito.className = classe;

            document.getElementById('metricsCard').style.display = 'block';
            document.getElementById('rideCard').style.display = 'block';
        }
    </script>
</body>
</html>
