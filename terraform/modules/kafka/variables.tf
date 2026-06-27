variable "kafka_broker_count" {
  description = "Number of Kafka brokers"
  type        = number
  default     = 1
}

variable "kafka_replica_count" {
  description = "Replication factor"
  type        = number
  default     = 1
}
