# app/controllers/audit_controller.py
from flask import Blueprint, jsonify
from app.services.audit_service import get_all_audits, get_audit_status
import logging

audit_bp = Blueprint('audit_bp', __name__)
logger = logging.getLogger(__name__)

@audit_bp.route('/get_audit_data', methods=['GET'])
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

@audit_bp.route('/audit-status', methods=['GET'])
def audit_status():
    try:
        response = get_audit_status()
        logger.info("Fetched audit status successfully")
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error fetching audit status: {str(e)}")
        return jsonify({"error": "Error fetching audit status"}), 500