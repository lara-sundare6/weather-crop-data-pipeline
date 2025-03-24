from google.cloud import storage
from google.auth import default
import json
import os

credentials, project = default()

if hasattr(credentials, 'service_account_email'):
    print(f"Authenticated as: {credentials.service_account_email}")
elif hasattr(credentials, 'to_json'):
    credentials_json = credentials.to_json()
    credentials_dict = json.loads(credentials_json)
    if 'email' in credentials_dict:
        print(f"Authenticated as: {credentials_dict['email']}")
    else:
        print("Authenticated with application default credentials. No email available.")
else:
    print("Could not get authenticated identity.")

print(credentials.to_json())
print(type(credentials))

def upload_to_gcp(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

if __name__ == "__main__":
    bucket_name = "weather-data-bucket-weather-crop-cloud-dev-x0kjiuom"
    source_file_name = "weather_data.csv"  
    destination_blob_name = "current-weather-data.csv"

    upload_to_gcp(bucket_name, source_file_name, destination_blob_name)