from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class SatelliteRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    start_date: date
    end_date: date

    max_cloud: float = Field(
        default=20,
        ge=0,
        le=100,
    )


class MagnetometerRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    magnetometer_nt: float


class ProspectivityRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    magnetometer_nt: Optional[float] = None


class SampleRequest(BaseModel):
    sample_no: str = Field(
        min_length=1,
        max_length=100,
    )

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    photo_url: Optional[str] = None
    magnetometer_nt: Optional[float] = None

    gps_accuracy_m: Optional[float] = Field(
        default=None,
        ge=0,
    )

    satellite_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    notes: Optional[str] = None