output "environment" {
  description = "Environment name"
  value       = var.environment
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

output "modules_deployed" {
  description = "List of deployed modules"
  value = compact([
    var.networking_enabled ? "networking" : "",
    var.docker_enabled ? "docker" : "",
    var.k3s_enabled ? "k3s" : "",
    var.kafka_enabled ? "kafka" : "",
    var.monitoring_enabled ? "monitoring" : "",
  ])
}

output "kafka_broker_count" {
  description = "Number of Kafka brokers deployed"
  value       = var.kafka_broker_count
}

output "k3s_version" {
  description = "k3s version deployed"
  value       = var.k3s_version
}

output "setup_complete" {
  description = "Setup completed successfully"
  value       = true
}
