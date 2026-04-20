var map = L.map('map').setView([25.0333673, 121.5433068], 16.5);

var marker = L.marker([25.0333673, 121.5433068]).addTo(map);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);