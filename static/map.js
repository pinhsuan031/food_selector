const lat = 25.0333673;
const lng = 121.5433068;

var map = L.map('map').setView([lat, lng], 16.5);

var marker = L.marker([lat, lng]).addTo(map);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);