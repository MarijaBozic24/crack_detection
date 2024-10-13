from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()
class CrackCoordinates(db.Model):
    __tablename__ = 'crackcoordinates'
    id = db.Column(db.Integer, primary_key=True)
    x_start = db.Column(db.Integer, nullable=False)
    y_start = db.Column(db.Integer, nullable=False)
    x_end = db.Column(db.Integer, nullable=False)
    y_end = db.Column(db.Integer, nullable=False)

 
    crack_details = db.relationship('CrackDetails', backref='crackcoordinates', lazy=True)

class CrackDetails(db.Model):
    __tablename__ = 'crackdetails'
    id = db.Column(db.Integer, primary_key=True)
    crack_name = db.Column(db.String(80), nullable=False)
    crack_length = db.Column(db.Float, nullable=False)
    coordinates_id = db.Column(db.Integer, db.ForeignKey('crackcoordinates.id'), nullable=True)
    image_id = db.Column(db.String(36), nullable=False) 
    processing_date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False) 
    crack_label = db.Column(db.String(255), nullable=True) 

