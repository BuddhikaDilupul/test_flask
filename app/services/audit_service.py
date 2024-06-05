import datetime
import logging
from app.models.audit_model import Audit
from app import db
from sqlalchemy.exc import SQLAlchemyError
from pytz import timezone

# Logger setup
logger = logging.getLogger(__name__)

def create_audit(problemTitle, subProblemTitle, impactedEntity, problemImpact, problemSeverity, problemURL, problemDetectedAt, serviceName, pid, executedProblemId, displayId, actionType, status, comments, problemEndAt,scriptExecutionStartAt):
    try:
        new_audit = Audit(
            problemTitle=problemTitle,
            subProblemTitle=subProblemTitle,
            impactedEntity=impactedEntity,
            problemImpact=problemImpact,
            problemSeverity=problemSeverity,
            problemURL=problemURL,
            serviceName=serviceName,
            actionType=actionType,
            status=status,
            pid=pid,
            executedProblemId=executedProblemId,
            displayId=displayId,
            comments=comments,
            problemDetectedAt=problemDetectedAt,
            problemEndAt=problemEndAt,
            scriptExecutionStartAt=scriptExecutionStartAt
        )
        db.session.add(new_audit)
        db.session.commit()
        logger.info("Created audit successfully")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error creating audit: {str(e)}")
        return False

def get_all_audits():
    try:
        audits = Audit.query.all()
        return audits
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all audits: {str(e)}")
        return {"error": str(e)}

def update_audit_status_closed(pid, new_status,scriptExecutionStartAt):
    try:
        ist_timezone = timezone('Asia/Kolkata')
        audit = Audit.query.filter_by(pid=pid).first()
        if audit:
            audit.status = new_status
            audit.problemEndAt=datetime.datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S'),
            audit.scriptExecutionStartAt=scriptExecutionStartAt
            db.session.commit()
            logger.info(f"Updated audit status for PID {pid} successfully")
            return {"message": f"Audit with PID {pid} updated successfully"}
        else:
            return {"error": f"Audit with PID {pid} not found"}, 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error updating audit status: {str(e)}")
        return {"error": str(e)}

def update_audit_status_to_failed(pid):
    try:
        audit = Audit.query.filter_by(pid=pid).first()
        if audit:
            audit.status = "FAILED"
            audit.problemEndAt = None
            db.session.commit()
            logger.info(f"Updated audit status for PID {pid} successfully")
            return {"message": f"Audit with PID {pid} updated successfully"}
        else:
            return {"error": f"Audit with PID {pid} not found"}, 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error updating audit status: {str(e)}")
        return {"error": str(e)}

def get_audit_status():
    try:
        open_count = Audit.query.filter_by(status="OPEN").count()
        in_progress_count = Audit.query.filter_by(status="IN_PROGRESS").count()

        latest_audits = Audit.query.order_by(Audit.problemDetectedAt.desc()).limit(5).all()

        audit_list = [
            {
                "id": audit.id,
                "problemTitle": audit.problemTitle,
                "subProblemTitle": audit.subProblemTitle,
                "impactedEntity": audit.impactedEntity,
                "problemImpact": audit.problemImpact,
                "problemSeverity": audit.problemSeverity,
                "problemURL": audit.problemURL,
                "serviceName": audit.serviceName,
                "actionType": audit.actionType,
                "status": audit.status,
                "pid": audit.pid,
                "executedProblemId": audit.executedProblemId,
                "displayId": audit.displayId,
                "comments": audit.comments,
                "problemDetectedAt": audit.problemDetectedAt,
                "problemEndAt": audit.problemEndAt
            } for audit in latest_audits
        ]

        response = {
            "count": open_count + in_progress_count,
            "activity": audit_list
        }

        return response
    except Exception as e:
        raise e
    
    
def update_in_progress_problems(serviceName, probId):
  """
  Updates all "in_progress" records with the specified serviceName to have their executedProblemId set to probId.

  Args:
      serviceName: The name of the service to update.
      probId: The new executedProblemId value.
  """
  try:
    # Update the records using SQLAlchemy
    db.session.query(Audit).filter(
        Audit.serviceName == serviceName, Audit.status == "IN_PROGRESS"
    ).update({Audit.executedProblemId: probId})

    # Commit the changes to the database
    db.session.commit()
    print(f"Successfully updated executedProblemId for 'in_progress' records with serviceName: {serviceName}")

  except Exception as e:
    # Rollback the changes in case of errors
    db.session.rollback()
    print(f"An error occurred: {e}")

