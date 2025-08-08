from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .restaurant import Restaurant
    from .menu_dish import MenuDish


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id', ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(255),)

    restaurant: Mapped["Restaurant"] = relationship(back_populates="dishes")
    menu_dishes: Mapped[list["MenuDish"]] = relationship(back_populates="dish")

    __table_args__ = (UniqueConstraint("name", "restaurant_id"),)
