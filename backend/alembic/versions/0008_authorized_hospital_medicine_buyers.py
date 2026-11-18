"""Tie medicine orders to an authorized staff account and facility.

Revision ID: 0008_authorized_medicine_buyers
Revises: 0007_medicine_payments_wallet
"""
from alembic import op
import sqlalchemy as sa

revision = "0008_authorized_medicine_buyers"
down_revision = "0007_medicine_payments_wallet"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("medicine_orders")}
    existing_indexes = {index["name"] for index in sa.inspect(bind).get_indexes("medicine_orders")}

    if "buyer_user_id" not in columns or "buyer_hospital_id" not in columns:
        with op.batch_alter_table("medicine_orders") as batch_op:
            if "buyer_user_id" not in columns:
                batch_op.add_column(sa.Column("buyer_user_id", sa.Integer(), nullable=True))
                batch_op.create_foreign_key("fk_medicine_orders_buyer_user", "users", ["buyer_user_id"], ["id"], ondelete="SET NULL")
            if "buyer_hospital_id" not in columns:
                batch_op.add_column(sa.Column("buyer_hospital_id", sa.Integer(), nullable=True))
                batch_op.create_foreign_key("fk_medicine_orders_buyer_hospital", "hospitals", ["buyer_hospital_id"], ["id"], ondelete="SET NULL")

    if "ix_medicine_orders_buyer_user_id" not in existing_indexes:
        op.create_index("ix_medicine_orders_buyer_user_id", "medicine_orders", ["buyer_user_id"])
    if "ix_medicine_orders_buyer_hospital_id" not in existing_indexes:
        op.create_index("ix_medicine_orders_buyer_hospital_id", "medicine_orders", ["buyer_hospital_id"])


def downgrade() -> None:
    op.drop_index("ix_medicine_orders_buyer_hospital_id", table_name="medicine_orders")
    op.drop_index("ix_medicine_orders_buyer_user_id", table_name="medicine_orders")
    with op.batch_alter_table("medicine_orders") as batch_op:
        batch_op.drop_constraint("fk_medicine_orders_buyer_hospital", type_="foreignkey")
        batch_op.drop_constraint("fk_medicine_orders_buyer_user", type_="foreignkey")
        batch_op.drop_column("buyer_hospital_id")
        batch_op.drop_column("buyer_user_id")
