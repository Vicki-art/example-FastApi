"""add more columns to posts

Revision ID: 07c6b0e4c3f4
Revises: 46c8e39842e1
Create Date: 2023-04-15 21:01:38.966883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07c6b0e4c3f4'
down_revision = '46c8e39842e1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default = "True", nullable = False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default =sa.text("Now()")))

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', "created_at")
    pass
