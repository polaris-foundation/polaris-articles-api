from flask_batteries_included.sqldb import db


def reset_database() -> None:
    session = db.session
    session.execute("TRUNCATE TABLE article_tag CASCADE")
    session.execute("TRUNCATE TABLE tag CASCADE")
    session.execute("TRUNCATE TABLE article CASCADE")
    session.commit()
    session.close()
