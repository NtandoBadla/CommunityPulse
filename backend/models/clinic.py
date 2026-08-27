from sqlalchemy import Column, Integer, String, Float

from backend.database import Base


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)

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

    operating_hours = Column(
        String(100),
        nullable=True
    )

    capacity = Column(
        Integer,
        nullable=False,
        default=100
    )