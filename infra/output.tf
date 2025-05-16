output "cloud_run_url" {
  description = "The deployed Cloud Run URL"
  value       = google_cloud_run_service.ona_vision.status[0].url
}

