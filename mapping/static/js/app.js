// 地理院地図　標準地図
var std = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
    {id: 'stdmap', attribution: "<a href='http://portal.cyberjapan.jp/help/termsofuse.html' target='_blank'>国土地理院</a>"})
// 地理院地図　淡色地図
var pale = L.tileLayer('http://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
    {id: 'palemap', attribution: "<a href='http://portal.cyberjapan.jp/help/termsofuse.html' target='_blank'>国土地理院</a>"})
// OSM Japan
var osmjp = L.tileLayer('http://tile.openstreetmap.jp/{z}/{x}/{y}.png',
    { id: 'osmmapjp', attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' });
// OSM本家
var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { id: 'osmmap', attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' });

var baseMaps = {
    "地理院地図 標準地図" : std,
    "地理院地図 淡色地図" : pale,
    "OSM" : osm,
    "OSM japan" : osmjp
};
// "map" div に地図を作成し、マップを埋め込む場所のidとマップオブジェクトの紐付け
var map = L.map('map', {layers: [osm]});

// マップの中心地点を[緯度,経度],ズーム倍率で指定
map.setView([43.060338, 141.348186], 12); //札幌

// コントロールはオープンにする　変数Lを使ってLeafletライブラリそのものにアクセスする
L.control.layers(baseMaps, null, {collapsed:false}).addTo(map);

//スケールコントロールを追加（オプションはフィート単位を非表示）
L.control.scale({imperial: false}).addTo(map);

// get geoJSON file and put markers on the map
$.getJSON("/mapping/geojson/", function(data) {
    var geojson = L.geoJson(data,  {
      pointToLayer: function (feature, coordinates) {
         return L.marker(coordinates, {icon:
            L.AwesomeMarkers.icon({icon: '',
            markerColor: 'darkblue',
            prefix: 'fa',
            html: (feature.properties.number)})})},
      onEachFeature: function (feature, layer) {
            layer.bindPopup(feature.properties.title);
        }
    });
    geojson.addTo(map);
});
