"""empty message

Revision ID: cfb07bcbd341
Revises: cd57316ae0c2
Create Date: 2021-10-25 17:19:03.117393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfb07bcbd341'
down_revision = 'cd57316ae0c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deposits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('date_start', sa.Date(), nullable=True),
    sa.Column('percent', sa.Float(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('amount_value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['amount_value'], ['currency.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deposits')
    # ### end Alembic commands ###
