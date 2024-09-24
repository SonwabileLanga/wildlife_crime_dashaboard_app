function initMap() {
    const map = L.map('map').setView([-30.5595, 22.9375], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    $.getJSON('/api/data', function(data) {
        const alertsDiv = $('#alerts');
        alertsDiv.append('<h3>Recent Alerts</h3>');

        // Display alerts
        data.alerts.forEach(function(alert) {
            alertsDiv.append(`<p>${alert}</p>`);
        });

        // Create markers for each location with incidents
        data.locations.forEach(location => {
            const marker = L.marker([location.latitude, location.longitude]).addTo(map);
            const weatherInfo = `Weather: ${location.weather}, Temp: ${location.temperature}°C`;
            marker.bindPopup(`${location.province}: ${location.incidents} incidents<br>${weatherInfo}`).openPopup();
        });

        // Plotting crime trends as a bar chart
        const xValues = data.trends.map(trend => trend.date);
        const yValues = data.trends.map(trend => trend.count);

        const trace = {
            x: xValues,
            y: yValues,
            type: 'bar',
            marker: {
                color: 'rgba(0, 128, 0, 0.6)',
                line: {
                    color: 'rgba(0, 128, 0, 1)',
                    width: 2
                }
            }
        };

        const layout = {
            title: 'Wildlife Crime Trends Over Time',
            xaxis: {
                title: 'Date'
            },
            yaxis: {
                title: 'Number of Incidents'
            }
        };

        Plotly.newPlot('crime-trends', [trace], layout);
    });
}

$(document).ready(function() {
    initMap();
});
