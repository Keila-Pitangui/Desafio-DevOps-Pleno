# 🔍 Guia de Troubleshooting Avançado - Jimi IoT Gateway

Este guia documenta os principais diagnósticos e resoluções para falhas de observabilidade e ingestão de dados identificadas durante a implementação.

---

### 1. Problemas de Permissão e Isolação (SELinux/Docker Socket)
**Cenário**: O Promtail inicia, mas exibe erros de "Permission Denied" ou "Cannot connect to the Docker daemon".
* **Causa**: No Fedora, o SELinux e as permissões padrão do `/var/run/docker.sock` impedem que o container acesse o socket do host.
* **Diagnóstico**: `docker logs promtail` apresenta erros de conexão.
* **Resolução**:
    * Executar `sudo chmod 666 /var/run/docker.sock` para ajustar permissões.
    * Utilizar `security_opt: - label:disable` e `privileged: true` no `docker-compose.yml` para contornar restrições do SELinux.

---

### 2. Erros de Configuração e Parse (YAML/Versão)
**Cenário**: O container Promtail falha ao iniciar com o erro "field not found" ou "mount path must be absolute".
* **Causa**: Uso de flags incompatíveis com a versão (ex: `host_networking`) ou falta de barra inicial (`/`) nos caminhos de volume do Compose.
* **Diagnóstico**: O comando `docker compose up` retorna erro de montagem de volume ou o log do container indica falha no parse do YAML.
* **Resolução**: 
    * Remover campos obsoletos do `promtail.yml`.
    * Garantir que todos os mapeamentos de volume à direita dos dois-pontos (`:`) comecem com `/`.

---

### 3. Ausência de Dados nos Painéis (Prometheus/Grafana)
**Cenário**: O painel exibe "Data is missing a number field" ou "No Data".
* **Causa**: Falta de tráfego recente ou intervalo de tempo muito longo selecionado no Dashboard.
* **Diagnóstico**: Consultar a métrica diretamente no console do Prometheus (`http://localhost:9090`).
* **Resolução**:
    * Gerar tráfego manual via `curl` para os endpoints `/v1/telemetry`, `/v1/heartbeat` ou `/v1/alarms`.
    * Ajustar o Time Picker do Grafana para "Last 5 minutes" para visualizar dados de teste.

---

### 4. Gargalos de Ingestão e Latência
**Cenário**: A latência P95 ultrapassa os limites aceitáveis e os dados começam a atrasar na Jimi Cloud.
* **Causa**: Insuficiência de recursos (CPU/RAM) para processar o volume de webhooks recebidos.
* **Diagnóstico**: Analisar o gráfico de "Latência P95" e verificar se o consumo de memória dos containers está próximo ao limite definido no Compose.
* **Resolução**:
    * Aumentar os `limits` e `reservations` de memória no arquivo `docker-compose.yml`.
    * Implementar `Rate Limiting` no Nginx para mitigar picos de tráfego abusivos.

---

### 5. Comandos Rápidos de Emergência
* **Reiniciar serviço limpando cache**: `docker compose up -d --force-recreate <servico>`.
* **Validar sintaxe do Compose**: `docker compose config`.
* **Monitorar métricas brutas**: `curl http://localhost:8080/metrics`.