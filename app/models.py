from sqlmodel import SQLModel, Field, Relationship
from typing import List

class Base(SQLModel):
    pass

class CreateOrganisation(Base):
    name: str

class Organisation(Base, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    locations: List["Location"] = Relationship(back_populates="organisation")

class CreateLocation(Base):
    organisation_id: int
    location_name: str
    longitude: float
    latitude: float

class Location(Base, table=True):
    id: int | None = Field(primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="locations")
    location_name: str
    longitude: float
    latitude: float
