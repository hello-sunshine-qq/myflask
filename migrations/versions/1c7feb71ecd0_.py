"""empty message

Revision ID: 1c7feb71ecd0
Revises: 33ca7850a15a
Create Date: 2017-12-01 09:40:32.068147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c7feb71ecd0'
down_revision = '33ca7850a15a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
