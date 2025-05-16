variable "project_id" {
  description = "juice-ai-452311"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "container_image" {
  description = "Container image path (e.g., gcr.io/project/image:tag)"
  type        = string
}

