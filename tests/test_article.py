import pytest
from flask_batteries_included.helpers import generate_uuid

from gdm_articles_api.models.article import Article


@pytest.mark.usefixtures("app")
class TestArticle:
    def test_image_url(self) -> None:
        article = Article(
            uuid=generate_uuid(),
            body="this is a really interesting article body",
            image="{image_path}/image.png",
            title="How to be healthy",
            intro="Best intro ever!",
            video="https://diabetes.video",
            tags=["blarg", "blorg"],
        )
        assert article.image_url() == "http://localhost/gdm/v1/image/image.png"
