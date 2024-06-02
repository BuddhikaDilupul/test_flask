# app/controllers/webhook_controller.py
from flask import Blueprint, jsonify, request
import logging
from app.services.problem_service import create_problem_auto, find_problem_id
from app.services.remediation_service import get_script_path_by_prob_id
from app.services.audit_service import create_audit, update_audit_status
from app.util.execute_script import execute_script

# Create a logger
logger = logging.getLogger(__name__)

webhook_bp = Blueprint('webhook_bp', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    data = request.json
    
    # Extract relevant data from the payload
    pid = data.get("PID")
    displayId = data.get("ProblemID")
    problemTitle = data.get("ProblemTitle")
    subProblemTitle = data.get("SubProblemTitle", "No_Sub_Problem_Detected")
    impactedEntity = data.get("ImpactedEntity", "Unknown")
    problemImpact = data.get("ProblemImpact", "Unknown")
    problemSeverity = data.get("ProblemSeverity", "Unknown")
    problemURL = data.get("ProblemURL", "No_URL")
    problemDetectedAt = data.get("ProblemDetectedAt")
    serviceName = data.get("ServiceName")
    state = data.get("State", "unknown")
    executedProblemId = data.get("ExecutedProblemId", None)

    if state == "OPEN":
        if "ServiceName" in data and "ProblemID" in data:
            logger.info("Received webhook notification. Service to restart: %s", serviceName)

            prob_id = find_problem_id(problemTitle, serviceName)
            if prob_id:
                script_path =  get_script_path_by_prob_id(prob_id)
                if script_path:
                    # Run the script
                    if execute_script(script_path, serviceName):
                        # Add execution data to the audit table
                        if create_audit(problemTitle, subProblemTitle, impactedEntity, problemImpact, problemSeverity, problemURL, problemDetectedAt, serviceName, pid, executedProblemId, displayId, actionType="auto", status="in_progress", comments="Successfully Executed", problemEndAt=None):
                            return 'Script execution success', 200
                        else:
                            update_audit_status(pid, "in_progress")
                            return 'Script execution success', 200
                    else:
                        return 'Script execution unsuccessful!', 400
                else:
                    logger.warning("No script found in DB")
                    return 'No script specified in DB', 400
            else:
                # New problem detected and saving
                result = create_problem_auto(problemTitle, subProblemTitle, serviceName, "not_resolved")
                create_audit(problemTitle, subProblemTitle, impactedEntity, problemImpact, problemSeverity, problemURL, problemDetectedAt, serviceName, pid, executedProblemId, displayId, actionType="manual", status="in_progress", comments="Waiting for manual instructions", problemEndAt=None)
                return result, 201
        else:
            logger.warning("No service found in webhook message")
            return 'No service specified in webhook payload.', 400

    elif state == "RESOLVED":
        update_audit_status(pid, "resolved")
        logger.info("Dynatrace Resolved notification received. Service up and running")
        return 'Dynatrace Resolved Confirmation', 200

    else:
        logger.info("Dynatrace unknown notification received.")
        update_audit_status(pid, "failed")
        return 'Dynatrace message', 200
