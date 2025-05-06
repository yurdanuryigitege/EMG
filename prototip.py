import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations

# Mahalle verileri
locations = {
    "Muttalip Orta Mah.": (39.839491, 30.546304),
    "Çanakkıran Mah.": (39.669940, 30.250660),
    "Yukarıılıca Mah.": (39.537610, 30.447030),
    "Karacaşehir Mah.": (39.737778, 30.456667),
    "Akpınar Mah.": (39.659440, 30.547780),
    "Aşağı Çağlan Mah.": (39.678720, 30.483750),
    "Ayvacık Mah.": (39.536200, 30.484490)
}

# Mesafe hesaplama fonksiyonu (Haversine formülü)
def haversine(coord1, coord2):
    R = 6371  # Dünya yarıçapı (km)
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2.0)**2 + \
        np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

# Tüm permütasyonları deneyerek en kısa rotayı bulma
min_distance = float('inf')
best_route = None
for perm in permutations(locations.keys()):
    distance = 0
    for i in range(len(perm)):
        start = locations[perm[i]]
        end = locations[perm[(i + 1) % len(perm)]]
        distance += haversine(start, end)
    if distance < min_distance:
        min_distance = distance
        best_route = perm

# Sonuçları yazdırma
print("En kısa rota:")
for place in best_route:
    print(place)
print(f"Toplam mesafe: {min_distance:.2f} km")

# Rota görselleştirme
lats = [locations[place][0] for place in best_route] + [locations[best_route[0]][0]]
lons = [locations[place][1] for place in best_route] + [locations[best_route[0]][1]]

plt.figure(figsize=(10, 6))
plt.plot(lons, lats, 'o-', color='blue')
for i, place in enumerate(best_route):
    plt.text(locations[place][1], locations[place][0], f"{i+1}. {place}", fontsize=9)
plt.title("En Kısa Rota - Gezgin Satıcı Problemi")
plt.xlabel("Boylam")
plt.ylabel("Enlem")
plt.grid(True)
plt.show()

