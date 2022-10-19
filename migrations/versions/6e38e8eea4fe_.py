"""empty message

Revision ID: 6e38e8eea4fe
Revises: cd9da91b8727
Create Date: 2022-10-19 03:51:25.533148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e38e8eea4fe'
down_revision = 'cd9da91b8727'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('post_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('post_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
