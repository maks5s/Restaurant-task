from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .menu import Menu
    from .dish import Dish


class MenuDish(Base):
    __tablename__ = "menu_dishes"

    menu_id: Mapped[int] = mapped_column(
        ForeignKey('menus.id', ondelete="CASCADE"),
        primary_key=True
    )
    dish_id: Mapped[int] = mapped_column(
        ForeignKey('dishes.id', ondelete="CASCADE"),
        primary_key=True
    )

    menu: Mapped["Menu"] = relationship(back_populates="menu_dishes")
    dish: Mapped["Dish"] = relationship(back_populates="menu_dishes")

    __table_args__ = (UniqueConstraint("menu_id", "dish_id"),)
