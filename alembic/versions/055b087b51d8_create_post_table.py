"""create post table

Revision ID: 055b087b51d8
Revises: 
Create Date: 2023-04-26 10:14:42.328121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '055b087b51d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key = True),
                    sa.Column('title', sa.String(), nullable = False),
                    sa.Column('content', sa.String(), nullable = False),
                    sa.Column('published', sa.Boolean(), nullable = True, server_default = 'TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP, server_default = sa.text('NOW()'))
                    )


def downgrade() -> None:
    op.drop_table('posts')
