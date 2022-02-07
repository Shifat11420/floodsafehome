// initialize the map on the "map" div with a given center and zoom
var map = L.map('map', {
    center: [29.99,-90.15],
    zoom: 13
});

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoiaml5b3VuZyIsImEiOiJja3o1eXFqNHIwdjhzMm9tejh3eWZjd2R4In0.Rz8iZagw0-OVOS1fjKMwzQ'
}).addTo(map);


var marker = L.marker([29.99,-90.15]).addTo(map);