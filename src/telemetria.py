# src/telemetria.py
# Geração de dados simulados de telemetria do satélite NavBR-1
# Trilha: MobilitySat — GNSS e Mobilidade
# Global Solution 2026.1 — FIAP

import random
from datetime import datetime

# Faixas nominais de cada parâmetro
FAIXAS_NOMINAIS = {
    "drift_oscilador":     (0.0, 2.0),
    "sync_constelacao":    (95.0, 100.0),
    "integridade_sinal_L1": (-128.5, -125.0),
    "integridade_sinal_L5": (-125.5, -122.0),
    "precisao_efemeride":  (0.0, 1.5),
    "margem_potencia":     (30.0, 100.0),
    "temperatura_payload": (-10.0, 45.0),
}

# Limites críticos de cada parâmetro
LIMITES_CRITICOS = {
    "drift_oscilador":      {"max": 5.0},
    "sync_constelacao":     {"min": 85.0},
    "integridade_sinal_L1": {"min": -131.0},
    "integridade_sinal_L5": {"min": -128.0},
    "precisao_efemeride":   {"max": 3.0},
    "margem_potencia":      {"min": 15.0},
    "temperatura_payload":  {"min": -20.0, "max": 60.0},
}

# Unidades de cada parâmetro (para exibição)
UNIDADES = {
    "drift_oscilador":      "ns/dia",
    "sync_constelacao":     "%",
    "integridade_sinal_L1": "dBW",
    "integridade_sinal_L5": "dBW",
    "precisao_efemeride":   "m",
    "margem_potencia":      "%",
    "temperatura_payload":  "°C",
}


def coletar(modo: str = "normal") -> dict:
    """
    Gera dados simulados de telemetria do NavBR-1.

    Parâmetros:
        modo (str): Define o cenário simulado.
            - "normal"     : todos os parâmetros dentro do nominal
            - "atencao"    : parâmetros se aproximando dos limites
            - "critico"    : um ou mais parâmetros fora do nominal
            - "emergencia" : falha múltipla — risco de perda de missão
            - "aleatorio"  : sorteia um modo aleatoriamente

    Retorna:
        dict com os valores dos parâmetros + timestamp
    """

    if modo == "aleatorio":
        modo = random.choice(["normal", "normal", "atencao", "critico", "emergencia"])

    if modo == "normal":
        dados = {
            "drift_oscilador":      round(random.uniform(0.2, 1.8), 2),
            "sync_constelacao":     round(random.uniform(96.0, 99.9), 1),
            "integridade_sinal_L1": round(random.uniform(-128.0, -125.5), 1),
            "integridade_sinal_L5": round(random.uniform(-125.0, -122.5), 1),
            "precisao_efemeride":   round(random.uniform(0.1, 1.3), 2),
            "margem_potencia":      round(random.uniform(40.0, 85.0), 1),
            "temperatura_payload":  round(random.uniform(5.0, 38.0), 1),
        }

    elif modo == "atencao":
        dados = {
            "drift_oscilador":      round(random.uniform(2.5, 4.0), 2),
            "sync_constelacao":     round(random.uniform(88.0, 94.0), 1),
            "integridade_sinal_L1": round(random.uniform(-130.0, -128.5), 1),
            "integridade_sinal_L5": round(random.uniform(-127.5, -125.5), 1),
            "precisao_efemeride":   round(random.uniform(1.6, 2.5), 2),
            "margem_potencia":      round(random.uniform(18.0, 29.0), 1),
            "temperatura_payload":  round(random.uniform(46.0, 55.0), 1),
        }

    elif modo == "critico":
        dados = {
            "drift_oscilador":      round(random.uniform(5.1, 8.0), 2),
            "sync_constelacao":     round(random.uniform(85.0, 91.0), 1),
            "integridade_sinal_L1": round(random.uniform(-131.5, -130.0), 1),
            "integridade_sinal_L5": round(random.uniform(-129.0, -128.0), 1),
            "precisao_efemeride":   round(random.uniform(2.6, 4.0), 2),
            "margem_potencia":      round(random.uniform(10.0, 17.0), 1),
            "temperatura_payload":  round(random.uniform(56.0, 65.0), 1),
        }

    elif modo == "emergencia":
        dados = {
            "drift_oscilador":      round(random.uniform(9.0, 15.0), 2),
            "sync_constelacao":     round(random.uniform(60.0, 84.0), 1),
            "integridade_sinal_L1": round(random.uniform(-135.0, -132.0), 1),
            "integridade_sinal_L5": round(random.uniform(-133.0, -130.0), 1),
            "precisao_efemeride":   round(random.uniform(4.5, 8.0), 2),
            "margem_potencia":      round(random.uniform(3.0, 10.0), 1),
            "temperatura_payload":  round(random.uniform(65.0, 80.0), 1),
        }

    else:
        # Fallback para modo normal
        return coletar("normal")

    dados["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["modo_simulado"] = modo
    return dados


def formatar_telemetria(dados: dict) -> str:
    """
    Formata os dados de telemetria em texto legível para injeção no prompt.
    """
    linhas = [f"📡 Telemetria NavBR-1 — {dados.get('timestamp', 'N/A')}"]
    linhas.append(f"Modo simulado: {dados.get('modo_simulado', 'desconhecido').upper()}")
    linhas.append("─" * 45)

    parametros = [k for k in dados if k not in ("timestamp", "modo_simulado")]
    for param in parametros:
        valor = dados[param]
        unidade = UNIDADES.get(param, "")
        linhas.append(f"  {param}: {valor} {unidade}")

    return "\n".join(linhas)
