import pandas as pd

# PTT şube verilerini içeren sözlük
data = {
    "Şube Adı": ["Odunpazarı PTT Merkez", "Emek Mahallesi Şubesi", "Gar Merkezi Şubesi", 
                  "Orhangazi Şubesi", "Sakarya Şubesi", "Çukurhisar Şubesi", "Batıkent Şubesi", 
                  "71 Evler Şubesi", "Kırmızıtoprak Şubesi", "Mamure Şubesi"],
    "Enlem": [39.766930, 39.766970, 39.775200, 39.770000, 39.776890, 39.723010, 39.770220, 
              39.780490, 39.775800, 39.776120],
    "Boylam": [30.519280, 30.520580, 30.528330, 30.517530, 30.520570, 30.501340, 30.528700, 
               30.524000, 30.529100, 30.501430]
}

# DataFrame oluştur
df = pd.DataFrame(data)

# Excel dosyasına yaz
df.to_excel("mahalleler.xlsx", index=False)
