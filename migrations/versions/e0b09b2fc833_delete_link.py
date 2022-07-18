"""delete link

Revision ID: e0b09b2fc833
Revises: 046e5436147c
Create Date: 2020-10-20 15:47:11.830717

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "e0b09b2fc833"
down_revision = "046e5436147c"
branch_labels = None
depends_on = None


def upgrade():
    """
    Remove BDA link for the "Food & diet" article.
    """
    op.execute("DELETE FROM link WHERE uuid = 'f06652ea-cf49-4e72-a340-0a59a12bdbcb'")


def downgrade():
    """
    No value in a downgrade here, so we'll leave it empty.
    """
