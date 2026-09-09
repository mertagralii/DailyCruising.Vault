---
rol: not
kapsam: api
guncelleme: 2026-09-06
durum: guncel
---

# Eski panelin tekne ekranları — ölçülmüş yapı ve API karşılıkları

2026-09-06'da Mert *"bu sayfayı incele ve tekne ekleme kısmını buna göre
ayarla"* dedi. Canlı yönetim paneli (`dailycruising.com.tr/admin`) tarayıcıdan
gezildi; aşağıdakiler **ekrandan okundu**, tahmin edilmedi.

## Tekne Ekle — `/admin/tekne-yonetimi/ekle`

Tek sayfa, beş bölüm, altta `Vazgeç` + `Tekneyi Ekle`.

| Bölüm | Alanlar |
|---|---|
| Genel Bilgiler | Ana resim* · **Tekne sahibi*** (33 işletme, `ad / tür`) · Tekne adı* · Bölge* (8) · **Para birimi*** (₺/$/€) · `Yayınla` anahtarı |
| Kiralama Tipleri | 8 tipten çoklu seçim |
| Kapasite & Boyut | Uzunluk* · Genişlik* · **Derinlik*** |
| Açıklama | Açıklama (TR)* · Açıklama (EN) |
| Konum | Haritadan Seç / Adres Gir / Koordinatlar — Leaflet |

⚠️ Bölüm adı "Kapasite & Boyut" ama **kapasite alanı YOK** — yalnız üç ölçü var.
Yolcu sayısı, kabin, yatak, banyo, mürettebat bu formda hiç sorulmuyor.

## Tekne Listesi — `/admin/tekne-yonetimi`

Kart ızgarası (4 sütun). Üstte arama + `Ara` + `Temizle` + "Toplam 35 tekne".
Kart: kapak · durum rozeti · ad · kiralama tipi rozetleri · son güncelleme ·
dört ikon düğme (**Fiyat · Özellik · Rota · Menü** → modal) · **Resimler** ve
**Detay** (sayfa) · turuncu **Düzenle**.

### Dört modal

| Modal | Yapı |
|---|---|
| **Ücret Bilgileri** | Sol: Başlangıç*/Bitiş tarihi*, Kiralama tipi* (yalnız O TEKNENİN tipleri), `Fiyatı Ekle`. Sağ: tablo — Başlangıç · Bitiş · Tip · Fiyat (Yetişkin/Çocuk/Bebek) · Güncelleme · Düzenle/Sil |
| **Ekstra Özellikler** | `Özellik (TR)` + `Feature (EN)` + `Ekle`; liste |
| **Tekne Rotaları** | `Rota (TR)` + `Route (EN)` + `Ekle`; liste |
| **Yemek Menüsü** | `Menü Adı (TR)` + `Menu Name (EN)` + **`Fiyat`** + `Ekle`; liste |

Üçü de aynı kalıp: TR/EN çifti + tek satırlık ekleme + boş durum metni.
Menü ötekilerden **fiyat alanıyla** ayrılıyor.

`Resimler` (`/tekne-resimleri/{id}`): ızgara, kart başına Görüntüle/İndir/Sil,
altta tek dosyalık `Yeni Resim Ekle`.

`Detay` (`/detay/{id}`): künye + "Tekne Albümü (Toplam N Resim)" + fiyat tablosu.

⚠️ **Ölçüm tuzağı:** modallar ilk denemede AÇILMADI ve "sitede bozuk" sanıldı.
Sebep, sayfa scriptleri yüklenmeden tıklamaktı; 3 saniye beklenince dördü de
açıldı. **Bir kez denenip "çalışmıyor" demek ölçüm değil** → [[api-yazilmis-ama-uygulanmamis-kontrol]]

## Bizim API'ye göre boşluklar

| Eski panel | Bizde | Fark |
|---|---|---|
| Tekne sahibi seçimi | yok | Tekne ekleme YALNIZ işletme hesabıyla, kendi teknesi için. Platform personelinin başkası adına tekne açacağı uç yok |
| Derinlik | yok | `Boats` içinde `LengthMeters`/`WidthMeters` var, derinlik yok → kolon + migration |
| Para birimi tekne başına | kiralama tipi başına (`ListCurrency`) | Hangisi doğru, karar Mert'te |
| Özellik / Rota / Menü serbest metin | katalog anahtarlı `Amenities`, `Rules`, tipli `Extras` | Eski panel her tekneye serbest metin yazdırıyor; bizde ortak katalog var ve arama süzgeci ona dayanıyor. **Serbest metne dönmek arama süzgecini bitirir** |
| Menü öğesi fiyatı | `BoatExtras` (`Menu` tipi, fiyatlı) | Karşılığı var |
| Kapasite alanları yok | zorunlu | Bizde daha katı; eski panelde nereden giriliyor bulunamadı |

**Not:** ekran tasarımı ve Next.js tarafı web oturumunun alanı; burada yalnız
ölçüm ve API karşılıkları duruyor → [[api-uc-envanteri-2026-08-30]]
