from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.farm import Farm
from backend.models.crop import Crop
from backend.models.farm_metric import FarmMetric


router = APIRouter(
    prefix="/agriculture",
    tags=["Agriculture"]
)


# -----------------------------
# GET ALL FARMS
# -----------------------------
@router.get("/farms/")
def get_farms(db: Session = Depends(get_db)):
    farms = db.query(Farm).all()

    return farms


# -----------------------------
# GET SINGLE FARM
# -----------------------------
@router.get("/farms/{farm_id}")
def get_farm(
    farm_id: int,
    db: Session = Depends(get_db)
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    return farm


# -----------------------------
# GET FARM CROPS
# -----------------------------
@router.get("/farms/{farm_id}/crops")
def get_farm_crops(
    farm_id: int,
    db: Session = Depends(get_db)
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    crops = db.query(Crop).filter(
        Crop.farm_id == farm_id
    ).all()

    return crops


# -----------------------------
# GET FARM METRICS
# -----------------------------
@router.get("/farms/{farm_id}/metrics")
def get_farm_metrics(
    farm_id: int,
    db: Session = Depends(get_db)
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    metrics = db.query(FarmMetric).filter(
        FarmMetric.farm_id == farm_id
    ).order_by(
        FarmMetric.timestamp.desc()
    ).all()

    return metrics