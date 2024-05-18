from google.oauth2 import service_account
from googleapiclient.discovery import build
import my_secrets

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DOCUMENT_ID = my_secrets.GOOGLE_DOC_ID

def get_google_doc_content(doc_id):
    creds = None
    creds = service_account.Credentials.from_service_account_file(my_secrets.my_json_file, scopes=SCOPES)
    service = build('docs', 'v1', credentials=creds)

    document = service.documents().get(documentId=doc_id).execute()
    doc_content = document.get('body').get('content')

    text = ''
    for element in doc_content:
        if 'paragraph' in element:
            elements = element.get('paragraph').get('elements')
            for elem in elements:
                text += elem.get('textRun').get('content', '')

    return text.strip()
