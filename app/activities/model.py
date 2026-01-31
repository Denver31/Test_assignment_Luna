from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
    )

    parent: Mapped["Activity | None"] = relationship(
        "Activity",
        back_populates="children",
    )

