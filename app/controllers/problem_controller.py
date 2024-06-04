# app/controllers/problem_controller.py
from flask import Blueprint, jsonify, request
from app.services.problem_service import create_problem_auto, get_all_problems, get_all_problems_with_remediations, update_status_by_id, find_problem_id, get_not_resolved_problems
from app.services.remediation_service import create_remediation
import logging

problem_bp = Blueprint('problem_bp', __name__)

# Set up logging
logger = logging.getLogger(__name__)

#get all problems
@problem_bp.route('/problems', methods=['GET'])
def get_problems():
    try:
        problems = get_all_problems()
        problems_list = [
            {
                "id": problem.id,
                "problemTitle": problem.problemTitle,
                "subProblemTitle": problem.subProblemTitle,
                "serviceName": problem.serviceName,
                "status": problem.status
            } for problem in problems
        ]
        logger.info("Fetched all problems successfully")
        return jsonify(problems_list), 200
    except Exception as e:
        logger.error(f"Error fetching problems: {str(e)}")
        return jsonify({"error": "Error fetching problems"}), 500


#display all available remediations
@problem_bp.route('/problems_with_remediations', methods=['GET'])
def get_problems_with_remediations():
    try:
        problems_with_remediations = get_all_problems_with_remediations()
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
                    "lastUpdateAt": remediation.lastUpdateAt if remediation else None
            } for problem, remediation in problems_with_remediations
        ]
        logger.info("Fetched all problems with remediations successfully")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error fetching problems with remediations: {str(e)}")
        return jsonify({"error": "Error fetching problems with remediations"}), 500

#brand new rule 
@problem_bp.route('/save_problem', methods=['POST'])
def create_problem():
    data = request.json
    try:
        problem_title = data['problemTitle']
        sub_problem_title = data['subProblemTitle']
        service_name = data['serviceName']
        recommendation_text = data['recommendation']
        script_path = data['resolutionScript']
        status = data['status']

        new_problem = create_problem_auto(problem_title, sub_problem_title, service_name, status)
        logger.info(f"Created problem with ID {new_problem.id} successfully")
        print(new_problem.id)
        new_remediation = create_remediation(recommendation_text, script_path, new_problem.id)
        logger.info(f"Created Recommendation with ID {new_remediation.id} successfully")
        return "New Rule Created Successfully", 201
    except Exception as e:
        logger.error(f"Error creating problem: {str(e)}")
        return jsonify({"error": "Error creating problem"}), 500

#problems wich has not resolution scripts
@problem_bp.route('/get_new_problems', methods=['GET'])
def get_not_resolved_problems_controller():
    try:
        problems = get_not_resolved_problems()
        problems_list = [
            {
                "id": problem.id,
                "problemTitle": problem.problemTitle,
                "subProblemTitle": problem.subProblemTitle,
                "serviceName": problem.serviceName,
                "status": problem.status
            } for problem in problems
        ]
        logger.info("Fetched all not resolved problems successfully")
        return jsonify(problems_list), 200
    except Exception as e:
        logger.error(f"Error fetching not resolved problems: {str(e)}")
        return jsonify({"error": "Error fetching not resolved problems"}), 500