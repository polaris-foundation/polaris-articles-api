"""update activity link

Revision ID: 8c6217b4b9ef
Revises: facbc0127b2e
Create Date: 2018-08-30 09:28:22.655860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c6217b4b9ef'
down_revision = 'facbc0127b2e'
branch_labels = None
depends_on = None


def upgrade():

    up = """
        UPDATE link set 
        url = 'https://www.nhs.uk/conditions/pregnancy-and-baby/pregnancy-exercise/', 
        modified = NOW(), 
        intro = 'Advice for exercise in pregnancy from the NHS.'
        WHERE uuid = '5b889584-8e88-4961-9c69-b2185cb713d9'
    """
    connection = op.get_bind()
    connection.execute(up)


def downgrade():
    down = """
        UPDATE link set 
        url = 'http://www.nhs.uk/news/2010/July07/Pages/new-nice-guidelines-weight-pregnancy.aspx', 
        modified = NOW(), 
        intro = 'New weight advice for pregnancy.'
        WHERE uuid = '5b889584-8e88-4961-9c69-b2185cb713d9'
    """
    connection = op.get_bind()
    connection.execute(down)
