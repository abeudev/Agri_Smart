from openagriculture import db


class Field(db.Model):

    id   = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    crop = db.Column(db.String(length=15), nullable=False, unique=False)
    area = db.Column(db.Float(), nullable=False, unique=False)
    geometry = db.Column(db.String(), nullable=False, unique=False)
    
