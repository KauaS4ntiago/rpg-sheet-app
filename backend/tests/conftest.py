import pytest
from flask_bcrypt import Bcrypt
from app import create_app
from database.connection import db
from models.user import User


@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)

    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_adm(app):
    bcrypt = Bcrypt()

    user = User(
        name="Admin Test",
        email="admin@test.com",
        password=bcrypt.generate_password_hash("12345678").decode("utf-8")
    )

    db.session.add(user)
    db.session.commit()

    yield {
        "user": user,
        "password": "12345678"
    }

    db.session.delete(user)
    db.session.commit()