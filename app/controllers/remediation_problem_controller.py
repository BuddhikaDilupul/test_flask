from flask import Blueprint, request, jsonify
import datetime
from app.services.remediation_service import create_remediation, get_problem_with_remediation, remediation_update
from app.services.problem_service import update_status_by_id, problem_update
from app.services.remediation_problem_service import get_problem_with_remediation_by_id
from app.services.audit_service import update_in_progress_problems,get_audit_record_by_id
from app.util.execute_script import execute_script

import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create a Blueprint for the remediation routes
remediation_problem_bp = Blueprint('remediation_problem_bp', __name__)
  
    
@remediation_problem_bp.route('/edit_remediation/<int:problem_id>/<string:remediation_id>', methods=['POST'])
def update_problem_with_remediation_route(problem_id,remediation_id):
    data = request.json
    
    try:
        scriptPath = data["resolutionScript"]
        subProblemTitle =  data["subProblemTitle"]
        recommendationText = data["recommendation"]
        problemTitle = data["problemTitle"]
        subProblemTitle = data["subProblemTitle"]
        serviceName = data["serviceName"]
    
        remediation_update(remediation_id,scriptPath, recommendationText)
        problem_update(problemTitle, subProblemTitle, serviceName, problem_id)
        logger.info(f"Fetched problem with remediation for problemId {problem_id} successfully")
        return jsonify("Updated successfully"), 200
    except Exception as e:
        logger.error(f"Error fetching problem with remediation for problemId {problem_id}: {str(e)}")
        return jsonify({"error": "Error fetching problem with remediation"}), 500
    
    
@remediation_problem_bp.route('/get_remediation/<int:remediation_id>', methods=['GET'])
def get_problem_with_remediation_route(remediation_id):
    try:
        problem, remediation = get_problem_with_remediation_by_id(remediation_id)
        if problem is None:
            return jsonify({"error": "Problem not found"}), 404
        if remediation is None:
            return jsonify({"error": "Remediation not found"}), 404

        result = {
            "problemId": problem.id,
            "problemTitle": problem.problemTitle,
            "subProblemTitle": problem.subProblemTitle,
            "serviceName": problem.serviceName,
            "status": problem.status,
            "remediationId": remediation.id,
            "recommendationText": remediation.recommendationText,
            "scriptPath": remediation.scriptPath,
            "createdAt": remediation.createdAt,
            "lastUpdateAt": remediation.lastUpdateAt,
        }
        logger.info(f"Fetched remediation for remediation_id {remediation_id} successfully")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error fetching problem with remediation for problemId {remediation_id}: {str(e)}")
        return jsonify({"error": "Error fetching problem with remediation"}), 500
    
    