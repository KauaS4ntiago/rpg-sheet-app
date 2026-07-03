from database.connection import db

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    user = db.relationship(
        'User',
        back_populates='characters'
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )
    
    current_hp = db.Column(
        db.SmallInteger,
        nullable=False
    )
    
    max_hp = db.Column(
        db.SmallInteger,
        nullable=False
    )
    
    current_sanity = db.Column(
        db.SmallInteger,
        nullable=False
    )
    
    max_sanity = db.Column(
        db.SmallInteger,
        nullable=False
    )    
    
    defense = db.Column(
        db.SmallInteger,
        nullable=False
    )

    image = db.Column(
        db.String(255)
    )

    notes = db.Column(
        db.Text
    )
    
    abilities = db.relationship(
        'Ability',
        back_populates='character',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    skills = db.relationship(
        'Skill',
        back_populates='character',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    attributes = db.relationship(
        'Attribute',
        back_populates='character',
        cascade='all, delete-orphan',
        passive_deletes=True
    )