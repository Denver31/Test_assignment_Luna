from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    CheckConstraint, text,
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from app.database import Base
from app.organizations.m2m import organization_activity
from app.organizations.model import Organization


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default=text("1"),
    )

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
    )

    parent: Mapped["Activity | None"] = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="children",
        lazy="selectin",

    )

    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin",

    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities",
        lazy="selectin",

    )

    __table_args__ = (
        CheckConstraint(
            "level >= 1 AND level <= 3",
            name="check_activity_level",
        ),
    )
