---
rol: map
kapsam: web
guncelleme: 2026-08-27
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

- **Geniş tablo kabı yalnızca dar ekranda kaydırır:** `overflow-x-auto
  wide:overflow-x-visible`. Her ölçüde açık bırakılırsa tarayıcı 15px kaydırma
  çubuğu ekliyor ve masaüstü ölçümü tasarımdan sapıyor; tasarımda kaydırma kabı
  yok, geniş tablo kartın dışına taşıyor -> [[web-kararlar]]

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

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-kararlar]] · [[web-gorevler]] · [[web-araclar]]
