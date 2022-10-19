"""empty message

Revision ID: cd9da91b8727
Revises: 24acc2a06845
Create Date: 2022-10-19 03:29:34.903452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd9da91b8727'
down_revision = '24acc2a06845'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_comment_post_id_post')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
