# src/engine.py
# Motor de análise da Mission Control AI — NavBR-1
# Trilha: MobilitySat — GNSS e Mobilidade
# Global Solution 2026.1 — FIAP

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

from src.telemetria import coletar, formatar_telemetria
from src.alertas import avaliar

load_dotenv()

# Identificação da trilha
TRILHA = "mobilitysat"


def llm(prompt: str, system: str = None, max_tokens: int = 800, temperature: float = 0.3) -> str:
    """Envia prompt ao gpt-oss:120b via Ollama Cloud e retorna resposta em texto."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            "https://ollama.com/api/chat",
            headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")},
            json={
                "model": "gpt-oss:120b",
                "messages": messages,
                "stream": False,
                "options": {"num_predict": max_tokens, "temperature": temperature}
            }
        )
        return response.json()["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt() -> str:
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de monitoramento de satélite GNSS."


class MissionEngine:
    """Motor central da Mission Control AI — integra telemetria, alertas e IA."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.historico = []          # histórico de ciclos para memória de contexto
        self.modo_simulacao = "aleatorio"  # modo padrão de simulação

    def is_ready(self) -> bool:
        """Retorna True quando o motor está implementado e pronto."""
        return True

    def set_modo(self, modo: str):
        """
        Define o modo de simulação da telemetria.
        Modos: normal | atencao | critico | emergencia | aleatorio
        """
        modos_validos = ["normal", "atencao", "critico", "emergencia", "aleatorio"]
        if modo in modos_validos:
            self.modo_simulacao = modo
            return f"✅ Modo de simulação alterado para: {modo.upper()}"
        return f"❌ Modo inválido. Use: {', '.join(modos_validos)}"

    def status_snapshot(self) -> str:
        """Coleta telemetria atual e retorna resumo do estado da missão."""
        dados = coletar(self.modo_simulacao)
        relatorio = avaliar(dados)

        telemetria_txt = formatar_telemetria(dados)
        resumo_alertas = relatorio["resumo"]

        return f"{telemetria_txt}\n\n{resumo_alertas}"

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Analisa a pergunta do operador com base na telemetria atual + alertas + IA.

        Fluxo:
            1. Coleta dados via telemetria.coletar()
            2. Avalia alertas via alertas.avaliar()
            3. Monta prompt com dados + alertas + histórico + pergunta
            4. Chama llm() com system prompt da missão
            5. Armazena no histórico e retorna resposta
        """

        # 1. Coletar telemetria
        dados = coletar(self.modo_simulacao)

        # 2. Avaliar alertas
        relatorio = avaliar(dados)

        # 3. Montar contexto para o prompt
        telemetria_txt = formatar_telemetria(dados)
        alertas_txt = relatorio["resumo"]
        acoes_txt = ""
        if relatorio["acoes_automaticas"]:
            acoes_txt = "\n".join(relatorio["acoes_automaticas"])

        # Histórico dos últimos 3 ciclos (memória de contexto)
        historico_txt = ""
        if self.historico:
            ultimos = self.historico[-3:]
            historico_txt = "📋 Histórico dos últimos ciclos:\n"
            for ciclo in ultimos:
                historico_txt += f"  [{ciclo['timestamp']}] Nível: {ciclo['nivel']} | "
                historico_txt += f"drift={ciclo['drift']} ns/dia | "
                historico_txt += f"potencia={ciclo['potencia']}%\n"

        # 4. Montar prompt completo
        prompt = f"""
{telemetria_txt}

{alertas_txt}

{acoes_txt}

{historico_txt}

Pergunta do operador: {pergunta_usuario}

Com base nos dados de telemetria acima e nos alertas detectados, responda à pergunta do operador seguindo o formato de resposta obrigatório definido no seu papel de ARIA.
""".strip()

        # 5. Chamar IA
        resposta = llm(prompt, system=self.system_prompt)

        # 6. Armazenar no histórico
        self.historico.append({
            "timestamp": dados.get("timestamp", ""),
            "nivel": relatorio["nivel"],
            "drift": dados.get("drift_oscilador", 0),
            "potencia": dados.get("margem_potencia", 0),
            "pergunta": pergunta_usuario,
        })

        return resposta