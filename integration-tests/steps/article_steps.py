import json
from pathlib import Path
from typing import Dict, List

from behave import step, then, when
from behave.runner import Context
from clients import article_client
from environs import Env
from faker import Faker
from helpers import article as article_helper
from requests import Response, codes


@step("a new article is created")
def create_new_article(context: Context) -> None:
    tag = _get_random_tag_body()
    context.article_tags += [tag]
    body = article_helper.get_body(tags=context.article_tags)
    context.article_body = body

    response: Response = article_client.create_article(body=body)
    response.raise_for_status()
    response_json: dict = response.json()
    assert "uuid" in response_json
    context.article_uuid = response_json["uuid"]
    context.article_uuids += [response_json["uuid"]]


@step("the article {can_or_can_not} be retrieved by its {what}")
def get_article_by_uuid_or_tag(
    context: Context, can_or_can_not: str, what: str
) -> None:
    if what == "uuid":
        response: Response = article_client.get_article(uuid=context.article_uuid)
    elif what == "tag":
        response = article_client.get_article_by_tag(tag=context.article_tags[0])
    else:
        raise ValueError(f"Unable to handle parameter {what}")

    if can_or_can_not == "can":
        response.raise_for_status()
        if what == "tag":
            # search for tags returns a list
            context.api_article_body = response.json()[0]
        else:
            context.api_article_body = response.json()
    else:
        if what == "tag":
            # search for tags returns a list, hence empty if not found
            assert len(response.json()) == 0
        else:
            assert response.status_code == codes.not_found


@when("all articles are retrieved")
def retrieve_all_articles(context: Context) -> None:
    response: Response = article_client.get_all_articles()
    response.raise_for_status()
    context.all_articles_response = response.json()


@when("all articles are retrieved using the previous ETag")
def retrieve_all_articles_using_etag(context: Context) -> None:
    last_etag: str = context.all_articles_response.headers["ETag"]
    response: Response = article_client.get_all_articles(etag=last_etag)
    response.raise_for_status()
    context.repeat_response = response.json()


@then("an the service indicates the resource has not been modified")
def assert_not_modified(context: Context) -> None:
    assert context.repeat_response.status_code == 304
    assert context.repeat_response.json() is None


@step("the article {can_or_can_not} be seen in all articles")
def assert_article_in_all_articles(context: Context, can_or_can_not: str) -> None:
    all_ids: list = [q["uuid"] for q in context.all_articles_response]
    if can_or_can_not == "can":
        assert context.article_uuid in all_ids
    else:
        assert context.article_uuid not in all_ids


@step("the article matches that previously created")
def assert_article_body(context: Context) -> None:
    _assert_articles_are_identical(context.article_body, context.api_article_body)


@step("the article is updated")
def update_article(context: Context) -> None:
    body: dict = article_helper.get_body()
    context.article_body = body

    response: Response = article_client.update_article(
        uuid=context.article_uuid, body=body
    )
    response.raise_for_status()
    context.updated_article_body = response.json()


@step("the updated article is persisted")
def assert_updated_body(context: Context) -> None:
    _assert_articles_are_identical(context.article_body, context.updated_article_body)


@step("the article is deleted")
def delete_article(context: Context) -> None:
    response: Response = article_client.delete_article(uuid=context.article_uuid)
    response.raise_for_status()


def _assert_articles_are_identical(expected: dict, actual: dict) -> None:
    assert sorted(expected["tags"]) == sorted([tag for tag in actual["tags"]])

    for attribute in ["body", "image", "intro", "title", "video"]:
        assert expected[attribute] == actual[attribute]

    for link_attribute in ["image", "intro", "title", "url"]:
        assert (
            expected["links"][0][link_attribute] == actual["links"][0][link_attribute]
        )


@then("there are the expected {locale} articles")
def check_static_articles_by_locale(context: Context, locale: str) -> None:
    tag = f"gdm-{locale.lower()}-default"
    static_articles_file = (
        Path(__file__).parent.parent / "fixtures" / "expected_static_articles.json"
    )
    static_articles = json.loads(
        static_articles_file.read_text().replace(
            "{image_path}", f"{Env().str('GDM_ARTICLES_WWW')}/gdm/v1/image"
        )
    )
    expected_articles: List[Dict] = [a for a in static_articles if tag in a["tags"]]
    response: Response = article_client.get_article_by_tag(
        tag=f"gdm-{locale.lower()}-default",
    )
    response.raise_for_status()
    assert response.json() == expected_articles


def _get_random_tag_body() -> str:
    fake: Faker = Faker()
    return f"{fake.word()}{fake.random_int()}"
