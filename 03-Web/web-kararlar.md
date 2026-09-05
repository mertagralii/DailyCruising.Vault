---
rol: history
kapsam: web
guncelleme: 2026-09-05
durum: guncel
---

# Web Kararları

**Append-only.** Karar değişirse eskisi silinmez; yeni giriş eskisini iptal eder.

---

## 2026-08-21 — Next.js 16, TypeScript, App Router, Tailwind v4

**Karar:** `create-next-app` ile TypeScript + App Router + Tailwind + ESLint +
`src/` dizini + `@/*` alias, npm ile.

**Neden:** Modern Next.js varsayılanı; Mert bu kombinasyonu seçti.

**Alternatif:** Tailwind'siz kurulum (stil çözümünü sonraya bırakmak) — seçilmedi.

---

## 2026-08-21 — Paket adı klasör adından farklı

**Karar:** `package.json` → `"name": "daily-cruising-web"`.

**Neden:** Hedef klasör adı `DailyCruising.Front-End` büyük harf içerdiği için npm
paket adı kuralına uymuyor; `create-next-app` bu adla çalışmayı reddediyor.

**Nasıl yapıldı:** Uygulama geçici dizinde `daily-cruising-web` adıyla oluşturulup
içeriği `DailyCruising.Front-End/` klasörüne taşındı.

**Sonucu:** Klasör adı ile paket adı kalıcı olarak farklı. Bu bir hata değil, bilinçli.

---

## 2026-08-21 — create-next-app'in AI dosyaları silindi

**Karar:** `CLAUDE.md` ve `AGENTS.md` ilk commit'ten önce silindi; repo geçmişinde
hiç görünmüyorlar.

**Neden:** Mert repoda AI aracı dosyası istemiyor → [[genel-kararlar|genel kararlar]].

**Kayıp:** Bu dosyalar Next.js 16 API rehberi içeriyordu. Gerekirse
`npx create-next-app` çıktısından tekrar alınabilir, repoya konmaz.

İlgili: [[web-mimari]] · [[durum]] · [[00-Index]]

---

## 2026-08-21 — Tasarım kaynağı: Rihtim.dc.html

**Karar:** Web arayüzü `claude.ai/design` üzerindeki "Rıhtım temeller sayfası"
projesindeki `Rihtim.dc.html` dosyasına göre uygulanır. Proje kimliği
`4d088e58-d5b3-4a6e-a824-4366bdb3a9ce`, `DesignSync` aracıyla okunuyor.

**Neden:** Mert tasarımı hazırlayıp onayladı.

**Kapsam:** Tek dosyada 7 sayfa — ana sayfa, tekne listesi, tekne detayı (+3 adımlı
rezervasyon), blog listesi, blog yazısı, hakkımızda, tekne sahibi kaydı. 1928 satır,
1687 inline style, 182 etkileşim binding'i, 3 kırılım (390 / 834 / masaüstü).

**Sonucu / uyarı:** Dosya `get_file` ile çekilirken **256 KiB sınırında kesiliyor**
(`truncated: true`). Sonundaki bir bölüm elde yok; uygulanmadan önce ayrıca
çekilmeli → [[durum]]

---

## 2026-08-21 — Palet tasarımdan, ölçekler tokens.css'ten

**Karar:** `tokens.css` **atılmıyor**, renk rampaları tasarımın paletiyle değiştirilerek
kullanılıyor.

**Neden:** Ölçüldü — tasarımın tipografi ölçeği (15/14/18/12.5/35/24/48/30 px),
radius seti (8/12/16/20/200) ve spacing'i `tokens.css` ile **birebir aynı**. Sadece
renkler farklı. Token dosyası zaten bunun için yazılmış: *"Roles are colour-agnostic:
swap the 3 brand ramps below and the whole kit re-themes."*

**Palet farkı (ölçüm):**

| Rol | tokens.css (eski) | Tasarım (yeni) |
|---|---|---|
| Ana metin | `#05073C` lacivert | `#10201C` (234 kullanım) |
| Aksiyon | `#EB662B` turuncu | `#D8366B` (91) · link `#C22F5F` (66) |
| Vurgu | — | `#F0A64B` amber (10) |

Tasarım hiçbir yerde `var(--...)` kullanmıyor (0 kullanım) — 1687 inline style ile
sabit hex yazılmış. Token'lara **biz** bağlayacağız.

**Alternatif:** Inline style'ları olduğu gibi taşımak — bakımsız sonuç verirdi, elendi.

---

## 2026-08-21 — Stil yöntemi: Tailwind + CSS değişkenleri

**Karar:** Token'lar `globals.css` içinde CSS özel değişkeni olarak tanımlanır,
Tailwind teması bunlara bağlanır. Bileşenler Tailwind sınıfı kullanır, sabit hex yazmaz.

**Neden:** Tailwind v4 zaten kurulu. Tek renk kaynağı olur; tema değişimi token
dosyasından yapılır. Inline style taşımak 1687 noktada bakım yükü demekti.

**Sonucu:** Bileşende sabit renk kodu görülürse hatadır — token'a bağlanmalı.

---

## 2026-08-21 — Önce tasarım sistemi ve ana sayfa, veri mock

**Karar:** Sıra: (0) token + tema, (1) tasarım sistemi bileşenleri, (2) kabuk
header/footer, (3) ana sayfa, (4) liste + detay, (5) blog/hakkımızda/tekne sahibi,
(6) mock veri katmanı → API sözleşmesi taslağı.

**Neden:** Backend'de yalnızca `/api/health` var; gerçek veriye bağlanmak mümkün değil.
Mock katman aynı zamanda API sözleşmesinin ilk taslağını üretir ve API tarafına girdi olur.

**Sonucu:** Mock veri şekli ile ileride yazılacak API sözleşmesi ayrışabilir. Faz 6'da
sözleşme taslağı çıkarılıp API tarafıyla karşılaştırılmalı → [[durum]]

---

## 2026-08-21 — Görünen marka adı "Daily Cruising" (ayrık)

**Karar:** `brand.name = "Daily Cruising"` — iki kelime, ayrık yazım.

**Neden:** Mert son talebinde bu yazımı kullandı. Daha önce "DailyCruising" (bitişik)
denmişti; repo adları hâlâ bitişik (`DailyCruising.API` / `.Web`) ama **görünen ad**
ayrık.

**Sonucu:** Değer tek sabitte (`src/lib/brand.ts`); yazım değişirse tek satır.
Repo adlarıyla görünen ad kasıtlı olarak farklı.

---

## 2026-08-22 — Tasarım kaynağı: aynı proje, tam kopyası yerelden okunuyor

**Karar:** Tasarım `r-ht-m-temeller-sayfas/project/Rihtim.dc.html` dosyasından okunuyor.
`DesignSync` MCP aracı **kaynak kayıt olarak geçerli** (proje bu araçla bulundu:
`get_project`, `list_files`, `get_file`) ama dosya içeriği için yerel kopya kullanılıyor.

**Neden:** MCP'nin `get_file` çağrısı **256 KiB'de kesiyor** ve bunu `truncated: true`
ile bildiriyor. Ölçüldü:

| | Karakter | Oran |
|---|---|---|
| MCP'nin verebildiği | 259.712 | %19,6 |
| Gerçek dosya | 1.327.181 | %100 |
| **Erişilemeyen** | **1.067.469** | **%80,4** |

**Denklik kanıtlandı:** Ortak 259.712 karakterin SHA-256'sı iki kaynakta da
`c6767c5a37880e55d2ce3fec0fb313a8` — yerel dosya MCP projesinin ta kendisi, sadece
eksiksiz hali. Hangisinden okunduğu içerik açısından fark etmiyor.

**Kesik sürümle çalışırken üç şey yanlış bilindi:**

1. Tasarımda 9 sayfa sanıldı — **20 sayfa var** (yönetim paneli, işletme paneli,
   destek paneli, hesap alanı, ticket ekranları hiç görünmüyordu).
2. "Footer yok" sanılıp uydurma footer yazıldı — footer satır 8090–8137'de duruyor.
3. Hero ve header davranışı yanlış uygulandı.

**Sonucu:** Bir aracın kırptığı çıktıya dayanarak "bu tasarımda yok" demek hatalıymış.
`truncated: true` alanı görülmüştü ama etkisi küçümsendi — %80'lik bir kayıptı.

**Projedeki diğer iki dosya okundu, ikisinde de uygulanacak şey yok:**
- `_ds_bundle.js` (315 B) — `"components":[]`, boş. Taşınacak paylaşılan bileşen yok.
- `support.js` (1911 satır) — Design Canvas çalışma zamanı (`<sc-if>`, `<sc-for>`,
  `{{ }}` yorumlayıcısı). Tasarım aracının motoru; uygulama kodu değil, Next.js
  yerini alıyor.

---

## 2026-08-22 — Ana sayfada header şeffaf, hero açık renkli

**Karar:** Ana sayfada header `fixed` ve şeffaf, hero'nun üstüne biner; 40px
kaydırınca beyaza döner ve `sticky` olur. Hero zemini **açık** gradyan
(`#BFD3C6 → #DCE6D9 → #E9E2D2`), yazılar koyu + beyaz metin gölgeli, `min-h-screen`.

**Neden:** Tasarımın durum mantığı böyle (satır 8221–8232 ve 267–273). Önceki
uygulamada header her sayfada beyaz, hero koyu gradyan + beyaz yazıydı — tamamen ters.

**Sonucu:** Hero animasyon gecikmeleri de tasarımdan alındı: metin 900ms,
arama kutusu 1080ms — açılış perdesi biterken devreye giriyorlar.

---

## 2026-08-22 — Kaydırma durumu için useSyncExternalStore

**Karar:** Header'ın kaydırma durumu `useEffect` + `setState` yerine
`src/lib/use-scroll-past.ts` içindeki `useSyncExternalStore` tabanlı hook ile okunuyor.
Çerez tercihi de aynı desende (`src/lib/cookie-consent.ts`).

**Neden:** Next 16'nın `react-hooks/set-state-in-effect` kuralı efekt içinde senkron
`setState` çağrısını **hata** olarak reddediyor (zincirleme render riski).

**Sonucu:** Tarayıcı dışı durum (kaydırma, localStorage) okunacaksa bu desen kullanılacak.

---

## 2026-08-22 — "Geçirmek" = front-end'e uygulamak, tasarım projesine yazmak değil

**Karar:** `Rihtim.dc.html` tasarımı **yalnızca Next.js kod tabanına** uygulanır.
claude.ai/design projesine hiçbir dosya yazılmaz, kopyalanmaz, yeniden adlandırılmaz.

**Neden:** Mert `/plan` çağrısında "bu tasarımın aynısını **front-end klasörüne**
geçirmeni istiyorum" dedi; hedef açıkça kod tabanı. 2026-08-22'de doğrudan soruldu ve
"Front-end'e geçir" cevabı verildi.

**Alternatif:** Tasarım projesinde "Daily Cruising" adlı kopya oluşturmak — reddedildi.

**Sonucu:** `DesignSync` yalnızca **okuma** için kullanılır (`get_project`,
`list_files`, `get_file`). `finalize_plan` / `write_files` / `delete_files`
çağrılmaz — Mert'in tasarım kaynağına dokunulmaz.


---

## 2026-08-22 — "Sayfa uygulandı" ölçütü: bölüm sayımı, ekran değil

**Karar:** Bir tasarım ekranının uygulandığını söylemek için rotanın açılması
yetmez; tasarımdaki **bölüm başlıkları ve etkileşimli öğeler tek tek** kodda
aranır. Ölçüm `_araclar/` dışında, tasarım dosyasından başlık çıkarıp kaynak
ağacında aratarak yapılır.

**Neden:** 2026-08-21'de "19/19 sayfa tamamlandı" denmişti. 2026-08-22'de ölçüldü:
tasarımdaki 155 bölüm başlığının **106'sı kodda yoktu**. Rotalar açılıyordu,
menüler doğruydu — ama liste tablolarının açtığı **detay ekranları** hiç yazılmamıştı.
"Sayfa açılıyor" ile "sayfa uygulandı" karıştırılmış.

**Ayrıca aynı gün yakalananlar (hepsi ana sayfa header'ında):**

| Eksik | Tasarımdaki hâli |
|---|---|
| Arama kutusu | Hap biçimli (`radius:200px`), SVG büyüteç, yazınca "Öneriler" paneli (6 satır + "tüm sonuçlar →"). Kodda: köşeli kutu, `⌕` karakteri, panel yok |
| Turlar menüsü | Akordiyon — "Günlük Turlar ›" / "Özel Turlar ›" yerinde açılıyor; "Konaklamalı" ve "Haftalık" grup dışında. Kodda: düz liste, hepsi bir arada |
| Özel teklifler | Menüde `%` rozetli ayrı giriş. Kodda: **hiç yoktu** |

**Sonucu:** `build` ve `lint` bu üçünü de temiz geçirdi — yine yalnızca tasarımla
yan yana koyunca görüldü → [[web-tailwind-katman-tuzagi]] ile aynı sınıf hata.
Bundan sonra her ekran için başlık sayımı yapılacak.

İlgili: [[web-eksik-detay-ekranlari]] · [[durum]] · [[web-mimari]]


---

## 2026-08-22 — Doğrulama ölçütü: hesaplanmış stil karşılaştırması

**Karar:** Bir ekranın tasarıma uyduğunu söylemek için metin/başlık sayımı yetmez.
Tasarım `python3 -m http.server` ile açılır, iki sayfadan da `getComputedStyle`
çıktısı alınır ve karşılaştırılır → [[web-tasarimi-tarayicida-acmak]]

**Neden:** Başlık sayımı 155/155 "tamam" derken ana sayfanın 14 bölümünden 11'inde
zemin rengi, tamamında dikey dolgu (120px yerine 72px) yanlıştı. Header'da "Kayıt
ol" butonu pembeydi, tasarımda koyu. Hiçbiri metin taramasına yakalanmıyordu.

**Sonucu:** `Section` bileşenine `sea` (#E4EAE5) ve `amber` (gradyan) tonları
eklendi; `muted` `--surface-1`den `--surface-2`ye taşındı. `--surface-1` (#F8F9F8)
tasarımda hiç kullanılmıyor.


---

## 2026-08-22 — Font: DM Sans değişken sürüm, `axes: ["opsz"]`

**Karar:** `next/font/google`'ın `DM_Sans` çağrısında `weight` listesi verilmiyor;
`axes: ["opsz"]` ile değişken font yükleniyor.

**Neden:** Sabit ağırlık listesi Next'e statik kesit indirtiyor. Tasarım DM Sans'ın
`opsz 9..40` eksenli değişken sürümünü kullanıyor ve 70px başlıkta optik boyut 40'a
gidiyor. Statik kesitle harfler **%10 geniş** çıkıyor: hero başlığı 1049px yerine
956px sarması gerekirken taşıyor, ardından bütün bölümler kayıyor.

**Sonucu:** Ölçüm birebir tuttu (satır genişlikleri 956 / 338). Font seçimi
tipografiden çok **düzen** meselesi — genişlik değişince her şey kayıyor.

---

## 2026-08-22 — Bölüm boşlukları `Section` bileşenine parametre

**Karar:** `Section` bileşeni `pad` ve `tone` parametreleri alıyor; dolgu bölüm
bazında veriliyor.

**Neden:** Tasarımda tek bir dikey ritim yok (ölçüm): 72/72, 72/0, 72/56, 56/80 ve
0 (koyu ve amber bantlarda) kullanılıyor. Ayrıca iki yerde bölüm arası boşluk
**margin** ile veriliyor — zeminler farklı olduğu için padding ile aynı sonucu
vermiyor. Ayrıntı → [[web-tasarimi-tarayicida-acmak]]


---

## 2026-08-22 — Dalga dikişi ana sayfadan kaldırıldı (bilinçli sapma)

**Karar:** `WaveStitch` bileşeni ve tek kullanımı (hero altı) silindi.
`src/components/ui/wave-stitch.tsx` dosyası artık yok.

**Neden:** Mert doğrudan istedi: *"ana sayfada şunu sil"* — öğenin HTML'ini
göstererek. Tasarımda bu öğe **var** (hero'nun altında, akış içinde,
`margin-top:32px`), yani bu **tasarımdan bilinçli bir sapma**.

**Sonucu:** Sonraki karşılaştırmalarda "eksik öğe" olarak görünecek. **Geri
eklenmeyecek.** Tasarımda `height:16px;background:radial-gradient` araması tek
sonuç veriyor; o sonuç bu öğedir ve karşılığı kodda olmayacak.

**Not:** Daha önce footer'a da bir dalga dikişi eklenmişti; o tasarımda hiç yoktu,
uydurmaydı ve aynı gün kaldırıldı.

---

## 2026-08-22 — Tasarımın `<button>` siyahı kopyalandı

**Karar:** Bölge, tekne ve kategori kartlarının başlıklarında `text-black`
kullanılıyor; marka rengi `#10201C` değil.

**Neden:** Tasarımda bu kartlar `<button>` ve buton rengi miras almadığı için
başlıklar tarayıcı varsayılanı **saf siyah** render ediliyor. Ölçümde 14 metinde
fark veriyordu. Mert "birebir aynı" istedi; bu yüzden kopyalandı.

**Uyarı:** Bu bir tasarım kararı değil, tarayıcı varsayılanı. Tasarım güncellenir
ve kartlar `<button>` olmaktan çıkarsa bu da düzeltilmeli.

---

## 2026-08-22 — Tekne listesi 1320px kap kullanıyor (tek istisna)

**Karar:** `/tekneler` gövdesi sitenin 1140px'lik `Container`'ını kullanmıyor;
tasarımdaki gibi `max-width:1320px; padding:0 24px` ile daha geniş.

**Neden:** Tasarımda `max-width:1320px` **tek bir yerde** geçiyor, o da liste
ekranı (ölçüm: `grep -c max-width:1320px` → 1). Izgara `280px 1fr`, boşluk 30px.
1140 ile ölçülünce filtre paneli 70px sağda kalıyor ve üç kart sığmıyor.

**Sonucu:** `Container` değişmedi; genişlik yalnızca o sayfada satır içi verildi.
Başka sayfada 1320 görürsem bileşene çıkarılacak.

---

## 2026-08-22 — Üst şerit yüksekliği: 9px dolgu + 1.45 satır yüksekliği

**Karar:** Header üst şeridinin iç dolgusu `py-2.5` (10px) yerine `py-[9px]`,
metin `leading-[18px]` yerine `leading-[1.45]` (=18.125px).

**Neden:** Şerit 48px yerine **46.13px** olmalı. Fark yalnızca 1.87px ama header
tüm sayfaların üstünde: liste sayfasının tamamı 1.87px kayıyordu ve bu, kartlarda
"2px aşağıda" gibi görünüp yanlış yerde aranmasına yol açtı.

**Sonucu:** Sayfa yüksekliği tasarımla **tam olarak** eşitlendi (2376/2376).
Bu düzeltme bütün sayfaları etkiliyor — diğerleri ölçülürken tekrar doğrulanacak.

---

## 2026-08-22 — Taban sınıfta ezilebilir renk yazılmıyor

**Karar:** Ortak sınıf dizeleri (`boxClass` gibi) `border-line-300` benzeri
**ezilmesi gereken** değerleri içermez; renk her kullanım yerinde verilir.

**Neden:** `cn()` düz birleştirme yapıyor, **tailwind-merge değil**. `cn(boxClass,
"border-action")` çağrısında iki sınıf da CSS'e giriyor ve hangisinin kazanacağını
sınıf sırası değil, üretilen stil dosyasındaki sıra belirliyor. Geliş tarihi
alanının pembe kenarlığı bu yüzden uygulanmıyordu.

**Uyarı:** Derleyici de lint de görmez; yalnızca hesaplanmış stil ölçülünce çıkar.

---

## 2026-08-23 — Panel yan menüsünde grup açıklığı etkin modülden türetiliyor

**Karar:** `PanelShell` açılır grupları artık "hepsi açık" başlatmıyor. Bir grup,
**etkin modülü içeriyorsa** açık gelir; kullanıcı elle açıp kapattığında o tercih
geçerli olur.

**Neden:** Tasarımın kuralı bu (`Rihtim.dc.html` 8580):
`const open = s[key] === undefined ? hasActive : s[key]`. Bizde hepsi açık geldiği
için yan menü tasarımdan uzundu ve **20 modülde** sayfa yüksekliği yanlış çıkıyordu —
yan menü içerikten uzun olduğunda sayfa boyunu o belirliyor.

**Ek:** Açık grubun çocukları tasarımda kendi kabında ve **altında 4px** boşluk var
(`padding-bottom:4px`, satır 3924). Bu 4px açık grup başına birikiyordu: 2 grup açıkken
−8px, 4 grup açıkken −16px. Kaynağı görünmez, yalnızca ölçümle bulunur.

---

## 2026-08-23 — Yönetim tablolarının sütun genişlikleri tasarımdan üretildi

**Karar:** `adminLists` içindeki her sütun `w` değeri elle yazılmadı; tasarımın
başlık satırlarındaki `flex:0 0 Npx` değerleri betikle çıkarılıp sütun etiketleri
eşleşen tabloya uygulandı. Tasarımda **esneyen sütun yok** — hepsi sabit.

**Neden:** Elle yazılan değerler tutmuyordu ve tek bir yanlış genişlik satırı
sardırıp satır yüksekliğini ikiye katlıyordu: "Yolcu gönder" modülünde satır adımı
55px yerine 136px olmuştu, modül tasarımdan **624px** uzundu.

**Kabul edilen sapma:** Tasarımda geniş tablolar kartın dışına taşıyor (bir hücre
`x=1318`'de, sayfa 1280px). Biz `overflow-auto` ile kart içinde kaydırıyoruz. Satır
yükseklikleri ve sol sütunlar birebir; yalnızca en sağdaki sütunların ekran dışı
davranışı farklı. Tasarımın bu davranışı sayfaya yatay kaydırma ekliyor.

---

## 2026-08-23 — Tasarımdaki `i̇` bozuk karakteri düzeltilerek alındı

**Karar:** Tasarımda geçen `tekneleri̇ne`, `tekneleri̇ni` gibi dizeler bizde
**`teknelerine`, `teknelerini`** olarak yazıldı.

**Neden:** Tasarımdaki karakter `i` + U+0307 (COMBINING DOT ABOVE) — büyük `İ`
harfinin küçültülmesinden kalan bir bozulma, kasıtlı bir yazım değil. Birebir
kopyalamak ürüne kırık bir karakter taşırdı.

**Sonucu:** Ölçüm karşılaştırmasında bu üç dize kalıcı olarak "fark" görünecek.
Fark listesinde `i̇` içeren satırlar bu karardandır, eksik iş değildir.

---

## 2026-08-23 — Turlar menüsü tasarımdan ayrılıyor: yana açılan alt menü

**Karar (kullanıcı isteği):** Header'daki "Turlar" menüsünde
1. "Konaklamalı Tur" ve "Haftalık Tekne Turu" artık **"Özel Turlar" altında**,
2. "Günlük Turlar" ve "Özel Turlar" **hem tıklamayla hem fareyle** açılıyor,
3. alt menüler aşağı değil **yana** (`left-full`) açılıyor.

**Neden:** Kullanıcı açıkça istedi. Tasarımdan **bilerek** sapıyoruz:
`Rihtim.dc.html` 138–168'de menü katlanır (akordiyon) yapıda, iki tur grubun
dışında tek başına duruyor ve hover yok. Bu üç davranış ölçüm farkı sayılmaz —
sonraki oturumda "tasarıma aykırı" diye geri alınmamalı.

**Uygulama ayrıntısı:** Alt menü, satırın kendi kabının **içinde** duruyor ve
aradaki 6px boşluk `pl-1.5` ile o kabın içinde kalıyor. Boşluk kabın dışında
kalsaydı fare satırdan alt menüye geçerken ölü bölgeye düşer, `mouseleave`
tetiklenir ve menü kapanırdı. Ölçüldü: satır sağ kenarı ile alt menü sol kenarı
arasındaki mesafe **0px**.

**İkinci tuzak:** Komşu gruba geçerken önce `mouseleave`, sonra `mouseenter`
geliyor. `onClose` koşulsuz `null` yazsaydı yeni açılan grubu hemen kapatırdı;
bu yüzden `setGroup((g) => (g === "daily" ? null : g))` — yalnızca hâlâ açık olan
grup kendini kapatıyor.

**Veri:** `standaloneTours` kaldırıldı, iki kayıt `specialTours` sonuna eklendi.
`allTours` sırası değişmedi (bu ikisi zaten özel turlardan sonra geliyordu), bu
yüzden hero, filtreler, footer ve mobil menü etkilenmedi.

---

## 2026-08-23 — Mobil kırılımlar tasarımın kendi değerlerinden alındı

**Karar:** Tailwind'in hazır ekran adları yerine tasarımın iki kırılımı temaya
eklendi: `wide` = **1180px**, `mid` = **720px**.

**Neden:** Tasarımın durum mantığı tek eşik kullanıyor — `const wide = vw >= 1180`
(`Rihtim.dc.html` 8162) — ve ikinci bir eşik daha var: `aboutCols`, `cardCols`,
`whyCols` için `vw < 720`. Tailwind'in `lg`'si 1024, `md`'si 768; ikisi de
tutmuyor. Kırılımı yanlış yerden alırsak 1024–1180 arasında tasarımdan sapıyoruz.

**Izgara kuralları** (tasarımdan birebir):

| Izgara | ≥1180 | 720–1180 | <720 |
|---|---|---|---|
| İstatistik (`statCols`) | 4 | 2 | 2 |
| Çift blok (`pairCols`) | 2 | 1 | 1 |
| Kart (`cardCols`, `aboutCols`) | 3 | 2 | 1 |
| Panel yan menü (`adminCols`) | 248px + içerik | tek kolon | tek kolon |
| Tekne kartı (`boatCols`) | 2 | 1 | 1 |

**Kırılım vitrini hakkında düzeltme:** `isBreak` ekranını "gerçek sayfa değil"
diye atlamıştım. Uygulanacak bir sayfa olmadığı doğru ama **mobil şartnamesi
orada**: 390px mobil (tek kolon + tam ekran menü), 834px tablet (iki kart),
masaüstü dört kart. Atlarken içindeki kuralları çıkarmamak hataydı.

---

## 2026-08-23 — Geniş tablolar yalnızca dar ekranda kaydırılıyor

**Karar:** Panel tablolarının kabı `overflow-x-auto wide:overflow-x-visible`.
Masaüstünde tasarımdaki gibi kartın dışına taşıyor, dar ekranda kaydırılıyor.

**Neden:** Tasarımda kaydırma kabı yok; geniş tablo kartın dışına taşıyor. Biz
her ölçüde `overflow-auto` verince tarayıcı **15px yatay kaydırma çubuğu**
ekliyor ve sayfa yüksekliği tasarımdan sapıyor — yönetim panelinde üç modülde
15'er piksel. Dar ekranda ise taşma kabul edilemez, orada kaydırma şart.

**Uyarı:** Kaydırma çubuğunun yer kaplaması işletim sistemi ayarına bağlı;
bir ölçümde çıkıp diğerinde çıkmayabilir. "Bir anda 15px büyüdü" belirtisi
görülürse önce bu akla gelmeli.

**Yan bulgu:** Elle yazılan tablolarda `flex-1` başlık hücresine `min-w-0`
eklemek çözüm değil — hücre küçülüp metni sarıyor ve satır uzuyor.

---

## 2026-08-24 — Rota klasörleri ve sorgu anahtarları İngilizce

**Karar (Mert):** Kodda açılan her klasör ve dosya adı İngilizce olacak. 17 rota
klasörü çevrildi; sorgu anahtarları da (`?tur=` → `?tour=`, `?bolge=` → `?region=`,
`?firsat=` → `?deal=`) İngilizceye alındı.

| Eski | Yeni |
|---|---|
| `tekneler` | `boats` |
| `rezervasyon` | `booking` |
| `tekneni-ekle` | `add-boat` |
| `hakkimizda` | `about` |
| `giris` / `kayit` | `login` / `register` |
| `hesabim` | `account` |
| `hesabim/sifre` | `account/password` |
| `hesabim/rezervasyon/[kod]` | `account/reservations/[code]` |
| `destek` | `support` |
| `destek/yeni` · `destek/[no]` | `support/new` · `support/[id]` |
| `destek-paneli` | `support-panel` |
| `isletme-paneli` | `owner-panel` |
| `yonetim` | `admin` |
| `tasarim-sistemi` | `design-system` |

**Neden:** Mert kalıcı kural olarak koydu. Ayrıca Next.js App Router'da klasör adı
aynı zamanda URL olduğu için bu, **herkese görünen adres yapısını da** İngilizceye
çeviriyor. Site henüz yayında olmadığı ve dış bağlantı bulunmadığı için maliyeti
sıfır — sonradan yapılsaydı yönlendirme tablosu gerekirdi.

**Kapsam dışı bırakılan:** Tur ve bölge **slug değerleri** (`gunluk-tekne-turu`,
`bodrum`) Türkçe kaldı. Bunlar ad değil **veri kimliği**; API sözleşmesine ve
mock veriye bağlılar, değiştirmek ayrı bir karar.

**Ekranda görünen metin Türkçe kalır** — çeviri yalnızca ad ve yol düzeyinde.

---

## 2026-08-26 — Geri bildirim katmanı tasarımdan değil token setinden türetildi

**Karar:** Toast, modal, hata sayfaları, iskelet, boş durum, sayfalama, dosya
yükleme ve rezervasyon başarı ekranı `Rihtim.dc.html`'e bakılarak değil,
`globals.css` token setinden türetildi.

**Neden:** Tasarım kaynağında bunların **hiçbiri yok** — 20 ekranın tamamı mutlu
yol. Hata, yükleme, boş durum ve onay katmanı hiç çizilmemiş. Uydurmamak için
her biçim kararı var olan bir tasarım öğesinden alındı: modal perdesi
`--surface-overlay`, hata sayfası iskeleti tasarımın koyu bölüm dilinden,
başarı ekranı rezervasyon detayının `1fr 360px` yerleşiminden, hareket süreleri
yalnız `--dur-fast/base` ve `--ease`'ten.

**Sonuç:** Bunlar "tasarıma birebir" değil **"tasarım diliyle tutarlı"**. Mert
tasarımı güncellerse bu ekranlar da gözden geçirilmeli — kaynakları yok.

---

## 2026-08-26 — QR kodunu front-end üretmiyor

**Karar:** `QrCode` bileşeni QR **çizmiyor**; API'den gelen görseli (`src`)
gösteriyor, gelmediğinde ne beklendiğini yazan bir yer tutucu çiziyor.

**Neden:** İki sebep. Birincisi mimari: QR'ın içeriği rezervasyonu doğrulayan
imzalı bir belirteç, imzayı yalnız API atabilir — istemcide üretilen QR
doğrulanamaz. İkincisi doğrulanabilirlik: yerel bir QR kodlayıcı yazmak
mümkündü ama ortamda karşılaştırılacak referans kütüphane yoktu
(`qrcode`, `segno`, `qrencode` üçü de kurulu değil). **Taranamayan bir QR,
basılı biniş belgesinde yer tutucudan kötüdür** — çalışıyormuş izlenimi verir.

Yer tutucu bilinçli olarak sahte bir QR **deseni** çizmiyor; ikon + açıklama
metni basıyor.

**Sözleşme:** Alan adı `qrImageUrl`. Mutlak URL ya da `cid:` eki olmalı —
Gmail ve Outlook data URI'yi engelliyor.

---

## 2026-08-26 — E-posta şablonlarında sabit renk kodu serbest

**Karar:** `src/emails/*.html` [[web-desenler]]'in "bileşende sabit hex yazılmaz"
kuralının **tek istisnası**. Renkler token değerlerinden elle kopyalandı.

**Neden:** E-posta istemcilerinin çoğu CSS değişkenini, harici stil sayfasını ve
sık sık `<style>` bloğunu desteklemez. Aynı sebeple yerleşim `<table>` ile,
`flex`/`grid` yok, `DM Sans` yedek yığınla veriliyor.

**Bedeli:** Marka rampası değişirse bu dört dosya **elle** güncellenmeli.
Kaçınılmaz tek çift kayıt noktası budur; `src/emails/README.md` içinde de yazılı.

---

## 2026-08-26 — 403 deneysel dosya sözleşmesiyle değil normal rotayla yapıldı

**Karar:** Yetkisiz erişim ekranı `app/forbidden/page.tsx` — normal bir rota.
Next 16'nın `forbidden.tsx` dosya sözleşmesi kullanılmadı.

**Neden:** `forbidden.tsx` `experimental.authInterrupts` bayrağını istiyor ve
doküman `version: experimental` diyor. Kimlik doğrulama henüz yok (→ [[durum]]
engel #1), yani bayrağın bugün getirisi sıfır. Kimlik doğrulama gelince
`forbidden()` çağrısına bağlanabilir; o zaman bayrak açılır.

**Yan bulgu — dokümana bakmasam yanlış yazacaktım:** Next 16'da `error.tsx`'in
ikinci prop'u `reset` **değil** `retry`. Eğitim verimdeki ad eski.
Kaynak: `node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`

---

## 2026-08-27 — Rota koruması: jetonlar `httpOnly` çerezde, proxy yalnız kapı

**Karar:** Kimlik akışı Next rota işleyicilerinden geçiyor. Giriş formu backend'i
doğrudan çağırmıyor; `/api/auth/login`'e POST ediyor, jetonlar orada alınıp
`httpOnly` çereze yazılıyor ve **tarayıcıya hiç dönmüyor**.

**Neden:** Jeton `localStorage`'da ya da JS'ten okunabilir bir çerezde dursaydı
tek bir XSS açığı tüm oturumları çalardı. `httpOnly` ile JS jetonu göremiyor —
tarayıcıda ölçüldü, `document.cookie` boş.

**Rol ayrı çerezde (`dc_role`), jetonun içinden okunmuyor.** Backend'de `role`
diye bir alan **yok**; rol üç alandan türetiliyor. Türetmeyi girişte bir kez
yapıp sonucu saklamak, proxy'nin her istekte JWT çözmesinden hem hızlı hem
sağlam — proxy jetonun iç yapısına hiç bakmıyor, sözleşme değişse etkilenmiyor.

**Proxy bir yetki sınırı değildir.** Jetonun imzasını doğrulamıyor; sahte
çerezle geçilebilir ama geçilince bir şey elde edilmez — asıl kapı API'de, her
istek Bearer ile gidiyor ve backend yeniden doğruluyor. Proxy'nin işi (1)
oturumsuz kullanıcıyı boş panele sokmak yerine girişe almak, (2) savunma
derinliği. **Bu ayrım yazılı olmazsa ileride "proxy var, güvendeyiz" denir.**

**Next 16'da dosya adı `proxy.ts`** — `middleware.ts` kullanımdan kalktı.
Dokümana bakmasam yanlış dosyayı yazacaktım; dosya sessizce hiç çalışmazdı.

---

## 2026-08-27 — Rol modeli backend'e uyduruldu: `staff` var, `admin`/`support` yok

**Karar:** Roller `customer` · `owner` · `staff`. `/admin` ve `/support-panel`
**aynı** role bakıyor.

**Neden:** İlk taslakta `admin` ve `support` ayrı iki rol yazmıştım — tasarımda
iki ayrı panel olduğu için. Backend'in gerçek modeli farklı: ikisi de
`isPlatformStaff === true` koşuluna bakıyor, ayrım **rotada değil ekran içinde**
ve `permissions` dizisinden yapılıyor (`boat.read`, `staff.manage`, …).

Ayrı iki rol tanımlasaydım backend'de karşılığı olmayan bir ayrım uydurmuş
olurdum: `dc_role=admin` ile `dc_role=support` arasındaki fark bizim
kurgumuz olurdu, sunucu ikisini de aynı görürdü. **Uydurma ayrım, olmayan bir
güvenlik hissi verir.**

`staff` ile `owner` aynı anda doğru olamaz — platform personelinin `partnerId`'si
yok, bu backend'de zorunlu kural.

---

## 2026-08-27 — Başarısız jeton yenileme asla tekrar denenmez

**Karar:** `refreshOnce` eşzamanlı yenilemeleri tek çağrıya bağlıyor ve
**başarısız yenileme tekrar denenmiyor**; çerezler silinip kullanıcı girişe
alınıyor.

**Neden:** Backend'de ölçüldü (2026-08-27): aynı yenileme jetonu ikinci kez
gönderilirse yalnız o istek düşmüyor, **oturum zinciri komple kapanıyor** — bir
önceki adımda alınan taze jeton da ölüyor. Tasarım böyle: çalınmış jeton
saptanınca zincir kapatılıyor.

Sonuç iki kural: (1) eşzamanlı iki `401` aynı jetonla yenilemeye giderse
kullanıcı **kesin** çıkışa düşer, sıraya alma şart; (2) **"hata olursa bir daha
dene" kodu yazılmayacak** — burada yeniden deneme, düzeltmeye çalıştığı şeyi
kesinleştirir.

Kapsam uyarısı: tek-uçuş kilidi **süreç içi**. Birden fazla sunucu örneğinde
yarış yine mümkün; ölçeklenince paylaşılan kilit gerekir.

---

## 2026-08-27 — Backend'in beş ayrı hata şekli var, hepsi tek yerde ele alınıyor

**Karar:** `api.ts` içindeki `hataOku` beş şekli de tanıyor.

| Durum | Gövde |
|---|---|
| Uygulama hatası | `{ error }` |
| Eşzamanlılık çakışması | `{ error, code: "ConcurrencyConflict" }` |
| JWT ara katmanı 401 | **boş** + `WWW-Authenticate: Bearer` |
| Doğrulama 400 | RFC 7807 `{ type, title, status, errors, traceId }` |
| Hız sınırı 429 | **boş**, `Retry-After` **yok** |

**Neden:** Son ikisini backend saymamıştı, ölçerken çıktı. İkisi de gövdesiz ya
da farklı şekilde; `res.json()` doğrudan çağrılsa ikisinde de patlardı.

**429 özellikle ayrı ele alınıyor:** kullanıcıya "tekrar dene" demek yanlış
olurdu — tekrar dener, yine 429 alır ve sayacı uzatır. `Retry-After` olmadığı
için "birkaç dakika" demekten başka seçenek yok, bu backend'e bildirildi.

**Giriş hatasında backend'in metni aynen geçirilmiyor:** "böyle bir kullanıcı
yok" ile "parola yanlış" ayrımı hesap sayımına (user enumeration) izin verir.
Tek ve aynı mesaj dönüyor.

---

## 2026-08-27 — Çift gönderim kapısı `useState`'te değil `ref`'te

**Karar:** `useSubmitGuard` kilidi bir `useRef` üzerinde tutuyor. `busy` durumu
yalnız **görünüm** için var — kapı için değil.

**Neden:** `setBusy(true)` eşzamanlı değil. Aynı kare içinde gelen iki tıklama
da `busy === false` görür ve **ikisi de geçer**; durum güncellemesi henüz
uygulanmamıştır. Ref anında yazılır, ikinci çağrı oradan döner.

Bu, "düğmeyi `disabled` yaparım, yeter" varsayımının da cevabı: `disabled`
render'dan sonra devreye giriyor ve forma **Enter** ile de gelinebiliyor. Kapı
görünümde değil mantıkta durmak zorunda.

**Ölçüldü:** vitrinde aynı karede üç tıklama → **1 istek**. `useState` tabanlı
bir kapıda 3 olurdu.

**Sınır:** Bu istemci koruması, sunucu idempotency'sinin yerini **tutmaz**.
Ağ tekrarı, sekme kopyalama ve geri tuşu bu kapıdan geçmez. Gerçek çözüm
`POST /api/reservations`'a idempotency anahtarı eklemek → `durum.md` engel 9.

---

## 2026-08-27 — Rezervasyon düğmesi `Button` primitifine taşınmadı

**Karar:** `booking-form.tsx`'teki "Ödemeye geç" düğmesi ham `<button>` kaldı.

**Neden:** Tasarımdaki ölçüsü 330×55, dolgu 16px, kenarlık yok. `Button`
primitifi `h-12`/`h-14` sabit yükseklik ve `px-5`/`px-7` veriyor. Eşitlemek için
`h-auto p-4 border-0` geçmek gerekirdi — ama **`cn()` tailwind-merge değil, düz
birleştirme**: `h-14` ile `h-auto` aynı sınıf dizesinde durur ve hangisinin
kazandığını sınıf sırası değil **CSS dosyasındaki sıra** belirler. Öngörülemez.

Aynı sebeple giriş formunun 52px'lik düğmesi de sarılmadı.

**Sonuç:** Yükleme davranışı primitife bağlı değil, **kancaya** bağlı. Ham
düğmeler de `useSubmitGuard` + `Spinner` kullanarak aynı korumayı alıyor.
Primitifi kullanamamak korumayı kaybettirmiyor.

---

## 2026-08-27 — Yükleme etiketi: genişlik sabitliği çağıranın seçimi

**Karar:** `Button`'da `loading` etiketi **korur**, gösterge üstüne biner ve
genişlik sabit kalır. `loadingLabel` verilirse etiket değişir ve genişlik oynar.

**Neden:** İkisi de bazen doğru. Tabloda ya da yan yana düğmelerde genişlik
oynaması yerleşimi sıçratır; tek başına duran bir gönder düğmesinde
"Gönderiliyor…" yazması daha açıklayıcıdır. Tek doğru olmadığı için seçim
çağıranda bırakıldı.

**Erişilebilirlik tuzağı — yakalandı ve düzeltildi:** İlk sürümde hem görünür
`loadingLabel` hem de `role="status"` canlı bölgesi basılıyordu. Ekran okuyucu
metni **iki kez** okurdu; `textContent` de `"Gönderiliyor…Gönderiliyor…"`
çıkıyordu. Canlı bölge artık **yalnız etiket görünmediğinde** basılıyor.
Ölçümde yakalandı, gözle görülmüyordu.

---

## 2026-08-27 — `W-04` bölündü: "API bağlantısı" tek görev olamaz

**Karar:** `W-04` iptal edildi, yerine **on üç yapılabilir + on API bekleyen**
görev açıldı (`W-14`, `W-15`…`W-30`, `W-31`…`W-40`, `W-42`).

**Neden:** Tek satır olarak durduğu sürece hangi parçanın **bugün
yapılabildiği**, hangisinin **uç beklediği** görünmüyordu. Backend görüşmesi ve
canlı ölçüm sonrası ikisi kesin olarak ayrıldı: bir kısmının uçları hazır, bir
kısmının **hiç yok** ve yazılmadan başlanırsa sahte veriyle ikinci kez yapılır.

Ölçüm üç bağımsız kaynaktan yapıldı ve **üçü de aynı sonucu verdi**: backend
oturumunun canlı ölçümü, `openapi.json` + controller kaynağı taraması, ve
front-end mock veri haritası. Tek kaynağa güvenilmedi.

---

## 2026-08-27 — Üretilen TypeScript tiplerine körlemesine güvenilmeyecek

**Karar:** `W-12` tip üretimi yazılacak ama **yanıt tipleri elle yazılacak** ve
üretilen istek tipleri de gözden geçirilecek.

**Neden — dördü de ölçüldü:**

1. **Yanıt şeması hiç yok.** 85 işlemin tamamı `"200": {"description":"OK"}`.
   Controller'lar `Task<IActionResult>` dönüyor, `[ProducesResponseType]`
   hiçbirinde yok. Üretilen istemci `unknown` yanıt verir
2. **Enum'lar belgede `integer`, telde `string`.** `SearchSort` belgede
   `{"type":"integer"}` ama canlıda `?sort=PriceAsc` çalışıyor. Üretilen tip
   `number` der, gönderilmesi gereken `string` — **derleyici bunu yakalamaz,
   çalışma zamanında 400 alınır**
3. **`decimal` → `["number","string"]` union.** Her para alanı `number | string`
   çıkar, doğrudan aritmetik yapılamaz
4. **Sayfalama casing'i iki uçta farklı:** `/api/search` PascalCase
   (`Page`/`PageSize`), `/api/boats/{slug}/reviews` camelCase

**İyi haber:** yanıtların çoğunun C# `record` karşılığı var
(`Application/**/*Contracts.cs`). Elle yazmak tahmin değil **birebir çeviri**;
gerçekten anonim olan yalnız 18 uç.

**Sonuç:** "tip üretimi kurulunca sözleşme güvenli olur" varsayımı bu projede
**yanlış**. Üretim, elle yazımın yerine değil **yanına** geliyor.

---

## 2026-08-27 — Zaman damgaları UTC, arayüzde çevrilecek

**Karar:** API'den gelen her `date-time` `Europe/Istanbul`'a çevrilerek
gösterilecek; ham damga hiçbir yerde basılmayacak.

**Neden:** Bütün damgalar `+00:00` geliyor. Kiralama tipi **09:00–17:00** olarak
tanımlıyken yanıtta `06:00:00+00:00`–`14:00:00+00:00` çıkıyor. Ham basılırsa
müşteriye **3 saat erken** söylenir — iskeleye yanlış saatte giden müşteri
demektir. Sadece-tarih alanları (`departureDate`) offset taşımıyor, onlara
çevrim uygulanmaz; ikisi karıştırılırsa tarih bir gün kayar.

---

## 2026-08-27 — Otorite tasarımdan backend'e geçti

**Karar (Mert):** *"Tasarımımız eksik olabilir çünkü bir temel olması adına
yaptık zaten. Sen çoğunlukla back-end tarafına odaklanarak ona göre tasarım
kısmını geliştir."*

Bu, 2026-08-21'den beri süren **"tasarıma birebir"** ilkesini iş kapsamı
açısından **değiştirir**: uç noktası varsa ekran yazılır, tasarımda karşılığı
olmaması artık gerekçe değil **görev**.

**Neyi değiştirmez:** var olan 19 ekranın tasarıma sadakati. Uygulanmış bir
ekranı "daha iyi" diye değiştirmek hâlâ sapmadır. Değişen, **olmayan ekranlar**
için ne yapılacağı.

**Neden:** Tasarım 2026-08-21'de çizildi; domain kararlarının çoğu 22–24
Ağustos'ta alındı. Yani tasarım, kendisinden **sonra** verilmiş kararları
bilemezdi. En net örnek: 23 Ağustos'ta *"iletişim telefonla değil sistem içi
mesajlaşmayla"* kararı alındı ve backend 7 uç yazdı — tasarımda o ekran yok,
olamazdı da.

**Görev listesi bu ayrıma göre yeniden kuruldu** → [[web-gorevler]]:
bağla (13) · ekran yaz (11) · veri eksik (2) · uç yok (12) · altyapı (1).

**Ekran yazarken kaynak:** `globals.css` token seti ve var olan bileşenler.
Geri bildirim katmanı (`W-10`) aynı yolla yapıldı ve tutarlı çıktı — yöntem
kanıtlı → 2026-08-26 kararı.

---

## 2026-08-27 — Eksik ekranların en kritiği: biniş (QR okutma)

**Bulgu:** `POST /api/boarding/scan` ve `/manual` hazır, izin `boarding.scan`
tanımlı — ama **işletme panelinde biniş modülü hiç yok.**

**Neden önemli:** Tasarımın her yerinde "iskelede QR'ını okut, varışın anında
onaylanır" yazıyor. Ana sayfada adım anlatımı var, rezervasyon detayında QR
kartı var, e-posta şablonunda QR var. **Müşteri tarafı baştan sona anlatılmış;
tekne sahibinin okutacağı ekran hiç çizilmemiş.**

Yani QR akışı tasarımda **yarım**: kod üretiliyor, gösteriliyor, e-postayla
gönderiliyor — ama okutulacak yer yok. Bu, tasarımın "temel" olduğunu gösteren
en net örnek.

`W-43` olarak açıldı: kamera · klavye/el terminali · elle giriş.

---

## 2026-08-27 — Tarayıcı backend'i doğrudan çağırmaz, vekilden geçer

**Karar:** İki istemci var. Sunucu bileşenleri `lib/api/client.ts` kullanır;
tarayıcı `lib/api/browser.ts` üzerinden `/api/dc/*` vekiline gider.

**Neden:** Jetonlar `httpOnly` çerezde — tarayıcıdaki JS onları **okuyamıyor**.
Okuyabilseydi tek bir XSS açığı bütün oturumları çalardı. Jetonu tarayıcıya
vermemenin bedeli bir vekil katman; karşılığı XSS'e kapalı bir oturum. Ölçüldü:
vekil eklendikten sonra da `document.cookie` **boş**.

**Vekil yetki yükseltmesi değil:** eklenen jeton kullanıcının kendi jetonu,
backend her istekte yeniden yetkilendiriyor. Buranın işi jetonu göstermeden
isteğe iliştirmek.

**Yine de izinli yol listesi var.** Serbest bir vekil her ucu çağrılabilir
yapardı; ayrıcalık kazandırmaz ama niyet edilmemiş bir yüzeyi açık bırakmanın
faydası da yok. Listede olmayan yol `404` döner — ölçüldü.

**Alternatif elendi:** jetonu `localStorage`'a ya da JS'ten okunabilir çereze
koymak. Vekil katmanını ortadan kaldırırdı ama XSS'te oturum çalınabilir olurdu.

---

## 2026-08-27 — Backend'in Türkçe hata metni doğrudan basılmaz

**Karar:** `hataMetni()` bilinen `code` değerlerini kendi metnimize çeviriyor;
backend'in mesajı yalnız **bilinmeyen kod** için son çare.

**Neden — üçü de ölçülmüş:**
1. Backend metinleri **sözleşme değil**; 2026-08-27'de yorum dönüşümü sırasında
   elden geçtiler, yarın yine değişebilirler
2. Bazı durumlarda **gövde hiç yok** — `401` (JWT ara katmanı) ve `429` (hız
   sınırı) `content-length: 0` dönüyor. Basılacak metin yok, üretmek zorundayız
3. Giriş hatasında backend'in ayrımını geçirmek **hesap sayımına** izin verir

**`429` özel:** `Retry-After` başlığı gelmiyor, süre bilinmiyor. "Birkaç dakika"
deniyor, **sayı uydurulmuyor**; "tekrar dene" düğmesi de konmuyor çünkü tekrar
deneme sayacı uzatıyor.

---

## 2026-08-28 — Oturum başlıkta rotadan değil çerezden okunuyor

**Karar:** `SiteHeader` ve `MobileMenu` gerçek oturum kullanıcısını prop olarak
alıyor. Kök yerleşim `oturumKullanicisi()` ile bir kez okuyup geçiriyor.

**Neden — önceki hâli bir tahmindi:**

```ts
const authed = ["/account", "/support", "/owner-panel", "/support-panel", "/admin"]
  .some((r) => pathname === r || pathname.startsWith(`${r}/`));
```

Yani *"hesap sayfasındaysa giriş yapmıştır"*. Kimlik doğrulama yokken tek
seçenekti ve tasarımın o ekranlarda başlığı oturum açık göstermesini taklit
ediyordu. Artık gerçek çerez var; tahmin kalırsa **çıkış yapmış kullanıcı
`/account`'a gidince kendini giriş yapmış görür.**

**`cache()` ile sarıldı:** aynı render geçişinde başlık, sayfa ve panel kabuğu
üçü de çağırsa `GET /api/auth/me` **bir kez** gidiyor.

**Misafirde hiç istek atılmıyor** — `erisimJetonu()` çerez yoksa doğrudan `null`
döner. Ölçüldü: oturumsuz ana sayfa yüklemesinde dev günlüğünde `auth/me`
çağrısı **0**.

---

## 2026-08-28 — "Onaylı hesap" mührü gerçek doğrulamaya bağlandı

**Karar:** Hesap sayfasındaki mavi onay mührü yalnız `emailVerified === true`
ise basılıyor.

**Neden:** Tasarımda mühür **koşulsuz** duruyordu — her hesap onaylı görünürdü.
`GET /api/auth/me` gerçek alanı döndürüyor ve yeni kayıtlarda `false` geliyor.
Doğrulanmamış hesaba "onaylı" mührü basmak **yanlış bilgi**; kullanıcı e-posta
doğrulama adımını atlamış olduğunu fark edemez.

Başlıktaki açılır menüye de "E-posta doğrulanmadı" satırı eklendi. Doğrulama
akışının kendisi ayrı görev (`W-44`).

---

## 2026-08-28 — Çıkış düğmesi tasarımda vardı ama çıkış yapmıyordu

**Karar:** İki yerdeki "Çıkış yap" bağlantısı `LogoutButton` bileşenine
çevrildi; `/api/auth/logout`'a POST edip çerezleri sildiriyor.

**Neden:** İkisi de `<Link href="/">` idi — **görünüşte çıkış, gerçekte yalnız
ana sayfaya gidiş.** Kullanıcı çıktığını sanır, oturumu açık kalırdı. Ortak
bilgisayarda bunun bedeli, bir sonraki kişinin hesaba erişmesi.

Ağ hatasında da çerezler siliniyor: kullanıcıyı ekranda tutmak, sunucudaki
yenileme zincirinin açık kalmasından kötü — o zincir zaten ilk yenileme
denemesinde `401` alıp temizlenir.

Bu, tasarımın "temel" olduğunu gösteren ikinci örnek: düğme çizilmiş, davranışı
yok. (Birincisi biniş ekranıydı — `W-43`.)

**`router.refresh()` şart:** başlık sunucu bileşeninden besleniyor. Yalnız
yönlendirme yapılsa kullanıcı çıkmış ama **adı ekranda durur** görünürdü.

---

## 2026-08-28 — Kimliksiz uçlar vekilden geçmez, doğrudan çağrılır

**Karar:** `pricing/quote`, `reservations`, `payments/*` tarayıcıdan
**doğrudan** backend'e gidiyor. Vekil (`/api/dc/*`) yalnız **jeton gerektiren**
uçlar için.

**Neden — bu bir hız sınırı gereği, mimari tercih değil.** Backend'in kimliksiz
politikaları `RemoteIpAddress` ile bölümleniyor ve `rezervasyon` kovası
**15 dakikada 10**. Vekilden geçen her istek backend'e **Next sunucusunun
IP'siyle** ulaşır — yani **bütün site tek kullanıcı sayılır ve 15 dakikada 10
rezervasyonla sınırlanır.** Geliştirmede hiç görünmez; yayında ilk yoğun
saatte görünür ve suçsuz kullanıcılar `429` alır.

Vekilin tek işi `httpOnly` çerezdeki jetonu iliştirmek. **Jeton gerektirmeyen
uçta vekilin faydası yok, zararı var.**

**`X-Forwarded-For` göndermiyoruz.** Backend `ForwardedHeaders` +
`KnownProxies` ile karşı tarafı hazırlamadan gönderilen başlık ya işe yaramaz
ya da sınırı tamamen deler. Bu bir güvenlik sınırı ve backend'in alanı.

**Kalan risk:** `/boats` araması sunucuda render ediliyor, yani `fiyat` kovası
(dk/60) hâlâ tek IP'den tüketiliyor. Bilinçli: sunucu render'ı SEO ve ilk
yükleme için gerekli. Backend `KnownProxies` çözümünü uygulayınca kapanacak.

---

## 2026-08-28 — Rezervasyon üç adımlı sihirbaz değil tek ekran

**Karar:** Tasarımın üç adımlı akışı (tur+kişi → iletişim → ödeme) **tek
ekrana** indirildi.

**Neden:** Gerçek uçlar üç adım gerektirmiyor. `pricing/quote` **bağlayıcı
değil** — saklanacak bir teklif yok, fiyat rezervasyon anında yeniden
hesaplanıyor. Rezervasyon ve ödeme başlatma tek gönderimde zincirleniyor.
Üç adımlı sihirbaz kullanıcıya iki gereksiz tıklama ve iki ekran daha
yaptırırdı; karşılığında hiçbir şey kazandırmıyordu.

**Sıra dışı yanıt yarışı:** parametreler hızlı değiştiğinde eski teklif sonra
dönüp **yanlış fiyatı ekranda bırakabiliyordu**. Her istek `AbortController`
ile iptal ediliyor ve yanıt yalnız kendi parametre anahtarıyla eşleşirse
yazılıyor. Ayrı bir "yükleniyor" durumu tutulmuyor; yüklenme, yüklenmiş
anahtarın geçerli anahtardan farklı olmasından türetiliyor.

---

## 2026-08-28 — Geniş tablolar her ölçüde kart içinde kaydırılıyor

**2026-08-23 kararını iptal eder.**

**Karar:** Panel tablolarının kabı artık her ölçüde `overflow-x-auto`;
`wide:overflow-x-visible` kaldırıldı.

**Neden eski karar verilmişti:** Tasarımda kaydırma kabı yoktu ve geniş tablo
kartın dışına taşıyordu; her ölçüde `overflow-auto` vermek 15px kaydırma
çubuğu ekleyip **sayfa yüksekliğini tasarımdan saptırıyordu**. O zaman ölçüt
tasarıma birebir uymaktı.

**Neden değişti:** Mert 2026-08-27'de otoriteyi tasarımdan backend'e taşıdı
(*"tasarımımız eksik olabilir, bir temel olması adına yaptık"*). "Tasarım da
böyle yapıyor" artık bir gerekçe değil.

Ve gerçek maliyet ölçüldü: 1280px'de işletme panelinin finans modülünde
**sayfanın tamamı 63px yana kayıyordu**. Kartın içinde kaydırılması gereken bir
tablo, bütün sayfayı kaydırıyordu — masaüstünde açık bir kusur.

**Ölçüldü:** değişiklikten sonra genel bakış, finans, rezervasyonlar ve
değerlendirmeler modüllerinin dördünde de yatay taşma **0**.

**Eski kararın uyarısı hâlâ geçerli:** kaydırma çubuğunun yer kaplaması
işletim sistemi ayarına bağlı; "bir anda 15px büyüdü" belirtisi görülürse önce
bu akla gelmeli.

---

## 2026-08-28 — Hakediş ekranı kapatıldı, uyarı yeterli değildi

**Karar:** İşletme panelinin finans bölümü tamamen kaldırıldı; yerine
"hazırlanıyor" mesajı ve destek telefonu kondu.

**Neden:** Bölümde "Ödendi", "Aktarıldı" ve "3 iş günü içinde IBAN'ınıza"
yazıyordu; hepsi tasarımdan gelen mock ve **hiçbir şeye dayanmıyordu**.
`LedgerEntries` ve `Payouts` dolu ama okuyan uç yok; üstelik `A-41` açılana
kadar para işletmeye **zaten gitmiyor**.

**Önce uyarı bandı eklendi, sonra yetersiz bulundu:** uyarının altında hâlâ
sahte tutarlar ve "Ödendi" rozetleri duruyordu. İşletme sahibinin parasının
yolda olduğunu sanması, ekranın hiç olmamasından kötü. Backend oturumu da
bağımsız olarak aynı sonuca vardı ve kapatılmasını istedi.

**Bu, diğer mock bölümlerden farklı:** öbürleri eksik ekran, bu **yanlış bilgi
gösteren** ekrandı. Ayrım önemli — eksik bölümler yerinde bırakıldı.

---

## 2026-08-28 — Görsel optimize edici yerel IP'ye yalnız adres yerelse açılıyor

**Karar:** `next.config.ts` içinde `images.dangerouslyAllowLocalIP`, ortam
değişkenine değil **`NEXT_PUBLIC_MEDIA_URL`'in kendi ana makine adına** bakarak
açılıyor:

```ts
const yerelKaynak = ["localhost", "127.0.0.1", "::1", "[::1]"].includes(hostname);
```

**Neden:** Next 16 optimize ediciye özel IP'ye çözülen adresi vermiyor
(`hostname resolved to private IP` → **400**), çünkü kapı açık olsaydı biri
bizim `/_next/image` uç noktamıza iç ağ adresi verip ağ taraması yapabilirdi —
klasik SSRF. Geliştirmede MinIO tam olarak orada (`localhost:9000`) durduğu
için kapının açılması gerekiyor.

**Neden `NODE_ENV` değil:** `NODE_ENV` yanlış ayarlanabilir ve o zaman kapı
yayında açık kalır. Adresin kendisine bakmak bunu imkânsız kılıyor: yayında
`NEXT_PUBLIC_MEDIA_URL` gerçek bir alan adı olacak, koşul kendiliğinden `false`
olacak. Karar bir **ortam tahmini** değil, **ölçülebilir bir olgu** üzerine
kuruldu.

---

## 2026-08-28 — Sıralama isteğinde `coverId` gönderilmiyor

**Karar:** `PUT /api/partner/boats/{id}/media/order` çağrılırken `coverId`
alanı **yalnız kapak gerçekten değiştirilecekse** gönderiliyor. Sürükleme /
sıra değiştirme isteklerinde alan hiç konmuyor.

**Neden:** Bu uçta 2026-08-28'e kadar `coverId` yoksa **yeni sıranın ilk
elemanı kapak oluyordu**. Yani sırayı değiştiren kullanıcı, seçtiği kapağı
istemeden kaybediyordu — belirtmediği, ekranda görmediği, geri alamayacağı bir
değişiklik. Backend'in kendi XML belgesi bile bu yanlış davranışı doğru diye
tarif ediyordu.

Backend oturumuna sorulunca kaynağa bakıldı, davranış **hata olarak kabul
edilip düzeltildi**: `coverId` yoksa mevcut kapak korunuyor. İki kalıcı test
eklendi.

**Bizim tarafta da niyeti açık tutuyoruz:** kapak değişecekse söyleriz,
değişmeyecekse alanı hiç koymayız. Backend davranışı yarın tekrar değişse bile
bizim isteğimiz belirsiz kalmaz.

**Ölçüldü:** kapağı ikinci sıraya taşıyan bir sıralamadan sonra sunucuda
`sortOrder 1 · isCover true` — kapak görselle birlikte taşındı, ilk sıraya
atlamadı.

---

## 2026-08-28 — Kiralama tipi seçicisi yok, her tipin kendi düğmesi var

**Karar:** Tekne detayında kiralama tipleri **liste** olarak basılıyor; her
satırın kendi fiyatı ve kendi "Rezervasyona geç" bağlantısı var. Bir seçici
(radyo / sekme) konmadı, yan panel seçime bağlanmadı.

**Neden:** Üç sebep, sırayla:

1. **JavaScript'siz çalışmaz.** Seçici istemci durumu ister; her satırın kendi
   bağlantısı olması sunucu render'ında da doğru çalışır.
2. **Seçili fiyat kaydırınca görünmez olur.** Yan panel yapışkan; kullanıcı
   tipler listesine indiğinde hangi tipin seçili olduğunu göremez ve yukarıda
   yazan tutarın hangisi olduğunu bilemez.
3. **Tipler karşılaştırmalı bir şey.** Ölçümde bir teknede kişi başı günlük tur
   (₺500) ile tekne başı 3 günlük konaklamalı (₺10.000) yan yanaydı. Seçici
   ikisinden birini gizler; liste ikisini de gösterir.

Yan panel yine de bir tutar gösteriyor — **en ucuz tipin fiyatı**, "başlangıç
fiyatı" etiketiyle. Bu, aramadaki `fromPrice` ile aynı anlam.

**Yan etki:** Detay sayfasındaki fazladan arama isteği kalktı. Detay ucu fiyat
vermediği için her açılışta **elli kayıtlık bir `/api/search`** çağrılıp tekne
içinden bulunuyordu; üstelik arama tekne başına tek tip döndürdüğü için birden
çok tipi olan tekne yanlış görünüyordu. `aramaKaydi()` silindi.

---

## 2026-08-28 — Fiyatı olmayan teknede ödeme metinleri basılmıyor

**Karar:** Tarifesi tanımlanmamış teknede yan paneldeki "KDV dahil · tarih ve
kişi sayısına göre değişir" ve "Ödeme 3D Secure ile alınır" satırları
**gösterilmiyor**. Yerine "Bu teknenin tarifesi henüz tanımlanmadı." yazıyor.

**Neden:** İkisi de gösterilmeyen bir tutardan söz ediyordu. "Ödeme 3D Secure
ile alınır" ise telefon numarası düğmesinin altında duruyordu — olmayan bir
ödeme akışı varmış gibi. [[web-kararlar]] 2026-08-28 hakediş kararıyla aynı
ayrım: **eksik bölüm kalır, yanlış bilgi kalmaz.**

---

## 2026-08-28 — Donanım süzgeci geri kondu, bir gün beklemişti

**Karar:** `/boats` filtre panelindeki "Teknede neler olsun" bölümü açıldı;
seçimler `?AmenityIds=a&AmenityIds=b` olarak gidiyor.

**Neden bir gün beklemişti:** Donanım listesi 2026-08-27'de dolmuştu ama
`GET /api/search` donanıma göre süzmüyordu. Filtre o gün **bilerek konmadı**:
*sessizce çalışmayan filtre, olmayan filtreden kötüdür* — kullanıcı seçtiğini
sanır, sonuç değişmez ve bunu bir hata olarak bile bildiremez. `AmenityIds`
gelince koşul ortadan kalktı.

**Kutular `append` ile yazılıyor, `set` ile değil.** Aynı adı paylaşan
denetimlerde `set` yalnız sonuncuyu bırakır; çoklu seçim sessizce tek seçime
düşerdi. Bu, yukarıdaki "sessizce çalışmayan filtre" kusurunun tam olarak
kendisi olurdu — bu kez kendi tarafımızda.

**Kullanıcıya VE mantığı yazıyla söyleniyor** ("Seçtiklerinin hepsi teknede
olmalı"). İki olanak seçip sıfır sonuç alan kullanıcı, süzgecin bozuk
olduğunu değil seçimini daralttığını anlamalı.

---

## 2026-08-28 — Kural üç halli, iki değil

**Karar:** İşletme panelindeki kural düzenlemesi **belirtilmedi / serbest /
kabul edilmiyor** olarak üç halli. Onay kutusu (var-yok) kullanılmadı.

**Neden:** Backend kural listesini **tam** kabul ediyor — gönderilmeyen kural
siliniyor. İki halli bir arayüzde "işaretsiz" hem *"bu kural yok"* hem
*"bu kural yasak"* anlamına gelirdi ve ikisi farklı şeyler: yasak bir kural
tekne sayfasında **"Kabul edilmiyor"** rozetiyle görünür, belirtilmemiş kural
hiç görünmez.

Müşteri tarafında da aynı ayrım korunuyor: `isAllowed` metnin kendisinde
geçiyor, yalnız renkte değil. "Evcil hayvan" satırını kırmızıya boyayıp yasak
olduğunu ima etmek renk göremeyen kullanıcıya hiçbir şey söylemez.

---

## 2026-08-28 — Komisyon oranı ve hakediş periyodu ön doldurulmuyor

**Karar:** Sözleşme gönderme formunda şablon, komisyon oranı ve hakediş
periyodu **üçü de boş** açılıyor. Hiçbirine varsayılan konmadı.

**Neden:** Şablon bu iki değeri taşımıyor (backend ölçtü); yani bir varsayılan
koymak **uydurmak** olurdu. Komisyon oranı bir iş kararıdır ve sözleşme metnine
yazılır: personel değiştirmeyi unutursa işletme yanlış oranla bağlanır ve bu,
imzalanmış bir belgede durur. Boş alan personeli durdurur, yanlış varsayılan
durdurmaz.

Sınırlar backend'den alındı ve istemcide de tutuluyor — komisyon 0–100,
periyot 1–90 gün. Formu doldurup gönderdikten sonra `400` görmek gereksiz.

**Mert cevapladı — 2026-08-28, karar kapandı:**

> *"Komisyon ve periyot alanı sitemizde sabit değil, her bir işletmeciye farklı
> periyotlar ve farklı komisyonlar tanımlayabiliriz."*

Yani şablona varsayılan **eklenmeyecek**. Boş açılan form bir eksiklik değil,
iş modelinin doğrudan karşılığı: oran ve periyot işletmeye göre pazarlık
konusu. Varsayılan koymak, pazarlığı gizli bir sayıya sabitlerdi.

Bu aynı zamanda `ContractTemplates`'e alan ekleme fikrini kapatıyor —
şablon **metni** taşır, **ticari koşulları** değil. Koşullar `Contracts`
satırında, sözleşme başına.

---

## 2026-08-28 — Sözleşme metni `sandbox` iframe içinde basılıyor

**Karar:** `Contracts.bodyHtmlSnapshot` ve şablon `bodyHtml` alanları
`dangerouslySetInnerHTML` ile **basılmaz**; `sandbox` özniteliği **boş** bir
`<iframe srcDoc>` içine verilir.

**Neden sunucu temizlemiyor:** Backend bunu bilerek yapmıyor ve gerekçesi
sağlam — **temizlemek dondurulmuş bir belgeyi değiştirmek olurdu.** İşletmenin
onayladığı metinle panelde görünen metin ayrışırsa, bir uyuşmazlıkta hangisinin
geçerli olduğu tartışmaya açılır. Yani yalıtma yükümlülüğü **bizde**.

**Neden gerekli:** Şablonu platform personeli yazıyor, yani ilk bakışta
"kendi kendine XSS" görünüyor. Ama bir kez kötü yazılan (ya da dışarıdan içe
aktarılan) şablon, o sözleşmeyi açan **her** personelin oturumunda çalışır —
ve o oturumlar bütün işletmeleri görebilen oturumlardır.

Boş `sandbox` her yetkiyi kapatır: betik çalışmaz, form gönderilmez, üst
pencereye ve çereze erişilmez. **Tarayıcıda doğrulandı:** `contentWindow.document`
erişimi `SecurityError` ile reddediliyor.

⚠️ **Yeni bir uç sözleşme, şablon ya da başka bir yerden gelen HTML
döndürürse aynı yalıtım zorunludur.** Bu kural bir kez uygulanıp geçilecek
bir önlem değil; metin taşıyan her uç için yeniden sorulur.

---

## 2026-08-28 — Biniş QR'ı istemcide üretilmiyor

**Karar:** Backend'in önerdiği "QR'ı rezervasyon oluşturma yanıtındaki
`boardingToken`'dan istemcide üret" ara çözümü **uygulanmadı**.

**Neden:** Jeton düz metin olarak **yalnız bir kez**, oluşturma yanıtında
dönüyor. Ödeme akışı arada dış bir sağlayıcıya tam sayfa yönlendirmesi
yapıyor, yani jetonu başarı ekranına taşımak için tarayıcı depolamasına
yazmak gerekirdi — ve o, **kaybedilirse geri üretilemeyen bir doğrulama
sırrını** diske yazmak demek.

Daha ağırı: sonuç **tutarsız** olurdu. QR yalnız ödemeden hemen sonraki
sekmede görünür; müşteri sayfayı kapatırsa, telefonundan açarsa ya da biniş
belgesini sonra yazdırırsa **QR bir daha hiç olmaz**. "Bazı müşterilerde
var, bazılarında yok" bir biniş belgesi, hiç QR olmamasından kötü: destek
hattı "benim QR'ım nerede" çağrılarıyla dolar ve kimse sebebini bilemez.

**Bugünkü davranış:** QR yerine yer tutucu, rezervasyon kodu **büyük ve
kopyalanabilir**. Kaptan elle kod okutabiliyor (`boarding/manual`), yani
biniş kilitli değil.

**Doğrusu sunucuda:** imzalı bir QR ucu ya da jetonun yeniden üretilebilir
olması. Backend `S-25` olarak Mert'e sordu → `W-66`.

---

## 2026-08-28 — Biniş belgesi korunan alandan çıkarıldı, erişim koda değil sahipliğe bağlı

**Karar:** Belge `/account/reservations/{kod}/voucher` yerine
`/reservations/{kod}/voucher` adresinde. `/account` korunan bir önek ve
**misafir kendi belgesini hiç açamıyordu** — giriş sayfasına düşüyordu.

**Neden:** Misafir rezervasyonu domainde birinci sınıf senaryo; o müşterinin
biniş belgesine erişememesi kabul edilemez. Belge zaten hesaba değil **koda**
bağlı ve sayfa sunucudan başkasının kaydını çekmiyor — korunan alanda
tutulması, koruduğu şeyden çok engellediği şeyle tanımlıydı.

**Kod tek başına hiçbir şey açmıyor.** Sayfa iki kaynaktan okuyor:

1. **Sunucu** — giriş yapmış kullanıcının **kendi** rezervasyon listesi.
   Kapsam sorgunun içinde (`Where(r => r.UserId == userId)`), bellekte
   süzülmüyor.
2. **Tarayıcı** — ödeme dönüşünde ya da sorgulama sonucunda oturum
   depolamasına yazılan özet. Kayıttaki kod adresteki kodla uyuşmuyorsa
   yok sayılıyor.

**`lookup` ucu ÇAĞRILMIYOR** ve bu bilinçli: çağrılsaydı ikinci faktörü
(e-posta/telefon) nereden alacağı sorusu çıkardı ve tek makul cevap onu
tarayıcıda saklamak olurdu — korumayı kendi elimizle zayıflatmak.

**Ölçüm matrisi** (giriş yapmış kullanıcının listesi gerçekten yüklüyken —
ilk denemede hız sınırı yüzünden liste hiç yüklenmemişti ve ekran **doğru
sonucu yanlış sebepten** veriyordu):

| Durum | Sonuç |
|---|---|
| Anonim, depo boş, misafir kodu | engellendi |
| Üye, liste **200**, başka üyenin kodu (`VBNGJXM2`) | engellendi |
| Üye, liste **200**, misafir kodu (`MC5GU38F`) | engellendi |
| Üye, kendi kodu (`RPAJWZCH`) | **açıldı** |

⚠️ **Ölçümün kendisi yanıltıcı olabilir.** İlk turda ekran "engellendi"
diyordu ama sebebi listenin `429` alması, kapsam denetimi değildi. Gerçek
bir sızıntı olsaydı o ekran "her şey yolunda" diyecekti.

**İki parçalı kural — ikisi birden gerekli:**

> Bir olumsuz sonuç, **olumsuz olmasının sebebi ölçülmeden** kanıt sayılmaz.
> Ve **olumlu durum ölçülmeden**, olumsuz sonuçların hiçbiri kanıt değildir.

İkincisi 2026-08-28'de üç kez karşılığını buldu: misafirin biniş belgesine
hiç erişememesi, ödeme ekranının sahte veri göstermesi, dosya deposundaki
`publiclyReadable` parametresinin hiç uygulanmaması. Üçü de "engelleniyor
mu" diye bakan bir gözden kaçardı; üçü de **olumlu durumun sessizce ölmesi**
idi.

⚠️ Üye-üye ve üye-misafir kapsamı **tek bir kısıttan** çıkıyor
(`Where(r => r.UserId == userId)`). Birini delen değişiklik ikisini birden
deler — o sorguya dokunan her düzenlemede dört satırlık matris yeniden
ölçülür.

---

## 2026-08-28 — Okuma hatası mock veriye ya da boş listeye düşmüyor

**Karar:** Bir liste okunamadığında ekran **ne mock veri ne boş durum**
basıyor; ayrı bir "okunamadı" kutusu basıyor.

**Neden:** İkisi de bir **olgu iddiasıdır** ve okuma başarısızken edilemez.

- **Mock'a düşmek**: işletme sahibi kendi panelinde *"Gulet Işıl", "Mavi
  Rüzgar", "Deniz Yıldızı"* teknelerini görüyordu — hiçbiri onun değil.
  Ödeme ekranındaki kusurun aynısı, başka yerde.
- **Boş listeye düşmek**: mesajlaşmada *"Henüz mesajın yok"*, personelde
  *"Henüz personel yok"*. Domain'e göre iletişim **yalnız** sistem içi
  mesajlaşmayla oluyor; tekne sahibine kimsenin yazmadığını söylemek,
  cevaplanmamış bir müşteriyi görünmez yapar.

**`null` ile `undefined` ayrı tutuluyor:** `undefined` = prop hiç geçilmedi
(tasarım önizlemesi) → mock meşru. `null` = okuma başarısız → mock yasak.
`??` ikisini aynı sayıyordu; ayrım bu yüzden kayboldu.

**Ölçüm sırası kusur üretti:** ilk yazışta hata denetimini "yükleniyor"
denetiminden **sonra** koydum ve ekran sonsuza kadar "Yükleniyor…" yazdı.
Liste `null` kalıyor çünkü artık hata halinde doldurulmuyor. Ölçülmeseydi
"düzelttim" diye geçilecekti.

**Sunucu tarafı hâli de ölçüldü** (2026-08-28, backend'in tarifiyle):
`panel` kovası **dakikada 120** ve jetonsuz istekler de aynı kovadan yiyor,
yani `429` üretmek için oturuma gerek yok. 130 kimliksiz istekten sonra
panel açıldı:

| Bölüm | Ekran |
|---|---|
| Tekne listesi | **"Tekne listesi okunamadı"** — mock tekneler **yok** |
| Değerlendirmeler | **"okunamadı"** |
| Belgelerim | okuma geçti → gerçek boş durum |

Üçünün ayrı davranması doğru: bir listenin düşmesi diğerlerini
karartmıyor. Kova 60 saniyede açıldı, sayfa yenilendi ve **gerçek tekneler
döndü** — olumlu hâl de ölçüldü, yoksa "her zaman hata gösteren" bir ekran
da bu sınamadan geçerdi.

## 2026-09-05 — İl açılır liste, ilçe serbest metin

**Karar:** başvuru ve işletme ayarlarında **il** 81 ilin sabit listesinden
seçiliyor; **ilçe** serbest metin ve **isteğe bağlı** (Mert, 2026-09-05).

**Neden il liste:** serbest metinde aynı il için `Muğla`, `MUĞLA`, `Mugla`,
`muğla` birikiyor; şehre göre süzme hiç çalışmıyor ve listeye bakan bunları
ayrı iller sanıyor.

**Neden ilçe liste DEĞİL:** ~970 ilçelik doğrulanmamış bir liste serbest
metinden **daha kötü** olur — kullanıcı kendi ilçesini bulamayınca yakın
olanı seçer ve yanlış veri "seçilmiş" göründüğü için kimse şüphelenmez.
Yanlış bir liste, olmayan listeden zararlıdır.

**Neden `city`'ye birleştirilmedi:** en kolay yol `"Muğla / Bodrum"` diye tek
dizede birleştirmekti ve hiç backend işi gerektirmezdi. **Ayrıştırma bir daha
yapılamaz:** birleştirilen veri yarın "Muğla'daki bütün işletmeler"
sorgusunda ayrılmak zorunda kalır ve o ayırma kullanıcının nasıl yazdığına
bağlı bir tahmine döner. Aynı gerekçe backend'in `Coupons.UserId`
itirazıyla birebir: iki anlamı tek alana koymak.

**Alternatif elendi — il listesini `lookups`'a koymak:** 81 il değişmiyor;
bir uç çağrısı daha eklemek bu alan için orantısız.

⚠️ **Kayıtlı değer listede yoksa listeye ekleniyor ve seçili kalıyor**
(`illerVe()`). Bu olmadan sessiz bir veri kaybı olurdu: demo işletmesinin
şehri `Bodrum` yazıyor — o bir **ilçe**. Açılır liste onu seçili
gösteremeseydi, kullanıcı başka bir alanı düzeltip kaydettiğinde şehrini
farkında olmadan değiştirmiş olurdu.

⚠️ Boş bırakılan ilçe **`null` gidiyor, `""` değil**: boş dize "ilçesi yok"
ile "yazmadı" arasındaki farkı kaybettirirdi.

---

## 2026-09-05 — Tablo sütunları oransal, yönetim paneli 1440px

Yönetim panelindeki yat işletmeleri tablosu kabından **510px taşıyordu**.
Yedi sütun sabit piksel genişlikteydi (240+220+80+110+130+150+230 = 1160,
aralarla 1256), kap ise 746px veriyordu: 1140px'lik panel kabından yan menü
(248) ve kart dolgusu (60) düşünce kalan buydu.

Taşmanın kendisinden **daha kötü olan yeriydi**: `overflow-x-auto` kaydırma
çubuğunu tablonun **altına** koyuyor. 31 satırlık listede yana kaydırmak için
sayfanın en dibine inmek gerekiyordu — yani sütunu görmek isteyen kişi önce
tabloyu terk etmek zorundaydı. Mert testte bunu bildirdi.

**Karar:** `AdminColumn.w` artık **sabit genişlik değil pay**; `min` ile birlikte
`minmax(min, w fr)` üretiyor. Tablo kaba sığacak şekilde dağıtılıyor, sığmadığında
kaydırıyor. Uzun metin `truncate` + `title` ile kırpılıyor.

**Neden oransal, neden "sütunları daralt" değil:** sabit piksel her yeni sütunda
aynı hatayı üretir ve hata **ancak birinin ekranında** görünür. Oransal dağıtım
kabın genişliğini ölçüt yapar, tasarımcının varsaydığı ekranı değil.

**İkinci karar — yönetim paneli 1440px kaba alındı.** Tasarımın ölçüsü 1140px ve
misafir sayfalarında öyle kalıyor. Sapma `PanelShell`'e `genis` bayrağıyla verildi;
işletme ve destek panelleri değişmedi.

**Neden bayrak, neden hepsini genişletmedim:** tasarımdan sapma yasağı duruyor ve
sapmanın **gerekçesi sütun sayısı**. Yedi sütunlu tablo yalnız yönetim panelinde
var; diğer iki paneli de genişletmek gerekçesiz sapma olurdu.

Ölçüm (Playwright, gerçek veri, 31 satır): 1440'ta ve 1280'de yatay taşma **0**;
1180'de tablo kendi içinde 77px kaydırıyor ve **sayfa taşmıyor**; 390'da sayfa
taşması 0. Destek ve yorum tabloları da 0 taşmaya düştü.

**Üçüncü karar — işlem düğmeleri iki sütunlu ızgarada.** `flex-wrap`'te düğme
genişliği etiket uzunluğuna bağlıydı; "Belgeler" ile "Sözleşme gönder" yan yana
gelince satır sağdan tırtıklı bitiyor, sonraki satır başka yerde kırılıyordu.
Beş düğmeye çıkan hücrede sonuç dağınıktı. Izgarada hepsi 99px, aynı satırdakiler
eşit yükseklikte. Sabit yükseklik **verilmedi**: dar sütunda uzun etiket iki satıra
sarıyor ve sabit yükseklik metni kırpardı — hizayı yükseklik değil ızgara sağlıyor.

İlgili: [[web-desenler]] · [[web-gorevler]] · [[web-durum]]

---

## 2026-09-05 — Başvuru durumu tek başına yalan söylüyordu

🔴 **Mert testte buldu:** başvuru yaptı, platform hesabından sözleşme gönderdi,
işletme hesabından reddetti, platforma döndü — **reddin hiçbir izi yoktu**, tablo
"Sözleşme gönderildi" diyordu.

Sebep bir uç eksiği değildi. İşletme sözleşmeyi reddettiğinde başvuru
`ContractSent` **kalıyor** ve bu kasıtlı: platform düzeltilmiş bir sözleşme
gönderebilsin diye. Uç `contractStatus` alanını **zaten döndürüyordu**; tip
tanımında da vardı (`PlatformPartner.contractStatus`). Ekran onu hiç okumuyordu.

**Karar:** rozet iki alanı birleştiriyor — `contractStatus === "Rejected"` ve
başvuru kapanmamışsa "Sözleşme reddedildi" basılıyor, aksi halde başvuru durumu.

**Neden en son sözleşmenin durumu doğru ölçüt:** `contractStatus` en son
sözleşmeyi gösteriyor, dolayısıyla platform yeni sözleşme gönderince alan `Sent`'e
dönüyor ve uyarı **kendiliğinden kalkıyor**. Yani rozet "geçmişte bir ret oldu"
değil **"cevaplanmamış bir ret var"** anlamına geliyor — pazarlık döngüsünde
platformun görmesi gereken tam olarak bu.

**Ders:** `W-85`'te sözleşme akışının iki ucunu da yazdım ve **işletme tarafını
ölçtüm**. Platform tarafının aynı olayı nasıl gördüğünü ölçmedim; akış tek yönlü
test edilince eksik yarısı sessiz kaldı. Karşılıklı bir akışta **her iki tarafın
ekranı ayrı ayrı ölçülür** — biri doğruyken diğeri yalan söyleyebiliyor.

⚠️ **Ret gerekçesi hâlâ görünmüyor.** `rejectionReason` ve `rejectedAt` yalnız
işletme yanıtında (`GET /api/partner/contracts`) dönüyor; platform yanıtında
(`GET /api/platform/partners/{id}/contracts`) yok. Yani platform reddi görüyor ama
**sebebini okuyamıyor**, dolayısıyla yeni sözleşmede neyi değiştireceğini bilmiyor.
Backend'e bildirildi → `W-86`

Kanıt: canlı, gerçek veri — Mert'in kendi başvurusu (`my_mert07@hotmail.com`,
`01a06f26-…`) tabloda **"Sözleşme reddedildi"** basıyor ve satırda "Sözleşme
gönder" düğmesi açık. 31 satırın rozet dağılımı: Aktif 19 · Sözleşme gönderildi 9 ·
Başvuru alındı 2 · Sözleşme reddedildi 1. `982ee73`

İlgili: [[web-gorevler]] · [[web-durum]] · [[durum]]
