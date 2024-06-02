# app/controllers/audit_controller.py
from flask import Blueprint, jsonify
from app.services.audit_service import get_all_audits
import logging

audit_bp = Blueprint('audit_bp', __name__)
logger = logging.getLogger(__name__)

@audit_bp.route('/audits', methods=['GET'])
def get_audits():
    try:
        audits = get_all_audits()
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
            } for audit in audits
        ]
        logger.info("Fetched all audits successfully")
        return jsonify(audit_list), 200
    except Exception as e:
        logger.error(f"Error fetching audits: {str(e)}")
        return jsonify({"error": "Error fetching audits"}), 500
