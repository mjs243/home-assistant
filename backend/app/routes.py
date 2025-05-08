from flask import Blueprint, request, jsonify
from app.ha_client import call_service, get_states, get_entity_state
from app.utils import get_domain

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/devices", methods=["GET"])
def list_devices():
    """List all devices in Home Assistant"""
    try:
        states = get_states()
        devices = [
            {
                "entity_id": state["entity_id"],
                "state": state["state"],
                "attributes": state.get("attributes", {}),
            }
            for state in states
        ]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route("/device/<entity_id>/on", methods=["POST"])
def device_on(entity_id):
    """Turn on a device"""
    domain = get_domain(entity_id)
    return jsonify(call_service(domain, "turn_on", {"entity_id": entity_id}))

@api_blueprint.route("/device/<entity_id>/off", methods=["POST"])
def device_off(entity_id):
    """Turn off a device"""
    domain = get_domain(entity_id)
    return jsonify(call_service(domain, "turn_off", {"entity_id": entity_id}))

@api_blueprint.route("/device/<entity_id>/command", methods=["POST"])
def device_custom_command(entity_id):
    """Send a custom command to a device"""
    domain = get_domain(entity_id)
    payload = request.json or {}
    service = payload.get("service")
    data = payload.get("data", {})
    data["entity_id"] = entity_id
    try:
        response = call_service(domain, service, data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500