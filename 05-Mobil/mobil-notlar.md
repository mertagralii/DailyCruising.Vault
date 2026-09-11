---
rol: map
kapsam: mobil
guncelleme: 2026-09-10
durum: guncel
---

# Mobil Notları

Claude'un `DailyCruising.Mobil/` üzerine serbest gözlem alanı — Expo/React Native
tuzakları, denenip olmayanlar, dikkat gerektiren davranışlar.

**Buraya ne yazılır:** karar olmayan ama tekrar karşılaşılacak mobil bilgisi.
Özellikle **kod karşılığı olmayan** hatalar: ortam, araç, süreç, dış servis.
Not, hata metnini **birebir** taşır — tetikleyici hatırlamak değil **aramaktır**.

**Buraya ne yazılmaz:** karar (→ [[mobil-kararlar]]), mevcut yapı tarifi
(→ [[mobil-mimari]]), koddan okunabilen şeyler. Bir kod satırına bağlanabilen
hatanın evi vault değil, **o satırdır** → [[genel-desenler]]

Dosyalar `05-Mobil/notlar/` altında, adları `mobil-` ile başlar.
Her not buradan linklenmeli ve en az bir başka nota link vermeli — bağlanmamış
veya yalıtılmış not `dogrula.py`'de hata verir.

## Notlar

- [[mobil-iptal-ucu-reason-zorunlu]] — `POST /api/reservations/{code}/cancel`
  `reason` zorunlu istiyor ama `openapi.json` alanı opsiyonel gösteriyor;
  üretilen tip yeşil geçer, uç çalışma zamanında reddeder. **İptal ekranı
  yazılmadan önce okunur.**

İlgili: [[mobil-kararlar]] · [[mobil-mimari]] · [[mobil-durum]] · [[00-Index]]

## Bu alanın diğer bölmeleri

- [[mobil-desenler]] — kod yazarken uyulacak kurallar
- [[mobil-gorevler]] — yapılacak / yapılıyor / tamamlandı
- [[mobil-araclar]] — hangi durumda hangi plugin, skill, MCP
