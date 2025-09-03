// Global variables
let map;
let markers = [];

// Initialize the application
function initApp() {
    showLoading();
    initMap();
    loadData();
}

// Show loading state
function showLoading() {
    $('#alerts').html('<div class="loading">Loading alerts...</div>');
    $('#crime-trends').html('<div class="loading">Loading trends...</div>');
}

// Initialize the map
function initMap() {
    map = L.map('map').setView([-30.5595, 22.9375], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

// Load data from the API
function loadData() {
    $.getJSON('/api/data')
        .done(function(data) {
            displayAlerts(data.alerts);
            displayMapMarkers(data.locations);
            displayTrends(data.trends);
        })
        .fail(function(xhr, status, error) {
            console.error('Error loading data:', error);
            showError('Failed to load data. Please try again later.');
        });
}

// Display alerts
function displayAlerts(alerts) {
    const alertsDiv = $('#alerts');
    alertsDiv.empty();
    
    if (alerts && alerts.length > 0) {
        alerts.forEach(function(alert, index) {
            setTimeout(() => {
                alertsDiv.append(`<div class="alert-item">${alert}</div>`);
            }, index * 200); // Staggered animation
        });
    } else {
        alertsDiv.html('<div class="alert-item">No recent alerts</div>');
    }
}

// Display map markers
function displayMapMarkers(locations) {
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    if (locations && locations.length > 0) {
        locations.forEach(location => {
            const marker = L.marker([location.latitude, location.longitude]).addTo(map);
            
            // Create custom popup content
            const popupContent = `
                <div style="min-width: 200px;">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">${location.province}</h4>
                    <p style="margin: 5px 0;"><strong>Incidents:</strong> ${location.incidents}</p>
                    <p style="margin: 5px 0;"><strong>Weather:</strong> ${location.weather || 'N/A'}</p>
                    <p style="margin: 5px 0;"><strong>Temperature:</strong> ${location.temperature || 'N/A'}°C</p>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            markers.push(marker);
        });
        
        // Fit map to show all markers
        if (markers.length > 1) {
            const group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        }
    }
}

// Display trends chart
function displayTrends(trends) {
    if (!trends || trends.length === 0) {
        $('#crime-trends').html('<div class="alert-item">No trend data available</div>');
        return;
    }
    
    const xValues = trends.map(trend => {
        const date = new Date(trend.date);
        return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    });
    const yValues = trends.map(trend => trend.count);

    const trace = {
        x: xValues,
        y: yValues,
        type: 'bar',
        marker: {
            color: 'rgba(52, 152, 219, 0.8)',
            line: {
                color: 'rgba(52, 152, 219, 1)',
                width: 2
            }
        },
        hovertemplate: '<b>%{x}</b><br>Incidents: %{y}<extra></extra>'
    };

    const layout = {
        title: {
            text: 'Wildlife Crime Trends Over Time',
            font: { size: 16, color: '#2c3e50' }
        },
        xaxis: {
            title: 'Month',
            titlefont: { color: '#2c3e50' },
            tickfont: { color: '#7f8c8d' }
        },
        yaxis: {
            title: 'Number of Incidents',
            titlefont: { color: '#2c3e50' },
            tickfont: { color: '#7f8c8d' }
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif' }
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('crime-trends', [trace], layout, config);
}

// Show error message
function showError(message) {
    $('#alerts').html(`<div class="alert-item">${message}</div>`);
    $('#crime-trends').html(`<div class="alert-item">${message}</div>`);
}

// Refresh data every 5 minutes
function startAutoRefresh() {
    setInterval(loadData, 300000); // 5 minutes
}

// Initialize when document is ready
$(document).ready(function() {
    initApp();
    startAutoRefresh();
});
