# Ona Vision Infrastructure

This folder contains Terraform files to deploy the Ona Vision app to Google Cloud Run.

## Prerequisites

- [ ] Terraform installed
- [ ] GCP account with billing enabled
- [ ] Enable APIs:
    - Cloud Run
    - Artifact Registry
- [ ] Your container image pushed to Artifact Registry

## How to Deploy

```bash
cd infra
terraform init

terraform apply \
  -var="project_id=your-gcp-project" \
  -var="container_image=gcr.io/your-project/ona-vision:latest"
