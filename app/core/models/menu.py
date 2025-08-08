import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .restaurant import Restaurant
    from .menu_dish import MenuDish
    from .vote import Vote


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id', ondelete="CASCADE"), index=True)
    date: Mapped[datetime.date] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(String(50))

    restaurant: Mapped["Restaurant"] = relationship(back_populates="menus")
    menu_dishes: Mapped[list["MenuDish"]] = relationship(back_populates="menu")
    votes: Mapped[list["Vote"]] = relationship(back_populates="menu")
