"""Fix wrong column name

Revision ID: 9aeda8f60a9b
Revises: 014a69de1525
Create Date: 2018-10-13 15:09:54.751473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9aeda8f60a9b'
down_revision = '014a69de1525'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'categories',
        'fontaweseome_icon',
        new_column_name='fontawesome_icon',
        existing_type=sa.UnicodeText(),
        existing_nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'categories',
        'fontawesome_icon',
        new_column_name='fontaweseome_icon',
        existing_type=sa.UnicodeText(),
        existing_nullable=True
    )
    # ### end Alembic commands ###
