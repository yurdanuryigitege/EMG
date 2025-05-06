import openrouteservice, requests_cache, folium, time
import pandas as pd

# Önbellek ayarı
requests_cache.install_cache('http_cache', backend='sqlite', expire_after=180)
cache = requests_cache.get_cache()
print("Önbellek etkin mi?", bool(cache))

# OpenRouteService istemcisi
client = openrouteservice.Client(key='5b3ce3597851110001cf62483850ac0e5b6347b19a8c87a85f4249e5')

# Excel'den mahalle bilgilerini al
bilgi = pd.read_excel('mahalleler.xlsx')
enlem, boylam = 'Enlem', 'Boylam'
konumlar = list(zip(bilgi[boylam], bilgi[enlem]))

# Mesafe matrisi oluştur
def mesafe_matrixi_olustur(konumlar):
    try:
        matrix = client.distance_matrix(
            locations=konumlar,
            profile='driving-car',
            metrics=['distance'],
            units='m'
        )
        return matrix['distances']
    except Exception as e:
        print("Mesafe matrisi alınamadı:", e)
        return []

# Nearest Neighbor algoritması
def en_yakin_komsu(mesafeler):
    n = len(mesafeler)
    ziyaret_edildi = [False] * n
    rota = [0]
    ziyaret_edildi[0] = True

    for _ in range(n - 1):
        son = rota[-1]
        en_yakin = min(
            [(i, mesafeler[son][i]) for i in range(n) if not ziyaret_edildi[i]],
            key=lambda x: x[1]
        )[0]
        rota.append(en_yakin)
        ziyaret_edildi[en_yakin] = True

    rota.append(0)
    return rota

# Rota uzunluğunu hesapla (mesafe matrisine göre)
def rota_uzunlugu(rota, mesafeler):
    return sum(mesafeler[rota[i]][rota[i+1]] for i in range(len(rota)-1))

# 2-opt algoritması
def iki_opt(rota, mesafeler):
    en_iyi = rota[:]
    iyilesti = True
    while iyilesti:
        iyilesti = False
        for i in range(1, len(rota) - 2):
            for j in range(i + 1, len(rota) - 1):
                yeni_rota = en_iyi[:i] + en_iyi[i:j+1][::-1] + en_iyi[j+1:]
                if rota_uzunlugu(yeni_rota, mesafeler) < rota_uzunlugu(en_iyi, mesafeler):
                    en_iyi = yeni_rota
                    iyilesti = True
        rota = en_iyi
    return en_iyi

# Mesafe matrisi al
mesafeler = mesafe_matrixi_olustur(konumlar)

# Başlangıç rotası: Nearest Neighbor
rota_sirasi = en_yakin_komsu(mesafeler)

# 2-opt ile iyileştirme
rota_sirasi_opt = iki_opt(rota_sirasi, mesafeler)

# Koordinatlara dönüştür
tsp_konumlar = [konumlar[i] for i in rota_sirasi_opt]

# Toplam mesafeyi hesapla
toplam_mesafe = 0
for i in range(len(tsp_konumlar) - 1):
    bas = tsp_konumlar[i]
    son = tsp_konumlar[i + 1]
    rota = client.directions([bas, son], profile='driving-car', format='geojson')
    mesafe_ = rota['features'][0]['properties']['summary']['distance']
    toplam_mesafe += mesafe_
    time.sleep(1)

print(f"\n 2-opt sonrası toplam mesafe: {toplam_mesafe / 1000:.2f} km")

# Harita oluştur
harita_merkezi = tsp_konumlar[0]
harita = folium.Map(location=[harita_merkezi[1], harita_merkezi[0]], zoom_start=12)

# Toplam mesafeyi gösteren yazı
toplam_mesafe_yaz = f"Toplam mesafe: {toplam_mesafe / 1000:.2f} km"
folium.Marker(
    location=[harita_merkezi[1], harita_merkezi[0]],
    icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: black;">{toplam_mesafe_yaz}</div>')
).add_to(harita)

# Başlangıç noktası kırmızı
folium.Marker(
    location=[harita_merkezi[1], harita_merkezi[0]],
    popup="Başlangıç Noktası",
    icon=folium.Icon(color="red")
).add_to(harita)

# Diğer noktalar
for konum in tsp_konumlar[1:-1]:
    folium.Marker([konum[1], konum[0]]).add_to(harita)

# Rota çiz
for i in range(len(tsp_konumlar) - 1):
    bas = tsp_konumlar[i]
    son = tsp_konumlar[i + 1]
    rota = client.directions([bas, son], profile='driving-car', format='geojson')
    koordinatlar = rota['features'][0]['geometry']['coordinates']
    folium.PolyLine(locations=[(enlem_, boylam_) for boylam_, enlem_ in koordinatlar], color='blue', weight=2.5, opacity=1).add_to(harita)

# Haritayı kaydet
harita.save("harita_tsp_2_opt.html")
print("Harita 'harita_tsp_2_opt.html' olarak kaydedildi.")
