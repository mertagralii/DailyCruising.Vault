---
rol: map
kapsam: web
guncelleme: 2026-08-26
durum: guncel
---

# Web Mimarisi

`DailyCruising.Front-End/` → repo `mertagralii/DailyCruising.Web`

## Yığın

| Katman | Seçim |
|---|---|
| Çerçeve | Next.js 16 (App Router) |
| Dil | TypeScript |
| Stil | Tailwind CSS v4 (`@tailwindcss/postcss`) |
| Lint | ESLint 9 (`eslint-config-next`) |
| Paket yöneticisi | npm |

Kaynaklar `src/` altında, import alias `@/*`.

## Yapı

```
src/app/          App Router kökü
  layout.tsx      kök layout — ToastProvider · RouteProgress · perde · header/footer
  globals.css     token'lar + Tailwind teması + keyframe'ler + baskı stilleri
  error.tsx · global-error.tsx · not-found.tsx     hata sınırları
src/components/   ui · layout · feedback · home · boats · account · panel · auth
src/lib/          brand · routes · nav · cn · cookie-consent · use-scroll-past · data/
src/emails/       back-end'in dolduracağı HTML e-posta şablonları
public/           statik varlıklar
```

**Rota envanteri: 25.** Sayım için `npm run build` çıktısına bakılır — burada
liste tutulmaz, bayatlar.

## API erişimi

Backend adresi `NEXT_PUBLIC_API_URL` ortam değişkeninden gelir.
`.env.local` (git'e girmez) ve `.env.example` (girer) ikisi de `http://localhost:5163`.

`NEXT_PUBLIC_` öneki bu değerin **tarayıcıya gönderildiği** anlamına gelir — buraya
gizli bilgi konmaz.

Henüz yazılmış bir API istemcisi/fetch katmanı **yok**. OpenAPI'den tip üretimi
kurulmadı → [[durum]]

`src/lib/data/*.ts` içindeki alan adları API sözleşmesinin taslağı sayılır.
2026-08-26 itibarıyla sözleşmeye girmesi beklenen iki ad: rezervasyon yanıtında
`qrImageUrl`, rezervasyon başarı ekranında `booking-success.ts` alanları.

## Paket adı

`package.json` → `"name": "daily-cruising-web"`. Klasör adı `DailyCruising.Front-End`
npm paket adı kurallarına uymadığı için (büyük harf) farklı → [[web-kararlar]]

İlgili: [[web-kararlar]] · [[proje]] · [[00-Index]]

---

## Tasarım sistemi katmanı (2026-08-21)

```
src/lib/brand.ts        marka adı + kurumsal veri — TEK KAYNAK
src/lib/cn.ts           koşullu sınıf birleştirici
src/app/globals.css     token'lar (CSS değişkeni) + Tailwind teması
src/components/ui/      container · section · button · badge · card
                        field (label/input/select/textarea) · rating
                        price · placeholder
src/app/design-system/  bileşen vitrini (geliştirme sayfası, yayına çıkmaz)
```

**Kural:** Bileşende sabit renk kodu (`#D8366B` gibi) yazılmaz; Tailwind sınıfı
üzerinden token okunur (`bg-action`, `text-fg-secondary`, `border-line`).
Renk değişimi yalnızca `globals.css` içindeki marka rampalarından yapılır.

`Price` bileşeni `amount={null}` aldığında "Fiyat için iletişime geçin" basar —
geçerli tarifesi olmayan tekne iş kuralının arayüz karşılığı → [[proje]]

`Placeholder` gerçek görseller gelene kadar tasarımdaki gradyan blokları taşır.

## Kabuk katmanı (2026-08-21)

```
src/lib/routes.ts       rota haritası — tipli rotalar bunu okur
src/lib/nav.ts          tur tipleri (slug + label ayrı), diller, menü
src/components/ui/dropdown.tsx     dışarı tıklama + Esc ile kapanan açılır menü
src/components/layout/site-header.tsx   üst şerit + header + açılır menüler
src/components/layout/mobile-menu.tsx   tam ekran mobil menü
src/components/layout/site-footer.tsx   ⚠️ tasarımdan gelmedi
src/components/layout/stub-page.tsx     uygulanmamış rota taslağı
```

**Tur tipinde `slug` ve `label` ayrı tutuluyor.** Eski sistemde tur tipinin iç adı
ile ekranda görünen adı farklıydı ve filtre query string'i iç adı kullanıyordu;
bu karışıklık tekrarlanmasın diye `slug` kalıcı kimlik, `label` yalnızca gösterim.

**Rota taslakları:** `/boats`, `/blog`, `/about`, `/add-boat`, `/login`,
`/register` şu an `StubPage` döndürüyor. Next 16'da tipli rotalar açık olduğu için
bağlantı verilen her yolun dosyası bulunmak zorunda; ilgili faz gelince içleri dolar.

## Ana sayfa (2026-08-21)

`src/app/page.tsx` — 14 bölüm, tasarımdaki sırayla:
hero+arama · tur tipleri · neden biz · 4 adım · bölgeler · öne çıkan tekneler ·
kategoriler · yorumlar · mobil uygulama · bloglar · tekne sahibi CTA · SSS ·
destek şeridi · iletişim

```
src/lib/data/home.ts          tüm içerik (mock) — ileride API sözleşmesi taslağı
src/components/home/hero.tsx       hero + arama formu
src/components/home/discovery.tsx  tur tipleri · bölgeler · tekneler · kategoriler
src/components/home/trust.tsx      neden biz · adımlar · yorumlar · destek şeridi
src/components/home/engage.tsx     mobil uygulama · bloglar · sahip CTA · iletişim
src/components/home/faq.tsx        akordeon (client)
```

Arama formu `GET /boats` yapıyor; `tur`, `bolge`, `tarih` sorgu parametreleri
API sözleşmesinin ilk taslağı sayılmalı.

## Açılış animasyonu (2026-08-21)

`src/components/layout/intro-overlay.tsx` — tasarımdaki preloader.
İki koyu yarım açılır, ortada marka belirir, altındaki çizgi çizilir (~1,25 sn).

- Sunucuda da basılır → içerik "önce görünüp sonra örtülmez"
- `pointer-events: none` → tıklamayı engellemez
- `prefers-reduced-motion` açıksa CSS ile tamamen gizlenir
- Animasyon bitince kaldırılır; hidrasyon gecikirse 2 sn'lik zamanlayıcı devreye girer

Keyframe'ler `globals.css` içinde: `introTop/Bottom/Line/Mark/Word/Gone`,
`heroRise` (hero içeriği), `pageFade` (modal). Hero bloklarında `data-hero-rise`.

## Faz A + B ilerlemesi (2026-08-22)

**Faz A — kabuk (tamam):**
```
lib/use-scroll-past.ts        useSyncExternalStore tabanlı kaydırma eşiği
lib/cookie-consent.ts         çerez tercihi dış deposu
components/layout/cookie-banner.tsx
```
`site-header.tsx` ana sayfada şeffaf/fixed, kaydırınca beyaz/sticky.
`site-footer.tsx` tasarımdaki içerikle yeniden yazıldı.
`hero.tsx` açık gradyan + koyu yazı + `min-h-screen`.

**Faz B — misafir sayfaları (devam ediyor):**
```
components/auth/auth-shell.tsx      giriş/kayıt ortak kabuğu + sosyal düğmeler
components/auth/password-field.tsx  "Göster" düğmeli parola alanı
app/login/page.tsx                  ✅
app/register/page.tsx                  ✅
app/about/page.tsx             ✅  (lib/data/about.ts)
app/blog/page.tsx                   ✅  (lib/data/blog.ts)
app/blog/[slug]/page.tsx            ✅  components/blog/post-faq.tsx
```
Blog yazısı tasarımda **tek örnek makale**; şu an tüm slug'lar onu gösteriyor.
Gerçek içerik API'den gelince slug'a göre çözümlenecek.

app/add-boat/page.tsx           ✅  (lib/data/owner.ts, components/owner/)
app/booking/page.tsx            ✅  components/boats/booking-form.tsx
```

**Faz B tamam — 11 rota.** Misafir tarafının tamamı uygulandı.

Rezervasyon akışı: tekne detayındaki panelden `Rezervasyona geç` → `/booking`
(3 adımlı: tur+kişi / iletişim / ödeme). Kupon kodu `ERKENREZ10` %10 indirim uyguluyor.

**Uyarı:** Toplam tutar istemcide yalnızca gösterim için hesaplanıyor. Ödeme adımı
yazılırken sunucu tutarı **yeniden hesaplamalı** — istemciden gelen fiyata güvenilmez.
Bu, PRD'nin 14. iş kuralı.

## Faz C — hesap alanı (2026-08-22)

```
lib/data/account.ts                 kullanıcı, sekmeler, rezervasyonlar, favoriler,
                                    kuponlar, bildirim tercihleri
components/account/account-view.tsx 7 sekmeli tek ekran (client)
app/account/page.tsx                ✅
```

Sekmeler: genel bakış · rezervasyonlarım · favori tekneler · kuponlarım ·
profil bilgileri · bildirim tercihleri · hesap ayarları.

Tasarım bunları **tek ekranda sekme durumu** ile gösteriyor; aynı yapı korundu.
Ayrı rota yapılmadı — derin bağlantı gerekirse sonra `?sekme=` sorgusuna taşınabilir.

**Doğrulandı:** açılış perdesi `/account`'da gösterilmiyor (`[data-intro]` DOM'da yok),
tasarımın kuralı bu.

Kalan Faz C: rezervasyon detayı, destek, ticket, yeni ticket, parola.

**Faz C tamam.** Eklenenler:
```
lib/data/support.ts                   ticket'lar, yazışma, rezervasyon detayı, şifre kuralları
components/account/page-head.tsx      hesap sayfalarının ortak başlığı (kırıntı + başlık)
app/support/page.tsx                   ✅ destek merkezi
app/support/[no]/page.tsx              ✅ ticket yazışması
app/support/new/page.tsx              ✅ yeni talep formu
app/account/password/page.tsx            ✅ şifre değiştirme + giriş hareketleri
app/account/booking/[kod]/page.tsx ✅ rezervasyon detayı + fatura + QR
```
QR kodu yer tutucu — üretimi API'ye bağlı.

## Faz D — paneller (2026-08-22)

**Yeniden kullanılabilir panel kabuğu** — işletme, destek ve yönetim panelleri
aynı iskeleti paylaşır:

```
components/panel/panel-shell.tsx
  PanelShell    daraltılabilir sol menü + başlık + içerik
  PanelStat     istatistik kartı
  PanelTable    başlıklı tablo (yatay kaydırmalı)
  PanelSection  bölüm başlığı + kart sarmalayıcı
```

```
lib/data/owner-panel.ts                 işletme paneli verisi
components/panel/owner-panel-view.tsx   10 bölüm
app/owner-panel/page.tsx             ✅
```

Bölümler: genel bakış · rezervasyonlarım · müsaitlik takvimi · tekne listesi ·
belgelerim · finans & hakediş · değerlendirmeler · personel · destek talepleri ·
ayarlar & profil.

**Doğrulandı:** açılış perdesi panel rotasında gösterilmiyor.

```
lib/data/support-panel.ts                 destek paneli verisi
components/panel/support-panel-view.tsx   4 bölüm
app/support-panel/page.tsx                ✅
```

Bölümler: genel bakış (performans çubukları, haftalık sütun grafiği, kanal dağılımı,
müşteri yorumları) · gelen kutusu (arama + durum filtresi) · tamamlanan · hazır yanıtlar.

**Faz D tamam.** Kalan: Faz E — yönetim paneli (3.752 satır, ~24 modül).

## Faz E — yönetim paneli (2026-08-22)

```
lib/data/admin.ts                       24 modülün verisi
components/panel/admin-panel-view.tsx   24 modül, gruplu menü
app/admin/page.tsx                    ✅
```

Menü grupları: Yönetim (işletmeler, müşteriler, personel) · Rezervasyon
(rezervasyonlar, müsaitlik, iptal, ayarlar, yolcu gönder) · Katalog (tekne, bölge,
reklam, kupon, belge, finans) · İçerik (blog, yorum, sözleşme) · Sistem (e-posta,
SMS, SMS gönderimleri, log, aktivite, destek).

**19/19 tasarım sayfası uygulandı.** `isBreak` bilerek yapılmadı — tasarımcının
kırılımları gösterdiği vitrin, gerçek sayfa değil.

## İmza öğe (2026-08-22)

`components/ui/wave-stitch.tsx` — "dalga dikişi", markanın imza öğesi.
Hero altında (`ink`) ve footer üstünde (`action`) kullanılıyor.
Kaynak: `Rihtim Foundations.dc.html` → [[web-imza-oge-dalga-dikisi]]

## Geri bildirim katmanı (2026-08-26)

Tasarım kaynağında olmayan, token setinden türetilen ortak parçalar
→ [[web-kararlar]] 2026-08-26.

```
src/components/feedback/
  toast.tsx        ToastProvider + useToast + görünüm penceresi (4 ton)
  modal.tsx        Modal (odak tuzağı, ESC, kaydırma kilidi) + ConfirmDialog
  skeleton.tsx     Skeleton · SkeletonText · SkeletonCard · SkeletonCardGrid · SkeletonRows
  empty-state.tsx  EmptyState — "blank" (hiç kayıt yok) / "filtered" (sonuç yok)
  pagination.tsx   Pagination + LoadMore
  file-upload.tsx  sürükle-bırak, istemci tarafı tür/boyut doğrulaması
src/components/layout/
  route-progress.tsx  üst ilerleme çubuğu
  error-page.tsx      404/500/403/503'ün paylaştığı iskelet
src/components/ui/
  qr-code.tsx      API'den gelen QR görseli, yoksa yer tutucu
src/components/account/print-button.tsx
src/components/design-system/feedback-demo.tsx
```

`ToastProvider` **kök yerleşimde**; istemci gezinmesinde ayakta kaldığı için
toast rota değişse de ekranda kalır. Modal `createPortal` ile `document.body`
üzerine kurulur — panel rotalarının `overflow` kapları kırpmasın.

**Hata sayfaları.** `not-found.tsx` (404) · `error.tsx` (500, segment sınırı) ·
`global-error.tsx` (kök yerleşim çökerse — kendi `<html>`/`<body>`'si ve satır
içi stilleri var, token'lara güvenilemez) · `app/forbidden/page.tsx` (403,
deneysel dosya sözleşmesi yerine normal rota) · `app/maintenance/page.tsx` (503).

**Akış tamamlayıcıları.**
```
app/booking/success/page.tsx                       kod + QR + sırada ne var
app/account/reservations/[code]/voucher/page.tsx   yazdırılabilir biniş belgesi
app/design-system/emails/page.tsx                  şablon önizlemesi (sandbox iframe)
src/emails/*.html                                  4 şablon + README
```

Baskı kuralları `globals.css` `@media print` içinde: gezinme öğeleri
`data-print-hide`, belge gövdesi `data-print-sheet`.

## Bu dosya nasıl güncel kalır

2026-08-21'den 2026-08-26'ya kadar bu dosyanın **hiçbir tetikleyicisi yoktu** ve
bayatladı (87 kaynak dosya değişmişti). Artık `CLAUDE.md`'de tetikleyicisi var:
*"Yapıya dokunacağım — yeni katman, uç nokta, dış servis"*.

**Buraya dosya listesi değil katman yazılır.** Tek tek dosya adı sayan bölümler
en hızlı bayatlayan bölümlerdir; yukarıdaki eski fazlar (A–E) tarihli kayıt
olarak duruyor, güncel yapı için bu bölüm okunur.
