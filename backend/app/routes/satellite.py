import os

from fastapi import APIRouter, HTTPException
from pystac_client import Client
import planetary_computer

from app.schemas import SatelliteRequest


router = APIRouter(
    prefix="/api/v1/satellite",
    tags=["satellite"],
)

CATALOG = "https://planetarycomputer.microsoft.com/api/stac/v1"


@router.post("/analyze")
def analyze(req: SatelliteRequest):
    if req.end_date < req.start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date must be after start_date",
        )

    try:
        catalog = Client.open(
            CATALOG,
            modifier=planetary_computer.sign_inplace,
        )

        search = catalog.search(
            collections=[
                os.getenv(
                    "SATELLITE_COLLECTION",
                    "sentinel-2-l2a",
                )
            ],
            intersects={
                "type": "Point",
                "coordinates": [
                    req.longitude,
                    req.latitude,
                ],
            },
            datetime=(
                f"{req.start_date.isoformat()}/"
                f"{req.end_date.isoformat()}"
            ),
            query={
                "eo:cloud_cover": {
                    "lte": req.max_cloud,
                }
            },
            max_items=20,
        )

        items = list(search.items())

        if not items:
            return {
                "status": "no_data",
                "source": "Microsoft Planetary Computer",
                "collection": "sentinel-2-l2a",
                "items_found": 0,
                "prospectivity_screening_score": None,
            }

        best = sorted(
            items,
            key=lambda x: x.properties.get(
                "eo:cloud_cover",
                100,
            ),
        )[0]

        return {
            "status": "ok",
            "source": "Microsoft Planetary Computer",
            "collection": "sentinel-2-l2a",
            "items_found": len(items),
            "best_item": best.id,
            "cloud_cover": best.properties.get(
                "eo:cloud_cover"
            ),
            "datetime": (
                best.datetime.isoformat()
                if best.datetime
                else None
            ),
            "prospectivity_screening_score": None,
            "note": (
                "STAC discovery succeeded. "
                "No gold-detection claim is made."
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Sentinel-2 catalog error: {exc}",
        )