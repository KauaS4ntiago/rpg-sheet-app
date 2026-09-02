from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def init_db(app,testing=False):
        required_vars =  [
            "DB_USER", 
            "DB_PASSWORD",
            "DB_HOST",
            "DB_NAME"
        ]

        for var in required_vars:
            if not os.getenv(var):
                raise RuntimeError(f"{var} não foi configurada.")
            
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")

        
        if testing==False:
            name = os.getenv("DB_NAME")
        else:
            name = "ficharpg_test"
        
        app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+pymysql://{user}:{password}@{host}/{name}")
        
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        db.init_app(app)
    