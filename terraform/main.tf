# Configure the Google Cloud provider
provider "google" {
  project = "weather-crop-cloud"  # The GCP project ID
  region  = "us-central1"         # The default region for resources
}

# Generate a random string to use as a suffix for the bucket name
resource "random_string" "bucket_suffix" {
  length  = 8        # Length of the random string
  special = false    # Exclude special characters
  upper   = false    # Exclude uppercase letters
  numeric = true     # Include numeric characters
}

# Define a variable for the bucket's location
variable "bucket_location" {
  description = "The location of the GCS bucket"  # Description of the variable
  type        = string                            # Data type of the variable
  default     = "us-central1"                     # Default value for the variable
}

# Define a variable for the bucket's storage class
variable "bucket_storage_class" {
  description = "The storage class of the GCS bucket"  # Description of the variable
  type        = string                                 # Data type of the variable
  default     = "STANDARD"                             # Default value for the variable
}

# Define a variable to enable or disable object versioning
variable "enable_versioning" {
  description = "Enable object versioning"  # Description of the variable
  type        = bool                        # Data type of the variable
  default     = true                        # Default value for the variable
}

# Create a Google Cloud Storage bucket
resource "google_storage_bucket" "weather_data_bucket" {
  name          = "weather-data-bucket-weather-crop-cloud-dev-${random_string.bucket_suffix.result}"  # Unique bucket name
  location      = var.bucket_location        # Use the location variable
  storage_class = var.bucket_storage_class   # Use the storage class variable
  force_destroy = true                       # Automatically delete objects when the bucket is destroyed

  # Enable versioning for the bucket
  versioning {
    enabled = var.enable_versioning          # Use the enable_versioning variable
  }
}

# Assign IAM permissions to a specific user for the bucket
resource "google_storage_bucket_iam_member" "bucket_access" {
  bucket = google_storage_bucket.weather_data_bucket.name  # Reference the bucket name
  role   = "roles/storage.admin"                          # Assign full permissions for the bucket
  member = "user:larasundare@gmail.com"                   # Specify the user to grant access
}
