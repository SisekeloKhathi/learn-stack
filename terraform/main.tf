terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.8.1"
    }
  }
}

resource "random_pet" "my_pet" {
  length = 3
}

output "pet_name" {
  value = random_pet.my_pet.id
}

# This defines a deployment for your Stack
deployment "dev" {
  inputs = {
    environment_name = "dev"
  }
}