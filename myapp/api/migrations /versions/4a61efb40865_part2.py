"""part2 

Revision ID: 4a61efb40865
Revises: e541a0e95d2a
Create Date: 2023-12-19 00:16:10.158825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a61efb40865'
down_revision = 'e541a0e95d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.VARCHAR(length=200), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
