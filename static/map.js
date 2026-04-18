var map = L.map('map').setView([25.0336646, 121.5438858], 16);

var marker = L.marker([25.0336646, 121.5438858]).addTo(map);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);