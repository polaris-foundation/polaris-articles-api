"""article_text_update

Revision ID: a5a0e22aa50a
Revises: 0b2b1ed3cfbe
Create Date: 2018-07-09 15:48:15.790402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5a0e22aa50a'
down_revision = '0b2b1ed3cfbe'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    articles = """
    UPDATE article
    SET 
    intro = 'Gestational diabetes (or GDM) is a condition where you develop high blood glucose levels. This usually happens in the second half of pregnancy. GDM can affect you and your baby''s health.',
    body = 'GDM can be managed by healthy eating, physical activity, weight management and medication. This app contains some useful tips for maintaining a healthy lifestyle, to support your individual programme for managing GDM.'
    WHERE uuid = '1c82c7ea-e984-41d3-b1e4-6228b400454d';

    UPDATE article
    SET 
    body = 'A healthy diet is recommended for all pregnant women. There are some foods that you are advised to avoid during pregnancy, and there are other dietary factors to consider when you have GDM which can affect your blood glucose. The main nutrient affecting blood glucose levels is called carbohydrate. This programme gives you more information about how diet can affect you, along with some recipes aimed to improve your condition and general health. You can find out more about diet and Gestational Diabetes by watching this video:'
    WHERE uuid = '040923f4-4436-4779-a363-f957afe53d98';

    UPDATE article
    SET 
    intro = 'Excessive weight gain in pregnancy can harm you and your baby''s health.', 
    body = 'Although it is important to limit weight gain in pregnancy, dieting for weight loss is not recommended. Many women want to know how much weight they should gain in pregnancy. Weight gain during pregnancy depends on your weight and body mass index (BMI) before you became pregnant. You can find out more about weight management by watching this video:'
    WHERE uuid = '86ca6744-97e7-4cf6-bfb4-9fadf1730c4b';

    """
    connection.execute(articles)

def downgrade():
    pass
