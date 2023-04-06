# 基于 Flask 实现 Alertmanager 的 Webhook 通知

1. 修改 `prometheus.yml` 的 `alerting` 和 `rule_files` 部分

```yaml
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093
          - 192.168.111.161:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  - "rules/*_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]

  - job_name: 'node_exporter_161'
    scrape_interval: 10s
    static_configs:
      - targets: ['192.168.111.161:9100']
```

2. 定义监控规则 `rules/webhook_rules.yml`

```yaml
groups:
- name: example
  rules:
  - alert: HighCPUUsage
    expr: 100 * (1 - avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[5m]))) > 0.1
    for: 10s # 定义了告警需要持续多长时间才会被触发
    labels:
      severity: critical
    annotations:
      summary: "Instance {{ $labels.instance }} has high CPU usage"
      description: "{{ $labels.instance }} CPU usage is above 80% (current value: {{ $value }}%)"
  - alert: HighMemoryUsage
    expr: 100 * (node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Buffers_bytes - node_memory_Cached_bytes) / node_memory_MemTotal_bytes > 10
    for: 10s
    labels:
      severity: warning
    annotations:
      summary: "Instance {{ $labels.instance }} has high memory usage"
      description: "{{ $labels.instance }} memory usage is above 90% (current value: {{ $value }}%)"
```

3. 修改 `alertmanager.yml`

```yaml
route:
  group_by: ['alertname']
  group_wait: 3s
  group_interval: 5s
  repeat_interval: 10s
  receiver: 'web.hook.flask'
receivers:
  - name: 'web.hook.flask'
    webhook_configs:
      - url: 'http://192.168.1.2:5000/webhook'
```