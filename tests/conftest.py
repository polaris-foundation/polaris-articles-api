from typing import Generator

import pytest
from flask import Flask
from flask_batteries_included.sqldb import db, generate_uuid

from gdm_articles_api.models.article import Article


@pytest.fixture()
def app() -> Flask:
    """Fixture that creates app for testing"""
    import gdm_articles_api.app

    return gdm_articles_api.app.create_app(
        testing=True, use_pgsql=False, use_sqlite=True
    )


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def article_with_tag() -> Generator[str, None, None]:
    article = Article(
        uuid=generate_uuid(),
        body="this is a really interesting article body",
        image="path/to/some/image.png",
        title="How to be healthy",
        intro="Best intro ever!",
        video="https://diabetes.video",
        tags=["recipe"],
    )
    db.session.add(article)
    db.session.commit()

    yield article.uuid

    db.session.delete(article)
    db.session.commit()
