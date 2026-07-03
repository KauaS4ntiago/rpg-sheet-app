from database.connection import db

class Ability(db.Model):
    __tablename__ = 'ability'

    id = db.Column(db.Integer, primary_key=True)

    character_id = db.Column(
        db.Integer,
        db.ForeignKey('characters.id', ondelete='CASCADE'),
        nullable=False
    )

    character = db.relationship(
        'Character',
        back_populates='abilities'
    )

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    image = db.Column(db.String(255))