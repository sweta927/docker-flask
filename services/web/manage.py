from flask.cli import FlaskGroup
from project.app import app
from project import db
from project.models.user import User

cli = FlaskGroup(app)



@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("update_db")
def update_db():
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="lx.raval01@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
