output "kafka_bootstrap_servers" {
  description = "Kafka bootstrap servers"
  value       = "kafka:9092"
}

output "kafka_broker_count" {
  description = "Number of brokers"
  value       = 1
}

output "kafka_ready" {
  description = "Kafka ready"
  value       = true
}
