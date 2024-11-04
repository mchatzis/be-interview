from fastapi import HTTPException
from sqlmodel import Session

from app.models import Organisation


def get_organisation_or_404(session: Session, organisation_id: int) -> Organisation:
    organisation = session.get(Organisation, organisation_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    return organisation