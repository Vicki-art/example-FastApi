"""add users table

Revision ID: b9b580e41804
Revises: 025e806ccd5f
Create Date: 2023-04-15 20:20:38.746757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9b580e41804'
down_revision = '025e806ccd5f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
                    sa.Column('id', sa.Integer(), nullable = False), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.String(), nullable = False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text("Now()")),
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
