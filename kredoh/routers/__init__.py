import json
import os
from typing import Dict, Optional

from google.cloud import firestore, secretmanager

secrets = secretmanager.SecretManagerServiceClient()
_name = f"projects/{os.environ.get('PROJECT_ID')}/secrets/{os.environ.get('SECRET_ID')}/versions/{os.environ.get('SECRET_VERSION')}"
app_secret = json.loads(secrets.access_secret_version(request={"name": _name}).payload.data.decode("utf-8"))
push_auth = app_secret['gcp']['push_auth']

debug = True


def push_notification(vals):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': push_auth
    }

    title = vals.get('title', None)
    message = vals.get('body', None)
    device_token = vals.get('device_token', None)

    if title and message and device_token:
        body = {
            'notification': {'title': title,
                             'body': message},
            'to': device_token,
            'priority': 'high',
        }
        import requests
        import json
        print(f'push_notification:: body --> {body} ')
        response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        print(f'push_notification:: response --> {response}  response.json() --> {response.json()}')
        return response.text
    else:
        return f'firebase_token is not defined'


def store_to_firestore(ref: str, data: Dict, path: str, table_name: Optional[str] = 'CALLBACKS'):
    if debug:
        table_name += '-TEST'
    db = firestore.Client()
    doc_ref = db.collection(table_name.lower()).document(ref)
    doc = doc_ref.get()
    if not doc.exists:
        content = {'path': path,
                   'data': data,
                   'ref': ref}
        doc_ref.set(content)
        return True

    return False


def _get_table_name(name):
    return name[1:].replace('/', '-')
