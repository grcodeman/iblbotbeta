import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import ArrayUnion, ArrayRemove

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def add_name(user,name):
    db.collection("users").document(str(user)).set({'name':name}, merge=True)

def get_name(user):
    db.collection("users").document(str(user)).set({'logic':1}, merge=True)
    info = db.collection("users").document(str(user)).get().to_dict()
    if ('name' in info):
        name = info['name']
    else:
        name = "Error"
    return name