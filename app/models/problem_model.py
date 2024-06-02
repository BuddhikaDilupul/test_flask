from app import db

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problemTitle = db.Column(db.String(255), nullable=False)
    subProblemTitle = db.Column(db.String(255), default="No_Sub_Problem_Detected")
    serviceName = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
