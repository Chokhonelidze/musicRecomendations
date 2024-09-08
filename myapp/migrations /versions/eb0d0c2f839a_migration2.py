"""migration2

Revision ID: eb0d0c2f839a
Revises: 
Create Date: 2024-09-04 03:46:09.875018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb0d0c2f839a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('localLink', sa.String(length=200), nullable=True))



def downgrade():
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_column('localLink')
