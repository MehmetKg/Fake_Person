from mimesis import Generic
from mimesis.enums import Locale
import json
import csv
import sqlite3

# Sahte kullanıcı üretme fonksiyonu
def sahte_kullanici_uret(locale=Locale.TR, adet=5):
    fake = Generic(locale=locale)
    return [ {
        "isim": fake.person.full_name(),
        "eposta": fake.person.email(),
        "şehir": fake.address.city(),
        "telefon": fake.person.telephone(),
        "kullanici_adi": fake.person.username(),
        "parola": fake.person.password(length=12),
        "dogum_tarihi": fake.datetime.date(start=1970, end=2005).isoformat(),
        "kimlik_no": fake.code.imei()
    } for _ in range(adet) ]

# Veri üret
kullanicilar = sahte_kullanici_uret(adet=10)

# 1. JSON çıktısı
with open("kullanicilar.json", "w", encoding="utf-8") as f_json:
    json.dump(kullanicilar, f_json, ensure_ascii=False, indent=4)

# 2. CSV çıktısı
with open("kullanicilar.csv", mode="w", newline="", encoding="utf-8") as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(["İsim", "Eposta", "Şehir", "Telefon", "Kullanıcı Adı", "Parola", "Doğum Tarihi", "Kimlik No"])
    for kisi in kullanicilar:
        writer.writerow([
            kisi["isim"], kisi["eposta"], kisi["şehir"], kisi["telefon"],
            kisi["kullanici_adi"], kisi["parola"], kisi["dogum_tarihi"], kisi["kimlik_no"]
        ])

# 3. SQLite veritabanı çıktısı
conn = sqlite3.connect("kullanicilar.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS kullanicilar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT,
        eposta TEXT,
        sehir TEXT,
        telefon TEXT,
        kullanici_adi TEXT,
        parola TEXT,
        dogum_tarihi TEXT,
        kimlik_no TEXT
    )
""")
for kisi in kullanicilar:
    c.execute("""
        INSERT INTO kullanicilar (isim, eposta, sehir, telefon, kullanici_adi, parola, dogum_tarihi, kimlik_no)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        kisi["isim"], kisi["eposta"], kisi["şehir"], kisi["telefon"],
        kisi["kullanici_adi"], kisi["parola"], kisi["dogum_tarihi"], kisi["kimlik_no"]
    ))
conn.commit()
conn.close()

print("✅ JSON, CSV ve SQLite dosyaları başarıyla oluşturuldu.")
