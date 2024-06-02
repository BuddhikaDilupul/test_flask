from app import db

class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problemTitle = db.Column(db.String(255), nullable=False)
    subProblemTitle = db.Column(db.String(255), default="No_Sub_Problem_Detected")
    impactedEntity = db.Column(db.String(255))
    problemImpact = db.Column(db.String(255))
    problemSeverity = db.Column(db.String(255))
    problemURL = db.Column(db.String(255))
    serviceName = db.Column(db.String(255), nullable=False)
    actionType = db.Column(db.String(255))
    status = db.Column(db.String(255), nullable=False)
    pid = db.Column(db.String(255))
    executedProblemId = db.Column(db.String(255))
    displayId = db.Column(db.String(255))
    comments = db.Column(db.String(255))
    problemDetectedAt = db.Column(db.DateTime, nullable=True)
    problemEndAt = db.Column(db.DateTime, nullable=True)
