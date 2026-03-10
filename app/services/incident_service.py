from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.incident import Incident
from app.models.incident_alert import IncidentAlert
from app.models.incident_comment import IncidentComment
from app.schemas.incident import IncidentCommentCreate, IncidentCreate, IncidentUpdate


def list_incidents(db: Session) -> list[Incident]:
    return db.query(Incident).order_by(Incident.id.asc()).all()


def create_incident(db: Session, payload: IncidentCreate) -> Incident:
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def get_incident(db: Session, incident_id: int) -> Incident:
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


def update_incident(db: Session, incident_id: int, payload: IncidentUpdate) -> Incident:
    incident = get_incident(db, incident_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return incident


def delete_incident(db: Session, incident_id: int) -> None:
    incident = get_incident(db, incident_id)
    db.delete(incident)
    db.commit()


def add_alert_to_incident(db: Session, incident_id: int, alert_id: int) -> IncidentAlert:
    get_incident(db, incident_id)
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    existing_link = (
        db.query(IncidentAlert)
        .filter(IncidentAlert.incident_id == incident_id, IncidentAlert.alert_id == alert_id)
        .first()
    )
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Alert is already linked to this incident",
        )

    link = IncidentAlert(incident_id=incident_id, alert_id=alert_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def add_comment_to_incident(
    db: Session,
    incident_id: int,
    user_id: int,
    payload: IncidentCommentCreate,
) -> IncidentComment:
    get_incident(db, incident_id)
    comment = IncidentComment(
        incident_id=incident_id,
        user_id=user_id,
        comment=payload.comment,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_incident_comments(db: Session, incident_id: int) -> list[IncidentComment]:
    get_incident(db, incident_id)
    return (
        db.query(IncidentComment)
        .filter(IncidentComment.incident_id == incident_id)
        .order_by(IncidentComment.id.asc())
        .all()
    )

