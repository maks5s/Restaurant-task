from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .menu import Menu
    from .employee import Employee
    from .dish import Dish


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255),)

    menus: Mapped[list["Menu"]] = relationship(back_populates="restaurant")
    employees: Mapped[list["Employee"]] = relationship(back_populates="restaurant")
    dishes: Mapped[list["Dish"]] = relationship(back_populates="restaurant")
