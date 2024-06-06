from app import db
from app.models.remediation_model import Remediation
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.models.problem_model import Problem

logger = logging.getLogger(__name__)

def create_remediation(recommendation_text, script_path, problem_id):
    try:
        new_remediation = Remediation(
            recommendationText=recommendation_text,
            scriptPath=script_path,
            probId=problem_id
        )
        db.session.add(new_remediation)
        db.session.commit()
        logger.info("Remediation created successfully")
        return new_remediation
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error creating remediation: {str(e)}")
        return {"error": str(e)}

#getExecuted script data
def get_problem_with_remediation(problem_id):
    try:
        problem_with_remediation = db.session.query(Problem, Remediation).join(Remediation, Problem.id == Remediation.probId).filter(Problem.id == problem_id).first()
        return problem_with_remediation
    except SQLAlchemyError as e:
        logger.error(f"Error fetching problem with remediation for problemId {problem_id}: {str(e)}")
        return {"error": str(e)}
    

def get_script_path_by_prob_id(prob_id):
    try:
        remediation = Remediation.query.filter_by(probId=prob_id).first()
        if remediation:
            return remediation.scriptPath
        else:
            return None
    except SQLAlchemyError as e:
        logger.error(f"Error fetching script path by problem ID: {str(e)}")
        return {"error": str(e)}


def remediation_update(remediationId,scriptPath, recommendationText):
    problem = Remediation.query.filter_by(id=remediationId).first()
    if problem:
        problem.scriptPath = scriptPath
        problem.recommendationText =recommendationText
        db.session.commit()
        logger.info(f"Updated Remediation for Problem {remediationId} successfully")
        return "Problem Remediation successfully"
    else:
        return "Remediation not found"

def delete_remediation(remediation_id):
    try:
        # Fetch the remediation record by its ID
        remediation = Remediation.query.get(remediation_id)
        
        # If the record does not exist, raise an exception
        if remediation is None:
            raise ValueError(f"Remediation with ID {remediation_id} does not exist.")

        # Delete the record from the database
        db.session.delete(remediation)
        db.session.commit()
        
        return {"status": "success", "message": f"Remediation with ID {remediation_id} deleted successfully."}
    
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        
        return {"status": "error", "message": str(e)}

#not used

def get_remediation_by_id(remediation_id):
    try:
        remediation = Remediation.query.get(remediation_id)
        return remediation
    except SQLAlchemyError as e:
        logger.error(f"Error fetching remediation by ID: {str(e)}")
        return {"error": str(e)}

def get_all_remediations():
    try:
        remediations = Remediation.query.all()
        return remediations
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all remediations: {str(e)}")
        return {"error": str(e)}
