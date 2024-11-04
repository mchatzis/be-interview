from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from typing import List, Optional, Tuple

from app.db import get_db
from app.models import Location, Organisation, CreateOrganisation
from app.api.routes.helpers import get_organisation_or_404

router = APIRouter()

#TODO: get_organisation_or_404 creates a N+1 query issue. Use transactions errors to check existence instead.

@router.post("/create", response_model=Organisation)
def create_organisation(create_organisation: CreateOrganisation, session: Session = Depends(get_db)) -> Organisation:
    """Create an organisation."""
    organisation = Organisation(name=create_organisation.name)
    session.add(organisation)
    session.commit()
    session.refresh(organisation)

    return organisation

@router.get("/", response_model=list[Organisation])
def get_organisations(session: Session = Depends(get_db)) -> list[Organisation]:
    """
    Get all organisations.
    """
    organisations = session.exec(select(Organisation)).all()

    return organisations

@router.get("/{organisation_id}", response_model=Organisation)
def get_organisation_by_id(organisation_id: int, session: Session = Depends(get_db)) -> Organisation:
    """
    Get an organisation by id.
    """
    organisation = get_organisation_or_404(session, organisation_id)

    return organisation

@router.get("/{organisation_id}/locations", response_model=List[Location])
def get_organisation_locations(organisation_id: int, session: Session = Depends(get_db)):
    """
    Get locations for a specific organisation.
    """
    organisation = get_organisation_or_404(session, organisation_id)
    
    return organisation.locations

@router.post("/{organisation_id}/locations", response_model=List[Location])
def get_organisation_locations_and_filter(
    organisation_id: int,
    boundingBox: Optional[Tuple[float, float, float, float]] = None, #TODO: Extract to own sqlmodel
    session: Session = Depends(get_db)
):
    """
    Get locations for a specific organisation with optional filtering.
    Filters: 
        - bounding box tuple (min_lon, min_lat, max_lon, max_lat)
    """
    get_organisation_or_404(session, organisation_id)
    
    query = select(Location).where(Location.organisation_id == organisation_id)
    
    #TODO: Add coordinate checks both here and in database. (i.e. 90 <= latitude <= 90)
    if boundingBox is not None:
        min_lon, min_lat, max_lon, max_lat = boundingBox
        
        if min_lon >= max_lon or min_lat >= max_lat:
            raise HTTPException(
                status_code=400,
                detail="Invalid bounding box coordinates: min values must be less than max values"
            )
        
        query = query.where(
            Location.longitude >= min_lon,
            Location.longitude <= max_lon,
            Location.latitude >= min_lat,
            Location.latitude <= max_lat
        )
    
    locations = session.exec(query).all()
    return locations