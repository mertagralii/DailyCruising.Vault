---
rol: map
kapsam: api
guncelleme: 2026-08-21
durum: guncel
---

# API Notları

Claude'un `DailyCruising.Back-End/` üzerine serbest gözlem alanı — .NET/araç
tuzakları, denenip olmayanlar, dikkat gerektiren davranışlar.

**Buraya ne yazılır:** karar olmayan ama tekrar karşılaşılacak API bilgisi.

**Buraya ne yazılmaz:** karar (→ [[api-kararlar]]), mevcut yapı tarifi
(→ [[api-mimari]]), koddan okunabilen şeyler.

Dosyalar `02-API/notlar/` altında, adları `api-` ile başlar.
Her not buradan linklenmeli — bağlanmamış not `dogrula.py`'de hata verir.

## Notlar

- [[api-slnx-formati]] — .NET 10 solution formatı ve araç uyumu
- [[api-webapi-sablon-tuzaklari]] — `dotnet new webapi` varsayılanları
- [[api-aralikla-silme-tuzagi]] — "A'dan B'ye kadar sil" beş görevi götürdü
- [[api-citext-toupper-tuzagi]] — `citext` kolonda `ToUpper()` indeksi öldürüyor
- [[api-hasindex-yutulmasi]] — aynı kolona ikinci `HasIndex` birincisini yok ediyor
- [[api-olay-gunlugu-iptal-jetonu]] — denetim kaydını saldırganın kendisi sildiriyordu
- [[api-jsonb-gin-opclass]] — jsonb GIN indeksi `->>` sorgularını hızlandırmaz
- [[api-terk-edilen-sefer-kilidi]] — süre dolunca sefer bırakılmazsa takvim kilitleniyor
- [[api-eszamanlilik-testi-yarismayabilir]] — "iki eşzamanlı istek" testi kısıtı ölçmüyor
- [[api-launchsettings-ortami-eziyor]] — üretim kapısı denemesi aslında Development'ı ölçüyor
- [[api-mv-ile-geri-alma-eski-dll]] — `mv` ile geri alınan mutasyon eski ikiliyi koşturuyor

İlgili: [[00-Index]] · [[api-kararlar]] · [[api-mimari]] · [[durum]]

## Bu alanın diğer bölmeleri

- [[api-desenler]] — kod yazarken uyulacak kurallar
- [[api-gorevler]] — yapılacak / yapılıyor / tamamlandı
- [[api-araclar]] — hangi durumda hangi plugin, skill, MCP
- [[api-benim-kararlarim]] — Mert'in toplu onayını bekleyen, benim aldığım kararlar
