from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/restaurants', methods=['POST'])
def restaurants():
    data = request.json
    lat = data['lat']
    lon = data['lon']
    radius = data.get('radius', 500)

    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f'''
    [out:json];
    (
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["amenity"="fast_food"](around:{radius},{lat},{lon});
      node["amenity"="cafe"](around:{radius},{lat},{lon});
    );
    out;
    '''

    res = requests.post(overpass_url, data=query)
    data = res.json()

    results = []
    for el in data['elements']:
        name = el.get('tags', {}).get('name')
        if name:
            results.append({
                "name": name,
                "lat": el["lat"],
                "lon": el["lon"]
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
