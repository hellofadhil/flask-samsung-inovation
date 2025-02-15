from flask import Blueprint, request, jsonify
from services.sensor_service import (
    add_sensor, get_all_sensors, get_sensor_by_id,
    update_sensor, delete_sensor
)

sensor_bp = Blueprint("sensor", __name__, url_prefix="/sensors")

@sensor_bp.route("/", methods=["POST"])
def create_sensor():
    """API endpoint to add a new sensor."""
    response, status_code = add_sensor(request.get_json())
    return jsonify(response), status_code

@sensor_bp.route("/", methods=["GET"])
def retrieve_sensors():
    """API endpoint to get all sensors."""
    response, status_code = get_all_sensors()
    return jsonify(response), status_code

@sensor_bp.route("/<sensor_id>", methods=["GET"])
def retrieve_sensor(sensor_id):
    """API endpoint to get a sensor by ID."""
    response, status_code = get_sensor_by_id(sensor_id)
    return jsonify(response), status_code

@sensor_bp.route("/<sensor_id>", methods=["PUT"])
def modify_sensor(sensor_id):
    """API endpoint to update a sensor."""
    response, status_code = update_sensor(sensor_id, request.get_json())
    return jsonify(response), status_code

@sensor_bp.route("/<sensor_id>", methods=["DELETE"])
def remove_sensor(sensor_id):
    """API endpoint to delete a sensor."""
    response, status_code = delete_sensor(sensor_id)
    return jsonify(response), status_code
