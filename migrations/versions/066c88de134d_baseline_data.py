"""baseline data

Revision ID: 066c88de134d
Revises: b68beb8b8d96
Create Date: 2018-04-10 15:29:08.913085

"""
from environs import Env
from alembic import op
from flask import current_app

env = Env()
GDM_ARTICLES_WWW = env.str("GDM_ARTICLES_WWW")

# revision identifiers, used by Alembic.
revision = "066c88de134d"
down_revision = "b68beb8b8d96"
branch_labels = None
depends_on = None


def image_url(filename, fqdn=None):

    if fqdn is None:
        with current_app.app_context():
            fqdn = current_app.config["GDM_ARTICLES_WWW"]

    base = "gdm/v1/image/"
    if not fqdn.endswith("/"):
        base = "/" + base
    return fqdn + base + filename


def upgrade():
    connection = op.get_bind()

    articles = (
        """
    INSERT INTO article
    (uuid, created, modified, title, image, deleted, body, video, intro)
    VALUES
    ('1c82c7ea-e984-41d3-b1e4-6228b400454d', '2018-04-10 15:14:20.119456',
    '2018-04-10 15:14:20.119461', 'About GDM',
    '"""
        + image_url("about.png", GDM_ARTICLES_WWW)
        + """', NULL,
    'GDM can be managed by healthy eating, physical activity, weight management and medication. This programme gives you more details about lifestyle management of GDM.',
    'https://youtu.be/1NdiDmsQxiw',
    'Gestational diabetes (or GDM) is a condition where you develop high blood glucose levels. This usually happens in the second half of pregnancy, GDM can affect you and your baby’s health.');

    INSERT INTO article
    (uuid, created, modified, title, image, deleted, body, video, intro)
    VALUES
    ('040923f4-4436-4779-a363-f957afe53d98', '2018-04-10 15:14:20.119464',
    '2018-04-10 15:14:20.119466', 'Food & diet',
    '"""
        + image_url("food.png", GDM_ARTICLES_WWW)
        + """', NULL,
    'A healthy diet is recommended for all pregnant women. There are some foods that you are advised to avoid during pregnancy, along with other dietary factors to consider when you have GDM and which affect your blood glucose. The main nutrient affecting blood glucose levels is called carbohydrate. This programme gives you more information about how diet can affect you, along with some recipes aimed to improve your condition and general health. You can find out more about diet and Gestational Diabetes by watching this video:', 'https://youtu.be/bepRWDigz1Q', 'What you eat during pregnancy can help your baby grow healthily and get the best start in life.');

    INSERT INTO article
    (uuid, created, modified, title, image, deleted, body, video, intro)
    VALUES
    ('86ca6744-97e7-4cf6-bfb4-9fadf1730c4b', '2018-04-10 15:14:20.119468',
    '2018-04-10 15:14:20.11947', 'Weight management',
    '"""
        + image_url("weight.jpg", GDM_ARTICLES_WWW)
        + """', NULL,
    'Although it is important to limit weight gain in pregnancy, dieting for weight loss is not recommended. Many women want to know how much weight they should gain in pregnancy. There are no guidelines in the UK, but there are some international recommendations. Weight gain during pregnancy depends on your weight and body mass index (BMI) before you became pregnant. You can find out more about weight management by watching this video:', 'https://youtu.be/E1JCPaUvNc4', 'Excessive weight gain in pregnancy can harm both your health and that of your baby.');

    INSERT INTO article
    (uuid, created, modified, title, image, deleted, body, video, intro)
    VALUES
    ('999d86d3-5f19-48e7-8170-466dbb297ad3', '2018-04-10 15:14:20.119472',
    '2018-04-10 15:14:20.119474', 'Activity & fitness',
    '"""
        + image_url("activity.png", GDM_ARTICLES_WWW)
        + """', NULL,
    'Physical activity can help control blood glucose levels, improve pregnancy outcomes as well as support weight management. You can find out more about activity and fitness by watching this video:', 'https://youtu.be/CS_hCY5nsH8', 'Physical activity is recommended as it benefits both you and your baby’s health.');
    """
    )
    connection.execute(articles)

    links = (
        """
    INSERT INTO link
    (uuid, created, modified, title, image, intro, article_id, deleted, url)
    VALUES
    ('49a61f45-2463-417e-bea7-c66c3c49bd25', '2018-04-10 15:14:20.124144', 
    '2018-04-10 15:14:20.124149', 'NHS.UK',
    '"""
        + image_url("nhs.png", GDM_ARTICLES_WWW)
        + """',
    'Overview and treatment information by the NHS.',
    '1c82c7ea-e984-41d3-b1e4-6228b400454d', NULL,
    'http://www.nhs.uk/conditions/gestational-diabetes/Pages/Introduction.aspx');

    INSERT INTO link
    (uuid, created, modified, title, image, intro, article_id, deleted, url)
    VALUES
    ('220423fa-1365-48e3-a4d2-7123740fcaf0', '2018-04-10 15:14:20.124151',
    '2018-04-10 15:14:20.124153', 'DIABETES.ORG.UK',
    '"""
        + image_url("diabetes-uk.png", GDM_ARTICLES_WWW)
        + """',
    'Basic information and advice from Diabetes UK.',
    '1c82c7ea-e984-41d3-b1e4-6228b400454d', NULL,
    'https://www.diabetes.org.uk/Diabetes-the-basics/Gestational-diabetes/');

    INSERT INTO link
    (uuid, created, modified, title, image, intro, article_id, deleted, url)
    VALUES ('e2fa4bfd-0f97-4b28-8b2b-11124fbcb173',
    '2018-04-10 15:14:20.124164', '2018-04-10 15:14:20.124166', 'NHS.UK',
    '"""
        + image_url("nhs.png", GDM_ARTICLES_WWW)
        + """',
    'Your pregnancy and baby guide from the NHS.',
    '040923f4-4436-4779-a363-f957afe53d98', NULL,
    'http://www.nhs.uk/conditions/pregnancy-and-baby/pages/healthy-pregnancy-diet.aspx');

    INSERT INTO link
    (uuid, created, modified, title, image, intro, article_id, deleted, url)
    VALUES ('f06652ea-cf49-4e72-a340-0a59a12bdbcb',
    '2018-04-10 15:14:20.124168', '2018-04-10 15:14:20.12417', 'BDA.UK.COM',
    '"""
        + image_url("bda.png", GDM_ARTICLES_WWW)
        + """',
    'Food fact sheet for pregnancy from the Association of UK Dieticians.',
    '040923f4-4436-4779-a363-f957afe53d98', NULL,
    'https://www.bda.uk.com/foodfacts/Pregnancy.pdf');

    INSERT INTO link
    (uuid, created, modified, title, image, intro, article_id, deleted, url)
    VALUES
    ('63fabf03-0cfc-4195-88c9-abc171320e0e', '2018-04-10 15:14:20.124172',
    '2018-04-10 15:14:20.124174', 'NHS.UK',
    '"""
        + image_url("nhs.png", GDM_ARTICLES_WWW)
        + """',
    'New weight advice for pregnancy from the NHS.',
    '86ca6744-97e7-4cf6-bfb4-9fadf1730c4b', NULL,
    'http://www.nhs.uk/news/2010/July07/Pages/new-nice-guidelines-weight-pregnancy.aspx');

    INSERT INTO link
    (uuid, created, modified, title, image, intro, article_id, deleted, url)
    VALUES ('5b889584-8e88-4961-9c69-b2185cb713d9',
    '2018-04-10 15:14:20.124176', '2018-04-10 15:14:20.124177',
    'NHS.UK', '"""
        + image_url("nhs.png", GDM_ARTICLES_WWW)
        + """',
    'New weight advice for pregnancy.', '999d86d3-5f19-48e7-8170-466dbb297ad3',
    NULL,
    'http://www.nhs.uk/news/2010/July07/Pages/new-nice-guidelines-weight-pregnancy.aspx');
    """
    )
    connection.execute(links)


def downgrade():
    pass
