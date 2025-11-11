
import math, time, httpx

def geocode(address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "jsonv2", "limit": 1}
    headers = {"User-Agent": "vertex-laudos/1.0"}
    r = httpx.get(url, params=params, headers=headers, timeout=30)
    if r.status_code != 200:
        return None
    data = r.json()
    if not data:
        return None
    time.sleep(1)  # polite to Nominatim
    return float(data[0]["lat"]), float(data[0]["lon"])

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    import math
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
