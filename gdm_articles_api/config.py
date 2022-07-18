from environs import Env
from flask import Flask


class Configuration:
    env = Env()
    GDM_ARTICLES_WWW: str = env.str("GDM_ARTICLES_WWW")


def init_config(app: Flask) -> None:
    app.config.from_object(Configuration)
