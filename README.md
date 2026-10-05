# agentes-ia-python

API de chat em Python (FastAPI) que conversa com qualquer provedor de LLM compatível com a API da OpenAI (`/chat/completions`). Sem chave configurada, roda em **modo eco**, útil para desenvolver e testar sem custo.

## Requisitos

- Python 3.10+

## Instalação

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e .
```

## Configuração

Copie o arquivo de exemplo e ajuste os valores:

```bash
cp .env.example .env
```

| Variável        | Padrão                      | Descrição                                              |
| --------------- | --------------------------- | ------------------------------------------------------ |
| `LLM_API_KEY`   | *(vazio)*                   | Chave do provedor. Vazia ativa o modo eco.             |
| `LLM_BASE_URL`  | `https://api.openai.com/v1` | URL base de um provedor compatível com a API da OpenAI |
| `LLM_MODEL`     | `gpt-4o-mini`               | Modelo usado nas requisições                           |
| `LLM_TIMEOUT`   | `60`                        | Timeout das chamadas ao provedor, em segundos          |
| `CORS_ORIGINS`  | `*`                         | Origens permitidas, separadas por vírgula              |

## Executando

```bash
uvicorn agentes_ia.api.app:app --reload
```

A API sobe em `http://127.0.0.1:8000`. A documentação interativa (Swagger) fica em `/docs`.

## Endpoints

### `GET /health`

Retorna o estado da API, o modo de operação (`llm` ou `echo`) e o modelo configurado.

```json
{ "status": "ok", "mode": "echo", "model": "gpt-4o-mini" }
```

### `POST /chat`

Recebe o histórico da conversa e devolve a resposta do assistente. Papéis aceitos: `system`, `user` e `assistant`. Se o histórico não tiver mensagem `system`, o serviço adiciona um prompt padrão.

```json
// requisição
{ "messages": [{ "role": "user", "content": "Olá, tudo bem?" }] }

// resposta
{ "message": { "role": "assistant", "content": "..." } }
```

Falhas no provedor de IA retornam `502`.

Há um exemplo de uso em [teste_api.py](teste_api.py), que exige a API rodando.

## Arquitetura

O projeto é dividido em camadas, e as dependências apontam das mais externas para as mais internas:

```
src/agentes_ia/
├── api/              # FastAPI: app, rotas, schemas e injeção de dependências
├── services/         # Regras de aplicação (ChatService)
├── infrastructure/   # Cliente de LLM (OpenAICompatibleClient e EchoClient)
├── domain/           # Modelos de domínio (Message, Role)
└── core/             # Configurações carregadas do ambiente
```

`build_client` escolhe o cliente conforme a configuração: com `LLM_API_KEY` usa o `OpenAICompatibleClient`, sem ela usa o `EchoClient`.

## Usando outro provedor

Basta apontar `LLM_BASE_URL` e `LLM_MODEL` para qualquer serviço que implemente `/chat/completions` (por exemplo, servidores locais como Ollama ou LM Studio).
