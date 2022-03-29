"""empty message

Revision ID: 0586de1a4a1c
Revises: 18f2ad5b2844
Create Date: 2022-03-29 04:15:51.985155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0586de1a4a1c'
down_revision = '18f2ad5b2844'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
