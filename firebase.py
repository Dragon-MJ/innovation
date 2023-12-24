import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# Use a service account.
cred = credentials.Certificate('innovation-6d72f-c6cd13cc9b27.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


# sign up
def make_user(id, password) -> bool:
    collection_name = 'user'

    # id <- 이미 db 에 있음 return False
    users_ref = db.collection(collection_name)
    query_ref = users_ref.where(filter=FieldFilter("id", "==", f"{id}"))
    docs = list(query_ref.stream())
    if len(docs) >= 1:
        return False
    # 없으면 id, password
    data = {"id": f"{id}", "password": f"{password}"}
    db.collection("user").add(data)

    return True

# sign in
def is_valid_user(id, password) -> bool:
    collection_name = 'user'

    # id <- 이미 db 에 있음 return False
    users_ref = db.collection(collection_name)
    query_ref = users_ref.where(filter=FieldFilter("id", "==", f"{id}"))
    docs = list(query_ref.stream())
    if len(docs) == 1:
        return True
    return False