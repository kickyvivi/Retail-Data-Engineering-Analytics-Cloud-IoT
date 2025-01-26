from google.cloud import storage
import re

# Function to list files in GCS bucket
def get_file_from_bucket(bucket_path, filename_template):
    """Retrieve the first file matching the template from the bucket."""
    # Extract bucket name and prefix
    bucket_name = bucket_path.replace("gs://", "").split("/")[0]
    prefix = "/".join(bucket_path.replace("gs://", "").split("/")[1:])
    
    # Initialize GCS client
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    
    # Filter files matching the filename template
    for blob in blobs:
        if re.match(filename_template, blob.name.split("/")[-1]):
            return f"gs://{bucket_name}/{blob.name}"
    
    return None 