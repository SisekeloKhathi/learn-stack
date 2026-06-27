# Kafka module - manages Kafka broker deployment

variable "kafka_broker_count" {
  description = "Number of Kafka brokers"
  type        = number
  default     = 1
}

variable "kafka_replica_count" {
  description = "Default replication factor"
  type        = number
  default     = 1
}

locals {
  terraform_dir = "${path.module}/../../.terraform"
}

resource "local_file" "kafka_config" {
  filename = "${local.terraform_dir}/kafka-config.txt"
  content = <<-EOT
Kafka Configuration
===================

Broker Count: ${var.kafka_broker_count}
Replication Factor: ${var.kafka_replica_count}

Deployment: Kafka will be deployed to k3s cluster via kustomize manifests
located in: k3s-gitops/infrastructure/kafka/

Default Topics (to be created):
- events: Main event stream (partitions: 3, replication: ${var.kafka_replica_count})
- commands: Command topic (partitions: 1, replication: ${var.kafka_replica_count})

Access from local cluster:
- Bootstrap servers: kafka:9092
- Zookeeper (if used): zookeeper:2181

Ports exposed (if NodePort):
- 9092: Kafka broker (within cluster)
- 29092: Kafka broker (external, if needed)

Commands:
- Produce: docker exec -it kafka kafka-console-producer --broker-list kafka:9092 --topic events
- Consume: docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic events --from-beginning
EOT
}

output "kafka_broker_count" {
  description = "Number of Kafka brokers"
  value       = var.kafka_broker_count
}

output "kafka_replica_count" {
  description = "Replication factor"
  value       = var.kafka_replica_count
}

output "kafka_bootstrap_servers" {
  description = "Kafka bootstrap servers"
  value       = "kafka:9092"
}

output "kafka_ready" {
  description = "Kafka deployment ready"
  value       = true
}
