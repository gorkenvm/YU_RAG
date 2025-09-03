################################################################################
from YU_functions import fetch_announcements, export_to_json, fetch_content, process_announcements_with_ai
################################################################################

# Kullanım
url = 'https://www.yasar.edu.tr/duyurular/'

# Duyuruları çek
duyurular = fetch_announcements(url)

# Duyuruların detaylarını çek
duyurular_detayli = fetch_content(duyurular)

# Duyuruları GEMINI ile işle
detailed_announcements = process_announcements_with_ai(duyurular_detayli)

# Duyuruları ekrana yazdır
for i, duyuru in enumerate(detailed_announcements):
    baslik = duyuru.get('baslik', 'Başlık Bulunamadı')
    aiicerik = duyuru.get('aiicerik', 'AI özet içeriği yok')
    print(f"----------------------------------")
    print(f"Duyuru {i + 1}:")
    print(f"Başlık: {baslik}")
    print(f"AI İçerik: {aiicerik}\n")


# Duyuruları JSON dosyasına kaydet
export_to_json(detailed_announcements, 'duyurular_aiicerik.json')
