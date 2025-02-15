from bson.objectid import ObjectId
from database import db

# Get the IoT collection
iot_collection = db["iot"]

def format_sensor(sensor):
    """Helper function to format a sensor document."""
    return {
        "id": str(sensor["_id"]),
        "temperature": sensor["temperature"],
        "humidity": sensor["humidity"]
    }

def add_sensor(data):
    """Add new sensor data with validation."""
    if not data or "temperature" not in data or "humidity" not in data:
        return {"error": "Missing temperature or humidity"}, 400
    
    sensor_id = iot_collection.insert_one({
        "temperature": data["temperature"],
        "humidity": data["humidity"]
    }).inserted_id

    return {"message": "Sensor data added", "id": str(sensor_id)}, 201

def get_all_sensors():
    """Retrieve all sensor data."""
    sensors = [format_sensor(sensor) for sensor in iot_collection.find()]
    return sensors, 200

def get_average_sensor():
    """Calculate the average temperature and humidity."""
    sensors = list(iot_collection.find())

    if not sensors:
        return {"error": "No sensor data available"}, 404

    total_temperature = sum(sensor["temperature"] for sensor in sensors)
    total_humidity = sum(sensor["humidity"] for sensor in sensors)
    count = len(sensors)

    return {
        "average_temperature": total_temperature / count,
        "average_humidity": total_humidity / count
    }, 200

def get_sensor_by_id(sensor_id):
    """Retrieve a sensor by its ID."""
    try:
        sensor = iot_collection.find_one({"_id": ObjectId(sensor_id)})
        if not sensor:
            return {"error": "Sensor not found"}, 404
        return format_sensor(sensor), 200
    except Exception:
        return {"error": "Invalid ID format"}, 400

def update_sensor(sensor_id, data):
    """Update sensor data with validation."""
    if not data:
        return {"error": "Invalid request body"}, 400

    try:
        updated_sensor = iot_collection.update_one(
            {"_id": ObjectId(sensor_id)},
            {"$set": {key: data[key] for key in ["temperature", "humidity"] if key in data}}
        )

        if updated_sensor.matched_count == 0:
            return {"error": "Sensor not found"}, 404
        return {"message": "Sensor updated successfully"}, 200
    except Exception:
        return {"error": "Invalid ID format"}, 400

def delete_sensor(sensor_id):
    """Delete a sensor by its ID."""
    try:
        deleted_sensor = iot_collection.delete_one({"_id": ObjectId(sensor_id)})
        if deleted_sensor.deleted_count == 0:
            return {"error": "Sensor not found"}, 404
        return {"message": "Sensor deleted successfully"}, 200
    except Exception:
        return {"error": "Invalid ID format"}, 400
