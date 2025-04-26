import json


def load_db():
    with open('flash_db.json', 'r') as f:
        db = json.load(f)
        return db
    

def save_db(db):
    with open('flash_db.json', 'w') as f:
        json.dump(db, f)

db=load_db()