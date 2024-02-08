from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.athletes.models import Athlete, Sport


class TournamentAthleteAssociations(Base):
    """Ассоциативная модель для связи М:М Турниров и Спортсменыов"""
    __tablename__ = "tournament_athlete_associations"
    __table_args__ = (
        UniqueConstraint(
            "tournament_id", "athlete_id", name="idx_unique_tournament_athlete"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"))
    place: Mapped[int] = mapped_column(nullable=True)


class Tournament(Base):
    """Модель турнира"""

    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    datetime: Mapped[datetime]
    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id", ondelete="SET NULL"))

    sport: Mapped["Sport"] = relationship(back_populates="tournaments")
    athletes: Mapped[list["Athlete"]] = relationship(
        secondary="tournament_athlete_associations", back_populates="tournaments"
    )
