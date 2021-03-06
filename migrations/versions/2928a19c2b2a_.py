"""empty message

Revision ID: 2928a19c2b2a
Revises: 1c7feb71ecd0
Create Date: 2017-12-01 15:05:37.807183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2928a19c2b2a'
down_revision = '1c7feb71ecd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
