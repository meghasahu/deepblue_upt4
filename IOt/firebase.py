import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./deepblueupt-4-firebase-adminsdk-5rnmz-3cc90e6541.json')


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://deepblueupt-4.firebaseio.com/'
})
ref = db.reference()
posts_ref = ref.child('users')
ref1 = db.reference()
usage_ref = ref1.child('usage')


code = input("Enter user code")
snapshot = posts_ref.order_by_child("Code").equal_to(code).get()
print(snapshot.items(0))
for i in snapshot.items():
    print(i[0])
    


