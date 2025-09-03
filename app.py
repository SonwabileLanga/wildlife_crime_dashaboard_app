from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import random
import json
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wildlife_crime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# API Configuration
OPENWEATHER_API_KEY = '4df0d76850d8b55311fb5c1fc3a90e2c'
OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Database Models
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    incident_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Active')

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='Medium')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

# Sample data for initial setup
def load_sample_data():
    """Load sample data if database is empty"""
    if Incident.query.count() == 0:
        sample_incidents = [
            Incident(province="Gauteng", latitude=-25.746111, longitude=28.188056, 
                    incident_type="Poaching", description="Rhino poaching incident reported"),
            Incident(province="Mpumalanga", latitude=-25.9705, longitude=31.1308, 
                    incident_type="Illegal Logging", description="Illegal logging detected"),
            Incident(province="KwaZulu-Natal", latitude=-29.0598, longitude=30.3782, 
                    incident_type="Wildlife Trafficking", description="Wildlife trafficking case"),
            Incident(province="Western Cape", latitude=-33.9249, longitude=18.4241, 
                    incident_type="Poaching", description="Elephant poaching incident"),
        ]
        
        for incident in sample_incidents:
            db.session.add(incident)
        
        sample_alerts = [
            Alert(message="Poaching incident reported in Kruger National Park.", severity="High"),
            Alert(message="Illegal logging detected in Mpumalanga province.", severity="Medium"),
            Alert(message="Wildlife trafficking case solved in Gauteng.", severity="Low"),
        ]
        
        for alert in sample_alerts:
            db.session.add(alert)
        
        db.session.commit()
        logger.info("Sample data loaded successfully")

def get_weather_data(latitude, longitude):
    """Fetch weather data from OpenWeatherMap API with error handling."""
    try:
        response = requests.get(OPENWEATHER_API_URL, params={
            'lat': latitude,
            'lon': longitude,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Weather API returned status {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None

def generate_trends_data():
    """Generate trends data for the last 6 months"""
    trends = []
    base_date = datetime.now() - timedelta(days=180)
    
    for i in range(6):
        date = base_date + timedelta(days=i * 30)
        # Generate realistic incident counts
        count = random.randint(5, 25) + (i * 2)  # Slight upward trend
        
        trends.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return trends

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get all dashboard data"""
    try:
        # Get incidents grouped by province
        incidents_by_province = db.session.query(
            Incident.province,
            db.func.avg(Incident.latitude).label('latitude'),
            db.func.avg(Incident.longitude).label('longitude'),
            db.func.count(Incident.id).label('incidents')
        ).group_by(Incident.province).all()
        
        locations = []
        for province_data in incidents_by_province:
            location = {
                "province": province_data.province,
                "latitude": float(province_data.latitude),
                "longitude": float(province_data.longitude),
                "incidents": province_data.incidents
            }
            
            # Get weather data
            weather_data = get_weather_data(location['latitude'], location['longitude'])
            if weather_data:
                location['weather'] = weather_data.get('weather', [{}])[0].get('description', 'No data')
                location['temperature'] = round(weather_data.get('main', {}).get('temp', 0), 1)
            else:
                location['weather'] = 'No data'
                location['temperature'] = 'N/A'
            
            locations.append(location)
        
        # Get active alerts
        alerts = [alert.message for alert in Alert.query.filter_by(is_active=True).all()]
        
        # Generate trends data
        trends = generate_trends_data()
        
        return jsonify({
            "alerts": alerts,
            "locations": locations,
            "trends": trends
        })
        
    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/incidents', methods=['GET', 'POST'])
def incidents():
    """API endpoint for incidents"""
    if request.method == 'GET':
        try:
            incidents = Incident.query.all()
            return jsonify([{
                'id': incident.id,
                'province': incident.province,
                'latitude': incident.latitude,
                'longitude': incident.longitude,
                'incident_type': incident.incident_type,
                'description': incident.description,
                'date_reported': incident.date_reported.isoformat(),
                'status': incident.status
            } for incident in incidents])
        except Exception as e:
            logger.error(f"Error fetching incidents: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            incident = Incident(
                province=data['province'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                incident_type=data['incident_type'],
                description=data['description']
            )
            db.session.add(incident)
            db.session.commit()
            return jsonify({"message": "Incident added successfully"}), 201
        except Exception as e:
            logger.error(f"Error adding incident: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.route('/api/alerts', methods=['GET', 'POST'])
def alerts():
    """API endpoint for alerts"""
    if request.method == 'GET':
        try:
            alerts = Alert.query.filter_by(is_active=True).all()
            return jsonify([{
                'id': alert.id,
                'message': alert.message,
                'severity': alert.severity,
                'date_created': alert.date_created.isoformat()
            } for alert in alerts])
        except Exception as e:
            logger.error(f"Error fetching alerts: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            alert = Alert(
                message=data['message'],
                severity=data.get('severity', 'Medium')
            )
            db.session.add(alert)
            db.session.commit()
            return jsonify({"message": "Alert added successfully"}), 201
        except Exception as e:
            logger.error(f"Error adding alert: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
