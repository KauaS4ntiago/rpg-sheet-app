from database.connection import db

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)

    character_id = db.Column(
        db.Integer,
        db.ForeignKey('characters.id', ondelete='CASCADE'),
        nullable=False
    )

    character = db.relationship(
        'Character',
        back_populates='skills'
    )

    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint('value BETWEEN -20 AND 20'),
    )
