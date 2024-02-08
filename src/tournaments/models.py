from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.athletes.models import Athlete, Sport


#  Создание ассоциативной таблицы Турниры и Спортсмены для M:M
tournament_athlete_association_table = Table(
    "tournament_athlete_associations",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("tournament_id", ForeignKey("tournaments.id"), nullable=False),
    Column("athlete_id", ForeignKey("athletes.id"), nullable=False),
    Column("place", Integer, nullable=True),
    UniqueConstraint(
        "tournament_id", "athlete_id", name="idx_unique_tournament_athlete"
    ),
)


class Tournament(Base):
    """Модель турнира"""

    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    datetime: Mapped[datetime]
    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id", ondelete="SET NULL"))

    sport: Mapped["Sport"] = relationship(back_populates="tournaments")
    athletes: Mapped[list["Athlete"]] = relationship(
        secondary=tournament_athlete_association_table, back_populates="tournaments"
    )
