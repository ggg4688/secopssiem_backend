from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.alert import (
    AlertCreate,
    AlertRead,
    AlertUpdate,
)

from app.schemas.asset import (
    AssetCreate,
    AssetRead,
)

from app.services.alert_service import (
    create_alert,
    create_asset,
    delete_alert,
    delete_asset,
    get_alert,
    get_asset,
    list_alerts,
    list_assets,
    update_alert,
    update_asset,
)

from app.services.auth_service import get_current_user


router = APIRouter(
    tags=["assets-alerts"],
    dependencies=[Depends(get_current_user)],
)


# ---------------- ASSETS ----------------


@router.post("/assets", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset_endpoint(payload: AssetCreate, db: Session = Depends(get_db)):
    return create_asset(db, payload)


@router.get("/assets", response_model=list[AssetRead])
def list_assets_endpoint(db: Session = Depends(get_db)):
    return list_assets(db)


@router.get("/assets/{asset_id}", response_model=AssetRead)
def get_asset_endpoint(asset_id: UUID, db: Session = Depends(get_db)):
    return get_asset(db, asset_id)


@router.put("/assets/{asset_id}", response_model=AssetRead)
def update_asset_endpoint(asset_id: UUID, payload: AssetCreate, db: Session = Depends(get_db)):
    return update_asset(db, asset_id, payload)


@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset_endpoint(asset_id: UUID, db: Session = Depends(get_db)):
    delete_asset(db, asset_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------- ALERTS ----------------


@router.post("/alerts", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert_endpoint(payload: AlertCreate, db: Session = Depends(get_db)):
    return create_alert(db, payload)


@router.get("/alerts", response_model=list[AlertRead])
def list_alerts_endpoint(db: Session = Depends(get_db)):
    return list_alerts(db)


@router.get("/alerts/{alert_id}", response_model=AlertRead)
def get_alert_endpoint(alert_id: UUID, db: Session = Depends(get_db)):
    return get_alert(db, alert_id)


@router.put("/alerts/{alert_id}", response_model=AlertRead)
def update_alert_endpoint(alert_id: UUID, payload: AlertUpdate, db: Session = Depends(get_db)):
    return update_alert(db, alert_id, payload)


@router.delete("/alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_endpoint(alert_id: UUID, db: Session = Depends(get_db)):
    delete_alert(db, alert_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------- WEBSOCKET ALERT STREAM ----------------


from fastapi import WebSocket, WebSocketDisconnect
import json

active_connections: list[WebSocket] = []


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # frontend отправляет auth после подключения
            if message.get("type") == "auth":
                token = message.get("token")

                # здесь можно добавить проверку JWT если нужно
                if token:
                    await websocket.send_json({
                        "type": "auth",
                        "status": "ok"
                    })
                else:
                    await websocket.close()

    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_alert(alert: dict):
    disconnected = []

    for connection in active_connections:
        try:
            await connection.send_json(alert)
        except:
            disconnected.append(connection)

    for connection in disconnected:
        active_connections.remove(connection)
