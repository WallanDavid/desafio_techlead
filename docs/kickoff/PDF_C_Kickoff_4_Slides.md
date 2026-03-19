# VBL Energy Intelligence — Estratégia, Liderança e Kickoff (PDF C)

## Slide 1 — Escopo Técnico e Objetivo (TRL 6 em 7 meses)

**Produto**

- Plataforma SaaS para monitorar energia, vibração e ruído em tempo real
- Mercado alvo: 100.000+ máquinas (agnóstico ao fabricante)
- Entrega TRL 6: protótipo funcional validado em ambiente relevante (piloto industrial)

**Desafios técnicos**

- Ingestão em alta taxa (picos) com baixa latência
- Persistência time-series (bilhões de pontos) + retenção/custos
- Predição com IA (anomalia + risco) integrada ao fluxo operacional
- Observabilidade, segurança e multi-tenant desde o MVP

---

## Slide 2 — Distribuição de Responsabilidades (Pleno / Júnior / Firmware)

**Back-end (Pleno)**

- Ingestion API (Node.js/NestJS ou Fastify), autenticação e validação
- Mensageria (Kafka/RabbitMQ): tópicos/partições, retry/DLQ
- Workers de processamento: batching, dedupe e persistência em TSDB
- APIs de dashboard (agregações) + cache (Redis)
- Observabilidade: métricas/alertas + hardening de segurança

**Front-end (Júnior)**

- Next.js + Tailwind: telas e componentes do dashboard
- Gráficos (Recharts/Chart.js) e estados de carregamento/erro
- Integração com APIs (filtros: tenant/site/máquina/tempo)
- UX de alertas: severidade, timeline, drill-down

**Firmware/Edge (20%)**

- Gateway agnóstico: coleta de sensores, normalização e timestamp
- Buffer local e retry (resiliência a queda de link)
- Segurança: assinatura do payload/credenciais por tenant
- Pacotes: MQTT/HTTP e compressão/opcional Protobuf

---

## Slide 3 — Uso dos Times Cross (QA / DevOps / UX)

**QA**

- Estratégia de testes por fase: unit, integração, E2E
- Testes de carga: simular 1k → 10k → 100k máquinas (picos e cauda)
- Critérios de aceitação: latência, perda de eventos, consistência e alertas

**DevOps**

- CI/CD com gates: build, testes, scan e deploy
- Infra como código e ambientes: dev/staging/prod
- Observabilidade: Prometheus, Grafana, logs centralizados
- Estratégia de custos: quotas por tenant, retenção, autoscaling

**UI/UX**

- Fluxo do operador: visão por planta/site/máquina
- Alertas acionáveis: prioridade, recomendação e histórico
- Evolução do dashboard: MVP → piloto → produção

---

## Slide 4 — Fluxo de Trabalho (Git flow, Review, Deploy)

**Git**

- `main`: produção
- `develop`: integração
- `feature/*`: desenvolvimento
- PR obrigatório, commits pequenos, mensagens claras

**Code Review**

- Checklist: performance, segurança, observabilidade, testes, custo
- Regras: sem merge direto em main; PR com aprovação mínima

**Deploy**

- Staging sempre atualizado
- Releases com canary/blue-green quando aplicável
- Pós-deploy: métricas + logs + alertas (SLO/erro/latência)

