from flask import Flask
from flask_migrate import Migrate
import os
from datetime import timedelta

from database.connection import init_db, db
from register import register_routes

from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(testing=False):
    
    app = Flask(__name__)
    
    init_db(app, testing)
    
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

    CORS(app)

    jwt_secret = os.getenv("JWT_SECRET_KEY")

    if not jwt_secret:
        raise RuntimeError("JWT_SECRET_KEY não foi configurada.")

    app.config['JWT_SECRET_KEY'] = jwt_secret
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    register_routes(app)
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

    


