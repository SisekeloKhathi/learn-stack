output "k3s_ready" {
  description = "k3s deployment ready"
  value       = true
}

output "k3s_version" {
  description = "k3s version"
  value       = ""
}

output "kubeconfig_path" {
  description = "kubeconfig path"
  value       = "~/.kube/config"
}
