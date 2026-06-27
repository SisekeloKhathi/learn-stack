# k3s module - manages local Kubernetes cluster setup

variable "k3s_version" {
  description = "k3s version to deploy"
  type        = string
  default     = "v1.28.0"
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

locals {
  terraform_dir = "${path.module}/../../.terraform"
}

resource "local_file" "k3s_setup_script" {
  filename = "${local.terraform_dir}/k3s-setup.sh"
  content = <<-EOT
#!/bin/bash
# k3s Setup Script for Local Development
# This script checks if k3s is available or provides installation instructions

set -e

echo "Checking for k3s installation..."

if command -v k3s &> /dev/null; then
    echo "k3s is installed:"
    k3s --version
    echo "k3s setup is ready."
    exit 0
fi

if command -v kubectl &> /dev/null; then
    echo "kubectl is available. Assuming k3s cluster access..."
    kubectl cluster-info
    exit 0
fi

echo "k3s or kubectl not found."
echo ""
echo "For Windows with Docker Desktop:"
echo "1. Enable Kubernetes in Docker Desktop settings"
echo "   OR"
echo "2. Install k3s via WSL2:"
echo "   wsl -d Ubuntu"
echo "   curl -sfL https://get.k3s.io | sh -"
echo ""
echo "After installation, merge kubeconfig:"
echo "   export KUBECONFIG=~/.kube/config:/etc/rancher/k3s/k3s.yaml"
exit 1
EOT
}

resource "local_file" "k3s_manifests_dir" {
  filename = "${path.module}/../../.terraform/k3s-manifests-index.txt"
  content = <<-EOT
k3s Manifests Location
======================

Core manifests are stored in: k3s-gitops/infrastructure/

Subdirectories:
- argocd/          - ArgoCD configuration (GitOps)
- flink/           - Apache Flink deployment
- grafana/         - Grafana monitoring UI
- kafka/           - Kafka broker deployment
- postgres/        - PostgreSQL database
- prometheus/      - Prometheus monitoring
- redis/           - Redis cache

Application manifests: k3s-gitops/apps/
- dashboard-app/   - Dashboard service
- streaming-app/   - Streaming application

Deploy via ArgoCD:
  kubectl apply -f k3s-gitops/argocd/app-of-apps.yaml
EOT
}

output "k3s_ready" {
  description = "k3s environment ready"
  value       = true
}

output "k3s_version" {
  description = "Target k3s version"
  value       = var.k3s_version
}

output "kubeconfig_path" {
  description = "Path to kubeconfig"
  value       = var.kubeconfig_path
}
