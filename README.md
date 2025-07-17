# Desafio C2S

O repositório consiste em uma aplicação que permite o usuário explorar uma base de dados sobre carros utilizando um AI agent. 

## Setup

Primeiramente, crie um arquivo .env executando o comando:

```bash
cp .env.example .env
```

Edite esse arquivo substituindo a OPENAI_API_KEY pela sua chave, gerada em "https://platform.openai.com/".

Verifique se `uv` está instalado no seu sistema. Caso não esteja, siga a documentação do projeto: https://docs.astral.sh/uv/getting-started/installation/.

Para instalar as demais dependências do projeto, execute:

```bash
uv sync
```

Para popular a base de dados com dados fictícios, execute:

```bash
uv run python main.py populate_db
```

Esse comando irá utilizar os pacotes Faker e faker_vehicle para gerar mocks dos dados de carros.

## Como executar

A aplicação depende de um servidor MCP que deve ser iniciado antes da execução dos demais comandos. Para rodá-lo, execute e deixe rodando em um terminal:

```bash
uv run python main.py run_mcp
```

### TUI

Para acessar uma UI no terminal, execute:

```bash
uv run python main.py run_agent_tui
```

### CLI
Para utilizar o agent via CLI, execute (alterando o argumento para sua pergunta):

```bash
uv run python main.py run_agent_cli "insira sua pergunta aqui..."
```

### Webui

Para executar a webui, execute:

```bash
uv run python main.py run_webui
```
