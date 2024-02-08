from geopy.distance import geodesic
import requests
import json

class googleGeo():
    def __init__(self, api, keyword):
        self.keyword = keyword
        self.API_KEY = api

    # 將地址轉換為經緯度
    def geocode_address_google(self, address):
        base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        endpoint = f"{base_url}address={address}&key={self.API_KEY}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            results = json.loads(response.content)
            if results['status'] == 'OK':
                location = results['results'][0]['geometry']['location']
                return location['lat'], location['lng']
        return None

    # 以 Keyword 搜索附近的醫院和便利商店
    def find_nearby_places(self, lat, lng, keyword):
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        location = f"{lat},{lng}"
        radius = 1000  # 1公里內的範圍
        endpoint = f"{base_url}location={location}&radius={radius}&keyword={keyword}&key={self.API_KEY}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            results = json.loads(response.content)
            return results.get('results', [])
        return []


    # 以經緯度計算距離
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        coords_1 = (lat1, lng1)
        coords_2 = (lat2, lng2)
        distance = geodesic(coords_1, coords_2).kilometers
        return distance

    def find_nearest_places(self, lat, lng, keyword):
        # 搜索附近的地標
        loccations = self.find_nearby_places(lat, lng, keyword)

        # 計算距離
        distances = []

        for place in loccations:
            dist = self.calculate_distance(lat, lng, place['geometry']['location']['lat'], place['geometry']['location']['lng'])
            distances.append((place['name'], dist))

        return distances


    def extract_place(self, data):
        location_count = len(data)
        try:
            nearest_location = min(data, key=lambda x: x[1])
            nearest_location_distance = nearest_location[1]
        except:
            nearest_location_distance = 0

        return location_count, nearest_location_distance