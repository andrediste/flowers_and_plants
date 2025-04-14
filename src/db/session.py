import streamlit as st

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.metadata import Base


DATABASE_PATH = st.secrets["database"]["path"]

engine = create_engine(DATABASE_PATH, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()


# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import streamlit as st
# from services.google_cloud_storage import GoogleCloudStorageService

# # Google Cloud Storage setup
# CREDENTIALS_FILE = "path/to/credentials.json"
# BUCKET_NAME = "my-database-bucket"
# DB_FILE_NAME = "database.db"
# TEMP_DB_PATH = f"/tmp/{DB_FILE_NAME}"

# gcs_service = GoogleCloudStorageService(CREDENTIALS_FILE, BUCKET_NAME)

# @st.cache_resource
# def download_database():
#     """Download the database file from GCS and cache it."""
#     gcs_service.download_file(DB_FILE_NAME, TEMP_DB_PATH)
#     return TEMP_DB_PATH

# def upload_database():
#     """Upload the database file back to GCS."""
#     gcs_service.upload_file(TEMP_DB_PATH, DB_FILE_NAME)

# def get_session():
#     # Step 1: Ensure the database file is downloaded
#     db_path = download_database()

#     # Step 2: Create SQLAlchemy session
#     engine = create_engine(f"sqlite:///{db_path}")
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     session = SessionLocal()

#     # Step 3: Commit changes and upload the database back to GCS
#     def commit_and_upload():
#         session.commit()
#         upload_database()

#     # Attach the upload function to the session's commit method
#     session.commit = commit_and_upload

#     return session
