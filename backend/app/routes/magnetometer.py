from fastapi import APIRouter
from app.schemas import MagnetometerRequest

router = APIRouter(
    prefix="/api/v1/magnetometer",
    tags=["magnetometer"],
)


@router.post("/survey")
def survey(req: MagnetometerRequest):
    return {
        "status": "ok",
        "latitude": req.latitude,
        "longitude": req.longitude,
        "magnetometer_nt": req.magnetometer_nt,
        "note": "Reading accepted; interpretation requires baseline and field context.",
    }