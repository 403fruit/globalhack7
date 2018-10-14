"""empty message

Revision ID: f637d261c5b3
Revises: 479aa1adc1c5
Create Date: 2018-10-14 00:20:15.329499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f637d261c5b3'
down_revision = '479aa1adc1c5'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='users',
        column_name='phone',
        type_=sa.Unicode(255),
        existing_type=sa.BigInteger
    )
    op.alter_column(
        table_name='users',
        column_name='secondary_phone',
        type_=sa.Unicode(255),
        existing_type=sa.BigInteger
    )


def downgrade():
    op.alter_column(
        table_name='users',
        column_name='phone',
        type_=sa.BigInteger,
        existing_type=sa.Unicode(255)
    )
    op.alter_column(
        table_name='users',
        column_name='secondary_phone',
        type_=sa.BigInteger,
        existing_type=sa.Unicode(255)
    )
