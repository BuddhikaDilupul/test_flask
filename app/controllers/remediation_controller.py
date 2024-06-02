from flask import Blueprint, request, jsonify
from app.services.remediation_service import create_remediation
from app.services.problem_service import update_status_by_id
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create a Blueprint for the remediation routes
remediation_bp = Blueprint('remediation', __name__)

@remediation_bp.route('/remediation_auto_detected', methods=['POST'])
def create_remediation_controller():
    data = request.json
    recommendation_text = data.get('recommendationText')
    script_path = data.get('scriptPath')
    problem_id = data.get('probId')

    if not all([recommendation_text, script_path, problem_id]):
        logger.error("Missing required fields in request data")
        return jsonify({"error": "Missing required fields"}), 400

    result = create_remediation(recommendation_text, script_path, problem_id)
    update_status_by_id(problem_id)
    return jsonify({"id": result.id}), 201
