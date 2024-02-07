from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Sports(Base):
    """Модель различных видов спорта"""

    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Athletes(Base):
    """Модель данных об спортсмене"""

    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    age: Mapped[int]
    country: Mapped[str]

    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id", ondelete="SET NULL"))
