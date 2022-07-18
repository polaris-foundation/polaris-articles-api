from typing import Any

import pytest
from flask.testing import FlaskClient
from marshmallow import RAISE

from gdm_articles_api.controllers import article_controller
from gdm_articles_api.models.api_spec import ArticleResponse


@pytest.mark.usefixtures("app")
class TestArticleController:
    def test_post_articles(self, client: FlaskClient) -> None:
        payload = {
            "body": "this is a really interesting article body",
            "image": "path/to/some/image.png",
            "title": "How to be healthy",
            "intro": "Best intro ever!",
            "video": "https://diabetes.video",
            "tags": ["recipe"],
            "links": [
                {
                    "title": "link title",
                    "intro": "link intro",
                    "body": "link body",
                    "image": "something.png",
                    "url": "https://some.url.com",
                }
            ],
        }

        response = client.post(
            "/gdm/v1/article", json=payload, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json["title"] == payload["title"]
        ArticleResponse().load(response.json, unknown=RAISE)

    def test_post_duplicate_article(self, client: Any, article_with_tag: str) -> None:
        payload = {
            "body": "this is a really interesting article body",
            "image": "path/to/some/image.png",
            "title": "How to be healthy",
            "intro": "Best intro ever!",
            "video": "https://diabetes.video",
            "tags": ["recipe"],
        }
        response = client.post(
            "/gdm/v1/article", json=payload, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 409

    def test_get_all_articles(self, client: Any, article_with_tag: str) -> None:
        response = client.get("/gdm/v1/article")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["uuid"] == article_with_tag

    def test_get_all_articles_filtered_by_tag(self, client: Any) -> None:
        articles = [
            {
                "body": "some body 1",
                "image": "path/to/some/image.png",
                "title": "some title 1",
                "intro": "some intro",
                "video": "https://diabetes.video",
                "tags": ["recipe"],
            },
            {
                "body": "some body 2",
                "image": "path/to/some/image.png",
                "title": "some title 2",
                "intro": "some intro",
                "video": "https://diabetes.video",
                "tags": [],
            },
            {
                "body": "some body 3",
                "image": "path/to/some/image.png",
                "title": "some title 3",
                "intro": "some intro",
                "video": "https://diabetes.video",
                "tags": ["recipe", "diabetes"],
            },
            {
                "body": "some body 4",
                "image": "path/to/some/image.png",
                "title": "some title 4",
                "intro": "some intro",
                "video": "https://diabetes.video",
                "tags": ["diabetes"],
            },
            {
                "body": "some body 5",
                "image": "path/to/some/image.png",
                "title": "some title 5",
                "intro": "some intro",
                "video": "https://diabetes.video",
                "tags": ["some_other_tag"],
            },
        ]
        for article in articles:
            response = client.post(
                "/gdm/v1/article",
                json=article,
                headers={"Authorization": "Bearer TOKEN"},
            )
            assert response.status_code == 200
        assert len(client.get("/gdm/v1/article?tag=recipe").json) == 2
        assert len(client.get("/gdm/v1/article?tag=diabetes").json) == 2
        assert len(client.get("/gdm/v1/article?tag=some_other_tag").json) == 1

    def test_get_all_articles_filtered_by_unknown_tag(
        self, client: Any, article_with_tag: str
    ) -> None:
        response = client.get("/gdm/v1/article?tag=something")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_get_article_by_uuid(self, client: Any, article_with_tag: str) -> None:
        response = client.open(f"/gdm/v1/article/{article_with_tag}")
        assert response == 200
        assert response.json["uuid"] == article_with_tag

    def test_update_article(self, client: Any, article_with_tag: str) -> None:
        update = {
            "title": "changed title",
            "intro": "A new intro",
            "body": "A new body!",
            "video": "https://gdm.video",
            "image": "something.png",
            "tags": ["newtag"],
            "links": [
                {
                    "title": "new link title",
                    "intro": "new link intro",
                    "body": "new link body",
                    "image": "newsomething.png",
                    "url": "https://some2.url.com",
                }
            ],
        }
        response = client.patch(
            f"/gdm/v1/article/{article_with_tag}",
            json=update,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json["title"] == update["title"]
        assert len(response.json["links"]) == 1
        assert len(response.json["tags"]) == 1

    def test_delete_article(self, client: Any, article_with_tag: str) -> None:
        response = client.delete(
            f"/gdm/v1/article/{article_with_tag}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        get_response = client.get(f"/gdm/v1/article/{article_with_tag}")
        assert get_response.status_code == 404

    def test_get_image(self, client: Any) -> None:
        response = client.get("/gdm/v1/image/about.png")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        ["image", "expected"],
        [
            (
                "https://something.com/folder/file.png",
                "https://something.com/folder/file.png",
            ),
            ("folder/file.png", "http://localhost/gdm/v1/image/folder/file.png"),
        ],
    )
    def test_to_image_url(self, image: str, expected: str) -> None:
        actual = article_controller.to_image_url(image)
        assert actual == expected
