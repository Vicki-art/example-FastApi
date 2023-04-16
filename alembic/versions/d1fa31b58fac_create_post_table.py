"""create_post_table

Revision ID: d1fa31b58fac
Revises: 
Create Date: 2023-04-15 19:11:22.938251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1fa31b58fac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True, ), 
                    sa.Column('title', sa.String(), nullable = False))
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass