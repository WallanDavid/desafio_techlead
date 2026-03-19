# VBL Energy Intelligence — Arquitetura e Modelagem (PDF A)

## Objetivo do Produto

Plataforma SaaS para monitorar, em tempo real, consumo elétrico, vibração e ruído de máquinas industriais de injeção (agnóstica ao fabricante), com predição de falhas via IA, suportando mercado de 100.000+ máquinas.

## Requisitos Não-Funcionais (orientadores)

- Escala: até 100.000 máquinas (alta taxa de eventos).
- Baixa latência de ingestão e alta disponibilidade.
- Resiliência a picos (buffer por mensageria).
- Multi-tenant readiness (segregação por cliente/plant/site).
- Observabilidade completa (métricas, logs, traces).
- Custo limitado (budget cloud R$ 15k/mês).

---

## C4 — Nível 1 (Contexto)

```mermaid
flowchart LR
  subgraph Campo[Chão de fábrica]
    M[Máquina Industrial\n(Sensores: energia, vibração, ruído)]
    G[Gateway/Edge\n(Agnóstico ao fabricante)]
    M -->|Coleta sensores| G
  end

  subgraph Cloud[Cloud / Data Center]
    V[VBL Energy Intelligence\n(Plataforma)]
  end

  U[Gestor de Manutenção\n(Usuário Web)]
  QA[QA/Operação]

  G -->|Telemetria\nMQTT/HTTP| V
  U <-->|Dashboards, alertas,\nconfigurações| V
  QA <-->|Observabilidade,\nSLO/SLA| V
```

**Observações**

- O gateway reduz acoplamento com fabricantes e garante buffering local (offline-first).
- A plataforma mantém a ingestão “thin” e transfere o custo para processamento assíncrono.

---

## C4 — Nível 2 (Containers)

```mermaid
flowchart TB
  subgraph Edge[Edge / IoT]
    GW[Gateway\n(Buffer local + normalização]
  end

  subgraph Platform[VBL Energy Intelligence]
    API[Ingestion API\nNode.js (NestJS/Fastify)\nAuth + validação + rate limit]
    MQ[Mensageria\nKafka/RabbitMQ]
    WK[Telemetry Processor\nNode.js Worker\nBatching + retries]
    TSDB[Time-series DB\nTimescaleDB/InfluxDB\nTelemetria]
    PG[PostgreSQL\nMetadados: tenants, máquinas, usuários]
    REDIS[Redis\nCache RT + estados + dedupe]
    AI[AI Service\nPython (FastAPI)\nAnomalia + risco de falha]
    FE[Frontend\nNext.js + Tailwind\nDashboard]
    OBS[Observabilidade\nPrometheus + Grafana]
  end

  GW -->|HTTP/MQTT -> JSON/Protobuf| API
  API -->|publish| MQ
  MQ -->|consume| WK
  WK -->|insert (batch)| TSDB
  WK -->|read/write| REDIS
  WK -->|feature window| AI
  AI -->|risk score| REDIS
  FE -->|REST/GraphQL| API
  API -->|read| PG
  API -->|read (hot)| REDIS
  API -->|metrics| OBS
  WK -->|metrics| OBS
  AI -->|metrics| OBS
```

---

## Pipeline de Dados (end-to-end)

1. Máquina envia sinais para o Gateway.
2. Gateway normaliza payload (unidades, timestamp, IDs), aplica buffering local e envia para a Ingestion API.
3. Ingestion API autentica, valida schema, aplica rate limit por tenant/máquina e publica evento na mensageria.
4. Worker consome do tópico/fila, agrega em lotes (batch), deduplica (Redis) e persiste no TSDB.
5. Worker cria janelas (sliding windows) e consulta AI Service para inferência de risco.
6. Resultado é cacheado (Redis) e exposto no Dashboard via API.

---

## Estratégia de Escalabilidade

- Ingestão stateless: escala horizontal com autoscaling.
- Kafka como buffer: controla backpressure e preserva eventos sob pico.
- Workers escaláveis: paralelismo por partição (machineId/tenantId).
- TSDB otimizado: particionamento por tempo + compressão + retenção.
- Redis: leitura quente e redução de carga em TSDB/PG.

---

## Multi-tenant Readiness (MVP compatível com produção)

- `tenant_id` presente em todos os eventos e tabelas.
- Chaves de partição Kafka: `tenant_id + machine_id`.
- Row-Level Security (RLS) no Postgres para isolamento por tenant.
- Namespace e dashboards por tenant.

---

## Estratégia de Custos (budget R$ 15k/mês)

- Banco: TimescaleDB/Postgres gerenciado (compressão + retenção) para reduzir storage.
- Kafka: começar com cluster pequeno (3 brokers) e crescer por partição conforme demanda.
- Compute: autoscaling (API/Workers) com limites por tenant.
- Observabilidade: Prometheus + Grafana (managed quando fizer sentido).
- Retenção: “hot 7–30 dias” no TSDB, “warm/cold” em storage barato (S3/Blob) se necessário.

---

## TRL 6 (7 meses) — Caminho pragmático

- M1–M2: ingestão + TSDB + dashboard básico (energia/vibração/ruído).
- M3–M4: pipeline assíncrono com mensageria + observabilidade + hardening.
- M5: IA simples (anomalia) + alertas operacionais.
- M6–M7: validação em ambiente relevante (piloto), ajustes de performance, multi-tenant e custos.

