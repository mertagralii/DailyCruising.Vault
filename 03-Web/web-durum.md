---
rol: status
kapsam: web
guncelleme: 2026-08-31
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
| S-29 | **`brand.ts`'teki "340+ onaylı tekne" ne olacak?** Bu ibare her sayfanın **üst şeridinde** duruyor ve en çok görülen sayı. Backend geliştirme veritabanını ölçtü: yayında **10** tekne (toplam 11), 7 aktif işletme, 11 bölge, 78 rezervasyon. Yani 340 "biraz yüksek" değil, **otuz kat**. Vault'taki veri göçü notu eski sistemden 35 tekne taşınacağını söylüyor — 340 onunla da uyuşmuyor. Seçenekler: **(a)** sayıyı hiç yazma ("Ege ve Akdeniz'de onaylı tekneler"), **(b)** gerçek sayıyı canlı yaz — `GET /api/search` zaten `totalCount` döndürüyor, ayrı uç gerekmez, **(c)** göç sonrası beklenen sayıyı yaz ve göçten önce yayına çıkma. Aynı soru blog için de geçerli: 7 yazı uydurma yazar adlarıyla duruyor ("Deniz Aksoy"), yayımlanacaklar mı yoksa bölüm kapansın mı → `W-38`. **Bir de dokunmadığım bir şey var:** ana sayfadaki tur kategorilerinde "₺750'den", "₺9.500'den" gibi başlangıç fiyatları duruyor. Tekne sayılarını sildim (250 tekne iddia ediyorlardı, 10 var) ama fiyatlara dokunmadım. **Ölçtüm:** `/api/search` katalogda en düşük **₺500** dönüyor (9 tekne: 500, 500, 750, 900, 900). Yani "₺750'den" yanlış değil ama veriden de türetilmiyor ve en düşük kaydın üstünde. Geliştirme verisiyle üretim ayrı olduğu için buradan kesin bir şey denemez — bunlar canlı sitedeki gerçek değerler mi? | `brand.ts`'teki sayıya dokunulmadı, `W-06` ile zaten sende. **`/about` düzeltildi:** "340+ tekne · 96.000 misafir yeri · 4,8/5 üzerinden 4.812 yorum · 8 bölge" kaldırıldı, yerine doğrulanabilir olan kondu (hizmet bölgesi, TÜRSAB belgesi, peşin tahsilat); aynı "340+" düzyazıda da geçiyordu, o da çıktı. Ana sayfa kategorilerinden tekne sayıları çıkarıldı. Blogda **yalnız kontrol edilebilir yanlış** düzeltildi: "Tümü · 48" yazıyordu, 7 yazı var — sayaç artık listeden hesaplanıyor. "Haftada iki yazı" yayın sıklığı sözü kaldırıldı. Yazıların kendisine ve yazar adlarına dokunulmadı |
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
