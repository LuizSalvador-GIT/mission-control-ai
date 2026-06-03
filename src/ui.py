# src/ui.py
# Interface CLI estilo Claude Code — Mission Control AI
# Trilha: MobilitySat — GNSS e Mobilidade
# Global Solution 2026.1 — FIAP

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))

COMANDOS = {
    "/help":       "Exibe esta tabela de comandos",
    "/status":     "Mostra snapshot atual da telemetria e alertas",
    "/modo":       "Altera modo de simulação: normal | atencao | critico | emergencia | aleatorio",
    "/historico":  "Exibe histórico dos ciclos analisados",
    "/about":      "Informações sobre o projeto e o grupo",
    "/clear":      "Limpa a tela e exibe o banner novamente",
    "/exit":       "Encerra o sistema",
}


def show_banner():
    """Exibe o banner ASCII e o card de boas-vindas."""
    console.clear()

    # Banner ASCII em duas linhas
    linha1 = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("NavBR-1", font="ansi_shadow")

    console.print(Align.center(Text(linha1, style="bold #06B6D4")))
    console.print(Align.center(Text(linha2, style="bold #A855F7")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP · MobilitySat 🚗 ──",
             style="italic #8484A0")
    ))
    console.print()

    # Card de boas-vindas
    console.print(Panel.fit(
        "[bold #06B6D4]Bem-vindo à Mission Control AI — NavBR-1[/]\n"
        "Sistema de monitoramento GNSS com análise por IA generativa.\n"
        "[dim]Satélite:[/] NavBR-1 · MEO ~20.200 km · Sinais L1/L5\n"
        "[dim]Modelo:[/]   gpt-oss:120b via Ollama Cloud\n"
        "[dim]Use[/] [bold]/help[/] [dim]para ver os comandos · [bold]/exit[/] [dim]para sair.",
        title="◆ MISSION CONTROL AI",
        border_style="#06B6D4",
    ))
    console.print()


def show_response(text: str):
    """Renderiza a resposta da IA em painel com timestamp."""
    agora = datetime.now().strftime("%H:%M:%S")
    console.print(Panel(
        text,
        title="[bold #A855F7]◆ ARIA — NavBR-1[/]",
        subtitle=f"[dim]{agora}[/]",
        border_style="#A855F7",
        padding=(1, 2),
    ))
    console.print()


def show_status(texto: str):
    """Renderiza o status da telemetria em painel destacado."""
    agora = datetime.now().strftime("%H:%M:%S")
    console.print(Panel(
        texto,
        title="[bold #06B6D4]◆ STATUS — NavBR-1[/]",
        subtitle=f"[dim]{agora}[/]",
        border_style="#06B6D4",
        padding=(1, 2),
    ))
    console.print()


def show_help():
    """Exibe tabela de comandos disponíveis."""
    tabela = Table(title="Comandos disponíveis", border_style="#06B6D4", show_lines=True)
    tabela.add_column("Comando", style="bold #06B6D4", no_wrap=True)
    tabela.add_column("Descrição", style="white")

    for cmd, desc in COMANDOS.items():
        tabela.add_row(cmd, desc)

    console.print(tabela)
    console.print()


def show_historico(historico: list):
    """Exibe histórico de ciclos analisados."""
    if not historico:
        console.print("[yellow]  ⚠ Nenhum ciclo analisado ainda.[/]\n")
        return

    tabela = Table(title="Histórico de ciclos", border_style="#8484A0", show_lines=True)
    tabela.add_column("#", style="dim", width=4)
    tabela.add_column("Timestamp", style="dim")
    tabela.add_column("Nível", style="bold")
    tabela.add_column("Drift (ns/dia)", justify="right")
    tabela.add_column("Potência (%)", justify="right")

    cores = {"NOMINAL": "green", "ATENCAO": "yellow", "CRITICO": "red", "EMERGENCIA": "white on red"}

    for i, ciclo in enumerate(historico, 1):
        nivel = ciclo.get("nivel", "?")
        cor = cores.get(nivel, "white")
        tabela.add_row(
            str(i),
            ciclo.get("timestamp", ""),
            f"[{cor}]{nivel}[/]",
            str(ciclo.get("drift", "")),
            str(ciclo.get("potencia", "")),
        )

    console.print(tabela)
    console.print()


def show_about():
    """Exibe informações sobre o projeto."""
    console.print(Panel.fit(
        "[bold]Mission Control AI — NavBR-1[/]\n"
        "[dim]Global Solution 2026.1 · FIAP · Ciência da Computação[/]\n\n"
        "[bold #06B6D4]Trilha:[/] 🚗 MobilitySat — GNSS e Mobilidade\n"
        "[bold #06B6D4]Satélite:[/] NavBR-1 (simulado) · MEO · L1/L5\n"
        "[bold #06B6D4]IA:[/] ARIA via gpt-oss:120b · Ollama Cloud\n"
        "[bold #06B6D4]Disciplina:[/] Prompt Engineering and Artificial Intelligence\n\n"
        "[dim]Parâmetros monitorados:[/] drift do oscilador, sincronização com\n"
        "constelação, integridade L1/L5, precisão da efeméride,\n"
        "margem de potência, temperatura do payload.",
        title="◆ SOBRE O PROJETO",
        border_style="#8484A0",
    ))
    console.print()


def run_cli(engine):
    """Loop principal da interface CLI."""
    show_banner()

    # Aviso se engine não estiver pronto
    if not engine.is_ready():
        console.print(
            "  [yellow]⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗[/]\n"
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando Mission Control AI...[/]")
            break

        if not user_input:
            continue

        # --- Comandos especiais ---

        if user_input == "/exit":
            console.print("[dim]Encerrando Mission Control AI. Até logo! 🚀[/]")
            break

        elif user_input == "/help":
            show_help()

        elif user_input == "/status":
            console.print("[dim]Coletando telemetria...[/]")
            snapshot = engine.status_snapshot()
            show_status(snapshot)

        elif user_input == "/historico":
            show_historico(engine.historico)

        elif user_input == "/about":
            show_about()

        elif user_input == "/clear":
            show_banner()

        elif user_input.startswith("/modo"):
            partes = user_input.split()
            if len(partes) < 2:
                console.print(
                    "[yellow]  Use: /modo [normal|atencao|critico|emergencia|aleatorio][/]\n"
                )
            else:
                resultado = engine.set_modo(partes[1].lower())
                console.print(f"  {resultado}\n")

        # --- Entrada livre para análise da IA ---
        else:
            with console.status("[dim]ARIA analisando...[/]", spinner="dots"):
                resposta = engine.analyze(user_input)
            show_response(resposta)
