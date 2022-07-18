"""empty message

Revision ID: 6bb7ec2b9f6b
Revises: 066c88de134d
Create Date: 2018-04-16 17:35:46.358149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb7ec2b9f6b'
down_revision = '066c88de134d'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column('article', sa.Column('created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('article', sa.Column('modified_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('link', sa.Column('created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('link', sa.Column('modified_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('tag', sa.Column('created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('tag', sa.Column('modified_by_', sa.String(), nullable=False, server_default='sys'))


def downgrade():

    op.drop_column('tag', 'modified_by_')
    op.drop_column('tag', 'created_by_')
    op.drop_column('link', 'modified_by_')
    op.drop_column('link', 'created_by_')
    op.drop_column('article', 'modified_by_')
    op.drop_column('article', 'created_by_')
