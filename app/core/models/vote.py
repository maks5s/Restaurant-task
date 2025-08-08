from datetime import date

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee
    from .menu import Menu


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id', ondelete="CASCADE"))
    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id', ondelete="CASCADE"), index=True)
    vote_date: Mapped[date] = mapped_column(index=True, server_default=func.current_date())

    employee: Mapped["Employee"] = relationship(back_populates="votes")
    menu: Mapped["Menu"] = relationship(back_populates="votes")

    __table_args__ = (UniqueConstraint("employee_id", "vote_date"),)
