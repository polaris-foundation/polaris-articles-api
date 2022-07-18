"""PLAT-657 upload DBm articles 2020-11-17

Revision ID: 675054358c9d
Revises: e0b09b2fc833
Create Date: 2020-11-17 14:57:06.941803

"""
import json
from datetime import datetime
from pathlib import Path

from alembic import op

# revision identifiers, used by Alembic.
revision = "675054358c9d"
down_revision = "e0b09b2fc833"
branch_labels = None
depends_on = None


def upgrade():
    file = Path(__file__).parent.parent / "articles_dbm_uk_default_20201117.json"
    articles = json.loads(file.read_text())
    query = ""
    for article in articles:
        tags = json.dumps(article["tags"])
        created = datetime.fromisoformat(article["created"].replace("Z", "+00:00"))
        modified = datetime.fromisoformat(article["modified"].replace("Z", "+00:00"))
        video = f"'{article['video']}'" if article.get("video") else "NULL"
        image = f"'{article['image']}'" if article.get("image") else "NULL"

        query += f"""
INSERT INTO article 
(uuid, created, modified, title, image, deleted, body, video, intro, tags)
VALUES
(
    '{article['uuid']}', '{created}', '{modified}', '{article['title']}', 
    {image}, NULL, '{article['body']}', {video}, '{article['intro']}', 
    '{tags}'
);
        """

        for link in article["links"]:
            link_created = datetime.fromisoformat(
                link["created"].replace("Z", "+00:00")
            )
            link_modified = datetime.fromisoformat(
                link["modified"].replace("Z", "+00:00")
            )
            query += f"""
INSERT INTO link 
(uuid, created, modified, title, image, intro, article_id, deleted, url)
VALUES
(
    '{link['uuid']}', '{link_created}', '{link_modified}', '{link['title']}',
    '{link['image']}', '{link['intro']}', '{article['uuid']}', NULL,
    '{link['url']}'
);
            """
    op.execute(query)


def downgrade():
    file = Path(__file__).parent.parent / "articles_dbm_uk_default_20201117.json"
    articles = json.loads(file.read_text())
    articles_uuids = []
    links_uuids = []
    for article in articles:
        articles_uuids.append(f"'{article['uuid']}'")
        for link in article["links"]:
            links_uuids.append(f"'{link['uuid']}'")

    query = f"""
DELETE FROM link WHERE uuid IN ({','.join(links_uuids)});
DELETE FROM article WHERE uuid IN ({','.join(articles_uuids)});
    """
    op.execute(query)
