from typing import Dict, List, Optional

import connexion
import flask
from flask import Response
from flask_batteries_included.helpers.error_handler import DuplicateResourceException
from flask_batteries_included.sqldb import db, generate_uuid
from she_logging import logger
from sqlalchemy import and_

from gdm_articles_api.models.article import Article
from gdm_articles_api.models.link import Link


def get_article_by_id(article_id: str) -> Dict:
    logger.debug("Getting article by UUID %s", article_id)
    article: Article = Article.query.filter_by(uuid=article_id).first_or_404()
    return article.to_dict()


def delete_article(article_id: str) -> Dict:
    logger.debug("Deleting article by UUID %s", article_id)
    article = Article.query.filter_by(uuid=article_id).first_or_404()
    article.delete()
    db.session.commit()
    return article.to_dict()


def get_all_articles(tag: Optional[str] = None) -> List[Dict]:
    logger.debug("Getting articles")
    articles: List[Article] = Article.query.all()
    if tag:
        logger.debug("Filtering articles by tag %s", tag)
        return [a.to_dict() for a in articles if tag in a.tags]
    else:
        return [a.to_dict() for a in articles]


def post_articles() -> Dict:
    article = connexion.request.get_json()
    logger.debug("Creating new article with title %s", article["title"])

    if _is_existing_article(article):
        raise DuplicateResourceException("Article already exists")

    links: List[Link] = []
    for link in article.get("links", []):
        links.append(
            Link(
                uuid=generate_uuid(),
                title=link["title"],
                intro=link["intro"],
                url=link["url"],
                image=to_image_url(link["image"]),
            )
        )

    insert = Article(
        uuid=generate_uuid(),
        title=article["title"],
        intro=article["intro"],
        body=article["body"],
        image=to_image_url(article["image"]),
        video=article.get("video", None),
        tags=article.get("tags", []),
        links=links,
    )

    db.session.add(insert)
    db.session.commit()

    return insert.to_dict()


def _is_existing_article(article: Dict) -> bool:
    is_existing = Article.query.filter(
        and_(Article.title.ilike(article["title"]), Article.body.ilike(article["body"]))
    ).first()
    return is_existing is not None


def update_article(article_id: str) -> Dict:
    article: Dict = connexion.request.get_json()
    logger.debug("Updating article with UUID %s", article_id)

    article_db = Article.query.filter_by(uuid=article_id).first_or_404()

    has_one_or_more_values = False
    if "tags" in article:
        has_one_or_more_values = True

    if "title" in article:
        has_one_or_more_values = True

        if "title" not in article or len(article["title"]) == 0:
            raise KeyError("'title' must contain a valid value")
        if article["title"] != article_db.title:
            if _is_existing_article(article):
                raise KeyError("Cannot change 'article' to match existing article")

    if "intro" in article:
        has_one_or_more_values = True

        if len(article["intro"]) == 0:
            raise KeyError("'intro' must contain a valid value")
        if article["intro"] != article_db.intro:
            if _is_existing_article(article):
                raise KeyError("Cannot change 'article' to match existing article")

    if "image" in article:
        has_one_or_more_values = True

        if len(article["image"]) == 0:
            raise KeyError("'image' must contain a valid value")

    if "video" in article:
        has_one_or_more_values = True

        if len(article["video"]) == 0:
            raise KeyError("'video' must contain a valid value")

    if "body" in article:
        has_one_or_more_values = True

        if len(article["body"]) == 0:
            raise KeyError("'body' must contain a valid value")
        if article["body"] != article_db.body:
            if _is_existing_article(article):
                raise KeyError("Cannot change 'article' to match existing article")

    if has_one_or_more_values is False:
        raise KeyError(
            "'title', 'image', 'body', or 'tags' are required to update article"
        )

    if "links" in article:
        links = []
        for link in article["links"]:
            link_db = None
            if "uuid" in link:
                link_query_result = Link.query.filter(uuid=link["uuid"]).first()
                if link_query_result:
                    link_db = link_query_result
            if link_db is None:
                link_db = Link(
                    uuid=generate_uuid(),
                    title=link["title"],
                    intro=link["intro"],
                    url=link["url"],
                    image=to_image_url(link["image"]),
                )

            links.append(link_db)
        article_db.links = links

    if "title" in article:
        article_db.title = article["title"]

    if "intro" in article:
        article_db.intro = article["intro"]

    if "body" in article:
        article_db.body = article["body"]

    if "image" in article:
        article_db.image = to_image_url(article["image"])

    if "video" in article:
        article_db.video = article["video"]

    if "tags" in article:
        article_db.tags = article["tags"]

    db.session.commit()
    return article_db.to_dict()


def get_image(filename: str) -> Response:
    static_dir = "static/images"
    return flask.send_from_directory(static_dir, filename)


def to_image_url(image: Optional[str]) -> Optional[str]:
    if image is None or image.startswith("http"):
        return image

    base = "gdm/v1/image/"
    gdm_articles_www: str = flask.current_app.config["GDM_ARTICLES_WWW"]
    if not gdm_articles_www.endswith("/"):
        base = "/" + base

    return gdm_articles_www + base + image
