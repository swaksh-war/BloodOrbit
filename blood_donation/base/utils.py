from math import sin, cos, atan2, radians, sqrt
from .models import Donor

def get_compatible_blood_groups(blood_group):
    compatibility = {
        "A+" : ["A+", "A-", "O+", "O-"],
        "A-" : ["A-", "O-"],
        "B+" : ["B+", "B-", "O+", "O-"],
        "B-" : ["B-", "O-"],
        "AB+" : ["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"],
        "AB-" : ["A-", "B-", "AB-", "O-"],
        "O+" : ["O+", "O-"],
        "O-" : ["O-"]
    }
    return compatibility.get(blood_group, [])

def haversine(lat1, lon1, lat2, lon2):
    R = 6731
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_compatible_donors(recipient_lat, recipient_lon, recipient_blood_group, radius_km=5):
    compatible_blood_groups = get_compatible_blood_groups(recipient_blood_group)
    donors = Donor.objects.filter(blood_group__in=compatible_blood_groups)
    compatible_donors = []
    for donor in donors:
        distance = haversine(recipient_lat, recipient_lon, donor.latitude, donor.longitude)
        donor.distance = distance
        compatible_donors.append(donor)
    return compatible_donors
