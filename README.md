# mission-control-ai
Global Solution 2026.1 — FIAP · MobilitySat · NavBR-1
# 🚀 Mission Control AI — NavBR-1

> Sistema de monitoramento de missão espacial com análise por IA generativa.
> O NavBR-1 é um satélite GNSS simulado em órbita média (MEO) que emite sinais de navegação L1/L5
> para receptores em território brasileiro. A ARIA — nossa IA embarcada — monitora a telemetria em
> tempo real, detecta anomalias e traduz cada alerta em impacto concreto para os setores de
> logística, agricultura de precisão e mobilidade autônoma.

---

## 👥 Integrantes

| Nome | RM | Turma |
|---|---|---|
| Luiz Cesar Conti Salvador | 571305 | 1CCPH |
| Victor do Prado Manzini | 572123 | 1CCPH |
| Guilherme de Oliveira Santos | 572195 | 1CCPH |

---

## 🛰️ O que o projeto faz

O **Mission Control AI** é uma CLI (interface de linha de comando) que simula o centro de controle
do satélite NavBR-1. O sistema:

- Gera dados simulados de telemetria com 7 parâmetros monitorados (drift do oscilador atômico,
sincronização com a constelação, integridade dos sinais L1/L5, precisão da efeméride, margem de
potência e temperatura do payload)
- Detecta anomalias automaticamente via lógica Python com thresholds definidos
- Aciona respostas automáticas em situações críticas (suspensão de operações RTK, modo economia
de energia, protocolo de veículos autônomos)
- Usa IA generativa (ARIA) via Ollama Cloud para analisar a telemetria em linguagem natural
- Articula o impacto terrestre de cada anomalia nos setores de logística, agricultura de precisão
e mobilidade autônoma

---

## 🎭 Persona atendida

**ARIA** (Autonomous Response and Intelligence Analyst) é a assistente de missão do CCM Brasil.
Ela fala diretamente com o engenheiro de operações do segmento espacial durante turnos de
monitoramento, interpretando dados técnicos e traduzindo cada anomalia em consequências concretas
para os usuários terrestres do sinal NavBR-1.

---

## 🗂️ Trilha

**🚗 MobilitySat — GNSS e Mobilidade**

Satélite simulado: NavBR-1 (GNSS, MEO, ~20.200 km)
Setor de impacto: Mobilidade e logística — frotas otimizadas, agricultura de precisão, base para
veículos autônomos.

---

## 🛠️ Tecnologias utilizadas

- Python 3.11+
- Ollama Cloud API — modelo `gpt-oss:120b`
- `ollama` — cliente oficial Python para Ollama Cloud
- `rich` — renderização de painéis e tabelas no terminal
- `prompt-toolkit` — input editável com histórico
- `pyfiglet` — banner ASCII art
- `python-dotenv` — gerenciamento seguro de credenciais
- `requests` — chamadas HTTP à API do Ollama

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/LuizSalvador-GIT/mission-control-ai.git
cd mission-control-ai
```

### 2. Crie o ambiente virtual (recomendado)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as credenciais

Crie um arquivo `.env` na raiz do projeto com:

```
OLLAMA_API_KEY=sua_chave_aqui
```

> Obtenha sua chave gratuita em [ollama.com/settings/api-keys](https://ollama.com/settings/api-keys)

### 5. Execute o sistema

```bash
python main.py
```

---

## 💬 Comandos disponíveis na CLI

| Comando | Descrição |
|---|---|
| `/status` | Mostra snapshot atual da telemetria e alertas |
| `/modo [modo]` | Altera simulação: `normal` \| `atencao` \| `critico` \| `emergencia` \| `aleatorio` |
| `/historico` | Exibe histórico dos ciclos analisados |
| `/about` | Informações sobre o projeto |
| `/clear` | Limpa a tela |
| `/help` | Lista todos os comandos |
| `/exit` | Encerra o sistema |

---

## 🖥️ Demonstração

### Banner inicial e interface CLI

![Banner inicial do sistema](assets/screenshot_banner.png)

### Análise da IA em situação de atenção

![ARIA analisando telemetria com alertas](assets/screenshot_analise.png)

---

## 🧠 System Prompt

O system prompt completo está em [`prompts/system_prompt.md`](prompts/system_prompt.md).

Ele define:
- Papel e identidade da ARIA
- Contexto da missão NavBR-1
- Tabela de parâmetros com faixas nominais e limites críticos
- Setores terrestres impactados (frotas, RTK, veículos autônomos)
- 4 níveis de severidade (Nominal / Atenção / Crítico / Emergência)
- Formato de resposta obrigatório
- 2 exemplos few-shot (nominal e crítico)

---

## 🧪 Cenários de teste demonstrados

1. **Operação normal** — todos os parâmetros dentro do nominal, missão estável
2. **Atenção** — drift do oscilador elevado, sincronização degradada, efeméride fora do nominal
3. **Crítico** — potência abaixo de 15%, sinal L5 inoperante, protocolo de suspensão acionado
4. **Emergência** — falha múltipla simultânea, risco de perda de missão

---

## 💼 Proposta de valor / modelo de negócio

### 1. Problema real terrestre que esta missão resolve

O Brasil depende de sinais GNSS externos (GPS americano, Galileo europeu) para operações críticas
de logística, agricultura de precisão e mobilidade. Uma falha ou degradação desses sinais impacta
diretamente frotas de transporte, plantadeiras autônomas e projetos de mobilidade urbana — sem
que os operadores terrestres sejam alertados com clareza sobre a causa e a gravidade do problema.
O NavBR-1 resolve isso com monitoramento inteligente e análise contextualizada em tempo real.

### 2. Quem paga pela solução?

Modelo híbrido:
- **Setor privado:** operadoras de frotas logísticas (ex: Tegma, Localfrio), cooperativas agrícolas
e empresas de agricultura de precisão que dependem de GNSS RTK pagam assinatura pelo serviço de
dados de alta precisão
- **Setor público:** AEB (Agência Espacial Brasileira) e Ministério da Agricultura financiam a
infraestrutura orbital como bem público estratégico

### 3. Métrica de impacto

Se o NavBR-1 operar 100% saudável por 1 ano:
- ~12 milhões de hectares monitorados com precisão RTK no agronegócio brasileiro
- ~850 mil veículos de frota com rastreamento confiável e rotas otimizadas
- ~200 municípios com infraestrutura preparada para projetos de mobilidade autônoma
- Redução estimada de 15% no desperdício de insumos agrícolas por posicionamento incorreto

### 4. Modelo de negócio

**Dado-como-serviço (DaaS)** combinado com **SaaS**:
- API de dados de precisão para integradores (preço por consulta ou volume)
- Dashboard SaaS para gestores de frota e cooperativas (assinatura mensal)
- Licença pública para órgãos governamentais (concessão AEB)

---

## ⚠️ Limitações conhecidas

- Os dados de telemetria são simulados — não conectam a satélites reais
- O modelo `gpt-oss:120b` pode ter variação de resposta entre chamadas (não-determinístico)
- A integração usa a API REST diretamente via `requests` em vez do cliente oficial `ollama`,
pois o endpoint Cloud da biblioteca ainda apresenta incompatibilidade de rota
- Não há persistência de histórico entre sessões — o histórico é resetado ao fechar o sistema

---

## 🎬 Vídeo de demonstração

🔗 [Assistir demonstração no YouTube](https://www.youtube.com/watch?v=SEU_ID_AQUI)

> Configurado como "Não listado" no YouTube.

---

*FIAP · Ciência da Computação · Global Solution 2026.1 · Prompt Engineering and Artificial Intelligence*