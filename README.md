# Wildlife Crime Monitoring Dashboard

A comprehensive Flask-based web application for monitoring wildlife crime incidents across South Africa with real-time data visualization and weather integration.

## 🌟 Features

- **Interactive Map**: Leaflet-based map showing incident locations with detailed popups
- **Real-time Weather Data**: OpenWeatherMap API integration for location-specific weather
- **Crime Trend Visualization**: Plotly charts showing incident trends over time
- **Alert System**: Real-time alerts for recent wildlife crime incidents
- **Responsive Design**: Modern, mobile-friendly interface
- **Database Integration**: SQLite database for persistent data storage
- **RESTful API**: Complete API endpoints for data management

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd wildlife_crime_dashaboard_app
```

2. **Create and activate virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000` to view the dashboard

## 📊 Dashboard Components

### Recent Alerts Section
- Displays active wildlife crime alerts
- Color-coded by severity level
- Auto-refreshes every 5 minutes

### Interactive Map
- Shows incident locations across South African provinces
- Click markers for detailed information including:
  - Province name
  - Number of incidents
  - Current weather conditions
  - Temperature data

### Crime Trends Chart
- Bar chart showing incident trends over the last 6 months
- Interactive hover tooltips
- Responsive design for all screen sizes

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/api/data` | GET | Get all dashboard data (alerts, locations, trends) |
| `/api/incidents` | GET | Get all incidents |
| `/api/incidents` | POST | Add new incident |
| `/api/alerts` | GET | Get all active alerts |
| `/api/alerts` | POST | Add new alert |

### Example API Usage

**Get all data:**
```bash
curl http://localhost:5000/api/data
```

**Add new incident:**
```bash
curl -X POST http://localhost:5000/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "province": "Limpopo",
    "latitude": -23.8962,
    "longitude": 29.4593,
    "incident_type": "Poaching",
    "description": "Rhino poaching incident reported"
  }'
```

## 🗄️ Database Schema

### Incidents Table
- `id`: Primary key
- `province`: Province name
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate
- `incident_type`: Type of incident (Poaching, Illegal Logging, etc.)
- `description`: Detailed description
- `date_reported`: When the incident was reported
- `status`: Current status (Active, Resolved, etc.)

### Alerts Table
- `id`: Primary key
- `message`: Alert message
- `severity`: Severity level (High, Medium, Low)
- `date_created`: When the alert was created
- `is_active`: Whether the alert is currently active

## 🎨 Customization

### Adding New Incident Types
Edit the `load_sample_data()` function in `app.py` to include new incident types.

### Modifying Weather Integration
Update the `OPENWEATHER_API_KEY` in `app.py` with your own API key from [OpenWeatherMap](https://openweathermap.org/api).

### Styling Changes
Modify `static/css/styles.css` to customize the appearance of the dashboard.

## 🔒 Security Notes

- Change the `SECRET_KEY` in `app.py` for production use
- Consider using environment variables for API keys
- Implement proper authentication for production deployment

## 🐛 Troubleshooting

### Common Issues

1. **Weather data not loading**: Check your internet connection and API key
2. **Map not displaying**: Ensure Leaflet CSS is loaded properly
3. **Database errors**: Delete `wildlife_crime.db` to reset the database

### Logs
The application logs important events to the console. Check for error messages if something isn't working.

## 📱 Mobile Support

The dashboard is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 📞 Contact

For any inquiries or feedback, feel free to reach out to me at langasonwabile1993@gmail.com.

## 🙏 Acknowledgments

- OpenStreetMap for the mapping service
- Plotly.js for data visualization
- OpenWeatherMap for weather data
- Leaflet.js for interactive maps