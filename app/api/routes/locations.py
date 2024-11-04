from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_db
from app.models import Location, CreateLocation
from app.api.routes.helpers import get_organisation_or_404

router = APIRouter()

@router.post("/create", response_model=Location)
def create_location(create_location: CreateLocation, session: Session = Depends(get_db)) -> Location:
    """Create a location."""
    get_organisation_or_404(session, create_location.organisation_id)
    
    location = Location(**create_location.model_dump())

    session.add(location)
    session.commit()
    session.refresh(location)
    return location