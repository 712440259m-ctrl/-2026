from fastapi import APIRouter
from app.schemas import ProspectivityRequest

router = APIRouter(
    prefix="/api/v1/prospectivity",
    tags=["prospectivity"],
)


@router.post("/analyze")
def analyze(req: ProspectivityRequest):
    return {
        "status": "ok",
        "latitude": req.latitude,
        "longitude": req.longitude,
        "prospectivity_screening_score": None,
        "classification": "screening_only",
        "warning": "No gold detection is claimed. Field and geological verification are required.",
    }