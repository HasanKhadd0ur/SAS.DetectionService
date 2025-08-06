from flask import Blueprint, request, jsonify
from app.core.services.policy_service import policy_service

policy_bp = Blueprint('policy', __name__)

@policy_bp.route("/", methods=["GET"])
def get_rules():
    return jsonify(policy_service.get_all_rules())

@policy_bp.route("/<string:name>", methods=["GET"])
def get_rule(name):
    try:
        rule = policy_service.get_rule(name)
        return jsonify(rule)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@policy_bp.route("/", methods=["POST"])
def update_rule():
    data = request.json
    name = data.get("name")
    value = data.get("value")

    try:
        updated = policy_service.update_rule(name, value)
        return jsonify({"updated": updated})
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    
@policy_bp.route("/toggle", methods=["POST"])
def toggle_rule():
    data = request.json
    name = data.get("name")
    enabled = data.get("enabled")

    try:
        updated = policy_service.toggle_rule(name, enabled)
        return jsonify({"updated": updated})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
