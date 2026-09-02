from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Crop(Base):
    __tablename__ = "crops"

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

    name = Column(
        String(100),
        nullable=False
    )

    planting_date = Column(
        Date,
        nullable=True
    )

    expected_harvest_date = Column(
        Date,
        nullable=True
    )

    growth_stage = Column(
        String(100),
        nullable=True
    )

    area_hectares = Column(
        Float,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="ACTIVE"
    )

    farm = relationship(
        "Farm",
        back_populates="crops"
    )