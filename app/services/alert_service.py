from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.asset import Asset
from app.schemas.alert import AlertCreate, AlertUpdate, AssetCreate, AssetUpdate


def list_assets(db: Session) -> list[Asset]:
    return db.query(Asset).order_by(Asset.id.asc()).all()


def create_asset(db: Session, payload: AssetCreate) -> Asset:
    asset = Asset(**payload.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def get_asset(db: Session, asset_id: int) -> Asset:
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


def update_asset(db: Session, asset_id: int, payload: AssetUpdate) -> Asset:
    asset = get_asset(db, asset_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(asset, field, value)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset_id: int) -> None:
    asset = get_asset(db, asset_id)
    db.delete(asset)
    db.commit()


def list_alerts(db: Session) -> list[Alert]:
    return db.query(Alert).order_by(Alert.id.asc()).all()


def create_alert(db: Session, payload: AlertCreate) -> Alert:
    get_asset(db, payload.asset_id)
    alert = Alert(**payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_alert(db: Session, alert_id: int) -> Alert:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return alert


def update_alert(db: Session, alert_id: int, payload: AlertUpdate) -> Alert:
    alert = get_alert(db, alert_id)
    data = payload.model_dump(exclude_unset=True)

    if "asset_id" in data and data["asset_id"] is not None:
        get_asset(db, data["asset_id"])

    for field, value in data.items():
        setattr(alert, field, value)
    db.commit()
    db.refresh(alert)
    return alert


def delete_alert(db: Session, alert_id: int) -> None:
    alert = get_alert(db, alert_id)
    db.delete(alert)
    db.commit()

