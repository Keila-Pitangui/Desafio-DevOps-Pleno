# IoTHub Gateway — Observability Platform

## Contexto do Desafio

Este projeto foi desenvolvido como solução para o **Desafio DevOps Pleno**, cujo objetivo é estruturar uma **plataforma de observabilidade** para um sistema de telemetria IoT, garantindo visibilidade operacional, confiabilidade e capacidade de diagnóstico em produção.

A proposta cobre **monitoramento de métricas, centralização de logs e visualização unificada**, simulando um cenário real de operação de sistemas distribuídos.

---

## Visão Executiva (Resumo para Avaliadores)

- Stack de observabilidade baseada em ferramentas **Cloud Native**
- Monitoramento orientado a **SLOs e indicadores de negócio**
- Logs estruturados e correlacionáveis
- Arquitetura modular e extensível
- Foco em **troubleshooting e operação real**

---

## Objetivos Técnicos

- Centralizar métricas e logs do gateway IoT
- Detectar falhas, erros HTTP e degradação de performance
- Facilitar análises operacionais e troubleshooting
- Garantir reprodutibilidade via infraestrutura containerizada
- Seguir boas práticas DevOps e SRE

---

## Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|------|-----------|---------------|
| Containerização | Docker / Docker Compose | Padronização e reprodutibilidade |
| Proxy Reverso | Nginx | Controle de entrada e base para rate limiting |
| Métricas | Prometheus | Coleta eficiente e padrão de mercado |
| Logs | Grafana Loki | Logs escaláveis e integrados ao Grafana |
| Coleta de Logs | Promtail | Parsing e enriquecimento de logs |
| Visualização | Grafana | Dashboards unificados e alertas |

> O Promtail foi adaptado para ambientes **Fedora com SELinux**, respeitando políticas de segurança do sistema operacional.

---

## Arquitetura da Solução

A arquitetura segue o princípio de **observabilidade desacoplada**, separando claramente ingestão, armazenamento e visualização.

┌────────────────────┐
│ Serviços / APIs │
└─────────┬──────────┘
│
┌──────▼───────┐
│ Promtail │ → Logs
└──────┬───────┘
▼
Loki
▼
Grafana
▲
┌──────┴───────┐
│ Prometheus │ → Métricas
└──────────────┘


---

## Execução do Projeto

### Pré-requisitos
- Docker
- Docker Compose
- Linux (testado em Fedora)

### Ajustes para Fedora / SELinux

```bash
sudo chmod 666 /var/run/docker.sock
sudo setsebool -P container_manage_cgroup on

Inicialização
docker compose up -d
```

Acessos
Serviço	URL
Grafana: http://localhost:3000
Prometheus:	http://localhost:9090
Credenciais padrão do Grafana: admin / admin

## 📊 Dashboard de Observabilidade

O dashboard entregue (**`grafana-dashboard-jimi-iot.json`**) foi construído com foco em **indicadores operacionais reais**, permitindo visibilidade clara sobre performance, erros e saúde da plataforma.

### Indicadores Monitorados

#### 🔁 Taxa de Webhooks por Endpoint
- Análise de throughput utilizando a função `rate()`

#### 🚨 Taxa de Erro HTTP
- Painel do tipo **Gauge**
- Threshold visual configurado em **5%**

#### ⏱️ Latência P95
- Avaliação de performance por meio de `histogram_quantile`

#### 🟢 Saúde dos Contêineres
- Status **UP / DOWN** com base na métrica `up`

#### 📋 Últimos Eventos Processados
- Logs estruturados com extração automática dos campos:
  - `device_id`
  - `level`

---

## 🔍 Troubleshooting e Operação

### Checklist Operacional

- **Verificação de containers**
```bash
  docker ps
```

### 📜 Logs do Promtail
Para verificar o status da coleta de logs e a comunicação com o Docker Socket:
```bash
docker logs promtail
```

### 💾 Validação de Volumes Persistentes
Garante a retenção mínima de 7 dias para métricas e logs:

* **Conferir montagem**: Validar se os diretórios `./prometheus_data`, `./grafana` e `./loki` estão persistindo dados corretamente no host.

### 🛠️ Estratégias de Mitigação
Ações para resolver gargalos de performance e garantir a disponibilidade (SRE):

* **Ajuste de recursos**: Readequação de limites de CPU e memória nos containers.
* **Otimização de regex**: Refinamento no Promtail para reduzir o overhead de processamento de logs.
* **Rate Limiting**: Implementação no Nginx para prevenir abuso e sobrecarga no backend.
* **Circuit Breaker**: Aplicação no backend para isolar falhas e evitar efeitos em cascata.

### 📂 Entregáveis
Arquivos essenciais que compõem a solução do desafio:

* **docker-compose.yml**: Orquestração da infraestrutura e redes segregadas.
* **promtail.yml**: Pipeline de coleta e estruturação de logs.
* **grafana-dashboard-jimi-iot.json**: Painel de visualização com métricas P95, Erros e Saúde.

### 🚀 Evoluções Planejadas (Roadmap)
Próximos passos para elevar a maturidade da infraestrutura:

* **Orquestração**: Migração para Kubernetes (EKS) utilizando Helm Charts.
* **Alertas**: Integração nativa com Alertmanager para notificações críticas.
* **IaC**: Provisionamento da infraestrutura via Terraform.
* **CI/CD**: Pipeline automatizado com validação de métricas (Canary/Blue-Green).
* **SRE**: Definição formal de SLOs e alertas orientados ao negócio.

### 🧾 Conclusão
Este projeto demonstra a aplicação prática de conceitos de **DevOps, SRE e Observabilidade**, indo além da instrumentação básica e abordando aspectos essenciais de operação, diagnóstico e escalabilidade.

A solução foi desenhada para refletir cenários reais de produção, mantendo flexibilidade para evolução contínua e garantindo que o **IoTHub Gateway** opere com alta visibilidade e resiliência.