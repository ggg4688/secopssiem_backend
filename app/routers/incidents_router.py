from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.incident import (
    IncidentAlertLinkCreate,
    IncidentAlertLinkRead,
    IncidentCommentCreate,
    IncidentCommentRead,
    IncidentCreate,
    IncidentRead,
    IncidentUpdate,
)
from app.services.auth_service import get_current_user
from app.services.incident_service import (
    add_alert_to_incident,
    add_comment_to_incident,
    create_incident,
    delete_incident,
    get_incident,
    list_incident_comments,
    list_incidents,
    update_incident,
)

router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident_endpoint(payload: IncidentCreate, db: Session = Depends(get_db)):
    return create_incident(db, payload)


@router.get("", response_model=list[IncidentRead])
def list_incidents_endpoint(db: Session = Depends(get_db)):
    return list_incidents(db)


@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident_endpoint(incident_id: UUID, db: Session = Depends(get_db)):
    return get_incident(db, incident_id)


@router.put("/{incident_id}", response_model=IncidentRead)
def update_incident_endpoint(
    incident_id: UUID,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
):
    return update_incident(db, incident_id, payload)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident_endpoint(incident_id: UUID, db: Session = Depends(get_db)):
    delete_incident(db, incident_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{incident_id}/alerts",
    response_model=IncidentAlertLinkRead,
    status_code=status.HTTP_201_CREATED,
)
def add_alert_to_incident_endpoint(
    incident_id: UUID,
    payload: IncidentAlertLinkCreate,
    db: Session = Depends(get_db),
):
    return add_alert_to_incident(db, incident_id, payload.alert_id)


@router.post(
    "/{incident_id}/comments",
    response_model=IncidentCommentRead,
    status_code=status.HTTP_201_CREATED,
)
def add_incident_comment_endpoint(
    incident_id: UUID,
    payload: IncidentCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_comment_to_incident(db, incident_id, current_user.id, payload)


@router.get("/{incident_id}/comments", response_model=list[IncidentCommentRead])
def list_incident_comments_endpoint(incident_id: UUID, db: Session = Depends(get_db)):
    return list_incident_comments(db, incident_id)