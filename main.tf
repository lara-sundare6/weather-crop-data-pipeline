provider "google" {
  project = "weather-crop-cloud"
  region  = "us-central1"
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric  = true
}

variable "bucket_location" {
  description = "The location of the GCS bucket"
  type        = string
  default     = "us-central1"
}

variable "bucket_storage_class" {
  description = "The storage class of the GCS bucket"
  type        = string
  default     = "STANDARD"
}

variable "enable_versioning" {
  description = "Enable object versioning"
  type        = bool
  default     = true
}

# Create a Google Cloud Storage bucket
resource "google_storage_bucket" "weather_data_bucket" {
  name          = "weather-data-bucket-weather-crop-cloud-dev-${random_string.bucket_suffix.result}"
  location      = var.bucket_location
  storage_class = var.bucket_storage_class
  force_destroy = true

  versioning {
    enabled = var.enable_versioning
  }
}

# Add IAM permissions for public access or specific users
resource "google_storage_bucket_iam_member" "bucket_access" {
  bucket = google_storage_bucket.weather_data_bucket.name
  role   = "roles/storage.admin"        # Full permissions for the bucket
  member = "user:larasundare@gmail.com"
}
