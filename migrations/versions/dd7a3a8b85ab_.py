"""empty message

Revision ID: dd7a3a8b85ab
Revises: e1ca9d14d772
Create Date: 2023-04-03 10:47:37.181867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd7a3a8b85ab'
down_revision = 'e1ca9d14d772'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('slug')

    # ### end Alembic commands ###