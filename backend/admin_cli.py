from backend.database import SessionLocal
from backend.models import WorkerAccount
from passlib.context import CryptContext  # <-- using for hashing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_worker():
    db = SessionLocal()
    try:
        username = input("Username: ")
        if db.query(WorkerAccount).filter_by(username=username).first():
            print("Username already exists.")
            return

        password = input("Password: ")
        hashed_pw = pwd_context.hash(password)  

        new_worker = WorkerAccount(username=username, password_hash=hashed_pw)
        db.add(new_worker)
        db.commit()
        print("Worker account created.")
    finally:
        db.close()

if __name__ == "__main__":
    create_worker()
