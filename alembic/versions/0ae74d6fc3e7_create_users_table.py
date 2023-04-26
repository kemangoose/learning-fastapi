"""create users table

Revision ID: 0ae74d6fc3e7
Revises: 055b087b51d8
Create Date: 2023-04-26 10:20:22.560114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ae74d6fc3e7'
down_revision = '055b087b51d8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key =True),
                    sa.Column('email', sa.String(), nullable = False, unique = True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP, server_default = sa.text('NOW()'))
                    )


def downgrade() -> None:
    op.drop_table('users')
