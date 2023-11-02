# Chargeback Model Demo

This demo showcases the Chargeback Monetisation model for the usage of Kafka cluster in a multi-tenant scenario. This helps to determine the usage by each tenant by employing unique chargecodes per tenant.

## Pre-requisites
- python
- docker

**Note**: Client quotas need to be configured in Kafka.

## Examples

### Chargeback Model Config
```yaml
clusters:
  - cluster1:
      cluster_name: Cluster1 # Joining Key
      cluster_id: 12345
      throughput_units: bytes
      currency_code: USD
      total_costs: 5000
      total_capacity:
        throughput_tps: 1000
        storage: 100000000
        partitions_max: 1000
      chargeback_model: cost_center
      chargeback_config:
        partition_unit_rate: 0.05
        throughput_unit_rate: 0.1
        storage_unit_rate: 0.001

  - cluster3:
      cluster_name: Cluster3
      cluster_id: 56789
      throughput_units: bytes
      currency_code: USD
      total_costs: 5000
      total_capacity:
        throughput_tps: 1000
        storage: 100000000
        partitions_max: 1000
      chargeback_model: usage_based
      chargeback_config:
        partition_unit_rate: 0.05
        throughput_unit_rate: 0.1
        storage_unit_rate: 0.001

  - cluster2:
      cluster_name: Cluster2
      cluster_id: 98765
      throughput_units: bytes
      currency_code: USD
      total_costs: 6000
      total_capacity:
        throughput_tps: 1000
        storage: 100000000
        partitions_max: 1000
      chargeback_model: client_usage_based
      chargeback_config:
        usage_model: producer_pays  # Supported models: producer_pays, consumer_pays, producer_consumer_pays
        throughput_in_unit_rate: 0.15
        throughput_out_unit_rate: 0.05
```

### Chargeback Codes Config
```yaml
chargecodes:
  - chargecode_name: Chargecode1
    target_cluster: Cluster1   # Joining Key
    match_config:
      - entity: client_id
        match_type: prefix
        match_expression: "clientA_"
      - entity: topic
        match_type: literal
        match_expression: "important_topics"

  - chargecode_name: Chargecode2
    target_cluster: Cluster2
    match_config:
      - entity: client_id
        match_type: regex
        match_expression: "^clientB_.+"
      - entity: topic
        match_type: literal
        match_expression: "special_topics"

  - chargecode_name: Chargecode3
    target_cluster: Cluster3
    match_config:
      - entity: client_id
        match_type: literal
        match_expression: "clientC"
      - entity: topic
        match_type: prefix
        match_expression: "experimental_"
```

## Validate the Chargeback Model Config
```bash
python chargeback_validator.py -m /path/to/chargeback_model.yaml
```

## Generate the Prometheus `metric_label_config`
```bash
python generate_label_config.py -m /path/to/chargeback_model.yaml -c /path/to/chargback_codes.yaml
```
**Note**: For demo purposes, the `metric_label_config` for prometheus is already configured

## Start the demo
```bash
./start.sh
```

## Stop the demo
```bash
./stop.sh
```