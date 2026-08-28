from database.connection import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    characters = db.relationship(
        'Character',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True
    )