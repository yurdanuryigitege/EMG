import openrouteservice,requests_cache,folium,time
import pandas as pd
"""
aşşağıdaki kod bir önbellek oluşturup openrouteservice'den sürekli yeni veri
istememek için böylece daha hızlı açılan bir uygulamamız olur ama özellikle
ücretsiz kullandığımız bu servisin günlük veri sınırı aşılmamış olur
"""
requests_cache.install_cache('http_cache', backend='sqlite', expire_after = 180)
cache = requests_cache.get_cache()
print("Önbellek etkin mi?", bool(cache))

#OpenRouteService istemcisi için API_KEY

client = openrouteservice.Client(key='5b3ce3597851110001cf62483850ac0e5b6347b19a8c87a85f4249e5')# <- Bu bana servisin verdiği anahtar

#Excelden mahalle bilgilerini almak için gerek kod
bilgi =pd.read_excel('mahalleler.xlsx') #dosya konumu belirtmediğimiz için aynı klasörde olmalı
#Excel dosyasındaki koordinat sütünlarının adları ile aynı olmalı dosyanın değişmesi halinde kodun sadece bu kısmını değiştirebilmek için böyle yazdık 
enlem,boylam = 'Enlem','Boylam'
#Veriyi işleyip kullanılabilir hale getiriyoruz
konumlar = list(zip(bilgi[boylam],bilgi[enlem]))
#Mesafe hesap fonksiyonu
def mesafe(bas,son):
    try:#bu kütüphaneyi kuşuçuşu değil de karayolu üzerinde gidebilmek için kullanıyoruz
        rota = client.directions([bas,son], profile='driving-car', format='geojson')
        mesafe = rota['features'][0]['properties']['summary']['distance']

        print(f"Mesafe: {mesafe /1000:.2f}")#virgülden sonraki iki basamak ile limitliyoruz
        return mesafe
    except openrouteservice.exceptions._OverQueryLimit:
        print("limit aşıldı")
        return float('inf')
# Toplam mesafeyi her node arası hesaplayalım
toplam_mesafe = 0
for i in range(len(konumlar)-1): # listeler python'da 0'dan başlıyor o yüzden 1 çıkarıyoruz
    bas = konumlar[i]
    son = konumlar[i + 1]
    toplam_mesafe += mesafe(bas,son)
    time.sleep(1)#API'ın veri sınırını zorlamamak için 1 saniye bekliyoruz bir sonraki istekten önce

print(f"\n Toplam mesafe: {toplam_mesafe /1000:.2f} km")

# folium kütüphanesi harita çizme haritada nokta belirtme işlevlerinden dolayı kullanılıyor

harita_merkezi = konumlar[0] # birinci konum harita merkezi olarak atandı
harita = folium.Map(location=[harita_merkezi[1],harita_merkezi[0]],zoom_start= 12)#folium ile harita oluşturuldu

#Toplam katedilen mesafenin ekranda yazmasını ve başlangıç konumunun kırmızı işaretçi ile gösterilmesini istiyorum
toplam_mesafe_yaz = f"Toplam mesafe: {toplam_mesafe / 1000:.2f} km"# Toplam mesafe yazısı
folium.Marker(
    location=[harita_merkezi[1], harita_merkezi[0]],
    icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: black;">{toplam_mesafe_yaz}</div>')
).add_to(harita)

folium.Marker(# kırmızı işaretçi
    location=[harita_merkezi[1],harita_merkezi[0]],
    popup="Başlangıç Noktası",
    icon=folium.Icon(color ="red")

).add_to(harita)
for konum in konumlar:#diğer konum işaretçileri
    folium.Marker([konum[1], konum[0]]).add_to(harita)
#rota hattını çizmek için
for i in range(len(konumlar) - 1):
    bas = konumlar[i]
    son = konumlar[i + 1]
    rota = client.directions([bas, son], profile= 'driving-car', format = 'geojson')
    koordinatlar = rota['features'][0]['geometry']['coordinates']
    folium.PolyLine(locations = [(enlem,boylam) for boylam, enlem in koordinatlar], color='blue', weight= 2.5, opacity=1).add_to(harita)
#haritayı HTML dosyası olarak kaydet
harita.save("harita.html")
print("Harita 'harita.html' olarak kaydedildi. ")

