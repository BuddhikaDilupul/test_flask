import datetime
from app import db

current_time = datetime.datetime.now()

class Remediation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recommendationText = db.Column(db.String(255), nullable=False)
    scriptPath = db.Column(db.String(255), nullable=False)
    probId = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=current_time, nullable=False)
    lastUpdateAt = db.Column(db.DateTime, default=current_time, onupdate=current_time, nullable=False)
