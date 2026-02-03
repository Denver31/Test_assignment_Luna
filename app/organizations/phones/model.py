from sqlalchemy import (
    String,
    ForeignKey, CheckConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)

from app.database import Base


class Phone(Base):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="phones",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint(
            "length(phone) >= 6",
            name="check_phone_min_length",
        ),
    )
