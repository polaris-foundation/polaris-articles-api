from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    Identifier,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import EXCLUDE, Schema, fields

gdm_articles_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="GDM Articles API",
    info={
        "description": "The GDM Articles API is responsible for storing and retrieving articles for GDM."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)

initialise_apispec(gdm_articles_api_spec)


@openapi_schema(gdm_articles_api_spec)
class LinkSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    title = fields.String(description="Title", required=True, example="Diabetes")
    intro = fields.String(
        description="Introduction", required=True, example="This is the introduction"
    )
    url = fields.String(
        description="Link url", required=True, example="www.sensynehealth.com"
    )
    image = fields.String(description="Image url", required=True, example="image.png")


@openapi_schema(gdm_articles_api_spec)
class ArticleSchema(Schema):
    class Meta:
        description = "Article create request"
        unknown = EXCLUDE
        ordered = True

    title = fields.String(description="Title", required=True, example="Diabetes")
    intro = fields.String(
        description="Introduction", required=True, example="This is the introduction"
    )
    body = fields.String(
        description="Introduction", required=True, example="This is the body"
    )
    image = fields.String(description="Image url", required=True, example="image.png")
    video = fields.String(description="Video url", required=False, example="image.mp4")
    tags = fields.List(
        fields.String(description="Tag name", required=True, example="medication"),
        description="Tags with which the article is associated",
        required=False,
    )
    links = fields.Nested(
        LinkSchema,
        description="Links with which the article is associated",
        many=True,
    )


@openapi_schema(gdm_articles_api_spec)
class ArticlePatchRequest(Schema):
    class Meta:
        description = "Article update request"
        unknown = EXCLUDE
        ordered = True

    title = fields.String(description="Title", required=False, example="Diabetes")
    intro = fields.String(
        description="Introduction", required=False, example="This is the introduction"
    )
    body = fields.String(
        description="Introduction", required=False, example="This is the body"
    )
    image = fields.String(description="Image url", required=False, example="image.png")
    video = fields.String(description="Video url", required=False, example="image.mp4")
    tags = fields.List(
        fields.String(description="Tag name", required=False, example="medication"),
        description="Tags with which the article is associated",
        required=False,
    )
    links = fields.Nested(
        LinkSchema,
        description="Links with which the article is associated",
        many=True,
    )


@openapi_schema(gdm_articles_api_spec)
class ArticleResponse(Identifier, ArticleSchema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
