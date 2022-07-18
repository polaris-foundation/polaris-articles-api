"""article_url

Revision ID: facbc0127b2e
Revises: a5a0e22aa50a
Create Date: 2018-07-13 10:30:58.905250

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'facbc0127b2e'
down_revision = 'a5a0e22aa50a'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    article_update = """
    UPDATE article
    SET image = '{image_path}/about.png'
    WHERE image LIKE '%%about.png';

    UPDATE article
    SET image = '{image_path}/food.png'
    WHERE image LIKE '%%food.png';

    UPDATE article
    SET image = '{image_path}/weight.jpg'
    WHERE image LIKE '%%weight.jpg';

    UPDATE article
    SET image = '{image_path}/activity.png'
    WHERE image LIKE '%%activity.png';

    UPDATE link
    SET image = '{image_path}/nhs.png'
    WHERE image LIKE '%%nhs.png';

    UPDATE link
    SET image = '{image_path}/diabetes-uk.png'
    WHERE image LIKE '%%diabetes-uk.png';

    UPDATE link
    SET image = '{image_path}/bda.png'
    WHERE image LIKE '%%bda.png';
    """
    connection.execute(article_update)


def downgrade():
    pass
