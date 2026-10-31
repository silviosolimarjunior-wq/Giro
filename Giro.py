import json
import os

CONFIG_FILE = "giro_config.json"

# Cores ANSI para o terminal do Termux
COR_VERDE = "\033[92m"
COR_AMARELO = "\033[93m"
COR_VERMELHO = "\033[91m"
COR_AZUL = "\033[94m"
COR_RESET = "\033[0m"


def carregar_config():
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
      return json.load(f)
  return {"meta_diaria": 150.0, "custo_km": 0.75}


def salvar_config(config):
  with open(CONFIG_FILE, "w") as f:
    json.dump(config, f, indent=4)


def main():
  config = carregar_config()

  print(f"{COR_AZUL}========================================={COR_RESET}")
  print(f"{COR_AZUL}        GIRO - COPILOTO DE CORRIDAS      {COR_RESET}")
  print(f"{COR_AZUL}========================================={COR_RESET}")
  print(f"Meta Diária Atual: R$ {config['meta_diaria']:.2f}")
  print(f"Custo Médio por KM: R$ {config['custo_km']:.2f}\n")

  try:
    valor_corrida = float(
        input("Digite o valor oferecido pela corrida (R$): ")
        .replace(",", ".")
    )
    km_total = float(
        input("Digite a distância total (KM - até o passageiro + destino): ")
        .replace(",", ".")
    )
  except ValueError:
    print(f"{COR_VERMELHO}Erro: Digite apenas números válidos!{COR_RESET}")
    return

  if km_total <= 0:
    print(
        f"{COR_VERMELHO}Erro: A distância em KM deve ser maior que zero.{COR_RESET}"
    )
    return

  # Cálculos
  ganho_por_km = valor_corrida / km_total
  custo_estimado = km_total * config["custo_km"]
  lucro_liquido = valor_corrida - custo_estimado

  print(f"\n{COR_AZUL}--- ANÁLISE DA CORRIDA ---{COR_RESET}")
  print(f"Valor Bruto: R$ {valor_corrida:.2f}")
  print(f"Custo Estimado (Combustível/Desgaste): R$ {custo_estimado:.2f}")
  print(f"Lucro Líquido Estimado: R$ {lucro_liquido:.2f}")
  print(f"Retorno por KM: R$ {ganho_por_km:.2f} por KM")

  # Avaliação baseada no ganho por KM
  print(f"\n{COR_AZUL}--- VEREDITO DO GIRO ---{COR_RESET}")
  if ganho_por_km >= 2.00:
    print(
        f"{COR_VERDE}🟢 EXCELENTE! Corrida altamente lucrativa. Aceita na hora!{COR_RESET}"
    )
  elif ganho_por_km >= 1.30:
    print(
        f"{COR_AMARELO}🟡 BOA/RAZOÁVEL. Vale a pena se estiver indo para uma zona de movimento.{COR_RESET}"
    )
  else:
    print(
        f"{COR_VERMELHO}🔴 RUIM! Abaixo do ideal. Vais pagar para trabalhar.{COR_RESET}"
    )

  print(f"{COR_AZUL}========================================={COR_RESET}")


if __name__ == "__main__":
  main()
