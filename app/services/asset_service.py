from sqlalchemy.orm import Session
from app.models.asset import Asset


def list_assets(db: Session):
    return db.query(Asset).all()


def create_asset(db: Session, hostname: str, ip: str):
    asset = Asset(
        hostname=hostname,
        ip=ip
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset