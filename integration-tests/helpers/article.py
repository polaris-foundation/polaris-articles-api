from typing import Any, Dict, Optional

from faker import Faker


def get_body(**kwargs: Optional[Dict]) -> Dict:
    fake: Faker = Faker()
    default_body: Dict[str, Any] = {
        "body": fake.text(),
        "image": f"{fake.uri()}.png",
        "intro": fake.sentence(),
        "links": [
            {
                "image": f"{fake.uri()}.jpg",
                "intro": fake.text(),
                "title": fake.sentence(),
                "url": fake.uri(),
            }
        ],
        "tags": [],
        "title": fake.sentence(),
        "video": f"{fake.uri_path(deep=4)}.mpg",
    }
    return {**default_body, **kwargs}
