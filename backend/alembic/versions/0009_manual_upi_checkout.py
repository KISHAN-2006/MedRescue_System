"""Add manual UPI collection fields to medicine orders.

Revision ID: 0009_manual_upi_checkout
Revises: 0008_authorized_medicine_buyers
"""
from alembic import op
import sqlalchemy as sa

revision = "0009_manual_upi_checkout"
down_revision = "0008_authorized_medicine_buyers"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("medicine_orders")}
    existing_indexes = {index["name"] for index in sa.inspect(bind).get_indexes("medicine_orders")}

    if "payment_method" not in columns:
        op.add_column("medicine_orders", sa.Column("payment_method", sa.String(20), nullable=False, server_default="razorpay"))
    if "buyer_payment_reference" not in columns:
        op.add_column("medicine_orders", sa.Column("buyer_payment_reference", sa.String(64), nullable=True))
    if "uq_medicine_orders_buyer_payment_reference" not in existing_indexes:
        op.create_index("uq_medicine_orders_buyer_payment_reference", "medicine_orders", ["buyer_payment_reference"], unique=True)


def downgrade() -> None:
    op.drop_index("uq_medicine_orders_buyer_payment_reference", table_name="medicine_orders")
    op.drop_column("medicine_orders", "buyer_payment_reference")
    op.drop_column("medicine_orders", "payment_method")
