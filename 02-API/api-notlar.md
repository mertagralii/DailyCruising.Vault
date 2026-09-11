---
rol: map
kapsam: api
guncelleme: 2026-09-11
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
- [[api-testlerde-aralikli-kirilma]] — bir kez kırılıp dört tur geçen test; kapatılmadı, izleniyor
- [[api-mv-ile-geri-alma-eski-dll]] — `mv` ile geri alınan mutasyon eski ikiliyi koşturuyor

### Gerekçe arşivi (2026-08-27)

Kod içi ⚠️ yorumları silinmeden önce birebir taşındı. Bir kararın *niçin*'ini
ararken önce [[api-kararlar]]'a, orada yoksa buraya bak.

- [[api-gerekce-arsivi-domain]] — varlıklar ve şema değişmezleri (23 blok)
- [[api-gerekce-arsivi-application]] — iş kuralları ve servisler (249 blok)
- [[api-gerekce-arsivi-infrastructure]] — EF, depolar, işler, dış servisler (152 blok)
- [[api-gerekce-arsivi-api]] — controller, yetki, boru hattı (90 blok)

İlgili: [[00-Index]] · [[api-kararlar]] · [[api-mimari]] · [[durum]]

## Bu alanın diğer bölmeleri

- [[api-desenler]] — kod yazarken uyulacak kurallar
- [[api-gorevler]] — yapılacak / yapılıyor / tamamlandı
- [[api-araclar]] — hangi durumda hangi plugin, skill, MCP
- [[api-benim-kararlarim]] — Mert'in toplu onayını bekleyen, benim aldığım kararlar
- [[api-sessiz-yutulan-hatalar]] — hatanın boş sonuca çökmesi API'de yok; denetim, sınır ve boşluk
- [[api-hiz-siniri-tetikleme]] — kova ömürleri, 429 tarifi, jetonsuz isteklerin de sayılması
- [[api-yazilmis-ama-uygulanmamis-kontrol]] — üç kez çıkan kusur sınıfı ve onu yakalayan iki soru
- [[api-uc-envanteri-2026-08-30]] — web panosundaki 12 iş için ölçülmüş uç envanteri ve eksikler
- [[api-eski-panel-tekne-ekranlari]] — canlı yönetim panelinin tekne ekranları, ölçülmüş yapı ve API boşlukları
- [[api-gelistirme-verisindeki-artiklar]] — "test artığı" sanılan kaydın gerçek kaynağı ve ayırt eden üç soru
- [[api-mutasyon-geri-alma]] — mutasyon geri alınmazsa geriye kapalı koruma ve yeşil süit kalır
