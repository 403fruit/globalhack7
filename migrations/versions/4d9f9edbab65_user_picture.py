"""user picture

Revision ID: 4d9f9edbab65
Revises: bdbda1f6de37
Create Date: 2018-10-13 20:59:31.446732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d9f9edbab65'
down_revision = 'bdbda1f6de37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('picture', sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'picture')
    # ### end Alembic commands ###