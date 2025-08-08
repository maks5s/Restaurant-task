"""Initial migration

Revision ID: 4fb4d313ac8e
Revises:
Create Date: 2025-08-08 00:33:19.166830

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4fb4d313ac8e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_restaurants")),
    )
    op.create_index(
        op.f("ix_restaurants_id"), "restaurants", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_restaurants_name"), "restaurants", ["name"], unique=True
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )
    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["restaurant_id"],
            ["restaurants.id"],
            name=op.f("fk_dishes_restaurant_id_restaurants"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dishes")),
        sa.UniqueConstraint(
            "name", "restaurant_id", name=op.f("uq_dishes_name_restaurant_id")
        ),
    )
    op.create_index(op.f("ix_dishes_id"), "dishes", ["id"], unique=False)
    op.create_index(
        op.f("ix_dishes_restaurant_id"),
        "dishes",
        ["restaurant_id"],
        unique=False,
    )
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["restaurant_id"],
            ["restaurants.id"],
            name=op.f("fk_employees_restaurant_id_restaurants"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_employees_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_employees")),
        sa.UniqueConstraint(
            "user_id",
            "restaurant_id",
            name=op.f("uq_employees_user_id_restaurant_id"),
        ),
    )
    op.create_index(op.f("ix_employees_id"), "employees", ["id"], unique=False)
    op.create_index(
        op.f("ix_employees_restaurant_id"),
        "employees",
        ["restaurant_id"],
        unique=False,
    )
    op.create_table(
        "menus",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["restaurant_id"],
            ["restaurants.id"],
            name=op.f("fk_menus_restaurant_id_restaurants"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_menus")),
    )
    op.create_index(op.f("ix_menus_date"), "menus", ["date"], unique=False)
    op.create_index(op.f("ix_menus_id"), "menus", ["id"], unique=False)
    op.create_index(
        op.f("ix_menus_restaurant_id"),
        "menus",
        ["restaurant_id"],
        unique=False,
    )
    op.create_table(
        "menu_dishes",
        sa.Column("menu_id", sa.Integer(), nullable=False),
        sa.Column("dish_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["dishes.id"],
            name=op.f("fk_menu_dishes_dish_id_dishes"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["menus.id"],
            name=op.f("fk_menu_dishes_menu_id_menus"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "menu_id", "dish_id", name=op.f("pk_menu_dishes")
        ),
        sa.UniqueConstraint(
            "menu_id", "dish_id", name=op.f("uq_menu_dishes_menu_id_dish_id")
        ),
    )
    op.create_table(
        "votes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("menu_id", sa.Integer(), nullable=False),
        sa.Column(
            "vote_date",
            sa.Date(),
            server_default=sa.text("CURRENT_DATE"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
            name=op.f("fk_votes_employee_id_employees"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["menus.id"],
            name=op.f("fk_votes_menu_id_menus"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_votes")),
        sa.UniqueConstraint(
            "employee_id",
            "vote_date",
            name=op.f("uq_votes_employee_id_vote_date"),
        ),
    )
    op.create_index(op.f("ix_votes_id"), "votes", ["id"], unique=False)
    op.create_index(
        op.f("ix_votes_menu_id"), "votes", ["menu_id"], unique=False
    )
    op.create_index(
        op.f("ix_votes_vote_date"), "votes", ["vote_date"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_votes_vote_date"), table_name="votes")
    op.drop_index(op.f("ix_votes_menu_id"), table_name="votes")
    op.drop_index(op.f("ix_votes_id"), table_name="votes")
    op.drop_table("votes")
    op.drop_table("menu_dishes")
    op.drop_index(op.f("ix_menus_restaurant_id"), table_name="menus")
    op.drop_index(op.f("ix_menus_id"), table_name="menus")
    op.drop_index(op.f("ix_menus_date"), table_name="menus")
    op.drop_table("menus")
    op.drop_index(op.f("ix_employees_restaurant_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_id"), table_name="employees")
    op.drop_table("employees")
    op.drop_index(op.f("ix_dishes_restaurant_id"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_id"), table_name="dishes")
    op.drop_table("dishes")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_restaurants_name"), table_name="restaurants")
    op.drop_index(op.f("ix_restaurants_id"), table_name="restaurants")
    op.drop_table("restaurants")
