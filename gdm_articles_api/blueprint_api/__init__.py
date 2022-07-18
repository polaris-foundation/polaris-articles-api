from typing import Optional

import flask
from flask import Response

from gdm_articles_api.controllers import article_controller

api_blueprint = flask.Blueprint("articles", __name__)


@api_blueprint.route("/image/<filename>", methods=["GET"])
def get_image(filename: str) -> Response:
    """---
    get:
      summary: Get an image
      description: Get an image by filename.
      tags: [article]
      parameters:
        - name: filename
          in: path
          required: true
          description: Image filename to retrieve
          schema:
            type: string
            example: image.png
      responses:
        '200':
          description: Returns image for given filename
          content:
            image/png:
              schema:
                type: string
                format: binary
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return article_controller.get_image(filename)


@api_blueprint.route("/article", methods=["GET"])
def get_all_articles(tag: Optional[str] = None) -> Response:
    """---
    get:
      summary: Get all articles
      description: Retrieve all articles.
      tags: [article]
      parameters:
        - name: tag
          in: query
          required: false
          description: Tag to filter articles by
          schema:
            type: string
            example: recipe
      responses:
        '200':
          description: The requested articles for the given subject tag
          content:
            application/json:
              schema:
                type: array
                items: ArticleResponse
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return flask.jsonify(article_controller.get_all_articles(tag))


@api_blueprint.route("/article/<article_id>", methods=["GET"])
def get_article_by_id(article_id: str) -> Response:
    """---
    get:
      summary: Get article by UUID
      description: Get an article by UUID
      tags: [article]
      parameters:
        - name: article_id
          in: path
          required: true
          description: ID of the article to retrieve
          schema:
            type: string
            example: "3eba78fc-2e44-4fdd-9064-39e9330d78e8"
      responses:
        '200':
          description: The requested article
          content:
            application/json:
              schema: ArticleResponse
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return flask.jsonify(article_controller.get_article_by_id(article_id))


@api_blueprint.route("/article", methods=["POST"])
def create_article() -> Response:
    """---
    post:
      summary: Create new article
      description: Create a new article
      tags: [article]
      requestBody:
        description: JSON body containing the article
        required: true
        content:
          application/json:
            schema: ArticleSchema
      responses:
        '200':
          description: The new article
          content:
            application/json:
              schema: ArticleResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """

    response = article_controller.post_articles()

    return flask.jsonify(response)


@api_blueprint.route("/article/<article_id>", methods=["DELETE"])
def delete_article(article_id: str) -> Response:
    """---
    delete:
      summary: Delete article
      description: Delete a article by UUID
      tags: [article]
      parameters:
        - name: article_id
          in: path
          required: true
          description: The article UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '200':
          description: The deleted article
          content:
            application/json:
              schema: ArticleResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    response = article_controller.delete_article(article_id)

    return flask.jsonify(response)


@api_blueprint.route("/article/<article_id>", methods=["PATCH"])
def patch_article(article_id: str) -> Response:
    """---
    patch:
      summary: Update article
      description: Update a article by UUID
      tags: [article]
      parameters:
        - name: article_id
          in: path
          required: true
          description: The article UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      requestBody:
        description: JSON body containing the article fields to be updated
        required: true
        content:
          application/json:
            schema: ArticlePatchRequest
      responses:
        '200':
          description: The updated article
          content:
            application/json:
              schema: ArticleResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """

    response = article_controller.update_article(article_id)

    return flask.jsonify(response)
