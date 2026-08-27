from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class ClinicMetric(Base):
    __tablename__ = "clinic_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id"),
        nullable=False,
        index=True
    )

    patients_waiting = Column(
        Integer,
        nullable=False,
        default=0
    )

    patients_arrived = Column(
        Integer,
        nullable=False,
        default=0
    )

    patients_served = Column(
        Integer,
        nullable=False,
        default=0
    )

    active_staff = Column(
        Integer,
        nullable=False,
        default=0
    )

    average_wait_minutes = Column(
        Float,
        nullable=False,
        default=0
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    clinic = relationship(
        "Clinic",
        back_populates="metrics"
    )