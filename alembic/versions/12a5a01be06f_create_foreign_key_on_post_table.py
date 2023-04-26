"""create foreign key on post table

Revision ID: 12a5a01be06f
Revises: 0ae74d6fc3e7
Create Date: 2023-04-26 10:25:02.437328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12a5a01be06f'
down_revision = '0ae74d6fc3e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_owner_fk', source_table='posts', referent_table = 'users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    op.drop_constraint('post_owner_id', 'posts')
