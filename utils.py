
import math, time, httpx

def geocode(address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "jsonv2", "limit": 1}
    headers = {"User-Agent": "vertex-laudos/1.0"}
    r = httpx.get(url, params=params, headers=headers, timeout=30)
    if r.status_code != 200 or not r.json():
        return None
    data = r.json()[0]
    time.sleep(1)
    return float(data["lat"]), float(data["lon"])

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(a))
