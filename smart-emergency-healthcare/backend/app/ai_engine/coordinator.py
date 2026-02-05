import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_score(hospital, distance_km):
    # Normalized scoring logic
    # ICU Beds weight: 40%, Doctors: 30%, Proximity: 30%
    
    icu_score = min(hospital.icu_beds_available / 10, 1) * 40
    doc_score = min(hospital.doctors_available / 5, 1) * 30
    
    # Distance score: closer is better. If distance < 2km -> max score. > 50km -> 0
    if distance_km < 2:
        dist_score = 30
    elif distance_km > 50:
        dist_score = 0
    else:
        dist_score = (1 - (distance_km / 50)) * 30
        
    return icu_score + doc_score + dist_score

def find_best_hospital(patient_lat, patient_lng, hospitals):
    best_hospital = None
    highest_score = -1
    
    for hospital in hospitals:
        dist = haversine_distance(patient_lat, patient_lng, hospital.latitude, hospital.longitude)
        score = calculate_score(hospital, dist)
        
        # Update hospital score in object for return if needed, or just compare
        hospital.readiness_score = score 
        
        if score > highest_score:
            highest_score = score
            best_hospital = hospital
            
    return best_hospital
