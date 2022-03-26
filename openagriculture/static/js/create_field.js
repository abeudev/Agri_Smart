// Declaring the map
var map = L.map('create-field-map-div');
map.setView([45.1544, 10.7896], 13);

// Tileset
// L.tileLayer('https://a.tile.openstreetmap.de/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Open Agriculture'
// }).addTo(map);
//
// map.options.minZoom = 12;
// map.options.maxZoom = 16;

var popup = L.popup();
var create_field_is_clicked = false;
var points = new Array();
var polyline = L.polyline(points).addTo(map);
var polygon_field;

function onMapClick(e)
{
    if(create_field_is_clicked)
    {
      polyline.remove();
      latLng = e.latlng
      points.push([latLng.lat,latLng.lng]);
      polyline = L.polyline(points).addTo(map);
   }
}

map.on('click', onMapClick);

function create_field_clicked()
{
   var element = document.getElementById("create_field_btn");

   if( element.textContent == "Define Field")
   {
      element.classList.remove("btn-success");
      element.classList.add("btn-danger");
      element.textContent="Save Field";
      create_field_is_clicked = true;
   }
   else
   {
         element.classList.remove("btn-danger");
         element.classList.add("btn-success");
         element.textContent="Define Field";
         create_field_is_clicked = false;

         geometry_string = ''

         for (var i = 0; i < points.length; i++)
         {
            geometry_string += points[i][0] + ','+ points[i][1] + ','
         }
         
         geometry_string = geometry_string.substring(0, geometry_string.length - 1);
         document.getElementById("field-geometry").value = geometry_string;
         document.getElementById("field-geometry").data = true;
         polygon_field = L.polygon(points).addTo(map);


         points = new Array();
   }

}
