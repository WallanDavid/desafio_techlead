# VBL Energy Intelligence — Avaliação Técnica do Legado (PDF B)

## Contexto

O ativo legado `TelemetryService.cs` (2021) foi proposto para acelerar o desenvolvimento do produto. O objetivo desta avaliação é determinar se ele suporta escala para milhares/centenas de milhares de máquinas com telemetria em tempo real, dentro do prazo de 7 meses e budget de cloud limitado.

---

## Achados Principais (riscos)

### Escalabilidade

- Uso de materialização completa em memória (ex.: `.ToList()` em consultas) cria risco direto de OOM sob alto volume.
- Ausência de paginação e/ou streaming em rotas de leitura torna o custo proporcional ao tamanho do histórico.
- Processamento síncrono acoplado à requisição aumenta latência e derruba throughput em pico.
- Não há desenho de backpressure: picos derrubam a API ao invés de serem amortecidos por buffer.

### Performance

- Consultas sem índices orientados a séries temporais e sem particionamento por tempo tendem a degradar rapidamente.
- Cálculos de agregação em tempo real feitos no caminho síncrono elevam custo e aumentam cauda de latência.
- Falta de batching (inserts um-a-um) aumenta I/O e consumo de conexões.

### Arquitetura e Evolutividade

- Forte acoplamento a um ORM/repositório específico limita migração para TSDB (TimescaleDB/InfluxDB).
- Não há separação clara entre: ingestão, processamento, persistência e analytics.
- Ausência de mensageria impede desacoplamento entre entrada e processamento pesado.
- Responsabilidades concentradas em classe/serviço único (risco de “god service”).

### Segurança e Confiabilidade

- Sem evidências de: autenticação/assinatura do payload, rate limiting por tenant/máquina e validação robusta de schema.
- Sem idempotência/deduplicação (risco de duplicação sob retry).
- Sem circuit breaker, retry controlado ou DLQ para eventos problemáticos.

---

## Impacto no Prazo (7 meses)

Manter o legado como base do produto introduz risco alto de atraso por:

- necessidade de re-arquitetar a ingestão para suportar picos;
- migração inevitável para pipeline assíncrono;
- retrabalho em persistência e modelagem para TSDB;
- hardening de segurança e observabilidade.

---

## Decisão Executiva (Tech Lead)

### ✅ DECISÃO FINAL: **DESCARTAR**

**Justificativa**

- O legado foi desenhado para um cenário de baixa escala e padrão CRUD, incompatível com telemetria massiva e contínua.
- A refatoração necessária equivale a reescrever os elementos centrais: filas, workers, persistência time-series, dedupe, retries e observabilidade.
- Reescrever com arquitetura dirigida a eventos reduz risco e acelera o caminho para TRL 6 dentro do prazo.

---

## Plano de Substituição (orientado a entrega)

- **Ingestion API (Node.js/NestJS ou Fastify)**: validação leve + autenticação + publish em fila.
- **Mensageria (Kafka/RabbitMQ)**: buffering e backpressure.
- **Workers**: consumo, batching, dedupe e persistência em TSDB.
- **TSDB + Postgres**: telemetria em TSDB; metadados e RBAC em Postgres.
- **Redis**: cache quente e estados/alertas.
- **AI Service (FastAPI)**: inferência simples de anomalia e score de risco.
- **Observabilidade**: Prometheus/Grafana, SLOs e alertas.

