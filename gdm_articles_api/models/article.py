from datetime import datetime
from typing import Dict, Optional

import flask
from flask_batteries_included.sqldb import ModelIdentifier, db

from gdm_articles_api.query.softdelete import QueryWithSoftDelete


class Article(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    title = db.Column(db.String, unique=False, nullable=False)
    image = db.Column(db.String, unique=False, nullable=False)
    intro = db.Column(db.String, unique=False, nullable=False)
    body = db.Column(db.String, unique=False, nullable=False)
    video = db.Column(db.String, unique=False, nullable=True)
    deleted = db.Column(db.DateTime, unique=False, nullable=True)
    tags = db.Column(db.JSON, unique=False, nullable=False)
    links = db.relationship("Link")

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {"tags": list, "video": str, "links": list},
            "required": {"title": str, "image": str, "intro": str, "body": str},
            "updatable": {
                "title": str,
                "image": str,
                "video": str,
                "body": str,
                "tags": list,
                "links": list,
            },
        }

    def image_url(self) -> Optional[str]:
        if self.image is None or "{image_path}" not in self.image:
            return self.image

        base = "gdm/v1/image/"
        gdm_articles_www: str = flask.current_app.config["GDM_ARTICLES_WWW"]
        if not gdm_articles_www.endswith("/"):
            base = "/" + base

        url = self.image.replace("{image_path}/", gdm_articles_www + base)
        return url

    def to_dict(self) -> Dict:
        article = {
            "title": self.title,
            "image": self.image_url(),
            "video": self.video,
            "intro": self.intro,
            "body": self.body,
            "tags": self.tags,
            "links": [link.to_dict() for link in self.links],
            **self.pack_identifier(),
        }

        if self.deleted is not None:
            article["deleted"] = self.deleted
        return article

    def delete(self) -> None:
        self.deleted = datetime.utcnow()
