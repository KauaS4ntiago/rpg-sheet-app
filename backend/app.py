from flask import Flask
import os
from datetime import timedelta
from database.connection import init_db, db
from register import register_routes
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)

init_db(app)

CORS(app)

with app.app_context():
    db.create_all()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

register_routes(app)

if __name__ == '__main__':
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=False
)