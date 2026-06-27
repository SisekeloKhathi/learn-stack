variable "environment" {
  description = "Environment name (dev or prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "kafka-platform"
}

variable "docker_enabled" {
  description = "Enable Docker module"
  type        = bool
  default     = true
}

variable "k3s_enabled" {
  description = "Enable k3s module"
  type        = bool
  default     = true
}

variable "kafka_enabled" {
  description = "Enable Kafka module"
  type        = bool
  default     = true
}

variable "monitoring_enabled" {
  description = "Enable monitoring module"
  type        = bool
  default     = true
}

variable "networking_enabled" {
  description = "Enable networking module"
  type        = bool
  default     = true
}

variable "kafka_broker_count" {
  description = "Number of Kafka brokers"
  type        = number
  default     = 1
}

variable "kafka_replica_count" {
  description = "Replication factor for Kafka topics"
  type        = number
  default     = 1
}

variable "k3s_version" {
  description = "k3s version tag"
  type        = string
  default     = "v1.28.0"
}
