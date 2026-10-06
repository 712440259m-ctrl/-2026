from fastapi import APIRouter, HTTPException

from app.db import get_conn
from app.schemas import SampleRequest


router = APIRouter(
    prefix="/api/v1/samples",
    tags=["samples"],
)


@router.post("")
def create_sample(req: SampleRequest):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO samples
                    (
                        sample_no,
                        geom,
                        gps_accuracy_m,
                        magnetometer_nt,
                        satellite_score,
                        photo_url,
                        notes
                    )
                    VALUES (
                        %s,
                        ST_SetSRID(
                            ST_MakePoint(%s, %s),
                            4326
                        ),
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id, sample_no, created_at
                    """,
                    (
                        req.sample_no,
                        req.longitude,
                        req.latitude,
                        req.gps_accuracy_m,
                        req.magnetometer_nt,
                        req.satellite_score,
                        req.photo_url,
                        req.notes,
                    ),
                )

                row = cur.fetchone()

        return {
            "status": "ok",
            "id": row[0],
            "sample_no": row[1],
            "created_at": row[2],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"sample save error: {exc}",
        )