# pip install google-api-python-client-stubs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO


import os

load_dotenv()


SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "service.json"
PARENT_FOLDER_ID = os.getenv("PARENT_FOLDER_ID")


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def upload(file_data, filename):
    service = authenticate()  # Ensure authenticate() is correctly implemented
    file_metadata = {
        "name": filename,  # Ensure this matches the uploaded file type
        "parents": [PARENT_FOLDER_ID],
    }
    file_path = BytesIO(file_data)
    media = MediaIoBaseUpload(
        file_path, mimetype="application/epub+zip", resumable=True
    )  # Correct way to upload file
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    file_path.seek(0)

    file_id = file.get("id")

    # Make the file publicly accessible (Optional)
    permission = {"role": "reader", "type": "anyone"}
    service.permissions().create(fileId=file_id, body=permission).execute()

    # Generate the shareable/download link
    download_link = f"https://drive.google.com/uc?id={file_id}&export=download"

    print("Successfully uploaded ")
    return download_link
