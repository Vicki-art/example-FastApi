"""add new column to the posts table

Revision ID: 025e806ccd5f
Revises: d1fa31b58fac
Create Date: 2023-04-15 19:51:04.596107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '025e806ccd5f'
down_revision = 'd1fa31b58fac'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
