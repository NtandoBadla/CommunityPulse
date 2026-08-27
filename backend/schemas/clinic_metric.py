from pydantic import BaseModel


class ClinicMetricCreate(BaseModel):
    patients_waiting: int
    patients_arrived: int
    patients_served: int
    active_staff: int
    average_wait_minutes: float