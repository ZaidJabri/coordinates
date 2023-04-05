api_key = "AIzaSyAKY_4kNJ0xHBgVCE6k9ZgSX-njXno1BTQ"
import requests
from flask import Flask, jsonify

app = Flask(__name__)


# def get_boundary_coordinates(place_name):
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     place_name = place_name.replace(" ", "%20")
#     query = f"""
#     [out:json];
#     area["name"~"{place_name}"];
#     (way(area)[boundary=administrative];
#     relation(area)[boundary=administrative];);
#     out body;
#     >;
#     out skel qt;
#     """
#     response = requests.get(overpass_url, params={"data": query})
#     response_json = response.json()
#     elements = response_json["elements"]
#     print(elements)
#     boundary_coordinates = []
#     for element in elements:
#         if element["type"] == "way":
#             nodes = element["nodes"]
#             for node_id in nodes:
#                 node = [x for x in elements if x["type"] == "node" and x["id"] == node_id][0]
#                 boundary_coordinates.append((node["lat"], node["lon"]))
#         elif element["type"] == "relation":
#             members = element["members"]
#             for member in members:
#                 if member["type"] == "way":
#                     way = [x for x in elements if x["type"] == "way" and x["id"] == member["ref"]][0]
#                     nodes = way["nodes"]
#                     for node_id in nodes:
#                         node = [x for x in elements if x["type"] == "node" and x["id"] == node_id][0]
#                         boundary_coordinates.append((node["lat"], node["lon"]))
#     return boundary_coordinates


def get_boundary_coordinates(place_name):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={api_key}"
    response = requests.get(geocode_url)
    response_json = response.json()
    results = response_json["results"]
    if len(results) == 0:
        return None
    result = results[0]
    geometry = result["geometry"]
    bounds = geometry.get("bounds")
    if bounds is None:
        viewport = geometry["viewport"]
        southwest = viewport["southwest"]
        northeast = viewport["northeast"]
        boundary_coordinates = [(southwest["lat"], southwest["lng"]), (northeast["lat"], northeast["lng"])]
    else:
        southwest = bounds["southwest"]
        northeast = bounds["northeast"]
        boundary_coordinates = [(southwest["lat"], southwest["lng"]), (northeast["lat"], northeast["lng"]),
                                (northeast["lat"], southwest["lng"]), (southwest["lat"], northeast["lng"])]
    return boundary_coordinates


# Example
co = []
co.append(get_boundary_coordinates("الجامعة الأردنية"))
print(co)


@app.route('/coordinates', methods=['GET'])
def coordinates_Convert():
    json_data = {}
    points = {}

    for i, point in enumerate(co[0]):
        point_key = f"Point {i + 1}"
        points[point_key] = {"latitude": point[0], "longtitude": point[1]}

    json_data = points

    return jsonify(json_data)


if __name__ == '__main__':
    app.run(debug=True)
