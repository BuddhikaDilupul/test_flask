from app import db
from app.models.remediation_model import Remediation
from app.models.problem_model import Problem
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.models.problem_model import Problem

logger = logging.getLogger(__name__)


def get_problem_with_remediation_by_id(remediation_id):
    try:
        # Query to retrieve problem details along with the remediation
        problem_with_remediation = db.session.query(Problem, Remediation).\
            join(Remediation, Problem.id == Remediation.probId).\
            filter(Remediation.id == remediation_id).\
            first() 

        if problem_with_remediation:
            return problem_with_remediation
        else:
            return "Not found for this Id", 404  # Return None if remediation with given id not found

    except SQLAlchemyError as e:
        logger.error(f"Error fetching problem with remediation: {str(e)}")
        return {"error": str(e)}
