from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Sport(Base):
    """Модель различных видов спорта"""

    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="sport")


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

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name})"
