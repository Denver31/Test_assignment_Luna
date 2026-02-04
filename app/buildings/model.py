from sqlalchemy import (
    String,
    Float, CheckConstraint, Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)

from app.database import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        back_populates="building",
        lazy="selectin",

    )

    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90",
            name="check_latitude_range",
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180",
            name="check_longitude_range",
        ),
        Index("idx_buildings_lat_lon", "latitude", "longitude"),

    )
