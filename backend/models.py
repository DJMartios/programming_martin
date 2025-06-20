from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    species = Column(String(30), nullable=False)
    breed = Column(String(30))
    age = Column(Integer, nullable=False)
    IsAdopted = Column(Boolean, default=False)

class Adopter(Base):
    __tablename__ = "adopters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)

class Adoption(Base):
    __tablename__ = "adoptions"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)
    adopter_id = Column(Integer, ForeignKey("adopters.id", ondelete="CASCADE"), nullable=False)
    adoption_date = Column(Date, nullable=False)

    pet = relationship("Pet")
    adopter = relationship("Adopter")

class WorkerAccount(Base):
    __tablename__ = "worker_accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
