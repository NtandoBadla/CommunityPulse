from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class FarmMetric(Base):
    __tablename__ = "farm_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    farm_id = Column(
        Integer,
        ForeignKey("farms.id"),
        nullable=False,
        index=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    temperature_c = Column(
        Float,
        nullable=True
    )

    humidity_pct = Column(
        Float,
        nullable=True
    )

    rainfall_mm = Column(
        Float,
        nullable=True
    )

    soil_moisture_pct = Column(
        Float,
        nullable=True
    )

    water_level_pct = Column(
        Float,
        nullable=True
    )

    crop_health_score = Column(
        Float,
        nullable=True
    )

    risk_level = Column(
        String(50),
        nullable=True
    )

    farm = relationship(
        "Farm",
        back_populates="metrics"
    )