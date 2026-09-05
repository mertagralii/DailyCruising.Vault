---
rol: map
kapsam: genel
guncelleme: 2026-09-05
durum: guncel
---

# Genel Notlar

Claude'un serbest gözlem alanı — her iki repoyu birden ilgilendiren veya hiçbirine
ait olmayan konular: araç davranışları, ortam tuzakları, çalışma akışı gözlemleri.

**Buraya ne yazılır:** karar olmayan ama tekrar karşılaşılacak bilgi. "Şu araç şöyle
davranıyor", "bunu denedim olmadı, sebebi şu", "bu davranış beklediğim gibi değil".

**Buraya ne yazılmaz:** karar (→ [[genel-kararlar]]), blocker (→ [[durum]]),
mevcut yapı tarifi (→ [[proje]]), tek oturumluk detay (→ `04-Oturumlar/`).

Dosyalar `01-Genel/notlar/` altında, adları `genel-` ile başlar.
Her not buradan linklenmeli — bağlanmamış not `dogrula.py`'de hata verir.

## Notlar

- [[genel-gateguard-davranisi]] — hook'ların hangi komutlarda gerçek olgu istediği
- [[genel-ecc-precompact-akisi]] — compact öncesi özetin nereden nereye gittiği

İlgili: [[00-Index]] · [[genel-kararlar]] · [[durum]] · [[calisma-duzeni]]

## Bu alanın diğer bölmeleri

- [[genel-desenler]] — kod yazarken uyulacak kurallar
- [[genel-gorevler]] — yapılacak / yapılıyor / tamamlandı
- [[genel-araclar]] — hangi durumda hangi plugin, skill, MCP
- [[genel-esszamanli-oturumlar]] — üç oturum aynı anda açıkken hook, `pwd` ve git durumu nasıl yanıltıyor
- [[genel-ecc-hook-profilleri]] — 33 ECC hook'u, işi durduranlar ve kapatma anahtarları
- [[genel-tasiyici-gerekce-taramasi]] — 10 bulgu: bir karar neye dayanıyor, o dayanak gerçekten var mı

- [[tercihler]] — kişisel katman, projeden bağımsız

