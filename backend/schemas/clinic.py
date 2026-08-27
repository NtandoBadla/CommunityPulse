from pydantic import BaseModel


class ClinicCreate(BaseModel):
    name: str
    location: str
    address: str
    latitude: float
    longitude: float
    operating_hours: str
    capacity: int