from flask import Flask
from routes.sensor_routes import sensor_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(sensor_bp)

if __name__ == "__main__":
    app.run(debug=True)
