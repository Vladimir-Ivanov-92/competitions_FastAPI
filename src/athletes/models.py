from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.tournaments.models import Tournament, TournamentAthleteAssociations


class Sport(Base):
    """Модель различных видов спорта"""

    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="sport")
    tournaments: Mapped[list["Tournament"]] = relationship(back_populates="sport")


class Athlete(Base):
    """Модель данных об спортсмене"""

    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    age: Mapped[int]
    country: Mapped[str]
    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id", ondelete="SET NULL"))

    sport: Mapped["Sport"] = relationship(back_populates="athletes")
    # tournaments: Mapped[list["Tournament"]] = relationship(
    #     secondary="tournament_athlete_associations", back_populates="athletes"
    # )
    tournaments_associations: Mapped[list["TournamentAthleteAssociations"]] = (
        relationship(back_populates="athlete")
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name})"
