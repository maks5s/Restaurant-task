from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .vote import Vote
    from .restaurant import Restaurant


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    is_admin: Mapped[bool] = mapped_column(Boolean(False))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id', ondelete="CASCADE"), index=True)

    user: Mapped["User"] = relationship(back_populates="employee_profiles")
    votes: Mapped[list["Vote"]] = relationship(back_populates="employee")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="employees")

    __table_args__ = (UniqueConstraint("user_id", "restaurant_id"),)
