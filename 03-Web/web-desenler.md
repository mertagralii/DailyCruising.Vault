---
rol: map
kapsam: web
guncelleme: 2026-09-11
durum: guncel
---

# Web Desenleri

`DailyCruising.Front-End/` altında kod yazarken uyulacak kurallar.

**Desen != karar.** Gerekçeler tarihleriyle [[web-kararlar]] içinde; burada yalnız
**uygulama kuralı** var.

## Renk ve stil

- **Bileşende sabit renk kodu yazılmaz.** `#D8366B` değil, Tailwind sınıfı üzerinden
  token okunur: `bg-action`, `text-fg-secondary`, `border-line`. Renk değişimi
  yalnız `globals.css` içindeki marka rampalarından yapılır
- **Taban sınıfa ezilebilir renk yazılmaz** — bileşenin varsayılan rengi, kullanım
  yerinde geçilen sınıfı ezmemeli
- `globals.css`'e yazılan **her element seviyesi stil `@layer base` içinde olmalı.**
  Katman dışı bir `a { }` kuralı, class seçicili Tailwind yardımcısını özgüllükten
  bağımsız olarak ezer -> [[web-tailwind-katman-tuzagi]]
- Bölüm boşlukları elle değil `Section` bileşenine parametre olarak verilir
- **Küçük metne açık satır yüksekliği yazılır.** `globals.css` gövdeye **26px sabit**
  veriyor; `leading-` verilmeyen her öğe bunu miras alıyor. Tasarımda `line-height`
  yoksa bizde `leading-[normal]` yazılmalı, boş bırakılmaz. 2026-08-24'te aynı hata
  dört ayrı yerde çıktı: tekne kartı satırları, takvim gün başlığı, hücre gün
  numarası, tablo rozet hücresi -> [[web-olcum-yanlis-pozitifleri]]
  *(Genel kural değil — bu projenin gövde ayarına özgü. Şablona taşınırsa
  "gövde sabit satır yüksekliği veriyorsa açık yaz" biçiminde genelleşir.)*

## Duyarlı kırılımlar

Tailwind'in hazır ekran adları bu tasarımla uyuşmuyor. Temaya iki kırılım eklendi;
**yeni ızgara yazarken bunlar kullanılır, `lg`/`md` değil**:

| Ad | Değer | Nereden |
|---|---|---|
| `wide` | 1180px | Tasarımın tek eşiği: `const wide = vw >= 1180` |
| `mid` | 720px | İkinci eşik: `aboutCols`, `cardCols`, `whyCols` için `vw < 720` |

Izgara kuralları (tasarımdan birebir): istatistik 4 → darda 2 · çift blok 2 → 1 ·
kart ızgarası 3 → 2 → 1 · panel yan menüsü `248px 1fr` → tek kolon.

- **Geniş tablo kabı her ölçüde kaydırır:** `overflow-x-auto`.
  2026-08-28'de değişti — eskiden masaüstünde kartın dışına taşıyordu (tasarıma
  uymak için) ama **sayfanın tamamını 63px yana kaydırıyordu**
  -> [[web-kararlar]] 2026-08-28

*(Kırılım değerleri DailyCruising tasarımına özgü; "hazır ekran adlarını değil
tasarımın kendi eşiklerini kullan" kuralı her projede geçerli.)*

## Yeni yardımcı sınıf yazarken

**Ham token'ın `:root`'ta olması sınıfın çalışacağı anlamına gelmez.** Tailwind
yalnız `@theme inline` içine bağlanmış eşlemeler için kural üretir; bağlanmamış
bir ada karşılık gelen sınıf DOM'da durur ama hiçbir şey yapmaz. Build, lint ve
tip denetimi üçü de temiz geçer -> [[web-baglanmamis-token-tuzagi]]

## Geri bildirim katmanı

Tasarım kaynağında yok, token setinden türetildi -> [[web-kararlar]] 2026-08-26.

- **Toast ve modal `ToastProvider` üzerinden**; sağlayıcı kök yerleşimde, her
  sayfa ve panel `useToast()` çağırabilir
- **Modal açılırken kaydırma çubuğu genişliği kadar sağ dolgu bırakılır**
  (`--scrollbar-w`), yoksa arkadaki sayfa 15px sıçrar
- **Hata varsayılan olarak kendiliğinden kapanmaz** (`duration: 0`), diğer
  tonlar 5 sn. Ekranda en fazla 3 toast durur
- **Yıkıcı eylem `ConfirmDialog` ile sorulur**, doğrudan yapılmaz
- **QR front-end'de üretilmez** — `QrCode` bileşeni API'den gelen `qrImageUrl`
  görselini gösterir, yoksa yer tutucu çizer
- **`src/emails/*.html` sabit hex kuralının istisnasıdır** — e-posta istemcileri
  CSS değişkeni desteklemiyor. Marka rampası değişirse elle güncellenir

## Kimlik ve korunan rotalar

- **Jeton hiçbir zaman istemciye dönmez.** Giriş `/api/auth/login` rota
  işleyicisinden geçer, jetonlar `httpOnly` çereze yazılır. Bileşenler jetonu
  görmez, göremez
- **`proxy.ts` yetki sınırı değildir** — imza doğrulamaz, yalnız yönlendirir.
  Asıl kapı API'de. Yeni korunan rota eklerken `GUARDED` listesine yazılır ve
  `matcher` güncellenir; **ikisinden biri unutulursa rota sessizce açık kalır**
- **Next 16'da dosya adı `proxy.ts`**, `middleware.ts` kullanımdan kalktı
- **Başarısız jeton yenilemesi tekrar denenmez** — backend zinciri kapatıyor,
  ikinci deneme kullanıcıyı kesin olarak dışarı atar → [[web-kararlar]]
- **Backend'in beş ayrı hata şekli var**, ikisi gövdesiz. `res.json()` doğrudan
  çağrılmaz; gövde okunup boşsa ayrıştırılmaz
- **Giriş hatasında backend metni aynen gösterilmez** — "kullanıcı yok" ile
  "parola yanlış" ayrımı hesap sayımına izin verir

## Gönderim ve yükleme

- **Her gönderim `useSubmitGuard`'dan geçer.** Kilit `ref`'te, `useState`'te
  değil: aynı karede gelen iki tıklama `busy === false` görür ve ikisi de geçer
- **`disabled` tek başına yetmez** — render'dan sonra devreye giriyor ve forma
  Enter ile de gelinebiliyor
- **`Button.loading`** etiketi korur, gösterge üstüne biner (genişlik sabit).
  `loadingLabel` verilirse etiket değişir; hangisinin doğru olduğu yere göre
  değişir, seçim çağıranda
- **Ham `<button>`'lar da korunabilir** — tasarım ölçüsü primitife uymuyorsa
  sarma, `useSubmitGuard` + `Spinner` kullan. `cn()` tailwind-merge **değil**;
  `h-14` ile `h-[52px]`'yi aynı dizeye koymak sonucu CSS sırasına bırakır
- ⚠️ **İstemci kapısı sunucu idempotency'sinin yerini tutmaz** — ağ tekrarı,
  sekme kopyalama ve geri tuşu buradan geçmez

## Oturum ve veri erişimi

- **Sunucu bileşeni** `@/lib/api/client` kullanır · **tarayıcı**
  `@/lib/api/browser` üzerinden `/api/dc/*` vekilinden geçer. Bileşenler
  backend'i doğrudan çağırmaz — jeton `httpOnly` çerezde
- **Oturum `oturumKullanicisi()`'nden okunur**, rotadan tahmin edilmez.
  `cache()` ile sarılı: aynı render'da tek istek
- **Vekile yeni bir yol önekinin eklenmesi gerekir** — listede olmayan `404`
- **Zaman damgaları UTC gelir**, `@/lib/api/format` üzerinden basılır. Ham
  basılırsa 3 saat kayar; sadece-tarih alanlarına çevrim **uygulanmaz**
- **Backend'in Türkçe hata metni doğrudan gösterilmez** — `hataMetni()` bilinen
  `code` değerlerini kendi metnimize çevirir

## Elle yazılan yanıt tipleri

`openapi.json` **hiçbir işlem için yanıt şeması taşımıyor**; bütün yanıt
tipleri elle yazılıyor ve uçla uyuşmadıklarında `tsc`, `lint`, `build`
üçü de temiz geçiyor.

- **Her yeni yanıt tipi uca istek atılarak doğrulanır.** Kaynak kodu okumak
  yetmez: sözleşme sınıfının adı ile telde giden ad ayrışabilir
- **İsteğe bağlı alanlar en tehlikelisi** — yanlışlığı normal kullanımda
  görünmez, yalnız formu tam dolduran kullanıcıda patlar
- **Katalog/kimlik listeleri koda gömülmez**, uçtan okunur. Gömülen anahtar
  bugün çalışsa da katalog değişince sessizce yanlış olur
  → [[web-elle-yazilan-tip-yalan-soyler]]

## Tek kaynaklar

Bu değerler koda dağıtılmaz; tek dosyadan okunur.

| Ne | Nereden |
|---|---|
| Marka adı ve kurumsal veri | `src/lib/brand.ts` |
| Rota yolları | `src/lib/routes.ts` |
| Tur tipleri, diller, menü | `src/lib/nav.ts` |
| Mock içerik | `src/lib/data/*.ts` |

**Tur tipinde `slug` ve `label` ayrı tutulur.** `slug` kalıcı kimliktir ve query
string'e girer; `label` yalnız gösterimdir. Eski sistemde ikisi karışmıştı.

## Veri

- Her şey şu an mock. `src/lib/data/*.ts` içindeki alan adları **API sözleşmesinin
  taslağı** sayılır — rastgele adlandırılmaz, backend'e geçerken bu adlar konuşulur
- `Price` bileşeni `amount={null}` alınca "Fiyat için iletişime geçin" basar —
  tanımlı tarifesi olmayan tekne iş kuralının arayüz karşılığı
- `Placeholder` gerçek görseller gelene kadar tasarımdaki gradyan bloklarını taşır

## Doğrulama — zorunlu

**`build` ve `lint` yeterli değil.** Bu vault'ta kayıtlı sekiz web tuzağının
tamamı ikisinden de temiz geçti, yalnız tarayıcıda görüldü.

- Sayfa geçirmeden önce [[web-tasarimi-tarayicida-acmak]] okunur
- Tasarım `python3 -m http.server 8899` ile açılır, hesaplanmış stiller karşılaştırılır
- **İki sekme de aynı boyutta olmalı** — `resize_page` sessizce başarısız olabiliyor;
  boyut doğrulanmazsa bütün `x` ölçümleri kayar ve "eşleşti" raporu yalan olur
- Sekme gizliyken animasyon ve scroll olayı tetiklenmez; ölçümden önce elle sürülür:
  `document.getAnimations().forEach(a => a.finish())` ve
  `window.scrollTo(0, N); window.dispatchEvent(new Event('scroll'))`

## "Sayfa uygulandı" ne demek

Ölçüt **bölüm sayımı**, ekran sayısı değil -> [[web-kararlar]] 2026-08-22.
Liste tablosu yapılmış olması detay ekranının yapıldığı anlamına gelmez —
bu hata bir kez yapıldı, 106 bölüm eksik çıktı -> [[web-eksik-detay-ekranlari]]

## Sunucudaki bir sayının kopyası arayüzde tutulmaz

Bir sınır, eşik veya çarpan sunucuda tanımlıysa **arayüzde yeniden yazılmaz**;
uçtan okunur. `boat-media` sınırı `20` yazıyordu, sunucununki `24`'tü —
ekran, sunucunun kabul edeceği dört görseli reddediyor ve işletmeye
*"sınıra ulaştın"* diyordu.

⚠️ **Bu sınıf en sessizi.** Alan adı uyuşmazlığını backend'in
`UnmappedMemberHandling = Disallow` kilidi 400 ile kapatıyor; tip
uyuşmazlığını kapatmıyor; **sayı uyuşmazlığını hiç göremiyor** — iki taraf da
kendi içinde tutarlı olduğu için hiçbir test kırmızı yanmıyor.

- Sınır `GET /api/lookups` → `limits` içinde gelir (`ff013e0`)
- Uç sınırı vermiyorsa **varsayılan uydurulmaz**: yükleyici gizlenmez, sunucu
  kendi mesajıyla reddeder. Uydurulan varsayılan, kaldırılan kopyayı geri
  getirir
- Aynı kural sayı **ilişkileri** için de geçerli: `boatPrice` ile
  `grandTotalTry` arasındaki çarpanı arayüzde kurmak yerine uca `billedDays`
  eklendi -> [[web-kararlar]] 2026-09-05

## `PUT` gövdesi şemanın **tamamını** taşır

Bu API'de `PUT` **tam değiştirmedir**: gövdede olmayan alan `null`'a çekilir.
Yani bir formda alanı unutmak, o alanı **her kaydetmede silmek** demek.

- Yeni bir `PUT` formu yazarken gövde `openapi.json`'daki `Save*Request`
  alanlarıyla **karşılaştırılır**; eksik alan varsa ya gönderilir ya da
  boşaltılmasının kasıtlı olduğu koda yazılır
- Alan listesi **tek yerde** durur. Okuma, yazma ve render ayrı listelere
  bakarsa biri güncellenip diğeri unutulur — `tursabNumber` kusuru
  tam olarak buydu -> [[web-durum]] 2026-09-06
- ⚠️ **Hiçbir otomatik kapı bunu yakalamıyor.** Backend'in
  `UnmappedMemberHandling = Disallow` kilidi *fazla* alanı reddeder,
  **eksik** alanı değil: eksik alan geçerli bir istektir

## `server-only` bir sözlük, tarayıcıda **ikinci kopyasını doğurur**

Çeviri sözlükleri (`Open → Açık`, `other → Diğer`) hem sunucu tarafında hem
istemci bileşenlerinde gerekiyor. Sözlük `server-only` bir dosyada yaşıyorsa
istemci onu **okuyamaz** ve kopyalar; kopya sessizce ayrışır.

2026-09-07'de ölçüldü: `TALEP_DURUMU` iki yerde yazılıydı —
`lib/api/panel.ts:384` (`server-only`) ve `components/panel/support-ticket.tsx`
— ve müşteri detayına destek sekmesi eklenirken **üçüncüsü** yazılmak üzereydi.

- Uç anahtarı → Türkçe etiket sözlükleri `lib/api/types/<alan>.ts` içinde
  durur: o katman **tarafsız**, iki taraf da okuyabilir
- Sözlükte olmayan anahtar `?? ham` ile **ham geçer**, gizlenmez:
  *uydurma anahtar sessiz, eksik anahtar görünür* -> [[web-kararlar]] 2026-09-06
- Anahtarlar backend enum'undan ya da izin listesinden **ölçülür**; İngilizce
  bir değeri tahmin etmek, ekrana hiç uğramayan ölü bir satır üretir

## Doğrulama, **ekranın bastığı katmanda** yapılır

Bir hesabın tuttuğunu göstermek için uçtan gelen sayıları toplamak yetmiyor;
kullanıcı o sayıları değil, **biçimlendirilmiş hâllerini** görüyor.

2026-09-08'de ölçüldü: rezervasyon ödeme dökümünde satırların toplamı
uçtaki değerlerle **tutuyordu** ama ekranda tutmuyordu — para tam sayıya
yuvarlanıyor ve üç ayrı yuvarlama toplamı ıskalıyordu.

```
F6BUGQXM  3.958 + 908 + 973 = 5.839    ekranda genel toplam 5.840
U7RPXUDR  7.917 + 642 + 1.712 = 10.271 ekranda genel toplam 10.270
```

⚠️ Ben aynı gün bu dökümü "doğrulamıştım" — **veriyi** toplayarak. Kusur
gösterim katmanındaydı ve doğrulamam oraya hiç bakmadı. Ölçüm doğruydu,
**ölçtüğü yer yanlıştı.**

- Toplanması gereken sayılar **kuruşuyla** basılır (`tlKurusla`); ilan ve
  liste fiyatları tam sayı kalır (`tl`). Ayrım *"para mı"* değil,
  **"bu sayı bir toplamın parçası mı"**
- Sapma **iki yönde** olabiliyor, yani "hep bir eksik" diye telafi edilemez
- ⚠️ **Tek örnek yeterli değil**: bazı rezervasyonlarda yuvarlama hataları
  birbirini götürüp tesadüfen tutuyor. `4P3WVK4Z` tutuyordu, `F6BUGQXM`
  tutmuyordu — ilkine bakıp "çalışıyor" demiştim
- Doğrulama, biçimlendiricinin çıktısı **yeniden ayrıştırılıp** toplanarak
  yapılır; girdi sayıları toplanarak değil

## Yarım çeviri, hiç çevirmemekten daha yanıltıcı

Bir satırın **etiketi** Türkçe, **değeri** ham İngilizce kalırsa okuyan o değeri
bir veri sanıyor, çevrilmemiş bir anahtar olduğunu anlamıyor.

2026-09-09'da ölçüldü. Personel etkinlik ayrıntısı şunu basıyordu:

```
İşlem     moderation.publish          ← ham
Sebep     İnceleme aşamasında değil   ← çevrilmiş
```

Aynı pencerede iki satır, biri çevrilmiş biri değil. Etiketlerin düzgün
Türkçe olması, ham değeri **daha** göze batmaz hâle getiriyor: okuyan
"etiketler çevrilmiş, demek ki bu da doğru biçimi" diye geçiyor.

- Çeviri **çift** yapılır: etiket ve değer. Biri yapılıp diğeri bırakılırsa
  yapılan kısım, yapılmayanı gizler
- Bu kusur **derlemede, testte ve uçtan bakınca görünmüyor** — yalnız
  ekranda, bir cümlenin ortasında görünüyor
- ⚠️ Sözlüğü **sunucu taşır**: değerler (`action`, `reason`, `stage`)
  kapalı küme değil, kod boyunca dağılmış düz dizeler. Ön yüzde sözlük
  tutmak `satisfies` ile korunamaz → [[web-enum-uretilemez]]

## Uç enum'una denk gelen sözlük `satisfies` ile yazılır

**Kural, ölçülebilir hâliyle:** anahtarları `openapi.json`'daki bir enum'un
**tam kümesine** eşit olan çeviri sözlüğü `satisfies Record<Enum, string>`
ile yazılır. Anahtarları serbest dize olanlar (kategori, hata kodu, kayıt
türü) **kapsam dışı** — onlarda korunacak bir küme yok.

```ts
export const TEKNE_DURUMU = {
  Draft: "Taslak", Published: "Yayında", Inactive: "Pasif",
} satisfies Record<BoatStatus, string> as Sozluk;
```

`satisfies` eksik **ve** uydurma anahtarı derleme hatası yapıyor; `as Sozluk`
çağıranı gevşek bırakıyor, yani `?? ham` çalışma zamanı koruması duruyor.

⚠️ **Kural neden bu kadar dar:** `Record<string, string>` 51 yerde geçiyor ve
çoğu serbest dize eşlemesi. Hepsini kapsayan bir kural %100 ihlal edilirdi ve
ölçülemezdi. Ölçüt **enum'a tam eşleşme**; o zaman ihlal sayısı bugün
**sıfır** ve artışı görünür.

### Ölçüm bu kuralı yazarken üç ihlal buldu (2026-09-09)

Kural yazılırken 22 sözlük enum'larla karşılaştırıldı; üçü tam eşleşti ve
`satisfies` taşımıyordu:

| Sözlük | Enum | Ne çıktı |
|---|---|---|
| `partner-profile.tsx: DURUM` | `PartnerStatus` | `ISLETME_DURUMU`'nun **birebir kopyası** |
| `document-list.tsx: BELGE_DURUMU` | `BoatDocumentStatus` | `panel.ts`'teki sözlüğün **ikinci kopyası** |
| `messaging/types.ts: KONUSMA_KAPANMA` | `ConversationCloseReason` | korumasız |

⚠️ **Üçünden ikisi kopyaydı** — aynı gün `TEKNE_DURUMU` (üç kopya, biri
ayrışmış) ve `TALEP_DURUMU` (iki kopya) düzeltilmişti. Yani `satisfies`
kuralı yalnız eksik anahtarı değil, **kopyayı da** açığa çıkarıyor: kopya
yazan kişi `satisfies` yazmıyor, çünkü tipi import etmek zorunda kalsa
zaten mevcut sözlüğü görürdü.

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-kararlar]] · [[web-gorevler]] · [[web-araclar]]

---

## İkinci ekran aynı satırı basacaksa tablo **ayrı dosyaya** çıkar

Bir liste tablosu ikinci bir ekranda görünecekse (aynı uç, aynı satır şekli),
satır **kopyalanmaz**; tablo kendi dosyasına çıkarılıp ikisi de onu basar.

**Ölçülen gerekçe — 2026-09-09'da beş kopya sözlük çıktı** ve üçü tam olarak
bu şekilde ayrışmıştı: `TEKNE_DURUMU`'nun bir kopyasında `Inactive` yoktu ve
pasif tekne ekranda ham `Inactive` yazıyordu. Satır için aynı mekanizma
geçerli: personel satırının bir kopyası "Parola değiştirilmedi" işaretini
kaçırır, biri `roleNames`'i `join(", ")` ile kırpar, biri askıdaki personeli
hiç göstermez. Üçü de ayrı ayrı yaşandı.

⚠️ **Kopya yazan kişi farkında olmuyor** ve mekanizması şu: ikinci ekranı
yazarken ilk ekranın dosyası açık değildir, bu yüzden `roleNames`'in çoğul
olduğu ya da `mustChangePassword`'ün kullanılamaz hesabı işaret ettiği
görülmez. Eksiklik *karar* değil, *görmeme*dir — bu yüzden gözden geçirmeyle
yakalanmıyor.

⚠️ **Ortak dosya, "birini diğerinden import et" değil.** `staff.tsx` rol
oluşturma modalını `roles.tsx`'ten alıyordu; tabloyu ters yönde import etmek
dairesel bağımlılık olurdu. Ölçüt: **iki çağıran varsa üçüncü dosya** —
hangisinin "asıl" olduğunu tartışmak, bir sonraki çağıranda yine tartışılır.
Karşılığı `staff-table.tsx`, iki çağıranı `staff.tsx` ve `roles.tsx`.

⚠️ **Paylaşılan tabloda `onSec` zorunlu değil, ve verilmediğinde "İşlem"
sütunu hiç basılmıyor.** Rol ayrıntısından personel ayrıntısına giden bir yol
yok; tıklanıp hiçbir şey yapmayan "Detay", ölü düğmeyle aynı şeydir →
[[web-kararlar]] (2026-09-06, *rotası olmayan giriş basılmaz*).

⚠️ **Dışarıya sayaç veren prop `ref`'te tutulur, bağımlılık dizisinde
tutulmaz.** `sayacYaz` effect bağımlılığı olsaydı, satır içi kapanış veren bir
çağıran (`sayacYaz={(n) => setToplam(n)}`) her renderda yeni kimlik üretir,
effect koşar, sayaç yazılır, render tetiklenir — sonsuz döngü. Bileşen
çağıranın yazım şekline bağlı olmamalı.

## Aynı ekranda iki aktörün gerekçesi varsa, etiket **kimin konuştuğunu** söyler

İade ekranında "Gerekçe" etiketli tek bir kutu vardı; içindeki değer
platformun muhasebe gerekçesiydi (`RefundReason`), müşterinin beyanı değildi.
Kutu **doluydu**, yani kusur boşluk olarak görünmedi — personel gördüğünü
doğru sandı.

Kural: bir ekranda aynı kavramın iki aktöre ait sürümü varsa (müşterinin
gerekçesi / platformun gerekçesi, müşterinin notu / personelin notu) etiket
aktörü **yazmak zorunda**, ve ikisi **yan yana aynı blokta basılmaz**.

⚠️ Nötr etiket en tehlikeli hâl: "Gerekçe", "Not", "Durum" gibi sözcükler iki
anlamı da taşıyabildiği için okuyan kişi eksik bilgiyi fark etmiyor, gördüğünü
aradığı şey sanıyor.

## Boş bir alanın **üç sebebi** vardır; üçü ayrı cümle ile basılır

*Okunuyor* · *okunamadı* · *kayıtta yok*. Aynı boşlukla gösterilirse hata veri
yokluğu gibi okunur.

⚠️ Ölçülmüş bedeli: müsaitlik ekranı sekiz takvim isteğinin 400 dönmesini
per-tekne `catch { return [] }` ile yutup ekrana *"0 kapatma"* yazdırdı
(2026-09-10). Ekran doğru görünüyordu ve yanlıştı.

⚠️ "Kayıtta yok" hâli de **sebebini** söyler: alan sonradan eklendiyse eski
kayıtlarda boştur ve bu bir kusur değil. Boş etiket basmak yerine *"Gerekçe
yok."* + tek cümle gerekçe.

## Zorunluluk üretilen tipten okunamıyorsa, çağıranlar **elle** bulunur

`CancelReservationRequest.reason` şemada nullable ve `required` dizisi yok;
zorunluluk yalnız sunucu kodunda. Üretilen tip alanı opsiyonel gösterdiği için
`tsc` · `lint` · `build` üçü de temiz geçti ve müşterinin iptal ekranı **kırık
olarak** durdu — uç her isteği reddediyordu.

⚠️ Böyle bir alan değiştiğinde tek güvenilir adım `grep` ile **bütün
çağıranları saymak**. Tip sistemi bu sınıfta sessizdir.

## Ölçüm betiği de bir veri yoludur — çöken betiğin çıktısı olgu değildir

Tek kullanımlık bir Python betiğiyle uç parametrelerini listeledim; betik
`format` çağrısında `TypeError` ile çöktü ve çökmeden önce **ilk yedi**
parametreyi bastı. Çöktüğü parametre tam olarak aradığım olandı
(`minTotal`'in şema tipi `["null","number"]`, yani bir liste). Yarım çıktıyı
tam liste sandım ve back-end'e *"alan belgede yok"* diye bildirdim — oysa
üreteç onu görmüş ve **aynı turda benim commit'ime yazmıştı**
(`uretilen.ts:11665`).

⚠️ Bu, projenin en sık kusurunun üçüncü yüzü: **hata, veri yokluğu gibi
okunur.** İlk ikisi üretim kodundaydı (müsaitlik ekranı sekiz takvim hatasını
*"0 kapatma"* yazdı; iade ekranı okunamayan gerekçeyi boş gösterecekti).
Üçüncüsü **ölçüm aracındaydı** ve bu yüzden daha tehlikeli: üretim kodunu
ölçümle yakalıyoruz, ölçümü yakalayan bir şey yok.

Kural: tek kullanımlık betikte bile çıktı **sayıyla doğrulanır**
(`"12 parametre bekleniyordu, 7 basıldı"`) ya da çökme açıkça *"ölçüm
başarısız"* diye basılır. "Traceback ekranda görünürdü" yetmiyor — makul
görünen yarım çıktı, görünmeyen bir traceback'ten daha çok ikna ediyor.

## Kaynağın iki kopyasını karşılaştıran kapı hiçbir şey ölçmez

`npm run build` içindeki `tip-uret --kontrol`, ürettiği tipi diskteki tiple
karşılaştırıyor. İkisi de aynı `openapi.json`'dan geliyor: kaynak bayatsa
**bayat kaynak kendisiyle tutarlı bir çıktı üretir** ve karşılaştırma her
zaman geçer.

⚠️ Bu kapı tipin **üretilmiş olduğunu** ölçüyor, **güncel olduğunu** değil.
Ön yüzde belgeyi üreten taraf olmadığı için burada kapatılacak bir yer de yok;
bayatlığın ölçüleceği yer belgeyi üreten taraf, yani API reposu. Orada sekizinci
denetim olarak duruyor (back-end `fe81262`) ve **kör testle** doğrulandı:
belge bir önceki commit'e çekildi, denetim eksik iki parametreyi adıyla söyledi,
diğer yedisi yeşil kaldı. Bir kapıya güvenmenin gerekçesi yazılı olması değil,
**kırdırılmış olmasıdır**.

## "Basılmamalı" ile "basılamıyor" aynı şey değil

İade yolu bir süre **kayıtsız para hareketi** üretiyordu: iade gerçekleşiyor,
muhasebe defterine satır yazılmıyordu. Back-end *"tekrar koşma"* dedi — ve bu
yeterli görünüyordu, çünkü o düğmeye basacak kişi bendim.

Değildi: **Mert paneli kendi kurcalıyor.** Sözlü uyarı, panele giren bir
kullanıcıyı bağlamaz. Düğme bayrakla kapatıldı ve yerinde sebebi yazıldı.

Kural: bir eylem "şu an yapılmamalı" durumundaysa, **kodda kapatılır**; bir
kişinin hatırlamasına bırakılmaz. Geçici kapatma bir bayrak + ekranda görünen
bir cümle demektir — sessiz eksik, görünen eksikten uzun yaşar.

⚠️ Bayrak **her kapalı yol için ayrı**: `IADE_YOLU_HAZIR` ile
`TAHSILAT_HAZIR` tek bayrakken, defter düzelince ikisi birden açılacaktı —
oysa tahsilat hâlâ yoktu. **Farklı sebeple kapalı olan iki şey aynı anahtarı
paylaşmaz.**

## Geliştirme aracı, üretim yüzeyine kalıcı olarak eklenmez

Zamanlanmış işleri elle tetikleyen uç (`/api/dev/jobs/…`) vekilin izin
listesinde yoktu. Kalıcı listeye eklemek en kolayıydı ve yanlıştı: üretimde
niyet edilmemiş bir yol açardı.

Doğrusu **üretimde boş kalan ayrı bir liste**:
`NODE_ENV === "production" ? [] : ["dev"]`. Backend de aynı uçları üretimde
`404` veriyor — iki taraf bağımsız kapatıyor ve **biri unutulursa diğeri
tutuyor**.

⚠️ Vekil izin listesi bu projede **dördüncü** kez unutuldu. Belirti her
seferinde aynı ve yanıltıcı: ekran `404` alıyor, kimse backend'e bakmıyor,
"uç yok" sanılıyor. Yeni bir önek çağıracak her ekranda önce buraya bakılır
→ [[web-mimari]]

## Aynı gün dördüncü kez: ölçüm doğru görünüp başka şeyi ölçüyor

2026-09-11'de dört ayrı biçimde yaşandı ve dördü de **makul çıktı** üretti:

| Ne | Gerçekte ne oluyordu |
|---|---|
| `set -- $degisken` (zsh) | Sözcük bölmesi yok; parametre URL'e hiç girmedi, iki çağrı da aynıydı |
| Çöken Python betiği | `TypeError` öncesi yarım liste basıldı, tam liste sanıldı |
| Bayat süreç | API düzeltmeden 10 dakika eski ikiliyi çalıştırıyordu |
| Zamanlanmış iş | Defter boştu çünkü iş 15 dakikada bir koşuyor, henüz koşmamıştı |

Ortak kural: **bir ölçüm "sonuç yok" diyorsa, önce ölçümün kendisini
doğrula.** Üç kontrol sorusu işe yarıyor:

1. Beklediğim kadar satır/alan geldi mi? (sayıyla doğrula)
2. İki farklı girdi aynı sonucu veriyorsa, gerçekten iki farklı istek mi
   attım?
3. Ölçtüğüm süreç, ölçmek istediğim kodu mu çalıştırıyor? (uptime, commit
   zamanı, işin periyodu)

İlk üçünde de hata bendeydi ve ikisinde yanlış rapor vermekten son anda
döndüm.

İlgili: [[web-kararlar]] · [[web-durum]]
