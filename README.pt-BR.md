# QueueGuard — Plataforma de Desduplicação e Filas Idempotentes

Plataforma corporativa para mitigação de processamento duplicado em filas assíncronas construída com **Angular 22**, **FastAPI** e **PostgreSQL 18**.

## Visão Geral da Arquitetura

O QueueGuard garante semântica de entrega atômica e execução única em pipelines assíncronos distribuídos, através de controle transacional de leases e hashing criptográfico de payloads.

- **Frontend**: Arquitetura standalone Angular 22 com `ChangeDetectionStrategy.OnPush`, Signals reativos granulares (`signal`, `computed`), acessibilidade WCAG AAA e folhas de estilo responsivas sem clichês visuais de IA.
- **Backend**: FastAPI com PostgreSQL assíncrono (Psycopg 3), autenticação por token Bearer, aquisição atômica de lease, cache de resposta de desduplicação e isolamento multi-tenant.
- **Banco de Dados**: Migrações relacionais no PostgreSQL controlando `idempotent_keys`, `queue_messages` e `audit_events`.
- **Testes**: Suíte de aceitação com Pytest, testes unitários com Vitest e testes de ponta a ponta no navegador com Playwright em três resoluções (390px, 768px, 1440px).

## Instalação e Execução

```bash
# Frontend
cd frontend
npm ci
npm run build

# Backend
cd ../backend
python -m pip install -r requirements.txt
uvicorn src.app.main:app --port 8000
```

## Licença

MIT © Felipe Madison (@FelipeMadson)
