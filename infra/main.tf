terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
  required_version = ">= 1.5"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "ona_vision" {
  name     = "ona-vision"
  location = var.region

  template {
    spec {
      containers {
        image = var.container_image
        ports {
          container_port = 5000
        }
      }
    }
  }

  traffics {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public_invoker" {
  service  = google_cloud_run_service.ona_vision.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

