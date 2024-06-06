from app.models.problem_model import Problem
from app.models.remediation_model import Remediation
from app import db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def create_problem_auto(problem_title, sub_problem_title, service_name, status):
    try:
        new_problem = Problem(
            problemTitle=problem_title,
            subProblemTitle=sub_problem_title,
            serviceName=service_name,
            status=status
        )
        db.session.add(new_problem)
        db.session.commit()
        logger.info("Problem created successfully")
        return new_problem
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error creating problem: {str(e)}")
        return {"error": str(e)}

def get_all_problems():
    try:
        problems = Problem.query.all()
        return problems
    except SQLAlchemyError as e:
        logger.error(f"Error fetching problems: {str(e)}")
        return {"error": str(e)}

#get all remediations
def get_all_problems_with_remediations():
    try:
        problems_with_remediations = db.session.query(Problem, Remediation).join(Remediation, Problem.id == Remediation.probId).all()
        return problems_with_remediations
    except SQLAlchemyError as e:
        logger.error(f"Error fetching problems with remediations: {str(e)}")
        return {"error": str(e)}
    
def update_status_by_id(id):
    try:
        problem = Problem.query.get(id)
        if problem:
            problem.status = "RESOLVED"
            db.session.commit()
            logger.info(f"Problem with ID {id} updated successfully")
            return {"message": f"Problem with ID {id} updated successfully"}
        else:
            return {"error": f"Problem with ID {id} not found"}, 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error updating problem status: {str(e)}")
        return {"error": str(e)}

def find_problem_id(problem_title, service_name):
    try:
        problem = Problem.query.filter_by(problemTitle=problem_title, serviceName=service_name).first()
        if problem:
            return problem.id
        else:
            return None
    except SQLAlchemyError as e:
        logger.error(f"Error finding problem ID: {str(e)}")
        return {"error": str(e)}


def get_not_resolved_problems():
    try:
        not_resolved_problems = Problem.query.filter_by(status='not_resolved').all()
        return not_resolved_problems
    except Exception as e:
        # You can add logging here if needed
        return {"error": str(e)}


def problem_update(problemTitle, subProblemTitle, serviceName, problemId):
    problem = Problem.query.filter_by(id = problemId).first()
    if problem:
        problem.serviceName = serviceName
        problem.problemTitle =problemTitle
        problem.subProblemTitle=subProblemTitle
        db.session.commit()
        logger.info(f"Updated problem for Problem {problemId} successfully")
        return "Problem updated successfully"
    else:
        return "Problem not found"
    
    
def delete_problem(problem_id):
    try:
        # Fetch the problem record by its ID
        problem = Problem.query.get(problem_id)
        
        # If the record does not exist, raise an exception
        if problem is None:
            raise ValueError(f"Problem with ID {problem_id} does not exist.")

        # Delete the record from the database
        db.session.delete(problem)
        db.session.commit()
        
        return {"status": "success", "message": f"Problem with ID {problem_id} deleted successfully."}
    
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        
        return {"status": "error", "message": str(e)}