from fastapi import FastAPI, Depends, HTTPException, status, Form, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .auth import create_access_token, verify_token
from .config import CORS_ORIGINS
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_current_user(token: str = Header(..., alias="Authorization")):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id

@app.get("/")
def root(user_id: str = Depends(get_current_user)):
    return {"message": "Welcome to PetAdopt API"}

@app.get("/pets/", response_model=list[schemas.PetOut])
def list_pets(db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    return crud.get_pets(db)

@app.get("/pets/{pet_id}", response_model=schemas.PetOut)
def get_pet(pet_id: int, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    pet = crud.get_pet(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@app.post("/pets/", response_model=schemas.PetOut)
def add_pet(pet: schemas.PetCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    return crud.create_pet(db, pet)

@app.put("/pets/{pet_id}", response_model=schemas.PetOut)
def update_pet(pet_id: int, pet: schemas.PetCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    updated = crud.update_pet(db, pet_id, pet)
    if not updated:
        raise HTTPException(status_code=404, detail="Pet not found")
    return updated

@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    deleted = crud.delete_pet(db, pet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"deleted": True}

@app.get("/adopters/", response_model=list[schemas.AdopterOut])
def list_adopters(db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    return crud.get_adopters(db)

@app.get("/adopters/{adopter_id}", response_model=schemas.AdopterOut)
def get_adopter(adopter_id: int, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    adopter = crud.get_adopter(db, adopter_id)
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter not found")
    return adopter

@app.post("/adopters/", response_model=schemas.AdopterOut)
def add_adopter(adopter: schemas.AdopterCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    return crud.create_adopter(db, adopter)

@app.put("/adopters/{adopter_id}", response_model=schemas.AdopterOut)
def update_adopter(adopter_id: int, adopter: schemas.AdopterCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    updated = crud.update_adopter(db, adopter_id, adopter)
    if not updated:
        raise HTTPException(status_code=404, detail="Adopter not found")
    return updated

@app.delete("/adopters/{adopter_id}")
def delete_adopter(adopter_id: int, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    deleted = crud.delete_adopter(db, adopter_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Adopter not found")
    return {"deleted": True}

@app.get("/adoptions/", response_model=list[schemas.AdoptionOut])
def list_adoptions(db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    return crud.get_adoptions(db)

@app.post("/adoptions/", response_model=schemas.AdoptionOut)
def add_adoption(adoption: schemas.AdoptionCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    return crud.create_adoption(db, adoption)

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    worker = crud.authenticate_worker(db, username, password)
    if not worker:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(worker.id)})
    return {"access_token": token}

@app.post("/logout")
def logout():
    # Stateless JWT: handled on frontend by deleting the token
    return {"message": "Logged out"}
