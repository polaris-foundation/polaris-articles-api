from typing import Dict, Optional

import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    base_url: str = Env().str("GDM_ARTICLES_BASE_URL", "http://gdm-articles-api:5000")
    return f"{base_url}/gdm/v1/article"


def create_article(body: Dict) -> Response:
    return requests.post(
        _get_base_url(),
        timeout=15,
        json=body,
    )


def get_article(uuid: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/{uuid}",
        timeout=15,
    )


def get_article_by_tag(tag: str) -> Response:
    return requests.get(
        f"{_get_base_url()}",
        params={"tag": tag},
        timeout=15,
    )


def get_all_articles(etag: Optional[str] = None) -> Response:
    return requests.get(_get_base_url(), timeout=15, headers={"If-None-Match": etag})


def update_article(uuid: str, body: Dict) -> Response:
    return requests.patch(
        f"{_get_base_url()}/{uuid}",
        timeout=15,
        json=body,
    )


def delete_article(uuid: str) -> Response:
    return requests.delete(
        f"{_get_base_url()}/{uuid}",
        timeout=15,
    )
