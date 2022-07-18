import pytest
from flask_batteries_included.sqldb import generate_uuid

from gdm_articles_api.models.link import Link


@pytest.mark.usefixtures("app")
class TestLink:
    def test_link_to_dict(self) -> None:
        link = Link(
            uuid=generate_uuid(),
            title="title",
            intro="intro",
            url="url",
            image="https//some.link",
        )
        actual = link.to_dict()
        assert actual["uuid"] == link.uuid
        assert link.image_url() == "https//some.link"

    def test_image_url(self) -> None:
        link = Link(
            uuid=generate_uuid(),
            title="title",
            intro="intro",
            url="url",
            image="{image_path}/something.png",
        )
        assert link.image_url() == "http://localhost/gdm/v1/image/something.png"
