"""url_update

Revision ID: 0b2b1ed3cfbe
Revises: 6bb7ec2b9f6b
Create Date: 2018-05-29 09:02:08.821699

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '0b2b1ed3cfbe'
down_revision = '6bb7ec2b9f6b'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    url_update = """
        UPDATE article SET video='https://youtu.be/8w5Dsmt1KSw'
        WHERE UUID = '1c82c7ea-e984-41d3-b1e4-6228b400454d';
        
        UPDATE article SET video='https://youtu.be/0LAvsCfHvaQ'
        WHERE UUID = '040923f4-4436-4779-a363-f957afe53d98';

        UPDATE article SET video='https://youtu.be/_poto0Gg_NI'
        WHERE UUID = '86ca6744-97e7-4cf6-bfb4-9fadf1730c4b';

        UPDATE article SET video='https://youtu.be/0dEsNTmGx8s'
        WHERE UUID = '999d86d3-5f19-48e7-8170-466dbb297ad3';
    """
    connection.execute(url_update)


def downgrade():
    connection = op.get_bind()
    url_update = """
        UPDATE article SET video='https://youtu.be/1NdiDmsQxiw'
        WHERE UUID = '1c82c7ea-e984-41d3-b1e4-6228b400454d';
        
        UPDATE article SET video='https://youtu.be/bepRWDigz1Q'
        WHERE UUID = '040923f4-4436-4779-a363-f957afe53d98';

        UPDATE article SET video='https://youtu.be/E1JCPaUvNc4'
        WHERE UUID = '86ca6744-97e7-4cf6-bfb4-9fadf1730c4b';

        UPDATE article SET video='https://youtu.be/CS_hCY5nsH8'
        WHERE UUID = '999d86d3-5f19-48e7-8170-466dbb297ad3';
    """
    connection.execute(url_update)
