# src/alertas.py
# Lógica de alertas e thresholds do satélite NavBR-1
# Trilha: MobilitySat — GNSS e Mobilidade
# Global Solution 2026.1 — FIAP

from src.telemetria import LIMITES_CRITICOS, FAIXAS_NOMINAIS

# Níveis de severidade
NOMINAL    = "NOMINAL"
ATENCAO    = "ATENCAO"
CRITICO    = "CRITICO"
EMERGENCIA = "EMERGENCIA"

# Emojis por nível
EMOJI_NIVEL = {
    NOMINAL:    "🟢",
    ATENCAO:    "🟡",
    CRITICO:    "🔴",
    EMERGENCIA: "⚫",
}


def avaliar(dados: dict) -> dict:
    """
    Avalia os dados de telemetria e retorna um relatório de alertas.

    Retorna:
        dict com:
            - nivel (str): severidade geral da missão
            - alertas (list): lista de alertas disparados
            - acoes_automaticas (list): ações automáticas acionadas
            - resumo (str): texto resumido para exibição no terminal
    """
    alertas = []
    acoes_automaticas = []

    # --- Avalia cada parâmetro ---

    drift = dados.get("drift_oscilador", 0)
    if drift > LIMITES_CRITICOS["drift_oscilador"]["max"]:
        alertas.append({
            "parametro": "drift_oscilador",
            "valor": drift,
            "mensagem": f"Drift do oscilador CRÍTICO: {drift} ns/dia (limite: 5.0)",
            "severidade": CRITICO,
        })
    elif drift > FAIXAS_NOMINAIS["drift_oscilador"][1]:
        alertas.append({
            "parametro": "drift_oscilador",
            "valor": drift,
            "mensagem": f"Drift do oscilador elevado: {drift} ns/dia (nominal: ≤ 2.0)",
            "severidade": ATENCAO,
        })

    sync = dados.get("sync_constelacao", 100)
    if sync < LIMITES_CRITICOS["sync_constelacao"]["min"]:
        alertas.append({
            "parametro": "sync_constelacao",
            "valor": sync,
            "mensagem": f"Sincronização com constelação CRÍTICA: {sync}% (limite: 85%)",
            "severidade": CRITICO,
        })
    elif sync < FAIXAS_NOMINAIS["sync_constelacao"][0]:
        alertas.append({
            "parametro": "sync_constelacao",
            "valor": sync,
            "mensagem": f"Sincronização com constelação baixa: {sync}% (nominal: ≥ 95%)",
            "severidade": ATENCAO,
        })

    sinal_l1 = dados.get("integridade_sinal_L1", -126.0)
    if sinal_l1 < LIMITES_CRITICOS["integridade_sinal_L1"]["min"]:
        alertas.append({
            "parametro": "integridade_sinal_L1",
            "valor": sinal_l1,
            "mensagem": f"Sinal L1 CRÍTICO: {sinal_l1} dBW (limite: -131.0)",
            "severidade": CRITICO,
        })
    elif sinal_l1 < FAIXAS_NOMINAIS["integridade_sinal_L1"][0]:
        alertas.append({
            "parametro": "integridade_sinal_L1",
            "valor": sinal_l1,
            "mensagem": f"Sinal L1 degradado: {sinal_l1} dBW (nominal: ≥ -128.5)",
            "severidade": ATENCAO,
        })

    sinal_l5 = dados.get("integridade_sinal_L5", -123.0)
    if sinal_l5 < LIMITES_CRITICOS["integridade_sinal_L5"]["min"]:
        alertas.append({
            "parametro": "integridade_sinal_L5",
            "valor": sinal_l5,
            "mensagem": f"Sinal L5 CRÍTICO: {sinal_l5} dBW (limite: -128.0)",
            "severidade": CRITICO,
        })
        # Ação automática: suspender operações de veículos autônomos
        acoes_automaticas.append(
            "🚨 AÇÃO AUTOMÁTICA: Sinal L5 inoperante — protocolo de suspensão de "
            "veículos autônomos acionado automaticamente."
        )

    efemeride = dados.get("precisao_efemeride", 0.5)
    if efemeride > LIMITES_CRITICOS["precisao_efemeride"]["max"]:
        alertas.append({
            "parametro": "precisao_efemeride",
            "valor": efemeride,
            "mensagem": f"Precisão da efeméride CRÍTICA: {efemeride} m (limite: 3.0 m)",
            "severidade": CRITICO,
        })
        # Ação automática: suspender operações RTK
        acoes_automaticas.append(
            "🚨 AÇÃO AUTOMÁTICA: Efeméride degradada — operações RTK "
            "(plantadeiras e drones autônomos) suspensas automaticamente."
        )
    elif efemeride > FAIXAS_NOMINAIS["precisao_efemeride"][1]:
        alertas.append({
            "parametro": "precisao_efemeride",
            "valor": efemeride,
            "mensagem": f"Precisão da efeméride elevada: {efemeride} m (nominal: ≤ 1.5 m)",
            "severidade": ATENCAO,
        })

    potencia = dados.get("margem_potencia", 70)
    if potencia < LIMITES_CRITICOS["margem_potencia"]["min"]:
        alertas.append({
            "parametro": "margem_potencia",
            "valor": potencia,
            "mensagem": f"Margem de potência CRÍTICA: {potencia}% (limite: 15%)",
            "severidade": CRITICO,
        })
        # Ação automática: ativar modo economia de energia
        acoes_automaticas.append(
            f"🚨 AÇÃO AUTOMÁTICA: Potência em {potencia}% — "
            "modo de economia de energia ativado. Payload em operação reduzida."
        )
    elif potencia < FAIXAS_NOMINAIS["margem_potencia"][0]:
        alertas.append({
            "parametro": "margem_potencia",
            "valor": potencia,
            "mensagem": f"Margem de potência baixa: {potencia}% (nominal: ≥ 30%)",
            "severidade": ATENCAO,
        })

    temp = dados.get("temperatura_payload", 20)
    if temp > LIMITES_CRITICOS["temperatura_payload"]["max"]:
        alertas.append({
            "parametro": "temperatura_payload",
            "valor": temp,
            "mensagem": f"Temperatura do payload CRÍTICA (alta): {temp}°C (limite: 60°C)",
            "severidade": CRITICO,
        })
    elif temp < LIMITES_CRITICOS["temperatura_payload"]["min"]:
        alertas.append({
            "parametro": "temperatura_payload",
            "valor": temp,
            "mensagem": f"Temperatura do payload CRÍTICA (baixa): {temp}°C (limite: -20°C)",
            "severidade": CRITICO,
        })
    elif temp > FAIXAS_NOMINAIS["temperatura_payload"][1]:
        alertas.append({
            "parametro": "temperatura_payload",
            "valor": temp,
            "mensagem": f"Temperatura do payload elevada: {temp}°C (nominal: ≤ 45°C)",
            "severidade": ATENCAO,
        })

    # --- Determina nível geral ---
    nivel = _determinar_nivel(alertas)

    # --- Monta resumo para exibição ---
    resumo = _montar_resumo(nivel, alertas, acoes_automaticas)

    return {
        "nivel": nivel,
        "emoji": EMOJI_NIVEL[nivel],
        "alertas": alertas,
        "acoes_automaticas": acoes_automaticas,
        "resumo": resumo,
    }


def _determinar_nivel(alertas: list) -> str:
    """Determina o nível geral de severidade com base nos alertas."""
    if not alertas:
        return NOMINAL

    severidades = [a["severidade"] for a in alertas]

    # Emergência: 3 ou mais parâmetros críticos simultaneamente
    criticos = severidades.count(CRITICO)
    if criticos >= 3:
        return EMERGENCIA

    if CRITICO in severidades:
        return CRITICO

    if ATENCAO in severidades:
        return ATENCAO

    return NOMINAL


def _montar_resumo(nivel: str, alertas: list, acoes: list) -> str:
    """Monta texto de resumo dos alertas para exibição no terminal."""
    emoji = EMOJI_NIVEL[nivel]
    linhas = [f"{emoji} Status geral: {nivel}"]

    if not alertas:
        linhas.append("  ✅ Todos os parâmetros dentro do nominal.")
    else:
        linhas.append(f"  ⚠️  {len(alertas)} alerta(s) detectado(s):")
        for alerta in alertas:
            e = "🔴" if alerta["severidade"] == CRITICO else "🟡"
            linhas.append(f"    {e} {alerta['mensagem']}")

    if acoes:
        linhas.append("")
        for acao in acoes:
            linhas.append(f"  {acao}")

    return "\n".join(linhas)
