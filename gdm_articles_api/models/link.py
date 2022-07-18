from datetime import datetime
from typing import Dict, Optional

import flask
from flask_batteries_included.sqldb import ModelIdentifier, db

from gdm_articles_api.query.softdelete import QueryWithSoftDelete


class Link(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    title = db.Column(db.String, unique=False, nullable=False)
    image = db.Column(db.String, unique=False, nullable=False)
    intro = db.Column(db.String, unique=False, nullable=False)
    url = db.Column(db.String, unique=False, nullable=False)

    article_id = db.Column(db.String, db.ForeignKey("article.uuid"))

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    @staticmethod
    def schema() -> Dict:
        return {
            "required": {"title": str, "image": str, "intro": str, "url": str},
            "updatable": {"title": str, "image": str, "intro": str, "url": str},
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
        link = {
            "title": self.title,
            "image": self.image_url(),
            "intro": self.intro,
            "url": self.url,
            **self.pack_identifier(),
        }

        if self.deleted:
            link["deleted"] = self.deleted

        return link

    def delete(self) -> None:
        self.deleted = datetime.utcnow()
