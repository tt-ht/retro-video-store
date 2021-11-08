"""empty message

Revision ID: dbf10158564b
Revises: 
Create Date: 2021-11-06 18:54:36.584253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbf10158564b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('phone_number', sa.String(length=14), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rental',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('video',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('rental')
    op.drop_table('customer')
    # ### end Alembic commands ###
