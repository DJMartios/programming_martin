from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from .models import WorkerAccount



def get_pets(db: Session):
    return db.query(models.Pet).all()

def get_pet(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def create_pet(db: Session, pet: schemas.PetCreate):
    db_pet = models.Pet(**pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def update_pet(db: Session, pet_id: int, pet_data: schemas.PetCreate):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if pet:
        for field, value in pet_data.dict().items():
            setattr(pet, field, value)
        db.commit()
        db.refresh(pet)
    return pet

def delete_pet(db: Session, pet_id: int):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if pet:
        db.delete(pet)
        db.commit()
        return True
    return False

def get_adopters(db: Session):
    return db.query(models.Adopter).all()

def get_adopter(db: Session, adopter_id: int):
    return db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()

def create_adopter(db: Session, adopter: schemas.AdopterCreate):
    db_adopter = models.Adopter(**adopter.dict())
    db.add(db_adopter)
    db.commit()
    db.refresh(db_adopter)
    return db_adopter

def update_adopter(db: Session, adopter_id: int, adopter_data: schemas.AdopterCreate):
    adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()
    if adopter:
        for field, value in adopter_data.dict().items():
            setattr(adopter, field, value)
        db.commit()
        db.refresh(adopter)
    return adopter

def delete_adopter(db: Session, adopter_id: int):
    adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()
    if adopter:
        db.delete(adopter)
        db.commit()
        return True
    return False

def get_adoptions(db: Session):
    return db.query(models.Adoption).all()

def create_adoption(db: Session, adoption: schemas.AdoptionCreate):
    db_adoption = models.Adoption(**adoption.dict())

    pet = db.query(models.Pet).filter(models.Pet.id == adoption.pet_id).first()
    if pet:
        pet.IsAdopted = True

    db.add(db_adoption)
    db.commit()
    db.refresh(db_adoption)
    return db_adoption


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)

def authenticate_worker(db: Session, username: str, password: str):
    user = db.query(WorkerAccount).filter(WorkerAccount.username == username).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None
