from sqlalchemy import (
    String,
    ForeignKey, )
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)

from app.database import Base
from app.organizations.m2m import organization_activity


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    building: Mapped["Building"] = relationship(
        "Building",
        back_populates="organizations",
    )

    phones: Mapped[list["Phone"]] = relationship(
        "Phone",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations",
    )
