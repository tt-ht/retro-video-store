from flask import current_app
from sqlalchemy.orm import backref
from app import db
from marshmallow import Schema, fields

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    renters = db.relationship("Customer", secondary="rental", backref="video")
    rentals = db.relationship("Rental", backref="video")

    def to_dict(self):
        video_dict = {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
        return video_dict

class PutVideoInputSchema(Schema):
    
    # the 'required' argument ensures the field exists
    title = fields.Str(required=True)
    total_inventory = fields.Int(required=True)
    release_date = fields.DateTime(required=True, format='%m-%d-%Y')

