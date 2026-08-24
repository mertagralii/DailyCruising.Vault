---
rol: history
kapsam: web
guncelleme: 2026-08-22
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
