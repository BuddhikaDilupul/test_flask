from flask import Blueprint, request, jsonify
import datetime
from app.services.remediation_service import create_remediation, get_problem_with_remediation
from app.services.problem_service import update_status_by_id
from app.services.audit_service import update_in_progress_problems_in_Audit,get_audit_record_by_id
from app.util.execute_script import execute_script

import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create a Blueprint for the remediation routes
remediation_bp = Blueprint('remediation', __name__)

@remediation_bp.route('/insert_recommendation', methods=['POST'])
def create_remediation_controller():
    data = request.json
    recommendation_text = data.get('recommendation')
    script_path = data.get('resolutionScript')
    service_name = data.get('serviceName')
    problem_id = data.get('problemId')
    problem_title = data.get('problemTitle')

    if not all([recommendation_text, script_path, problem_id, service_name, problem_title]):
        logger.error("Missing required fields in request data")
        return jsonify({"error": "Missing required fields"}), 400
    if(execute_script(script_path,service_name)):
        result = create_remediation(recommendation_text, script_path, problem_id)
        update_status_by_id(problem_id)
        update_in_progress_problems_in_Audit(service_name, problem_id, problem_title)
        return "Remediation Saved Successfully", 201
    else:
        return "Cannot run script", 400
    
    
@remediation_bp.route('/problem_recommendations/<int:problem_id>/<string:pid>', methods=['GET'])
def get_problem_with_remediation_route(problem_id,pid):
    try:
        problem_with_remediation = get_problem_with_remediation(problem_id)
        if not problem_with_remediation:
            return jsonify({"error": "Problem not found"}), 404
        audit=get_audit_record_by_id(pid)
        problem, remediation = problem_with_remediation
        result = [
            {
                "problemId": problem.id,
                "problemTitle": problem.problemTitle,
                "subProblemTitle": problem.subProblemTitle,
                "serviceName": problem.serviceName,
                "status": problem.status,
                "remediationId": remediation.id if remediation else None,
                "recommendationText": remediation.recommendationText if remediation else None,
                "scriptPath": remediation.scriptPath if remediation else None,
                "createdAt": remediation.createdAt if remediation else None,
                "lastUpdateAt": remediation.lastUpdateAt if remediation else None,
                "scriptExecutionStartAt": audit.scriptExecutionStartAt if audit else None,
                "actionType": audit.actionType if audit else None,
                "problemEndAt" :audit.problemEndAt if audit else None
            }
        ]

        logger.info(f"Fetched problem with remediation for problemId {problem_id} successfully")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error fetching problem with remediation for problemId {problem_id}: {str(e)}")
        return jsonify({"error": "Error fetching problem with remediation"}), 500