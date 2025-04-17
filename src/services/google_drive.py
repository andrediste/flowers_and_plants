import json

import streamlit as st
from google.cloud import storage


class GoogleCloudStorageService:
    def __init__(self, bucket_name, credentials_json):
        self.bucket_name = bucket_name
        self.client = self.authenticate(credentials_json)

    def authenticate(self, credentials_json):
        credentials_dict = json.loads(credentials_json)
        return storage.Client.from_service_account_info(credentials_dict)

    def upload_file(self, file_path, destination_blob_name):
        """Uploads a file to the bucket."""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to {destination_blob_name}.")

    def download_file(self, source_blob_name, destination_file_name):
        """Downloads a file from the bucket."""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"File {source_blob_name} downloaded to {destination_file_name}.")
        return destination_file_name

    def list_files(self):
        """Lists all the blobs in the bucket."""
        bucket = self.client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs]


# Initialize the service using secrets
bucket_name = st.secrets["gcs"]["bucket_name"]
credentials_json = st.secrets["gcs"]["credentials"]

gcs_service = GoogleCloudStorageService(bucket_name, credentials_json)
