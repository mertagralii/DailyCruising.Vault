---
rol: status
kapsam: web
guncelleme: 2026-09-12
durum: guncel
---

# Web Durumu

> **Bu dosyanın sahibi `DailyCruising.Front-End/` içinde çalışan oturumdur.**
> Web tarafının güncel durumu buraya yazılır; `01-Genel/durum.md`'ye **yazılmaz**.
> Genel dosya bu dosyayı özetler → [[durum]]

## ✅ Tasarım bitti (2026-08-24)

19 ekranın tamamı uygulandı, ölçüldü ve doğrulandı. `isBreak` hariç — kırılım
vitrini, gerçek sayfa değil; mobil şartnamesi oradan çıkarıldı.

| Alan | Masaüstü (1280) | Mobil (390) |
|---|---|---|
| 16 misafir/hesap sayfası | 12'si birebir, kalanı ≤4px | taşma yok |
| Yönetim paneli (24 modül) | 19'u birebir · 18px | taşma yok |
| Destek paneli (4 bölüm) | 12px | taşma yok |
| İşletme paneli (10 bölüm) | 4'ü birebir · 16px | taşma yok |

Kalan sapmaların ortak kaynağı koyu başlık bandındaki kicker satırı (+2px, üç
panelde de aynı). Metin farkı yalnızca iki bilinçli sapma: tasarımdaki bozuk `i̇`
karakteri ve gerçek `<input placeholder>` kullanımı → [[web-kararlar]]

## ✅ Geri bildirim katmanı bitti (2026-08-26)

Tasarım kaynağında **olmayan** ortak parçalar token setinden türetildi (`W-10`):
toast · modal + onay diyaloğu · 404/500/403/503 · iskelet · boş durum · sayfalama
· üst ilerleme çubuğu · dosya yükleme · rezervasyon başarı ekranı · yazdırılabilir
QR biniş belgesi · 4 e-posta şablonu → [[web-kararlar]]

Rota sayısı 20 → **25**. Hepsi 1280×730 ve 390px'te ölçüldü, taşma yok.

**Bu ekranlar "tasarıma birebir" değil "tasarım diliyle tutarlı".** Kaynakları
olmadığı için Mert tasarımı güncellerse ayrıca gözden geçirilmeleri gerekir.

Kapsam dışı bırakılan iki parça (Mert seçmedi): satır içi uyarı bandı ve
`Button`'a `loading` durumu. İkincisi hâlâ açık bir risk — kullanıcı gönder
düğmesine iki kez basarsa çift rezervasyon oluşabilir; sunucu tarafı
`A-22`'de bunu engelliyorsa sorun yok, engellemiyorsa istemcide de gerekir.

## ✅ Yapılabilir işlerin tamamı bitti (2026-08-28)

Pano `🟩 A`, `🟪 B` ve `🟦 E` **boş**. Kalan 13 görevin **12'si backend'de**,
biri (`W-06`) Mert'te.

**36 rota**, `npm run build` ve `npm run lint` temiz, 17 sayfa 390px'te
**sıfır yatay taşma**. On dört commit, hepsi `origin/main`'de.

> ⚠️ **Bu satırdaki 36 o günün ölçümü, bugünün değil** (2026-09-09'da
> düzeltildi). Güncel sayı **41**; ölçüm `web-mimari` sonundaki blokta
> yaşıyor ve orası tek otorite. Tarihli bir bölümdeki sayıyı güncellemek
> o günün kaydını bozardı, o yüzden satır duruyor ama işaretlendi.

### Gerçek uçlara bağlananlar

Arama · filtreler · sayfalama · tekne detayı · yorumlar · rezervasyon akışı
(teklif → rezervasyon → ödeme) · rezervasyon iptali · rezervasyonlarım ·
işletme paneli (tekne, belge, değerlendirme) · yönetim paneli (işletme,
destek, yorum, iş sağlığı) · izin bazlı menü · kimlik (giriş, kayıt, çıkış,
parola sıfırlama, e-posta doğrulama, hesap kapatma)

### Tasarımda olmayıp yazılan on bir ekran

En kritiği **biniş (QR okutma)**: tasarımın her yerinde "iskelede QR'ını okut"
yazıyordu ama tekne sahibinin okutacağı ekran hiç çizilmemişti — QR akışı
tasarımda **yarımdı**.

Diğerleri: mesajlaşma + özel teklif (iki taraf) · yorum daveti · kayıt ·
parola sıfırlama · e-posta doğrulama · hesap kapatma · rol yönetimi +
sahiplik devri · tekne durum etkisi önizlemesi · iş sağlığı · işletme başvurusu

### Bulunan ve düzeltilen üç ciddi hata

Dördü de geliştirmede kolayca gözden kaçan, yayında görünecek türden:

1. **Render'da çerez yazılamıyor.** Jeton 15 dakikada ölüyor ve yenileme
   render sırasında çöküyordu. Kod ilk 15 dakika kusursuz çalışıyor ve **her
   kullanıcıyı 16. dakikada 500'e düşürecekti** → [[web-render-sirasinda-cerez]]
2. **Yenileme bir istek geç kalıyordu.** Proxy jetonu yanıta yazıyor, aynı
   isteğin render'ı eskisini görüyordu; kullanıcı bir kez 404 görüyordu
3. **Vekil tüm siteyi tek IP yapıyordu.** `rezervasyon` kovası 15 dk/10 ve IP
   bazlı — **tüm site 15 dakikada 10 rezervasyonla sınırlıydı**
4. **Vekil çok parçalı gövdeyi bozuyordu.** `request.blob()` `boundary`
   parametresini düşürüyor, sunucu gövdeyi ayrıştıramıyordu. **Vekilden geçen
   her dosya yüklemesi** — tekne görselleri ve belgeler — çalışmıyordu
   → [[web-vekil-multipart-boundary]]

## 🔜 Sıradaki iş

⚠️ **2026-08-28 akşamı bu cümle geçersiz oldu.** `openapi.json`'daki 74 yol
front-end'in gerçekten çağırdığı yollarla karşılaştırıldı: **21 yolun çağrısı
yok** ve **beşinin ekranı zaten var**, yalnız mock veriyle çalışıyor. Yani
uç bekleyen değil, **bağlanmayı bekleyen** iş var → `W-58` … `W-63`.

Önceki ölçüm gevşekti: uç adının kaynakta geçip geçmediğine bakıyordu ve
"hepsi bağlı" diyordu. Doğru ölçüt **`api()`/`dcFetch()` çağrısında yolun
kendisi**.

En ağır ikisi: işletme **kendi fiyatını giremiyor** (`W-58`, 12 işlem) ve
platform personeli bir başvuruyu **onaylayamıyor** (`W-59`, 6 işlem) — ikincisi
yeni işletmenin sisteme girişini tamamen kesiyor.

Uç bekleyenler ise şunlar:

1. **`W-34` müsaitlik takvimi** — yalnız tek tarih sorgulanabiliyor
2. **`W-35` finans** — arayüzdeki bölüm **kapatıldı**; uç gelene ve `A-41`
   açılana kadar geri konmayacak
3. **`W-37` yönetim paneli** — 16 modülün ucu yok
4. **`W-39` favoriler / kuponlarım / bildirim tercihleri** — hiçbirinin ucu yok
5. **`W-57` tekne kaydının kalan alanları** — kapasite, marina, ruhsat,
   kaptan; yazma ekranı yok

**`W-55` tekne detay ucu 2026-08-28'de neredeyse kapandı.** İşletme adı,
kiralama tipleri (çoğul), fiyat tablosu, açıklama, kalkış tarifi, teknede
neler var ve kurallar bağlandı; aramaya donanım süzgeci geri kondu; işletme
paneline "tanıtım ve donanım" yazma ekranı yazıldı. Tek kalan `program`
(tur akışı) — çeviri tablosu boş.

**`W-03` tekne görselleri 2026-08-28'de kapandı.** `search.coverUrl`,
`boats/{slug}.media[]`, `partner/boats.coverUrl + mediaCount` ve dört medya
ucu bağlandı; işletme paneline yükle/sırala/kapak seç/sil ekranı yazıldı.
Kanıt → [[web-gorevler]]

`W-06` (`brand.ts` kurumsal verileri) Mert'te.

## ❓ Mert'e sorulacaklar — web

Numara `02-API/api-durum.md` ile **ortak seridir**; en büyük kullanılan
numaranın bir fazlası alınır, numara geri kullanılmaz.

| # | Soru | Şimdilik ne yapıldı |
|---|---|---|
| S-30 | **Blog: uç yazılsın mı, yoksa statik mi kalsın?** Varsayımım yanlıştı — şema **tamamen var** (4 tablo, çeviri + kategori + kapak + görüntülenme + onay akışı) ve `C5` kararın şemaya işlenmiş (`ApprovedByUserId`). Yani soru "tablo açalım mı" değil, **"yazılmamış uç yazılsın mı"**. Seçenekler: **(a)** uç yazılsın, blog panelden yönetilsin ve tekne sahipleri de yazabilsin (`blog.write` yetkisi zaten katalogda, onay `blog.approve`'da), **(b)** **statik kalsın + dört tablo düşürülsün**, **(c)** statik kalsın + tablolar dursun ama vault'a "bilerek boş, gerekçesi şu" yazılsın. ⚠️ **Düz "statik kalsın" bir seçenek değil:** kullanılmayan şema bayatlıyor ve altı ay sonra biri bu tablolara bakıp "blog yazılmış" sanıyor — bu hafta `publiclyReadable` ve `reservation.read` tam olarak böyle oldu. Ayrıca yedi yazı **uydurma yazar adlarıyla** duruyor ("Deniz Aksoy"); yayımlanacaklar mı? | Yalnız **ölçülebilir yanlış** düzeltildi: "Tümü · 48" yazıyordu, 7 yazı var — sayaç artık listeden hesaplanıyor; "haftada iki yazı" yayın sıklığı sözü kaldırıldı. Yazılara ve yazar adlarına dokunulmadı |
| S-29 | **`brand.ts`'teki "340+ onaylı tekne" ne olacak?** Bu ibare her sayfanın **üst şeridinde** duruyor ve en çok görülen sayı. Backend geliştirme veritabanını ölçtü: yayında **10** tekne (toplam 11), 7 aktif işletme, 11 bölge, 78 rezervasyon. Yani 340 "biraz yüksek" değil, **otuz kat**. Vault'taki veri göçü notu eski sistemden 35 tekne taşınacağını söylüyor — 340 onunla da uyuşmuyor. Seçenekler: **(a)** sayıyı hiç yazma ("Ege ve Akdeniz'de onaylı tekneler"), **(b)** gerçek sayıyı canlı yaz — `GET /api/search` zaten `totalCount` döndürüyor, ayrı uç gerekmez, **(c)** göç sonrası beklenen sayıyı yaz ve göçten önce yayına çıkma. Aynı soru blog için de geçerli: 7 yazı uydurma yazar adlarıyla duruyor ("Deniz Aksoy"), yayımlanacaklar mı yoksa bölüm kapansın mı → `W-38`. **Bir de dokunmadığım bir şey var:** ana sayfadaki tur kategorilerinde "₺750'den", "₺9.500'den" gibi başlangıç fiyatları duruyor. Tekne sayılarını sildim (250 tekne iddia ediyorlardı, 10 var) ama fiyatlara dokunmadım. **Ölçtüm:** `/api/search` katalogda en düşük **₺500** dönüyor (9 tekne: 500, 500, 750, 900, 900). Yani "₺750'den" yanlış değil ama veriden de türetilmiyor ve en düşük kaydın üstünde. Geliştirme verisiyle üretim ayrı olduğu için buradan kesin bir şey denemez — bunlar canlı sitedeki gerçek değerler mi? | **Ana sayfada üç uydurma tekne 404 veriyordu, düzeltildi** (`W-71`) — gerçek katalogdan geliyor. Üst şerit, yorum istatistiği, uygulama puanı ve bölge tekne sayıları da kaldırıldı. `brand.ts`'teki telefon/adres/TÜRSAB'a dokunulmadı, `W-06` ile sende. **`/about` düzeltildi:** "340+ tekne · 96.000 misafir yeri · 4,8/5 üzerinden 4.812 yorum · 8 bölge" kaldırıldı, yerine doğrulanabilir olan kondu (hizmet bölgesi, TÜRSAB belgesi, peşin tahsilat); aynı "340+" düzyazıda da geçiyordu, o da çıktı. Ana sayfa kategorilerinden tekne sayıları çıkarıldı. Blogda **yalnız kontrol edilebilir yanlış** düzeltildi: "Tümü · 48" yazıyordu, 7 yazı var — sayaç artık listeden hesaplanıyor. "Haftada iki yazı" yayın sıklığı sözü kaldırıldı. Yazıların kendisine ve yazar adlarına dokunulmadı |
| S-26 | **İş ortağı sayfasındaki sayısal vaatler ne olacak?** `/add-boat` herkese açık ve işletmeciye verilen taahhüdü taşıyordu: "%12 komisyon", "3 gün ödeme", "ayda 120 bin arama", "onay ortalama 2 iş günü" ve üç isimli kaptan görüşü. Hiçbirinin karşılığı yok — komisyon ve periyot **sözleşme başına** (`Contract.CommissionRate`, `PayoutPeriodDays`, varsayılan 14 gün), canlı veride hepsi %15, para bugün zaten elle aktarılıyor. Seçenekler: **(a)** rakam hiç verme, "sözleşmende yazar" de (bugünkü hâli), **(b)** bir taban oran ilan et ("%12'den başlayan") ve sözleşmede farklılaştır, **(c)** gerçek ortalama oranı yaz. Görüşler için: izinli gerçek işletmeci görüşü verecek misin, yoksa bölüm kapalı mı kalsın? Onay süresi için ölçülen bir hedef var mı? | Yanlış rakamlar kaldırıldı, yerine doğru olduğu ölçülebilen ifade kondu ("Sözleşmene özel", "Sözleşmendeki periyotta"). Görüş bölümü **boşken hiç basılmıyor**. Geri almanın maliyeti sıfır: rakamlar `src/lib/data/owner.ts` içinde tek yerde, karar gelince yazılır. `340+ tekne` bu kapsamda değil, `brand.ts` ile `W-06`'da |
| S-28 ✅ | **CEVAPLANDI 2026-08-31** — Mert: "ayarlar ucunu da yaz, sadece işletmenin değiştirebileceği alanlar." Yazılabilir beş alan: `displayName, email, phone, address, city`. IBAN kendi doğrulama akışını bekliyor, panelde yalnız son dört hane. Özgün soru: **İşletme kendi ayarlarında neyi değiştirebilsin?** "Ayarlar & profil" ekranı bugün form basmıyor çünkü profili okuyan/yazan uç yok ve hangi alanların işletmeye açık olduğu belli değil. Kesin olan: komisyon ve ödeme periyodu **işletmenin yetkisinde değil** (`Contract.CommissionRate`, `PayoutPeriodDays` — personel belirliyor). Tartışmalı olanlar: işletme tanıtım metni, ana liman, iletişim telefonu/e-postası, bildirim tercihleri. **IBAN ayrı bir soru:** evrak kontrolünden geçmesi gerektiği için panelden doğrudan değişmemeli — talep akışı mı olsun, yoksa hiç mi görünmesin? Seçenekler: **(a)** yalnız tanıtım metni ve iletişim açılsın, gerisi destek talebiyle, **(b)** tanıtım + iletişim + bildirim tercihleri açılsın, **(c)** hiçbiri açılmasın, tüm değişiklik destek üzerinden. | Ekran form yerine durumu yazıyor: hangi bilginin nerede tutulduğunu ve IBAN için ne yapılacağını söylüyor. Uydurma IBAN ve vergi numarası kaldırıldı. Backend ayarlar yazma ucunu bu karar gelmeden yazmayacağını bildirdi |

## 🟡 Karara bağlanmamış — web

| Konu | Durum | Not |
|---|---|---|
| Gövde satır yüksekliği | Tasarımdan farklı | `globals.css` gövdeye 26px sabit veriyor, tasarım `normal` kullanıyor. Açık `leading-` verilmeyen küçük metinler şişiyor. Tek tek düzeltiliyor; global değişiklik 19 sayfayı birden etkileyeceği için yapılmadı |
| Gerçek görseller | Yok | Her yerde gradyan yer tutucu (`Placeholder`). Tasarımda da öyleydi ama yayın için gerçek fotoğraf şart |
| `brand.ts` kurumsal verileri | Yer tutucu | Telefon, e-posta, adres, TÜRSAB no tasarımdan geldi. Yayın öncesi doğrulanmalı |
| `/design-system` rotası | Yayına çıkıyor | Bileşen vitrini; geliştirme sayfası olduğu hâlde derlemede statik rota olarak üretiliyor. Yayın öncesi kaldırılmalı veya korunmalı → [[web-mimari]] |
| Frontend↔API sözleşmesi | Yok | OpenAPI üretiliyor ama istemci tarafında tip üretimi yok → `A-07` (API panosunda, web değil) |
| E-posta şablonları gerçek istemcide | Denenmedi | Tarayıcıda `/design-system/emails` üzerinden görüldü; Gmail, Outlook, Apple Mail'de gerçek gönderimle **doğrulanmadı**. Sağlayıcı seçilince test gönderimi şart |
| İptal e-postasındaki iade oranı | Bilinmiyor | Şablonda `RefundFormatted` ve `RefundDays` var ama müşteri kaynaklı iptalde iade oranı kararlaşmadı → API'nin `S-12` sorusu. Cevap gelmeden iptal e-postası gönderilmemeli |
| `Button` yükleme durumu | Yok | Çift gönderim mümkün; Mert kapsam dışı bıraktı |

## ⚠️ Hata değil — bilinçli davranış

Bunlar rapor edilirse "bug" sanılmasın:

- **1180px üstünde geniş tablolar kartın dışına taşar.** Tasarım da böyle yapıyor;
  sütun genişlikleri tasarımla birebir aynı, dolayısıyla taşma miktarı da aynı.
  Kaydırma kabı yalnızca dar ekranda devrede (`wide:overflow-x-visible`)
  → [[web-kararlar]]
- **Hesabım sayfası tasarımdan 18px uzun.** "Daily Cruising puanı" istatistik
  kartında iki satıra sarıyor, tasarımdaki "Rıhtım puanı" tek satır. Marka adı
  uzunluğunun sonucu → [[web-olcum-yanlis-pozitifleri]]

## 🟢 Doğrulanmış

- `npm run build` başarılı, `npm run lint` temiz
- Mobil kırılım 19 rotada 390px'te tarandı, yatay taşma yok; 834px'te iki kart.
  Ölçüm **Playwright** ile yapıldı — `chrome-devtools` `resize_page` 390'a inemiyor
  → [[web-tasarimi-tarayicida-acmak]]
- Modal: 560px ortalı, perde `rgba(0,0,0,.5)`, kaydırma kilidi 15px telafiyle
  sıçramasız, ESC kapatıyor, odak çağırana dönüyor. 390px'te alttan çıkan sayfa
- Toast: en fazla 3, hata `role="alert"` diğerleri `role="status"`
- 404 gerçekten HTTP 404 dönüyor; baskı kuralları seçici bazında doğrulandı
- **Düzeltilen hata:** `rounded-circle` ölü sınıftı — `--r-circle` `:root`'ta
  vardı ama `@theme inline`'a bağlanmamıştı, `border-radius: 0` üretiyordu.
  Build, lint ve tip denetimi üçü de temiz geçti
  → [[web-baglanmamis-token-tuzagi]]

İlgili: [[durum]] · [[web-gorevler]] · [[web-kararlar]] · [[web-desenler]] · [[web-araclar]] · [[web-notlar]]

## ⚠️ 2026-08-28 — paylaşılan dosya silmesi bir görseli götürdü

Backend'in bulduğu hata (`SHA256` içerik anahtarı yüzünden aynı dosyayı
paylaşan iki kaydın birinde silme, diğerinin dosyasını da siliyordu)
geliştirme verisinde **gerçek bir kaybı** yaptı: `tohum-fiyatli-1787869006`
teknesinin ikinci galeri görseli 404 döner hale geldi.

Sabah aynı test görselini iki kez yüklemiştim (biri doğrudan, biri vekilden);
içerikleri aynı olduğu için tek dosyayı paylaşıyorlardı. Birini silince
diğeri bozuldu.

**Öksüz satır panelden silindi**, kapak sağlam. Bugün bütün galeriler
tarandı: kalan görsellerin hepsi **200** dönüyor.

`BoatImage`'ın `onError` yer tutucusu bu durumda kırık simge yerine gradyan
bastı — yani kullanıcı hiç kırık görsel görmedi.

## 🔴 2026-08-28 — ödeme sonrası ekran tamamen mock veriydi

**Müşteri parayı ödüyor ve kendisine ait olmayan bir rezervasyon görüyordu.**
`/booking/success` sabit veriden okuyordu: kod `RH-84213`, tekne "Gulet Işıl",
tutar `₺6.525`, e-posta `zeynep@example.com`. Biniş belgesi (`voucher`) de
aynı sabit veriyi basıyordu.

Sonucu somut: müşteri yazdığı kodla iskeleye gitse **ne QR okunurdu ne kod
tutardı**. Ayrıca ekranda "kalkış hatırlatması telefonuna gönderildi"
yazıyordu — **SMS bildirimi diye bir şey hiç yok.**

**Düzeltildi:** kod ödeme dönüşünden (`?code=`) geliyor, üye kullanıcıda
rezervasyon çekiliyor, misafirde yalnız **gerçek kod** basılıp sorgulama
sayfasına yönlendiriliyor. Kodsuz gelinirse "ödeme akışının dışından
gelinmiş" deniyor — sabit bir "başarılı" ekranı, ödeme yapmamış birine
ödeme yapmış izlenimi verirdi.

Kanıt: `?code=RPAJWZCH` → `A04 Teknesi · 3 Eylül 2026 09:00 · 4 yetişkin ·
₺3.600`. Eski mock dizelerinin beşi de sayfada **0 kez**.

**Misafir tarafı da kapandı** (2026-08-28, aynı gün): geri çağrı rezervasyon
özetini döndürmeye başladı, özet ödeme dönüşünden başarı ekranına taşınıyor.

**Uçtan uca tıklama zinciri doğrulandı** (ilk denemede kendi test isteklerim
hız sınırını tüketmişti; backend API'yi yeniden başlattı): misafir olarak
rezervasyon → ödeme sayfasında **"Ödemeyi onayla"** tıklandı → `/booking/success`
açıldı ve `Tohum Fiyatlı · 21 Kasım 2026 09:00 · 2 yetişkin, 1 çocuk ·
₺2.300` gösterdi. Sunucuda `Paid · 2300`. **Sayfa yenilendi, özet durdu.**
Konsol temiz, 390px'te taşma 0.

Kurcalanmış kayıt (depodaki kod adresle uyuşmuyor) **yok sayılıyor**, ekran
koda düşüyor.

**Biniş belgesi de düzeltildi** (aynı gün). İki kusuru vardı:

1. **Aynı sabit veriyi basıyordu** — üstelik bu belge **yazdırılıp iskeleye
   götürülüyor**. Kağıda basılmış yanlış bilgi ekrandakinden zor fark
   edilir; müşteri ona güvenerek yola çıkar.
2. 🔴 **Misafir belgesini hiç açamıyordu.** Yol `/account/...` altındaydı ve
   `/account` korunan bir önek: misafir giriş sayfasına düşüyordu. Yani
   misafir rezervasyonu domainde birinci sınıf senaryo sayılırken, o
   müşterinin biniş belgesine erişimi **yoktu**.

Yol `/reservations/{kod}/voucher`'a taşındı. Belge zaten hesaba değil
**koda** bağlı; üye kaydı uçtan, misafir kaydı tarayıcıdan çözülüyor ve
sayfa sunucudan başkasının kaydını çekmiyor.

Kanıt: `/reservations/MC5GU38F/voucher` girişsiz açılıyor ve
`Tohum Fiyatlı · 21 Kasım 2026 09:00 · 2 yetişkin, 1 çocuk · ₺2.300`
basıyor. Eski mock dizelerinin üçü de **yok**. Geri bağlantısı misafirde
sorgulamaya, üyede rezervasyon detayına gidiyor.

⚠️ QR yer tutucusunun metni de düzeltildi: "rezervasyon onaylanınca burada
görünür" yazıyordu — rezervasyon **zaten onaylı**, müşteriye beklemesi
gereken bir şey olduğunu söylüyordu. Artık "QR henüz hazır değil — kaptana
aşağıdaki kodu söyle".

## 🔴 2026-09-05 — sözleşme akışı tek yönlü test edilmişti

`W-85`'te sözleşme gönderme, okuma, onaylama ve reddetme yazıldı ve **işletme
tarafı** uçtan uca ölçüldü. Platform tarafının aynı olayı nasıl gördüğü
ölçülmedi. Mert testte buldu: reddettikten sonra platform panelinde reddin
**hiçbir izi yoktu**, tablo "Sözleşme gönderildi" diyordu.

Uç suçsuzdu — `contractStatus` alanını zaten döndürüyordu ve elle yazılan tipte
de duruyordu (`PlatformPartner.contractStatus`). **Ekran onu hiç okumamıştı.**

Ders: karşılıklı bir akışta her iki tarafın ekranı **ayrı ayrı** ölçülür. Bir
taraf doğruyken diğeri yalan söyleyebiliyor ve tek yönlü test bunu görmüyor.
→ [[web-kararlar]] 2026-09-05

✅ **Yarısı aynı gün kapandı:** backend platform yanıtına `rejectedAt` ve
`rejectionReason` ekledi, sözleşme listesi ikisini de basıyor. Pazarlık döngüsü
uçtan uca çalışıyor: işletme reddediyor, platform gerekçeyi okuyor, düzeltilmiş
sözleşme gönderiyor ve rozet kendiliğinden kalkıyor → `W-86`

Aynı gün yerleşim de düzeltildi: yat işletmeleri tablosu kabından 510px
taşıyordu, sütunlar oransal yapıldı ve yönetim paneli 1440px kaba alındı.
1440 ve 1280'de yatay taşma 0. `982ee73`

## 🟡 2026-09-06 — tekne yönetimi altı ekran yazıldı, hiçbiri doğrulanmadı

Mert canlı paneli (`dailycruising.com.tr/admin/tekne-yonetimi`) gösterdi:
*"tekne ekleye bak, teknelerin listelenmesine bak, sonrasında fiyat özellik
rota menü resimler ve detay kısmına bak … buna göre bizim tekne ekle
kısımlarını yapmanı istiyorum."* Dipnotu: **tekne sahibi seçimi yalnız
platform panelinde**.

Altı ekran yazıldı ve `build`/`lint`/`tsc` temiz: liste (`c829c26`), tekne
ekle (`5497725`), düzenle · detay · belgeler (`df1a74f`), fiyat · resimler
(`60cadfb`). Backend dört uç ailesini `40e59ff` ile açtı.

⚠️ **Hiçbiri personel hesabıyla açılmadı.** Yereldeki tarayıcı oturumu Mert'in
müşteri hesabı (`my_mert07@hotmail.com`), `/admin` doğru şekilde 403 veriyor.
Parolayı ben yazmıyorum. Doğrulanacak iki şey var ve ikincisi daha ağır:

1. `PanelKabuk` refaktörü **işletme panelindeki beş modalı** bozmuş olabilir.
2. Her yazma **uçtan geri okunarak** ölçülmeli — toast kanıt değil; bu
   oturumda "kaydedildi" yazıp hiçbir şey kaydetmeyen iki ekran çıktı.

Yol boyunca ölçülen iki kusur düzeltildi: `/admin/tekneler` **yoktu** (arama
ve sayfalama 404 veriyordu), ve `boat-media` sınırı 20 iken sunucununki 24 —
ekran, sunucunun kabul edeceği dört görseli reddediyordu → [[web-kararlar]]

## ✅ 2026-09-06 — gün aralığı açığı kapandı

Kiralama tipinde `MinNights`/`MaxNights` **yoktu**; tek sınır 365 gecelik genel
tavandı. *"3 günlük"* ilan edilen tarife `nights: 1` ile üçte bir fiyata
alınabiliyordu ve **korumanın tek dayanağı bizim ekranımızın `nights`
göndermemesiydi** — istemci hatası değil, sözleşme boşluğu.

Mert onayladı, backend bağlayıcı yaptı (`e1e6c12`). Fiyat hesabı aralığı
uyguluyor ve hata mesajı sayıyı söylüyor. Formda alan var (yalnız çok günlü
tipte), müşteri sayfasında rozet olarak görünüyor (`fe33940`).

⚠️ **Aralık tanımlı değilse denetim yok** — var olan tiplerin hiçbirinde
değer yok ve zorunlu saymak bugün satılan turları satılamaz hâle getirirdi.
Boş bırakılması hata değil.

## 🟡 2026-09-06 — dalışçı kontenjanı kaydediliyor ama uygulanmıyor

`diverCapacity` / `nonDiverCapacity` tipe eklendi, panelde giriliyor, müşteri
ucundan dönüyor — **ama hiçbir yerde uygulanmıyor.** Rezervasyon
dalışçı/refakatçi ayrımı taşımıyor; yalnız yetişkin/çocuk/bebek sayısı var.

Müşteri sayfasında **gösterilmedi**: rozet şeridi "bu tekne şunu garanti
ediyor" diye okunuyor ve uygulanmayan bir kontenjanı oraya yazmak olmayan bir
söz vermek olurdu. Panelde alan var ve yanında uygulanmadığı yazılı.

**Mert kararını 2026-09-06'da iki kez verdi ve ikincisi geçerli.** Önce
*"bilgi olarak gösterilsin"*, sonra backend oturumuna *"rezervasyon formunu da
değiştir, dalışçı sayısı sorulsun"* — yani **bağlayıcı**. İkinci karar bana
aktarıldığında inşaya başlamadım; aktarılan cümle onay sayılmıyor, Mert'e
doğrudan sordum ve *"Evet, bağlayıcı olsun"* dedi. Bağlandı (`3c8b844`).

⚠️ Kontenjan **seferin tamamı** için geçerli, istek başına değil: teklif `200`
dönse bile rezervasyon `409` dönebilir. Arayüz ikisini ayırıyor — `400` formu
düzeltmek, `409` başka tarih seçmek.

İlk karar (aşağıda) tarih olarak duruyor: Tekne sayfasında
"Dalış kontenjanı" bölümü, tarife başına satır, altında *"Bu sayılar işletmenin
beyanıdır. Rezervasyon sırasında dalışçı sayısı sorulmuyor, bu yüzden yerinizi
işletmeyle teyit edin."* Uygulanmadığı bilgisi **cümlenin kendisinde** taşınıyor
(`fe33940` · sonraki commit).

⚠️ Rozet şeridine **konmadı ve konmayacak**: şerit müşteri tarafından bir vaat
gibi okunuyor. Aynı cümle rozet olarak yazılsaydı, kelimeler değişmeden anlamı
değişirdi — *bulunduğu yer* bilgiyi güvenceye çeviriyor.

Ayrıca Mert kataloğa `supportsDivers` bayrağı eklenmesini onayladı; kapsam
bugünkü iki tip (`dalis-turu`, `ozel-dalis-turu`), şnorkel/yüzme **dahil değil**.
Backend yazacak; gelince formdaki dört kutu ona bağlanacak. O güne kadar alanlar
her tipte görünüyor — yanlış gizlemektense fazladan göstermek geri alınabilir.

## 🟡 2026-09-06 — işletme kendi belgesini panelden yükleyemiyor

`POST /api/partner/documents` **var**, ekranı **yok**. İşletme panelinde
belgeler yalnız okunuyor (`isletmeBelgeleri`, eylem sütunu "Görüntüle").
Yani bir işletme ruhsatını ya da vergi levhasını platforma panelden
gönderemiyor; **tekne** belgeleri için yükleme var, **işletmenin kendi**
belgeleri için yok.

Bu bugün ortaya çıktı çünkü `document-uploads.tsx` silindi: sahte dosya
adlarıyla ("elverislilik-2026.pdf") bir belge listesi ve tıklanamayan bir
`<span>` basan, **hiçbir yerden çağrılmayan** bir bileşendi. Başlığında
*"dosya alma servisi yok"* yazıyordu ve bu cümle artık yanlıştı. Ölü mock
gittiği için altındaki gerçek boşluk göründü.

⚠️ Ders: **ölü mock, kapattığı boşluğu da gizler.** Dosya orada durduğu
sürece "belge yükleme yapılmış" görünüyordu.

`limits.partnerDocumentMaxBytes` uçta hazır (`0864abc`) ve tipte duruyor;
ekran yazıldığında sayı elle yazılmayacak.

## 🔴 2026-09-06 — profil kaydı TÜRSAB numarasını siliyordu

Backend `PUT`'un **tam değiştirme** olduğunu sözleşmeye yazınca (`b681aee`)
bütün `PUT` gövdelerini şemalarına karşı ölçtüm: on bir şema, ikisi yanlış
alarm, **biri gerçek**.

İşletme profili formu **6 alan** gönderiyordu, şema **7** tanıyor.
`tursabNumber` hiç gitmiyordu → her kaydetmede `null`. Ardından
`PartnerProfileService.UpdateAsync` doğrulama damgasını da düşürüyor.
Yani **işletme telefonunu düzeltince TÜRSAB numarasını ve doğrulamasını
kaybediyordu**; damgayı yalnız platform personeli geri verebiliyor ve
`partner-card.tsx` müşteriye giden güven satırını o damgaya bağlıyor.

⚠️ **Kökü ikinci bir alan listesiydi.** `formDegerleri` aynı kümeyi elle
tekrar sayıyordu; biri güncellenip diğeri unutuldu. Okuma, yazma ve render
artık tek listeye bakıyor (`25f9197`).

⚠️ **Bu kusuru hiçbir kapı yakalamıyordu ve yakalayamazdı**: `Disallow`
kilidi *fazla* alanı reddediyor, **eksik** alanı değil. Eksik alan geçerli
bir istek — "o alanı boşalt" demek. Sözleşme yazılana kadar ikimizin de
gördüğü şey aynıydı: `204`, toast "güncellendi", ve sessizce giden bir veri.

Ölçüm salt okunurdu; yazma tarafı hâlâ personel/işletme hesabıyla
doğrulanmadı.

## ✅ 2026-09-09 — personel, roller ve parola akışı

Panelde **15 modül uca bağlı**, 9'u statik. Bugün eklenenler: personel
listesi + ayrıntı + etkinlik geçmişi, personel ekleme/düzenleme, **Roller ve
yetkiler** modülü (oluşturma · düzenleme · silme · kişiye özel rol), ve
parola akışı.

### 🔴 Parola ekranı **maketti** — akışı kopartıyordu

`/account/password` gönderim kodu taşımıyordu, alanda `defaultValue="parola12"`
gömülüydü ve kural metni uydurmaydı ("10 karakter, bir büyük harf, bir
rakam"; gerçek kural **8, karmaşıklık şartı yok**).

Kusur "ilk girişte parola değiştirme" isteğiyle görünür oldu: backend kapıyı
yazdı (bayrak açıkken her uç `403`) ama **çıkış yolu yoktu** — yönetici
tarafından açılan personel giriş yapıp hiçbir şey gönderemiyordu.

⚠️ Aynı ekranda **uydurma giriş geçmişi** vardı ("Bodrum · iPhone · 18 Ağu").
Bir **güvenlik ekranında** uydurma veri, kullanıcıya hesabına başka şehirden
girildiğini düşündürür. Kaldırıldı; uçta giriş geçmişi yok.

### Kilitlenme kapıları **uçta**, ekranda değil

`CannotModifySelf` · `LastAdmin` · `SystemRoleImmutable` · `RoleInUse`.
Ekranda denetim yazılmadı: iki gerçek olur ve `curl` ile atlanırdı. Ekranın
işi kodu okunur cümleye çevirmek → [[web-kararlar]]

⚠️ Bir rolün yetkisini almak, o rolü taşıyan **herkesin** yetkisini alıyor ve
hepsinin oturumu düşüyor. Ekran kaç kişiyi etkilediğini **denemeden önce**
yazıyor.

### Ölçüm

`41 rota · 132 bileşen · 12 API istemcisi` · `tsc` · `lint` · `build` temiz.

⚠️ **Panel hâlâ tarayıcıda gezilmedi** (giriş parolası Mert'te). Bugünkü
kusurların tamamı ölçümle ya da backend oturumunun ekran raporlarıyla
bulundu — gözle bulunacaklara hiç sıra gelmedi.

## 🟡 2026-09-07 — yönetim panelinde sekiz kusur, hiçbiri gözle değil ölçümle çıktı

Panel gün boyu gerçek veriye bağlandı. **Bulunan kusurların tamamı ölçümden
çıktı; hiçbiri "ekrana bakınca" görülmedi** — ve panel hâlâ **tarayıcıda hiç
gezilmedi** (giriş parolası Mert'te).

| Kusur | Nasıl çıktı |
|---|---|
| Destek sekmesi `Answered`/`other` ham basıyordu | veri gelince |
| `TEKNE_DURUMU` `Inactive`'i kaçırıyordu, üç kopyadan biri ayrışmıştı | `satisfies` kapısı |
| `SATIS_MODU` `Exclusive` diyordu, değer `ExclusiveOpen` | `satisfies` kapısı |
| `KUPON_RED_METNI` `NotYours` taşımıyordu (**müşteri ödeme akışı**) | `satisfies` kapısı |
| Listelenen kuponda ölü "Kişiye ata" düğmesi | demo veri çeşitlenince |
| Ek hizmetler bölümü boşken gizleniyordu | Mert ekrana baktı |
| Rezervasyon ayrıntısına giden yol yoktu | Mert kodu aradı, bulamadı |
| "183 uç" sayısı yanlıştı, doğrusu 129 | peer ölçtü |

**Ortak sınıf ve günün ana dersi:** *boş ya da tek çeşit veri, kusuru
gizler.* Destek talepleri 0'dı, ek hizmetler boştu, dört kuponun dördü de
listeliydi, biletlerin hepsi jetonsuzdu. Her biri veri çeşitlendiği an
kusurunu gösterdi.

⚠️ İkinci sınıf: **aracın ne ölçtüğünü sormadan sayısına güvenmek.** Üreteç
"183/184" basıyordu ve hata şemalarını sayıyordu; doğru sayı 129. Aynı
oturumda `grep -c` (satır sayar, eşleşme değil) ve backend'in
`n_live_tup`'ı (bayat olabiliyor) da aynı aileden çıktı.

## ✅ 2026-09-07 — sözleşme zinciri üç halkalı, üçü de otomatik

```
enum/sayı → belge : backend testi (e0c53ac, 30eb60b)
belge     → tip   : npm run build → tip-uret --kontrol (5c04112)
tip       → sözlük: satisfies Record<Enum, string> (7d49d26)
```

Kapı ilk iki gününde **üç kez** gerçekten durdurdu. Boşluk bir derleme
kadar; tamamen kapatmak her derlemede kardeş repoyu okumak olurdu.

Belgede artık **29 enum değerleriyle** ve **sıfır `number|string` birleşimi**
var; ikisi de gün içinde ölçülüp bildirildi ve backend düzeltti
→ [[web-enum-uretilemez]] · [[web-gorevler]] W-92

## 🔴 2026-09-07 — biniş jetonu artık saklanıyor (güvenlik dengesi değişti)

Panelde karekod gösterilebilsin diye jeton **saklanmaya başladı**; eskiden
yalnız SHA-256 özeti duruyordu. Mert riski açıkça yazılmış hâliyle seçti
→ [[web-kararlar]] 2026-09-07.

Backend AES-GCM ile şifreli saklıyor, anahtar veritabanı dışında, görüntüleme
olay günlüğüne yazılıyor. **"Hiç saklamamak kadar güvenli değil"** — iki ayrı
sırrın birden sızmasını gerektiriyor, o kadar. Yayın öncesi anahtar yönetimi
konuşulmalı → [[yayin-oncesi]]


## 🔴 2026-09-06 — veritabanı sıfırlandı, tek hesap kaldı

Mert uçtan uca test için `dailycruising_dev`'i sıfırlattı: 70 kullanıcı,
31 işletme, 23 tekne, 157 rezervasyon silindi. Duran tek şey referans
katalogu (bölge, tekne tipi, kiralama tipi, olanak, kural, vergi oranı,
yorum ölçütü) — hepsi migration'lardan geliyor.

**Tek hesap:** `admin@dailycruising.test` (platform.admin). İşletme yok,
tekne yok, sözleşme şablonu bile yok.

⚠️ **Ekranlardaki her ölçüm bu tarihten önceyse geçersiz.** "23 tekne
listeleniyor", "31 işletme" gibi kanıtlar artık boş listeye bakıyor.

### Sözleşme şablonu ekranı — sistemi açan parça

Şablon **yaratan uç yoktu**; metin yalnız SQL ile yazılabiliyordu. Sıfır
veritabanında platform hiçbir işletmeye sözleşme gönderemiyor, tekne eklemek
onaylı sözleşmeye bağlı olduğu için **sistem baştan tıkalıydı**. Uçlar
`bb29101` ile geldi, ekran `de0f2ce` ile yazıldı ve yönetim panelindeki
"Sözleşme listesi" modülünün yerine geçti.

⚠️ `bodyHtml` **ham ve sunucuda temizlenmiyor**. `dangerouslySetInnerHTML`
kullanılmadı; `<iframe sandbox="">` deseni (`contract-viewer`,
`contract-accept`) aynen uygulandı. *"Metni personel yazıyor"* bir yalıtım
değil — aynı HTML işletmenin ekranında da basılıyor.

⚠️ `isActive` her `PUT`'ta açıkça gönderiliyor: alanın sunucudaki varsayılanı
`true` ve `PUT` tam değiştirme, yani pasif bir şablonu düzenlerken alanı
atlamak onu **sessizce geri açardı** → [[web-desenler]]

### Düzeltilen bir vault kaydı

Daha önce buraya *"`contract.send` platform-destek rolünde de var"* diye
yazılmıştı. Backend ölçümünü düzeltti: o ölçüm **demo verisindenmiş**, temiz
kurulumda `platform-destek` diye bir rol yok. Yetki ayrımının kendisi doğru,
gerekçesi yanlıştı.

---

## 2026-09-10 — Roller modülü, personel tablosu, rezervasyon süzgeci

Yönetim panelinde bugün yazılanlar (commit sırası):

| Commit | Ne |
|---|---|
| `75f2c2f` · `d63d733` | Rol ayrıntısı ekranı + o rolü taşıyan personel |
| `f7f49bb` · `7e257b3` | Enum sözlüklerini `satisfies` ile koruma + `araclar/sozluk-denetle.py` |
| `f795068` | Rol ayrıntısı modal yerine **sayfa**, sistem rollerinde kırmızı "Zorunlu" |
| `5ddc75a` | Personel tablosu `staff-table.tsx`'e çıktı; iki ekran aynı tabloyu basıyor |
| `9364f81` | Rol satırında **kalem ve çöp kutusu** — rolleri değiştir / bu rolü kaldır |
| `2e52d8b` | Rezervasyon süzgeç şeridi tek ızgara + yedi duruma ayrı renk |

### Dosya bölünmeleri

`role-form.tsx` (yeni) ← `YetkiSecici` · `RolOlustur` · `personelHatasi`;
`staff-table.tsx` (yeni) ← `PersonelTablosu` · `RolDuzenle` · satır işlemleri.
Graf tek yönlü: `role-form ← staff-table ← {staff, roles}`. Sebep ve ölçüt
→ [[web-desenler]], [[web-kararlar]]

### Ölçülen ve kapatılan borç

- Aynı hata çevirisinin **üç kopyası** tek kapıya indi (`personelHatasi`).
- `kit.tsx`'in sekiz sabit hex satırı belirtece çevrildi: *"bileşende sabit
  renk kodu"* borcu **87 → 79**, `vault.json` tavanı indirildi.
- `AdminIslem` birliğinde varsayılan düşüş kapatıldı (`admin-panel-view.tsx`):
  yeni bir çeşit sessizce *"İşletmeyi onayla"* düğmesi basıyor olurdu.

### Back-end'den bu turda gelenler

- `rentalTypeId` süzgeci (`GET /api/platform/reservations`) — bağlandı.
  `PlatformReservationItem` artık `rentalTypeId` de taşıyor.
- ⚠️ **Tur türü adları İngilizce dönüyordu** ("Day cruise"); dört sorgu çeviri
  tablosunu dil süzgeci olmadan okuyordu. Uçta düzeltildi (back-end `440648e`).
  Dört ekranı birden etkiliyordu: genel bakış tur dağılımı · müşteri kartı
  rezervasyonları · rezervasyon ayrıntısı · rezervasyon listesi. Ön yüzde
  kiralama tipi sözlüğü **yok** (ölçüldü), adlar uçtan geliyor; `GET /api/lookups`
  canlıda Türkçe dönüyor (8 kayıt, ölçüldü) — yani dördü de düzeldi.

### ⚠️ Kapanmayan boşluk

**Bugün yazılan yazma yollarının hiçbiri tarayıcıda denenmedi**: personel
ekleme, rol oluşturma/düzenleme/silme, rol kaldırma, askıya alma, ilk girişte
parola değiştirme. Parolayı Claude girmiyor; tur Mert'te.

## 2026-09-10 — İptal ve iadeler: müşterinin gerekçesi (commit `91f14ae`)

Mert iade ekranındaki "Gerekçe" kutusunu müşterinin beyanı sanıyordu; içindeki
değer `RefundReason` — **platformun muhasebe gerekçesi**. Müşterinin kendi
sebebi hiçbir ekranda yoktu, şemada da yoktu → [[web-kararlar]]

Back-end aynı gün ekledi (`b07da48`): `CancellationReason` +
`CancellationNote`, `reason` iptal ucunda **zorunlu**, `Other` için `note`
zorunlu; ikisi de hem serviste hem veritabanı kısıtında.

| Ekran | Ne oldu |
|---|---|
| İade modalı | Müşterinin gerekçesi **en üstte ayrı kutuda**; ayrıntı ucundan okunuyor (liste satırı taşımıyor) |
| İade modalı | Platform kutusu *"İade gerekçesi · platform kaydı"* etiketini aldı |
| Rezervasyon ayrıntısı | `IptalKarti` — yalnız `cancelledAt` dolu kayıtta |
| Müşterinin iptal ekranı | Onay penceresi forma dönüştü: zorunlu sebep + açıklama |

### 🔴 Ekran **kırıktı** ve hiçbir araç söylemedi

`openapi.json`'da `reason` nullable, `CancelReservationRequest.required` dizisi
`None` — zorunluluk yalnız C# kodunda. Üretilen tip alanı opsiyonel gösterdiği
için `tsc` · `lint` · `build` üçü de temiz geçiyordu ve
`account/cancel-reservation.tsx` gerekçesiz istek atıyordu; uç hepsini
reddediyordu. Tek çağıran `grep` ile bulundu.

⚠️ Mobil oturuma (`dailycruising-mobil-fb`) haber verildi — back-end o oturuma
ulaşamıyor.

### Ölçülen veri durumu (dev veritabanı)

53 rezervasyon · **1 iptal** (`BYQSN37K`) · **0 gerekçeli**. Yani ekranın bugün
göstereceği şey *"Gerekçe yok."* dalı — alan bir günlük ve geçmiş kayıtlara
uydurma gerekçe yazılmadı.

### 🟡 Uzun açıklama 400 değil **500** döndürüyor (back-end'e bildirildi)

`CancellationNote` kolonu `varchar(500)` ama sınır denetimi **hiçbir
katmanda yok**: istekte `[MaxLength]` yok, serviste uzunluk kontrolü yok.
501 karakter → Postgres 22001 → `DbUpdateException` → iptal ucunun `catch`'i
yalnız `ReservationException` yakalıyor → genel işleyici → `500 "Beklenmeyen
bir hata oluştu."`

⚠️ Diğer iki kural (gerekçe zorunlu · Other'da açıklama zorunlu) kullanıcıya
**ne yapacağını söyleyen** 400 veriyor; bu üçüncüsü vermiyor ve doğru eylem
(kısaltmak) hiç önerilmiyor.

Ön yüzde **iki katman** var: `maxLength={500}` yazmayı/yapıştırmayı
engelliyor, gönderirken `trim().slice(0, 500)` kesiyor. İkincisi tek başına
`maxLength`'e güvenilmediği için değil, **hata hâlinin 400 olmaması** için
var.

### Gerekçe listesi sessizce büyümüyor

Değer veritabanında Postgres enum değil, `varchar(32)` metin — **ama**
`CK_Reservations_CancellationReason_Enum` altı değeri tek tek listeliyor
(migration `20260910175534_A115_IptalGerekcesi`). Yeni değer = C# enum üyesi
**+ migration**, yani kazara eklenmiyor.

⚠️ Buna rağmen `IPTAL_SEBEBI[ham] ?? ham` kuralı duruyor: sözlük `satisfies`
ile üretilen enum'a bağlı olduğu için web derleme zamanında uyarılır, ama
ayrı dağıtılan bir istemci (mobil) eski sürümde kalıp yeni değeri bilmeyebilir.

## 2026-09-10 — Tutar süzgeci (commit `9e4c0f9`)

Uç geldi (back-end `547c014`: `minTotal`/`maxTotal`) ve **iki listeye birden**
bağlandı — rezervasyonlar ve iptal/iadeler aynı ucu okuyor; birinde olup
diğerinde olmayan süzgeç kusur gibi okunur.

`TutarAraligi` + `tersMi` + `tutarSorgusu` **kit'e** kondu: iki çağıran var,
ikinci kopya yazılmadan ortaklaştırıldı.

⚠️ Süzgeç **`grandTotalTry`** üzerinde, `totalTry` üzerinde değil — tabloda
basılan sayı o. Tur bedeline bakılsaydı ek hizmetli bir rezervasyon kendi
tutarıyla aranınca bulunamazdı (satırda 1.100 TL yazarken "1.000 üstü"
süzgecinde görünmezdi). Back-end testi de ek hizmetli kayıtla kurulmuş; ek
hizmetsiz veride iki yanlış kod aynı sonucu verir.

⚠️ **Ters aralıkta istek hiç atılmıyor.** Uç `400 InvalidRange` döndürüyor ama
kullanıcı alt sınırı yazıp üst sınıra geçerken aralık bir an ters kalıyor; o
anın hatası ekrana kırmızı kutu basardı. İki alan birden düşüyor (birini
göndermek, görünmeyen bir süzgeç uygulamak olurdu) ve sebebi ekranda yazıyor.

⚠️ Kutular **400ms geciktirilmiş**: "3000" dört tuş, her tuşta istek atılsaydı
üçü boşa giderdi ve ara değerlerin sonucu ekranda parlayıp geçerdi.

### 🔴 Kendi ölçümüm yanlıştı: çöken betiğin çıktısını "alan yok" diye okudum

Back-end'e *"`openapi.json` bayat, `minTotal`/`maxTotal` dosyada yok"* diye
bildirdim. **Yanlıştı.** Parametreler dosyada vardı, üreteç onları görmüştü ve
üretilmiş tipe yazmıştı — kanıt benim kendi commit'imin içinde duruyordu
(`9e4c0f9`, `uretilen.ts:11665` `minTotal?: null | number`).

Sebep: parametreleri listelemek için yazdığım tek kullanımlık Python betiği
`format` çağrısında **`TypeError` ile çöktü** ve çökmeden önce yalnız ilk yedi
parametreyi bastı. Çöktüğü parametre tam olarak aradığım olandı: `minTotal`'in
şema tipi `['null','number']`, yani bir **liste**, ve biçimlendirici listeyi
kabul etmiyordu.

⚠️ **Yarım çıktıyı tam liste sandım.** Traceback ekrandaydı; "yedi parametre
göründü, sonrakiler yok" diye okudum. Bu, aynı gün iki kez yazdığım kusurun
üçüncü örneği ve bu kez kurbanı bendim:

| Nerede | Ne oldu |
|---|---|
| Müsaitlik ekranı | Sekiz takvim hatası `catch → []` ile yutuldu, ekran *"0 kapatma"* yazdı |
| İade ekranı | Gerekçe okunamazsa boş görünürdü → üç hâl üç cümleye ayrıldı |
| **Bu ölçüm** | Betik çöktü, yarım liste **tam liste** sayıldı |

**Kural:** *ölçüm betiği de bir veri yoludur ve hata hâli tasarlanmalıdır.*
Çöken bir betiğin çıktısı olgu değildir. Tek kullanımlık betikte bile ya
`try/except` ile "ölçüm başarısız" yazılmalı, ya da çıktı **sayıyla**
doğrulanmalı ("12 parametre bekleniyordu, 7 basıldı").

### Yanındaki tespit yine de doğruydu ve gerçek bir boşluk kapattı

Örnek yanlıştı ama yapısal iddia doğru: **`tip-uret --kontrol` bayat bir
kaynağı yakalayamaz.** Ürettiği tipi diskteki tiple karşılaştırıyor, ikisi de
aynı `openapi.json`'dan geliyor; bayat kaynak kendisiyle tutarlı bir çıktı
üretir ve karşılaştırma her zaman geçer. **Bir kapı kaynağı değil, kaynağın
iki kopyasını karşılaştırıyorsa hiçbir şey ölçmüyordur.**

Back-end bunu kendi tarafında ölçtü: yedi OpenAPI denetiminin **hiçbiri sorgu
parametrelerine bakmıyordu**. Sekizinci denetimi yazdı (`fe81262`) ve **kör
testle** doğruladı — belgeyi bir önceki commit'e çekti, yeni denetim eksik iki
parametreyi adıyla söyledi, diğer yedisi yeşil kaldı.

⚠️ Bizim tarafta bu boşluk **hâlâ açık**: ön yüzde belgeyi üreten taraf yok,
o yüzden kapı eklenecek yer de yok. Koruma artık back-end'in sekizinci
denetiminde — yani ön yüz, belgeyi back-end'in üretmesine **güveniyor** ve bu
bilinçli.

### Back-end'in ikinci bulgusu: türetilen metin de sınıra tabi

500 karakter hatası düzeltildi (artık `400` + *"Açıklama en çok 500 karakter
olabilir."*). Düzeltirken **ikinci** bir taşma çıktı: tam 500 karakterlik
geçerli bir açıklama, durum geçmişi cümlesine etiketle birlikte yazılınca o
`varchar(500)` kolonu taşırıyordu — yani sınırı geçen hiçbir şey olmadan taşma
üretiliyordu ve ön yüzdeki `slice(0, 500)` bile bu isteği patlatırdı.

⚠️ Kural (back-end'in çıkardığı, bizde de geçerli): **bir alanın uzunluk
sınırı, o alandan türetilen her metnin de sınırını belirler.** Kısaltma
**kopyada** yapılır, kaynakta değil — hangisinin veri hangisinin gösterim
olduğu ayrımı.

## 2026-09-10 — Tarayıcı testi: bir kusur çıktı (`e9a4b54`)

Mert giriş yaptı, dört ekran denendi. Üçü doğru çalıştı, biri kusurluydu.

| Ne | Sonuç |
|---|---|
| İade modalı — müşterinin gerekçesi | ✅ *"Gerekçe yok."* + sebebini açıklayan cümle; platform kutusu ayrı etiketle |
| Rezervasyon ayrıntısı — İptal kartı | 🔴 **"UYGULANAN İADE ORANI: %10000"** |
| Tutar süzgeci (rezervasyonlar) | ✅ 53 kayıt → `en az 3000` → **41 kayıt**; back-end ölçümüyle birebir |
| Ters aralık | ✅ Uyarı basıldı, liste 53'e döndü, hata kutusu yok, istek atılmadı |

### 🔴 Oran ölçeği: `%10000`

Oranı **kesirli** sanıp `× 100` yapmıştım. Ölçüldü: `RefundPolicy.For`
doğrudan `100m · 50m · 0m` döndürüyor ve `RefundService.cs:79` aynı kaydı
(`CancellationRefundRate`) iade yanıtının `rate` alanına koyuyor — yani
**ikisi de 0–100 ölçeğinde**, kesirli değil.

⚠️ Hata **iki** yerdeydi ve ikincisi ekrandan görülemezdi: iade **başarıyla
bittikten sonra** basılan bildirimde (`"${tutar} · oran %${rate * 100}"`).
Gerçek bir para hareketi olmadan tetiklenmiyor, yani ancak canlı bir iadede
ortaya çıkardı — ve o an personel ekranda **%5000** görürdü.

Biçim `format.ts → iadeOrani`'ye alındı: ölçek bir bilgidir ve iki çağıran
varken üçüncü dosyaya çıkarılmazsa biri sessizce ayrışır.

### Ders: tip kontrolü ölçek hatasını göremez

`number` her iki ölçekte de `number`. `tsc` · `lint` · `build` üçü de temizdi
ve ekran **bir sayı** basıyordu — boş değil, yanlış. Bu kusuru yakalayan tek
şey gerçek veriyle **ekrana bakmak** oldu; `%100` beklenen yerde `%10000`
görmek.

⚠️ Aynı sınıf 2026-09-07'de de ölçülmüştü: *"sekiz kusurun hiçbiri gözle
değil ölçümle çıktı"*. Bunun tersi: **ölçümle değil gözle çıktı.** İkisi
birbirinin yerine geçmiyor.

## 2026-09-11 — Tarih değiştirme: üç yolun ikisi doğrulandı

Mert: *"müşteri bir rezervasyon yapmıştır ama sonrasında bir değişikliğe
ihtiyaç duyduğunda buradan da müdahale edebilmemiz gerekiyor."* Seçenekleri
maliyetiyle sorup **tarih/sefer değiştirme** ve **fark için ödeme bağlantısı**
kararlarını aldı → [[web-kararlar]]

Ekran **rezervasyon ayrıntısında**, "Rezervasyon ayarları"nda değil: ayarlar
platform geneli kurallar, müdahale tek kaydın kendisine ait ve ayrıntı ekranı
üç listeden birden açılıyor.

### Tarayıcıda doğrulananlar (`a88da8e`)

| Ne | Sonuç |
|---|---|
| Pencere | `11 Mart – 8 Haziran 2027 · 89 uygun gün` — rezervasyonun etrafına oturuyor, mevcut gün düşüyor |
| Önizleme (`action: None`) | `₺4.350 → ₺4.350 · Tutar değişmiyor · Boş koltuk 12` |
| Kapalı onay | Düğmenin yerinde *"Taşıma ucu henüz hazır değil"* satırı |

### 🔴 İki kimlik karıştırıldı: `rentalTypeId` ≠ `boatRentalTypeId`

Gün seçici ilk denemede `400 BoatNotFound` aldı. Ayrıntı **katalog** tur
türünün kimliğini (`RentalTypes.Id`) döndürüyordu; müsaitlik ucu teknenin o
türü **satan kaydının** kimliğini (`BoatRentalTypes.Id`) istiyor
(`AvailabilityRepository:65`). Back-end ayrıntıya ikincisini de ekledi
(`02cbaeb`); ilki kalıyor, çünkü rezervasyon listesi süzgeci onu kullanıyor.

⚠️ Parametreyi hiç göndermemek de çalışıyordu — uç boşta teknenin tek türüne
düşüyor ve bugün **sekiz teknenin hiçbirinin ikinci türü yok**. Reddedildi:
bir tekne ikinci tür sattığı gün **yanlış ürünün** takvimi gösterilir ve kimse
fark etmez. *Veri bugün tek çeşit diye kod varsayım yapmaz.*

### 🔴 Sabit pencere, uzak rezervasyonda işe yaramıyordu

Seçici "yarından itibaren 90 gün" gösteriyordu. Test verisi hazırlanırken
ölçüldü: taşımaya uygun **altı kaydın hepsi 2027 Mart–Nisan'da**, yani
pencerenin altı ay ötesinde — personel müşterinin istediği tarihleri
**hiç göremezdi** ve seçici çalışıyor görünüp işe yaramazdı. Artık mevcut
kalkış pencerenin dışındaysa pencere onun iki hafta öncesinden başlıyor,
ayrıca ileri/geri geziliyor (uç bir seferde en çok 92 gün veriyor).

### Uçtan uca doğrulananlar (tarayıcı + veritabanı)

| Yol | Sonuç |
|---|---|
| `None` (tutar aynı) | ✅ Taşındı, bildirim ve zaman tüneli doğru, geri alındı |
| `Refund` (tutar düşüyor) | ✅ Taşındı `₺4.350 → ₺2.700`, iade kaydı açıldı, **iş koştu**, defter yazdı |
| `Collect` (tutar artıyor) | ⏳ Önizleme doğrulandı; onay **kapalı** (tahsilat altyapısı yok) |
| Biniş jetonu | ✅ İleri taşımada `BoardingTokenExpiresAt` yeni turla birlikte gitti |

**Defter — kararın kanıtı burada**, ekranda değil:

```
Customer | Refund |  1650.00      net:  Customer  -2700.00
Partner  | Refund | -1402.50            Partner    2295.00
Platform | Refund |  -247.50            Platform    405.00
TOPLAM   |            0.00              TOPLAM        0.00
```

⚠️ `Platform = 405` tek başına Mert'in **orantılı bölüştürme** kararının
kanıtı: komisyon eski tutarın değil **yeni tutarın** %15'i. "Tamamı
işletmeden düşsün" seçilseydi platform 652,50'de kalırdı.

### Bu turda yakalanan beş kusur — hiçbirini derleyici görmedi

| # | Kusur | Nasıl çıktı |
|---|---|---|
| 1 | `rentalTypeId` ≠ `boatRentalTypeId` → `400 BoatNotFound` | Ekranda "Tekne bulunamadı" |
| 2 | Sabit 90 günlük pencere, 6 ay sonraki rezervasyonda işe yaramıyor | Test verisi hazırlanırken |
| 3 | Biniş jetonunun geçerliliği taşınmıyor (back-end) | Kartta iki çelişen tarih |
| 4 | İade işi iade kayıtlarını görmüyor (back-end) | Back-end ölçümü |
| 5 | İade oluyor, **defter yazmıyor** (back-end) | Back-end ölçümü |

Bende olan iki tanesi (1 ve 2) ve bir de bildirimde **eksi işaretli iade
tutarı** (`−₺1.650 iade kaydı açıldı`) — üçü de `tsc` · `lint` · `build`
üçlüsünden temiz geçiyordu.

### 🟡 Para hareketi doğuran yollar bayrakla yönetiliyor

`IADE_YOLU_HAZIR = true` · `TAHSILAT_HAZIR = false`. Bayrak **ikiye
bölündü**, çünkü kapalı olma sebepleri farklıydı ve tek bayrak ikisini
birden açardı.

⚠️ İade yolu bir süre kapatıldı: defter yazmıyordu. Back-end bana *"tekrar
koşma"* demişti ama **Mert paneli kendi kurcalıyor** — *"basılmamalı"* ile
*"basılamıyor"* aynı şey değil. Düğmeyi kodda kapatmak, sözlü uyarıdan
farklı bir korumadır.

### Geliştirmede iş tetikleme (`bb2dfb3`)

İade işi 15 dakikada bir koşuyor; para yolunu doğrulamak her turda o kadar
bekleme demekti. Back-end `POST /api/dev/jobs/{ad}/run` açtı.

⚠️ **Vekilin izin listesi yine engel oldu** — `dev` listede yoktu, istek
backend'e hiç ulaşmıyordu. Bu tuzağa bu projede **dördüncü** düşüş; bu sefer
"neden 404" diye aranmadan önce ölçüldü.

Önek **kalıcı listeye konmadı**: üretimde boş kalan ayrı bir liste
(`NODE_ENV === "production" ? [] : ["dev"]`). Kalıcı listeye koymak,
unutmanın tersi bir hata üretirdi — üretimde niyet edilmemiş bir yol. Backend
de aynı uçları üretimde `404` veriyor; iki taraf bağımsız kapatıyor.

### Bekleyen

- **Fark tahsilatı** (back-end): kısmi `Payment` · jetonlu bağlantı · dönüşün
  farkı işlemesi · taşımanın tamamlanması. Gelince `TAHSILAT_HAZIR` açılıp
  `Collect` koşulacak.
- **Ayrıntı yükü**: bekleyen talep şeridi · iade listesi · `RefundStatus` ve
  talep durumu enum'ları. Ölçüldü (2026-09-11): üçü de şemada **henüz yok**,
  yani o ekranlar bugün yazılamıyor.

⚠️ **Bekleyen taşıma hiçbir yerde görünmüyor** ve şerit gelene kadar öyle
kalacak: fark ödenene kadar rezervasyon `Paid` ve eski tarihinde duruyor.
İkinci bir personel aynı kaydı başka tarihe taşımaya kalkabilir ya da iptal
edebilirken müşteri farkı ödüyor olabilir. Mert kararı verdi: **iptal
kazanır**, bağlantı iptal anında geçersiz olur, ödenmişse fark iade edilir.

### ⚠️ Kapanmayan boşluk

- ✅ **Tarayıcıda denendi** (Mert giriş yaptı): iade modalı · İptal kartı ·
  tutar süzgeci · ters aralık. Bir kusur çıktı ve düzeltildi (`e9a4b54`).
- **Gerekçesi dolu dal hiç görülemez**: dev veritabanında gerekçeli tek kayıt
  yok ve ilki ancak bir müşteri iptal edince doğacak.
- **Misafir rezervasyonu arayüzden iptal edilemiyor**: `CancelReservation`
  yalnız `/account/reservations/[code]`'da basılıyor, misafir kaydı o listede
  yok. Dev veritabanındaki iptal edilebilir 28 kaydın **tamamı misafir**.

## 2026-09-11 gecesi — Yolcu gönder: telefonla rezervasyon açma

Menü girişi *"Yolcu gönder"* ama modülün işi başka: **telefonda anlaşılan
müşteri için personelin kayıt açması**. Sahil Güvenlik yolcu listesi bu
kaydın bir çıktısı, modülün kendisi değil — bu ayrım 2026-09-06'da bir kez
yapılmıştı, ekran o gün yine de statik kalmıştı.

**Bağlandı** (`b91c9d6`):

| Uç | Ne için |
|---|---|
| `POST platform/reservations` | Kaydı `AwaitingCollection` ile açar |
| `POST pricing/quote` | **Kayıt açılmadan önce** fiyat |
| `GET platform/reservations?channel=phone` | Liste, sunucu tarafı sayfalama |
| `GET platform/partners/{id}/boats/{id}/rental-types` | Tur tipi kutusu |

⚠️ **Fiyat önce soruluyor ve teklif gelmeden düğme açılmıyor.** Telefondaki
soru sırası bu: müşteri "ne kadar" diye soruyor, duyduktan sonra "tamam"
diyor. Fiyatı ancak kayıt açarak öğrenen bir ekran personeli önce açıp
sonra iptal etmeye zorlardı — her vazgeçen müşteri için bir hayalet
rezervasyon ve dolu görünen bir koltuk → [[web-kararlar]]

⚠️ **Tutar kutusu yok, indirim yalnız kuponla.** Elle yazılan tutar,
işletmenin hakedişini haberi olmadan azaltabilecek ikinci bir yol olurdu;
komisyon o tutardan hesaplanıyor. Kuponun arkasında kim tanımladı, kime
tanımlı, kaç kez kullanıldı var — elle yazılan sayının arkasında hiçbir şey.

⚠️ **Çok günlü tarifede gece sayısı soruluyor** (`durationKind: MultiDay`),
gün içi turda hiç gönderilmiyor. Bunun bir bedeli var ve bilerek kabul
edildi: `minNights`/`maxNights` bugün **bütün tiplerde boş**, yani üç günlük
ilan edilen tarife `nights: 1` ile üçte bir fiyata alınabiliyor ve tek
koruma müşteri ekranımızın `nights` göndermemesiydi. Artık personel ekranı
da gönderiyor; sormasaydık çok günlü tur telefonla hiç satılamazdı.

⚠️ **Bu bulguyu back-end'e yanlış bildirdim ve düzeltildi.** *"Sunucuda
denetim yok"* demiştim; `PricingService` kontrolü **yapıyor** (satır 218,
224). Eksik olan kod değil **veri** — sekiz satış biçiminin hiçbirinde
sınır dolu değil. Ders yine aynı: *"alan boş"* ile *"kural yok"* farklı
şeyler ve ikincisini iddia etmeden önce kodun kendisine bakmam
gerekiyordu → [[web-desenler]]

⚠️ **Dalışçı kutusunun kapısı `supportsDivers`**, `diverCapacity` değil:
kontenjanı sınırsız olan dalış turunda kapasite `null` gelir ve o tur,
dalış yapılmayan turdan ayırt edilemez.

**Silinen örnek veri:** `ORNEK_TELEFON_SUTUNLARI` · `ORNEK_TELEFON_REZERVASYONLARI`.
Bu, statik verinin gerçek sanıldığı sınıftan **beşinci** temizlik.

### Bekleyen — tahsilat dilimi

Back-end'e iletildi: `POST /{id}/collect` (elle tahsil işaretleme, yöntem
burada seçiliyor — açılışta değil), `POST /{id}/payment-link` (ödeme
bağlantılı SMS/e-posta), detaya `collection` · `paymentLinkSentAt` ·
`channel`. Modül bu yüzden `admin-durum.ts`'de `statik` değil **`kismi`**.

Cevabı beklenen tek soru: tutma süresi dolunca kayıt düşüyor mu, yoksa
`AwaitingCollection`'da mı kalıyor — ekranda "süresi doldu" hâlini basmak
için hangi durumu okuyacağım belli değil.

⚠️ **Tarayıcıda doğrulanmadı.** `build` · `lint` · `tsc` temiz ama ekran
personel hesabıyla açılmadı: yereldeki oturum Mert'in müşteri hesabı ve
parolayı ben yazmıyorum. Sabah doğrulanacak.

## 2026-09-11 gecesi — Örnek veri dosyası **silindi**

`src/lib/data/admin-ornek.ts` artık yok. Bu oturumda yönetim panelinin
kalan bütün uydurma verisi kaldırıldı ve dosyayı hiçbir yer okumaz hâle
gelince silindi.

⚠️ **Kaldırma ile doldurma ayrı iki iş ve ikisi de yapıldı.** Bazı
modüllerde gerçek uç zaten vardı ve ekran onu kullanmıyordu; bazılarında
uç hiç yok ve ekran artık *"yok"* diyor. Karıştırılırsa yanlış yere iş
yazılır.

| Modül | Ne oldu |
|---|---|
| Bölge yönetimi | `lookups.regions` + `platform/boats` → **gerçek**. Uydurma tur/ciro sütunları silindi |
| Reklam yönetimi | Uydurma kampanya, sayaç ve performans grafiği silindi. Kapsam `S-01` ile daraltıldı |
| Aktivite kayıtları | `platform/staff/{id}/activity` → **gerçek**. Liste ortak dosyaya taşındı |
| Log kayıtları | Uydurma istek satırları ve **uydurma JSON ödeme gövdesi** silindi |
| E-posta · SMS · SMS gönderimleri | Uydurma şablon, oran ve sağlayıcı ayarı silindi |
| Finans | `platform/overview` → ciro, komisyon, ortalama sepet, aylık eğri **gerçek** |
| Sözleşme listesi | İmzalanmış işletme sözleşmeleri bölümü eklendi (gerçek) |
| Yolcu gönder | Form + liste + **elle tahsilat** bağlandı |

### İki kez aynı ders: eksik notları da çürüyor

⚠️ **`activity.tsx`** *"openapi.json'da activity kelimesi hiç geçmiyor"*
yazıyordu — uç vardı ve personel detayında **zaten kullanılıyordu**.
⚠️ **`finance.tsx`** platform geneli uç yok diyordu — `overview` ciroyu ve
komisyonu zaten döndürüyordu.

İkisini de uçları yeniden ölçünce gördüm, okuyunca değil. Kendi yazdığım
*"uç yok"* notu, yazıldığı gün doğru olsa bile **tetikleyicisi olmadan
bayatlıyor** ve bayat bir eksik notu, olmayan bir işi duyurup var olan
veriyi gizliyor → [[genel-desenler]]

Bunun araç karşılığı var: `admin-durum.ts` bugün elle yazılıyor ve
`openapi.json`'a karşı denetlenmiyor. Bir betik, `uc:` alanındaki yolların
gerçekten var olduğunu **ve** `eksik:` metninde adı geçen yolların
gerçekten yok olduğunu ölçebilir. Vault oturumuna öneriliyor.

### Kopya yerine ortak parça

- `components/panel/admin/activity-log.tsx` — etkinlik listesi + olay
  ayrıntısı; personel detayı ve aktivite modülü paylaşıyor.
- `kit.tsx: BeklenenUclar` — "back-end'den beklenen" kutusu; **beş** modül.
- `kit.tsx: egri` — aylık eğri kurucusu; genel bakış ve finans.

### Bekleyen

- Ödeme bağlantısı (`POST /{code}/payment-link`) back-end'de sırada.
- Spec geçilenler: genel aktivite akışı · istek günlüğü · belge onay/red
  kuyruğu · platform finans · bildirim şablonları · reklam · referans
  kataloğu yazma. Hepsi `src-d9`'a tek mesajda iletildi.

⚠️ **Bu gece yazılan hiçbir ekran tarayıcıda açılmadı.** `build` · `lint`
· `tsc` · sözlük denetimi temiz ama personel girişi Mert'te; parolayı ben
yazmıyorum. Sabah doğrulanacaklar: tahsilat formu (`VZZC9JG8` bekliyor,
`3S2G3T3K` form için duruyor) · telefon listesi süzgeci · bölge tablosu ·
aktivite seçicisi · finans sayaçları.

## 2026-09-11 gecesi — Telefonla rezervasyon **uçtan uca** bitti

Ödeme bağlantısı geldi (`aae6ba4`) ve bağlandı (`4cf7550`). Modül artık tam:

1. Personel formu doldurur → kayıt `AwaitingCollection` açılır.
2. Parayı elden alırsa **tahsilatı işaretler** → kayıt `Paid` olur.
3. Almazsa **ödeme bağlantısı gönderir** (e-posta · SMS · ikisi) →
   müşteri `/odeme?jeton=…` sayfasından öder.
4. Süre dolarsa kayıt **`Expired`** olur (`ExpireReservationHoldsJob`).

⚠️ **`Confirmed` diye bir durum yok** ve eklenmedi (back-end kararı):
para geldiyse rezervasyon ödenmiştir, elden mi sağlayıcıdan mı geldiği
`Payment` kaydının bilgisi. Ayrı bir durum *"ödenmiş mi"* sorusunu iki
değere bölüp onu okuyan her yeri ikisini birden saymak zorunda bırakırdı.
Ekranda "elden tahsil edildi" bilgisi `collection` alanından basılıyor.

⚠️ **Bağlantının ömrü `holdExpiresAt` ile birebir aynı.** Uzun olsaydı
müşteri ödeyip koltuk bulamazdı. Tekrar gönderim serbest ve **aynı
jetonu** taşıyor: yeni jeton ilk mesajı açmış müşteriyi kilitlerdi.

⚠️ Ayrıntı ucu `paymentLinkSentAt` **döndürmüyor**, yani gönderim bilgisi
sayfa yenilenince kayboluyor. Eksik olarak yazıldı.

## Yokluk iddiası artık denetleniyor

`ModulKaynagi`'ye **`istenen: {yol, ne}[]`** eklendi ve on iki modülde
dolu. `araclar/durum-denetle.py` üç şey ölçüyor:

1. `uc:` içindeki her yol şemada **var mı**,
2. `istenen` içindeki her yol şemada **yok mu** — uç geldiği gün kırmızı,
3. `statik` modülde `uc:` dolu **olmasın**.

⚠️ **İlk sürüm `eksik:` düzyazısını tarıyordu ve atıldı:** dört bulgunun
üçü yanlış pozitifti, çünkü düzyazı var olan bir ucun **sınırını**
anlatmak için de ondan söz ediyor (*"/api/lookups yalnız aktif bölgeleri
döndürüyor"* bir yokluk iddiası değil). İddia makine-okunur olmadan
denetlenemiyor → [[genel-desenler]]

⚠️ Aynı liste **ekranda** da basılıyor: `BeklenenUclar` artık `slug`
alıyor ve `MODUL_DURUMU`'dan okuyor. Personelin *"bu modül neden boş"*
sorusuna verilen cevap, denetlenen cevabın kendisi.

Bozma senaryoları koşturuldu: var olan ucu `istenen`'e yazmak ve olmayan
yolu `uc:`'a yazmak, ikisi de `IHLAL=1` üretti; geri alınca `IHLAL=0`.

## `belirtec-denetle.py` yazıldı, dört ihlal kapandı

`border-success-line` ve `text-success-deep` tanımlı değildi; dört üretim
dosyasında yeşil rozetlerin kenarlığı ve yazı rengi **basılmıyordu**
(`5242ab3`). Tanımlı belirteç sayısı 40, ihlal 0.

⚠️ Ölçüt bir kez daraltıldı: geniş tarama 175 satır üretti ve 171'i
yanlış pozitifti (`border-b`, `divide-y`, `shadow-e3`). Gerçek dördünün
içinde kaybolduğu bir liste, listesizlikten kötü.

## Sabah yapılacak — tarayıcı doğrulaması

Mert giriş yapınca, sırayla:

| Ne | Nasıl |
|---|---|
| Tahsilat formu | `VZZC9JG8` → "tahsil edildi işaretle" → kayıt görünümü + `Paid` |
| Ödeme bağlantısı | `3S2G3T3K` → e-posta + SMS gönder → Mailpit ve `NotificationOutbox` |
| `/odeme` sayfası | Bağlantıdaki jetonla aç, tutarı ve süreyi doğrula |
| Telefon listesi | `?channel=phone` iki kaydı getiriyor mu |
| Bölge tablosu | On bölge, tekne sayıları 1/1/1/1/1/1/1/1/0/0 |
| Aktivite | Personel seçici + tür süzgeci + olay ayrıntısı |
| Finans | Sayaçlar ve aylık eğri, dönem değişince |

⚠️ Para hareketi doğuran adım yalnız **tahsilat işaretleme**; gözetimsiz
yapılmadı ve Mert başındayken yapılacak.

## Tarayıcı doğrulama defteri

> **Bu bölüm makine-okunur.** Her satır `tarayıcıda doğrulandı: <ekran> · <tarih>`
> ya da `tarayıcıda doğrulanmadı: <ekran> · <sebep>` biçiminde.
>
> ⚠️ **Neden gerekli:** `build`, `lint`, `tsc` ve ölçüm betikleri bir ekranın
> **derlendiğini** söylüyor, **göründüğünü** söylemiyor. Bu oturumda derlemesi
> temiz olup ekranda hiçbir şey yapmayan üç kusur çıktı: uydurma fatura,
> gönderilmeyen iptal gerekçesi ve basılmayan rozet kenarlığı. Üçünü de
> yakalayan şey tarayıcıydı.
>
> ⚠️ *"Yazıldı"* ile *"görüldü"* arasındaki farkı yalnız bu defter taşıyor.
> Ayrı tutulmazsa ikisi aynı kelimeye çöküyor ve panoda tamamlanmış görünen
> bir görev, hiç açılmamış bir ekran oluyor.
>
> ⚠️ **Dosya yolu zorunlu ve kaydın ölçülebilir olmasının tek şartı.**
> Kontrol 28 o dosyanın son değişiklik tarihini doğrulama tarihiyle
> karşılaştırıyor: dosya sonra değiştiyse doğrulama **o hâli görmemiştir**
> ve kayıt kırmızı yanar. Yol yazılmazsa kontrol tahmin etmiyor — ekran
> adından dosya çıkarmak yanlış kırmızı üretirdi — **sayıyor ve
> bildiriyor**, yani ölçülemeyen kayıt sessizce temiz görünmüyor.
>
> ⚠️ **Çapa gün değil commit.** İlk sürümde tarih karşılaştırılıyordu ve
> kör noktası **kalıcıydı**: aynı gün doğrulanıp aynı gün değişen bir ekran
> iki eşit tarih üretiyor, yarın da eşit kalıyor — yani o değişiklik
> *hiçbir zaman* görünmüyordu. **Gün belirsizdir, commit değildir.**
>
> Çapa, doğrulama anında `HEAD`'de olan commit. Ölçüt: *o commit'ten bu
> yana bu dosyaya dokunuldu mu*.
>
> ⚠️ Dört kaydın dördü de bugün **kırmızı yanacak ve yanması doğru.**
> Doğrulama `9e4c0f9` üzerindeyken yapıldı ve çıkan kusurun düzeltmesi
> (`e9a4b54`) **o doğrulamadan doğdu** — yani görülen hâl, düzeltilmiş hâl
> değil. Üstüne bu gece tahsilat kartı ve ödeme bağlantısı da eklendi.
> Müşteri iptal ekranı `1ac13a3`'e çapalı: üye rezervasyonuyla denendiğinde
> `HEAD` oradaydı ve iki kusur (misafir olarak açılan rezervasyon, uydurma
> fatura) o denemeden çıktı.
>
> ⚠️ **Çapalar bilerek erken seçildi.** Emin olunmayan durumda daha eski
> commit yazmak kaydı kırmızıya, daha yenisini yazmak yeşile götürür;
> yanlış yeşil sessizdir, yanlış kırmızı bakılır. Belirsizlik ölçümün
> lehine çözülüyor.
>
> ⚠️ Bir satır diğerlerinden farklı: `/odeme` sayfası **giriş meselesi
> değil akış meselesi**. Personel girişi geldiğinde on sekiz kayıt
> kapanacak, o bir tane kapanmayacak — jeton yalnız gerçek bir gönderimle
> üretiliyor. Sebebi ayrı yazmak, kapanmayanın neden kapanmadığını
> görünür tutuyor.

tarayıcıda doğrulandı: yolcu gönder · 2026-09-11 · src/components/panel/admin/phone-booking.tsx · 8586b59
tarayıcıda doğrulandı: tahsilat kartı ve ödeme bağlantısı · 2026-09-11 · src/components/panel/admin/reservation-detail.tsx · 8586b59
tarayıcıda doğrulandı: iptal kartı · 2026-09-11 · src/components/panel/admin/reservation-detail.tsx · 8586b59
tarayıcıda doğrulandı: /odeme müşteri ödeme sayfası · 2026-09-11 · src/app/odeme/page.tsx · 8586b59
tarayıcıda doğrulandı: sözleşme listesi · 2026-09-11 · src/components/panel/admin/contracts.tsx · ccb8730
tarayıcıda doğrulandı: bölge yönetimi · 2026-09-11 · src/components/panel/admin/regions.tsx · c1e22c6
tarayıcıda doğrulandı: finans · 2026-09-12 · src/components/panel/admin/finance.tsx · 0fd5356
tarayıcıda doğrulandı: aktivite kayıtları · 2026-09-11 · src/components/panel/admin/activity.tsx · ccb8730
tarayıcıda doğrulandı: etkinlik listesi · 2026-09-11 · src/components/panel/admin/activity-log.tsx · ccb8730
tarayıcıda doğrulandı: reklam yönetimi · 2026-09-11 · src/components/panel/admin/adverts.tsx · c1e22c6
tarayıcıda doğrulandı: log kayıtları · 2026-09-12 · src/components/panel/admin/logs.tsx · d0bb7aa
tarayıcıda doğrulandı: e-posta yönetimi · 2026-09-11 · src/components/panel/admin/email.tsx · ccb8730
tarayıcıda doğrulandı: sms yönetimi · 2026-09-11 · src/components/panel/admin/sms.tsx · c1e22c6
tarayıcıda doğrulandı: sms gönderimleri · 2026-09-11 · src/components/panel/admin/sms-log.tsx · c1e22c6
tarayıcıda doğrulandı: bildirim şablonları · 2026-09-11 · src/components/panel/admin/notification-templates.tsx · ccb8730
tarayıcıda doğrulandı: bildirim günlüğü · 2026-09-11 · src/components/panel/admin/notification-log.tsx · c1e22c6
tarayıcıda doğrulandı: belge kuyruğu · 2026-09-11 · src/components/panel/admin/document-queue.tsx · c1e22c6
tarayıcıda doğrulandı: rezervasyon ayarları · 2026-09-12 · src/components/panel/admin/reservation-settings.tsx · 0fd5356
tarayıcıda doğrulandı: iade modalı · 2026-09-11 · src/components/panel/admin/cancellations.tsx · 8586b59
tarayıcıda doğrulandı: iptal tutar süzgeci · 2026-09-11 · src/components/panel/admin/cancellations.tsx · 8586b59
tarayıcıda doğrulandı: müşteri iptal ekranı · 2026-09-11 · src/components/account/cancel-reservation.tsx · 1ac13a3


⚠️ **`/odeme` için kısmi kanıt var ama "doğrulandı" sayılmadı.** Sayfa
sunucuda basıldığı ve giriş istemediği için `curl` ile **üç** hâli okundu
(2026-09-11 gecesi):

| Hâl | Ekranda | Doğru mu |
|---|---|---|
| jetonsuz | *"Bağlantı eksik"* | ✓ |
| geçersiz jeton, **API kapalı** | *"Bağlantı okunamadı"* | ✓ |
| geçersiz jeton, **API açık** | *"Bu bağlantı tanınmadı"* | ✓ |
| ödenebilir | — | **görülmedi** |

⚠️ Son ikisinin **ayrı** çıkması bu ölçümün asıl değeri: sayfa *"tanınmayan
bağlantı"* (404) ile *"sunucuya ulaşılamadı"* hâllerini gerçekten ayırıyor.
Tek mesaj basan bir sayfa, sunucu çökükken müşteriye *"bağlantın sahte"*
derdi. İkisi ancak API'yi bir kapalı bir açık görerek ayrı ayrı ölçülebildi —
ve kapalı hâl kazayla oluştu, planlanmadı.

Ödenebilir hâl gerçek jeton gerektiriyor; o da personel girişi.

Bu satırın `tarayıcıda doğrulandı` olmamasının sebebi: sunucu çıktısını
okumak, ekranı görmek değil. Yerleşim, düğme ve tıklama yolu ölçülmedi.
Kanıtın **cinsini** karıştırmak, defterin taşıdığı tek bilgiyi bozar.
tarayıcıda doğrulanmadı: belge talepleri · personel girişi Mert'te · src/components/panel/admin/documents.tsx
tarayıcıda doğrulanmadı: kupon rozetleri · personel girişi Mert'te · src/components/panel/partner-coupons.tsx
tarayıcıda doğrulanmadı: blog rozetleri · personel girişi Mert'te · src/components/panel/blog-moderation.tsx
tarayıcıda doğrulanmadı: hesap kuponu rozetleri · personel girişi Mert'te · src/components/account/coupons.tsx

tarayıcıda doğrulandı: genel bakış · 2026-09-12 · src/components/panel/admin/overview.tsx · 0fd5356
tarayıcıda doğrulandı: müşteri listesi · 2026-09-12 · src/components/panel/admin/customers.tsx · 0fd5356
tarayıcıda doğrulandı: rezervasyonlar · 2026-09-12 · src/components/panel/admin/reservations.tsx · 0fd5356
tarayıcıda doğrulandı: müsaitlik yönetimi · 2026-09-12 · src/components/panel/admin/availability.tsx · 0fd5356
tarayıcıda doğrulandı: personel listesi · 2026-09-12 · src/components/panel/admin/staff.tsx · 0fd5356
tarayıcıda doğrulandı: rol yönetimi · 2026-09-12 · src/components/panel/admin/roles.tsx · 0fd5356
tarayıcıda doğrulandı: kupon yönetimi · 2026-09-12 · src/components/panel/admin/coupons.tsx · 0fd5356
tarayıcıda doğrulandı: iş sağlığı · 2026-09-12 · src/components/panel/job-health.tsx · 0fd5356
tarayıcıda doğrulandı: yat işletmeleri · 2026-09-12 · src/components/panel/admin-panel-view.tsx · 0fd5356
tarayıcıda doğrulandı: destek talepleri · 2026-09-12 · src/components/panel/admin-panel-view.tsx · 0fd5356
tarayıcıda doğrulandı: yorum yönetimi · 2026-09-12 · src/components/panel/admin-panel-view.tsx · 0fd5356
tarayıcıda doğrulandı: tekne yönetimi · 2026-09-12 · src/components/panel/admin-panel-view.tsx · 0fd5356
⚠️ **Son sekizi "doğrulandı" diye yazmadım ve yazmamak bilinçli.** Bu
ekranların bir kısmı önceki oturumlarda Mert giriş yapmışken açıldı, ama
**hangisinin hangi gün** açıldığının kaydı yok — defter bugün açıldı.
Tarihsiz bir "doğrulandı", kontrol 28'in karşılaştıracağı şeyi yok eder ve
kayıt sessizce temiz görünür. Bilinmeyeni bilinmeyen olarak yazmak,
uydurulmuş bir tarihten iyi.

⚠️ Dört modülün **kendi dosyası yok** ve bu bir eksik değil bir yapı:
`isletmeler`, `destek`, `yorum` ortak `ListeModulu` üzerinden basılıyor,
`tekneler` ise görünümün içinde satır içi JSX. Dördünün de ekranı
`admin-panel-view.tsx` ve defterde öyle yazılı.

⚠️ Betik bunları önce *"çözülemedi"* diye sayıyordu. Sayı doğruydu ama
**işe yaramıyordu**: dördü de ölçülebilir, yalnız kendi dosyaları yok.
*"Bilinmiyor"* ile *"başka yerde"* ayrı şeyler ve ilkine düşmek,
kapanabilecek bir boşluğu açık tutuyordu. Eşleşme yine **türetiliyor**:
satır içi olanlar görünümün kendisine, ortak listeden basılanlar
`admin-sayfa.ts`'teki `gercek: { … }` anahtarlarından — dördüncü bir
modül eklendiği gün kendiliğinden görünsün diye.

⚠️ **Parolayı ben yazmıyorum** — Mert bilgiyi verdiğinde bile. Giriş onun
elinden yapılıyor, doğrulama ondan sonra başlıyor. Bu bir araç kısıtı değil,
oturum boyunca tutulan bir kural.

## 2026-09-11 öğleden sonra — tarayıcı doğrulaması

Mert giriş yaptı, on üç ekran açıldı. **İki gerçek kusur çıktı, ikisi de
derleme ve üç denetim betiği temizken duruyordu** — defterin var olma
sebebi tam bu.

### Kusur 1 — bölge tablosu on bölgeyi de "0 tekne" gösterdi

Tarayıcıdan ölçtüm: çalışan API `regionId` alanını hiç döndürmüyordu,
süreç alanı ekleyen commit'ten eskiydi. Kod doğruydu, **sunucu eskiydi**.

⚠️ Asıl kusur bendeydi: bu kalkan **vardı** (hiçbir eşleşme yoksa sıfır
yerine `—`), kimliğe geçerken *"artık ayrışamaz"* diyerek kaldırdım.
Kimlik ayrışamaz ama **eksik olabilir** ve ekrandaki sonucu aynı: sessiz
sıfır. Geri kondu (`8586b59`).

**Kural:** kalkanın gerekçesini koruduğu **yönteme** değil ürettiği
**sessizliğe** bağla. Yöntem değişince kalkanı kaldırmak, yöntemi
kalkanın sebebi sanmaktır → [[web-desenler]]

### Kusur 2 — yoktu; şüphelendim, ölçtüm, yanılmışım

Tahsilat kaydında *"11 Eyl 17:06"* beklediğimden ileriydi. Uçtan okudum:
`collectedAtUtc` 14:06 UTC, tarayıcı saati 17:06 TR — çeviri doğru, saat
gerçekten 17:06. Bildirmeden önce ölçtüm.

### Uçtan uca doğrulanan akış

`VZZC9JG8` elden tahsil edildi (Mert onayıyla): form → kayıt görünümü
(yöntem · tutar · **tahsil eden** · zaman · not), durum **`Paid`**,
biniş belgesi **kendiliğinden üretildi** ve karekod göründü. Back-end'in
*"tahsilat gerçek bir `Payment` satırı açıyor"* iddiası doğrulandı.

`3S2G3T3K`'ya ödeme bağlantısı gönderildi (e-posta + SMS): ekranda
*"17.07'de gönderildi · 12 Eyl 07:49'a kadar geçerli"*, e-posta
Mailpit'te, jeton çıkarıldı ve `/odeme` sayfasının **ödenebilir hâli**
ilk kez görüldü — son geçerlilik saati panelle **birebir aynı**, yani
`expiresAt = holdExpiresAt` iddiası da doğrulandı. "Ödemeye geç"e
basılmadı; o onay alınmadı.

⚠️ **`NotificationOutbox` boş.** Bildirimler `Notifications` /
`NotificationDeliveries` tablolarından geçiyor; outbox artık
kullanılmıyor. SMS gönderimleri modülünün istediği uç buna göre
güncellenmeli — back-end'e iletildi.

## 2026-09-11 akşamı — gönderim günlüğü bağlandı (`S-09`)

Mert **(b) ayrı günlük** dedi, back-end aynı gün yazdı, bağlandı.

⚠️ **Ölü şema canlandı.** `Notifications` + `NotificationDeliveries`
zaten tasarlanmıştı ve hiç bağlanmamıştı — durum kümesi kuyruğunkinden
zengin (`Queued`/`Sent`/`Failed`/**`Bounced`**). Yani karar yeni bir şey
kurmadı, unutulmuş bir tasarımı uyandırdı.

⚠️ **Mesaj gövdesi saklanmıyor** ve saklanmayacak: kayıtta `TemplateKey`
ve `Payload` var, metin şablondan yeniden üretiliyor. Ekran *"gitti mi"*
sorusunu cevaplıyor, *"ne yazıyordu"* sorusunu değil. KVKK açısından
saklanan şey alıcı adresi ve değişkenler.

⚠️ **`Failed` yalnız deneme hakkı bitince** yazılıyor. Ekranda deneme
sayısı durumun yanında basılıyor, çünkü *"Sırada"* ile *"Sırada · 3
deneme"* farklı iki şey söylüyor ve personelin tek ipucu bu.

⚠️ **`Bounced` bugün hiç yazılmıyor** — sağlayıcı geri bildirimi
bağlanmadı. Sözlükte yine de var: gelmeyen bir değerin karşılığını
hazırlamak, geldiği gün ham İngilizce görünmesinden iyi.

Liste **ortak bileşen** (`notification-log.tsx`): tek uç, iki ekran.
`sms-gonderim` artık tam bağlı, `eposta` kısmi (şablon tarafı eksik ama
gönderim listesi gerçek).

### Doğrulama — yarım

Tarayıcıda açıldı: süzgeçler, boş durum metni ve sayfalama basılıyor.
Ama **veriyle görülmedi**: üç tablo da sıfır, çünkü günlük bağlandıktan
sonra hiç bildirim gönderilmedi (ödeme bağlantısı 17:07'de gitti,
bağlanma ondan sonra). "0 kayıt" bu yüzden **dürüst** — ölçüldü, uydurma
değil.

⚠️ Veriyle doğrulama için yeni bir gönderim gerekiyor ve o **dışarıya iş
yapan** bir eylem; Mert'in onayı bekleniyor.


## 2026-09-11 gece — on soru kapandı, iki karar tersine döndü

`SORULAR.md` **silindi**. On sorunun hepsi Mert'e soruldu, hepsi
cevaplandı ve kararlar [[web-kararlar]]'a taşındı. Dosyanın kendisi
geçiciydi; **geçici dosyada biriken karar, silindiği gün kaybolur** —
taşıma bu yüzden silmeden önce yapıldı.

⚠️ **İki cevap benim önerimin tersi çıktı** ve ikisi de ekranda yazılı
bir cümleyi yalanladı:

- `S-02` — iptal kademeleri **değiştirilebilir olacak**. Ekranda
  *"değiştirilmemeli"* yazıyordu ve bu benim gerekçemdi, Mert'in kararı
  değil. Cümle *"henüz değil"*e döndü; gerekçe ortadan kalkmadı,
  **sıraya** dönüştü (önce sürümleme, sonra yazma).
- `S-05` — şablonlar **düzenlenebilir olacak**. Aynı kalıp: üç yerde
  (`email.tsx`, `notification-templates.tsx`, `admin-durum.ts`)
  *"eksiklik değil karar"* yazıyordu.

**Ders:** kendi önerimi ekrana *karar* diliyle yazmışım. Öneri ile karar
aynı cümleyle yazılırsa, karar tersine döndüğünde ekran **eski öneriyi
savunmaya** devam eder. Artık ikisi ayrı yazılıyor: kararın sahibi
cümlede geçiyor.

⚠️ İki yeni uç `admin-durum.ts: istenen` alanına yazıldı ve **ekranda**
basılıyor (`BeklenenUclar`). Bu alan bir süredir boştu — beş modülün
hepsi bağlanınca kutu hiçbir yerde görünmüyordu; bileşenin *"aynı liste
ekranda da basılıyor"* notu o sırada **sessizce yalan**dı. Şimdi iki
modülde tekrar görünür: `rez-ayar` ve `eposta`.

### `S-04` — saklama süresi 24 ay

Ekranda **hiçbir yerde tavan yoktu**: `SORULAR.md`'de "en fazla 12 ay"
yazıyordu ama kodda karşılığı yoktu — tarih kutuları sınırsızdı. Yani
karar bir yere yazılmıştı, **ürüne hiç geçmemişti**.

Tavan artık `SAKLAMA_AYI = 24` sabitinde, tek yerde; iki ekranın dört
tarih kutusu ondan besleniyor. Tarayıcıda ölçüldü: `min=2024-09-11`,
`max=2026-09-11`.

⚠️ Sınır **sunucuda hesaplanmıyor** — `useSyncExternalStore` ile
istemcide. Sunucu UTC, tarayıcı Türkiye: gece yarısından sonraki üç
saatte iki taraf farklı gün üretir ve hidrasyon uyuşmazlığı çıkardı.

⚠️ Bu bugün **yalnız ekranın tavanı**: `EventLogs` eski satırı silmiyor.
*"24 ay saklıyoruz"* cümlesi ancak back-end budama işini yazınca doğru
olur — istendi.

### Doğrulama

Üç ekran tarayıcıda açıldı ve **veriyle** görüldü: aktivite kayıtları
(1264 kayıt, tarih sınırları ölçüldü), rezervasyon ayarları ve e-posta
yönetimi (iki "beklenen uç" kutusu da basılıyor). Hidrasyon uyarısı yok.

⚠️ Konsolda üç uçta `401` göründü (`platform/partners`, `support/tickets`,
`platform/reviews`) — **kusur değil**, oturum açılmadan önceki
yüklemelerden kalma. Konsol temizlenip sayfa yeniden yüklendi: temiz, ve
üç listenin ikisi aynı anda veriyle basılıyordu. Ölçmeden bildirilseydi
olmayan bir hata duyurulmuş olacaktı.

### Önceki bir notun düzeltmesi

⚠️ Yukarıdaki *"`NotificationOutbox` boş → outbox artık kullanılmıyor"*
cümlesi **yanlıştı**. Outbox bir **kuyruk**: gönderdiği satırı siliyor,
yani boş olması başarı demek. Ölçüm yerine çıkarım yapılmıştı.

## 2026-09-12 — iki sayaç üreticiye taşındı (`8bfc630`)

`mimari-cikar.py` iki satır daha basıyor: **yanıt tipi dosyası**
(`src/lib/api/types`) ve **ölçüm betiği** (`araclar/*.py`).

**Neden kod reposunda bir değişiklik:** ikisi de gece `web-mimari.md`'ye
**elle** yazılmıştı ve orası append-only anlatı — altı ay sonra *"19 modül
dosyası"* ile *"30 modül dosyası"* yan yana duracak ve okuyan hangisinin
güncel olduğunu bilemeyecekti. Üstelik "30" **zaten** üretilen tabloda
vardı; elle yazmam düpedüz kopyaydı.

⚠️ Bu, aynı gün vault oturumunun bulduğu `41 rota` kusurunun birebir
aynısı: rota sayısının otoritesi de elle yazılan anlatıda kalmıştı.
İkimiz de aynı tuzağa aynı gün düştük ve **ikimiz de kuralı biliyorduk**.
Kuralın kolay atlanan yarısı şu: *bir envanter üretilmeye başlandığı gün,
o sayıyı okuyan **her yer** yeni dosyaya taşınmalı.*

Anlatıda artık sayı yok, **ne olduğu** var: hangi ekranlar eklendi, hangi
tip dosyaları, hangi betikler.

## 2026-09-12 — süreler panelden yazılıyor (`0342b5f`)

Back-end `PUT /api/platform/settings` gönderdi (`0eae276`); tutma süresi
ve tahsilat penceresi artık **panelden değiştiriliyor**.

⚠️ **Ekran kodunda tek satır değişmeden açıldı.** Form `editable` alanına
bakıyordu, benim varsayımıma değil; uç `true` dönünce düğme kendiliğinden
göründü. Alanın var olma sebebi buydu ve **karşılığını bugün verdi** —
"bugün düzenlenemiyor" diye bir cümle yazsaydım, bugün birinin gelip onu
kaldırması gerekirdi ve kimse hatırlamazdı.

**Sınır sayıları ekrana yazılmadı.** Sunucu tutmayı 1–120 dakika,
pencereyi 1–168 saat kabul ediyor; ikisini de kutuya `max` yazmak kolaydı
ve sunucu tavanı değiştirdiği gün sessizce yalan olurdu. Bedeli kabul
edildi: operatör aralığı **kaydetmeden önce** göremiyor. Dürüst yolu
tavanları uçtan almak — istendi.

**Tarayıcıda üç yol da denendi:**

| Deneme | Sonuç |
|---|---|
| 500 dakika | `400` · *"kabul edilen aralığın dışında"* |
| 20 dakika | `204` · liste yeniden okundu, `Son değişiklik` güncellendi |
| 15'e geri | `204` · başlangıç değerine döndürüldü |

⚠️ Kutuların başlangıç değeri **efektle senkronlanmıyor**, form
`updatedAt` ile anahtarlanmış bir alt bileşende `useState` ile bir kez
okunuyor. Efekt hem lint kuralına takılıyordu hem de araya giren bir
yeniden okuma personelin yazdığı değeri geri alırdı.

### Doğrulanmamış bir bulgu kaydedildi

⚠️ Konsolda üç sunucu tarafı okuması (`platform/partners` ·
`support/tickets` · `platform/reviews`) tekrar tekrar `401` veriyor.
**Bir kez "bayat kayıt" diye eleyip geçmiştim ve o eleme yanlıştı** —
temiz bir yeniden yükleme tekrarlamayacağı anlamına gelmiyormuş.
Belirti ölçüldü, sebep **ölçülmedi** → [[web-sunucu-render-401]]

## 2026-09-12 gece — genel bakışta çubuklar hiç çizilmiyormuş (`0fd5356`)

Defterde **on iki ana ekranın doğrulama kaydı yoktu** ("bu defter
açılmadan önce görülmüş olabilir"). Altısını açtım ve ilki bir kusur
çıkardı.

⚠️ **Genel bakıştaki üç eğride ve finanstaki ciro eğrisinde çubuklar
hiç görünmüyordu.** Sayılar ve ay adları basılıyordu, çubuk alanı
bomboştu. Ekran "veri yok" gibi duruyordu; oysa veri oradaydı —
`135 K`, `159 K`, `91 K` ekranda yazılıydı.

Ölçüm: on iki çubuğun hepsi `height: 4%` taşıyor, hesaplanan yükseklik
**0**. Sebep, yüzdelik yüksekliğin `auto` yükseklikli bir kaba karşı
çözülememesi: sütun kutusu `items-end`'li bir flex satırının içindeydi ve
yüksekliği içeriğinden geliyordu. Sütun **grid**'e çevrildi
(`grid-rows-[auto_1fr_auto]`), orta satır kesin yükseklik kazandı.

⚠️ Aynı yerde ikinci kusur: etiketlerde `truncate` vardı ama **genişlik
yoktu**, o yüzden kırpmıyordu ve on iki sütunlu eğride komşu ay adları
üst üste biniyordu — "AraOca 26Şub" tek kelime gibi okunuyordu.
`w-full text-center` eklendi.

**Bu ikisi neden bu kadar geç bulundu:** derleme, lint ve üç ölçüm betiği
temizdi ve temiz kalmaya devam ediyor. Görünmeyen bir çubuğu hiçbir
statik denetim yakalamıyor — yalnız ekrana bakmak yakalıyor. Defterin
varlık sebebi tam buydu ve **ilk boş satırı açtığımda karşılığını verdi.**

### Süre ayarlarında ikinci tur (`limits` · `updatedByName`)

Back-end istediğim iki alanı aynı gece ekledi. Aralık artık ekranda
yazıyor (`1 – 120 dakika`, `1 – 168 saat`) ve **tek bir sayı bile
kopyalanmadı**; değiştirenin adı da kullanıcı satırından çözülüyor.

⚠️ Dün *"aralığı gösterememenin bedeli kabul edildi"* diye yazmıştım.
Yanlış değildi ama eksikti: **kopyalamamanın karşılığı eksikliğin kalıcı
olması değil, doğru yerin cevap vermesi oldu.** Eksikliği yazmak, onu
görünür kılıp çözdürdü.

## 2026-09-12 · defterdeki on iki boş satır kapandı

Hepsi tarayıcıda **veriyle** görüldü: genel bakış · müşteri listesi ·
rezervasyonlar · müsaitlik · personel · roller · destek · yorum · tekne
yönetimi · kupon · iş sağlığı · belge kuyruğu.

**Bir kusur çıktı** (görünmeyen çubuklar, üstteki bölümde) ve iki şey
**kusur değildi** — ama ikisini de ölçmeden anlayamazdım:

⚠️ **`rezervasyonlar` ve `musaitlik` bir kez "çıkış yapmış" gibi açıldı.**
Kod değil, API'nin o an yeniden başlaması. Ama ortaya çıkardığı davranış
gerçek bir kusur ve ayrı notta → [[web-ulasilamayan-api-cikis-gibi]]

⚠️ **Tekne kartlarında kapak görselleri boş.** Kart *"1 görsel"* diyor,
kutu gri. Ölçüldü: `next/image` **500** dönüyor çünkü nesne deposu
(MinIO, `:9000`) **çalışmıyor**. Kod tarafında yapacak bir şey yok ve
bozulma doğru yönde: kart kırık görsel ikonu değil sakin bir gri kutu
basıyor. Ortam notu, kusur değil.

### Kayıp sayacı ekrana bağlandı

Back-end istek günlüğünde iki kusur buldu: düşen kayıt sayacı **hiç
artmıyordu** (`DropWrite` kipinde `TryWrite` dolu sırada da `true`
dönüyor) ve sayacı **hiçbir yer okumuyordu**. İkincisi benim tarafıma
düşüyordu; `droppedSinceStart` artık yanıtta ve ekranda.

⚠️ Kutu **listenin üstünde** ve yalnız sıfırdan büyükken basılıyor.
*"0 kayıp"* yazmak, sayacın **süreçle sıfırlandığı** gerçeğini gizleyen
bir güvence olurdu; o ayrım dipnotta tek cümleyle duruyor. Uç alanı hiç
göndermezse de sessiz — bilinmeyen hakkında iddia üretmiyor.

Ölçüldü: uç `droppedSinceStart: 0` dönüyor, 409 istek. Uyarı doğru
biçimde **görünmüyor**.

## 2026-09-12 · tekne alt ekranları ilk kez açıldı

Defterde **66 panel bileşeninin 28'i** kayıtlıydı; kalanın en riskli
kümesi `/admin/tekneler/*` alt ekranlarıydı çünkü hiç açılmamışlardı.
Beşi de açıldı ve **beşi de düzgün**: künye/kapasite, fiyatlandırma
(kiralama tipi · taban fiyat · dört ek hizmet), görseller, belgeler
(üç belge, "İnceleniyor"), düzenleme formu.

⚠️ **Bir şeyi kusur sanıp ölçtüm ve kusur değildi.** Görsel yükleme
kutusu *"En fazla 23 dosya · dosya başına 10 MB"* yazıyor ve bu, gecenin
en çok tekrar eden kusur sınıfına (sunucu değerinin ekranda kopyası)
benziyordu. Ölçüm: ikisi de `lookups.limits`'ten geliyor
(`boatPhotoMax`, `boatPhotoMaxBytes`), 23 = tavan eksi mevcut görsel.
Kopya yok. `file-upload.tsx`'teki `maxFiles = 8` varsayılanı yalnız
çağıran sınır vermediğinde devreye giriyor; burada veriliyor.

**Benzemek kanıt değil** — sınıfı tanımak nereye bakacağımı söylüyor,
ne bulacağımı değil. Bu gece bunun tersini bir kez yaptım (401'leri
"bayat" sayıp geçmek) ve yanılmıştım.

tarayıcıda doğrulandı: tekne detayı (admin) · 2026-09-12 · src/components/panel/boat-screen-shell.tsx · d0bb7aa
tarayıcıda doğrulandı: tekne fiyatlandırma · 2026-09-12 · src/components/panel/boat-pricing.tsx · d0bb7aa
tarayıcıda doğrulandı: tekne görselleri · 2026-09-12 · src/components/panel/boat-media.tsx · d0bb7aa
tarayıcıda doğrulandı: tekne belgeleri · 2026-09-12 · src/components/panel/boat-documents.tsx · d0bb7aa
tarayıcıda doğrulandı: tekne düzenleme formu · 2026-09-12 · src/components/panel/boat-form.tsx · d0bb7aa
