from flask import current_app
from app import db
from datetime import timedelta, date

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    due_date = db.Column(db.DateTime, default=date.today() + timedelta(days=7))