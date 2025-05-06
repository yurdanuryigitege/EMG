import pandas as pd

# Mahalle verilerini içeren sözlük
data = {
    "Mahalle Adı": ["Muttalip Orta Mah.", "Çanakkıran Mah.", "Yukarıılıca Mah.", 
                    "Karacaşehir Mah.", "Akpınar Mah.", "Aşağı Çağlan Mah.", "Ayvacık Mah."],
    "Enlem": [39.839491, 39.669940, 39.537610, 39.737778, 39.659440, 39.678720, 39.536200],
    "Boylam": [30.546304, 30.250660, 30.447030, 30.456667, 30.547780, 30.483750, 30.484490]
}

# DataFrame oluştur
df = pd.DataFrame(data)

# Excel dosyasına yaz
df.to_excel("mahalleler.xlsx", index=False)
