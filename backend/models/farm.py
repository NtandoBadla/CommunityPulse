from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    location = Column(
        String(150),
        nullable=False
    )

    address = Column(
        String(255),
        nullable=True
    )

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )

    farm_size_hectares = Column(
        Float,
        nullable=True
    )

    soil_type = Column(
        String(100),
        nullable=True
    )

    water_availability = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    crops = relationship(
        "Crop",
        back_populates="farm",
        cascade="all, delete-orphan"
    )

    metrics = relationship(
        "FarmMetric",
        back_populates="farm",
        cascade="all, delete-orphan"
    )