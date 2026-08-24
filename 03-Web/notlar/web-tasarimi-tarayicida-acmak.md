---
rol: not
kapsam: web
guncelleme: 2026-08-22
durum: guncel
---

# Tasarımı tarayıcıda açıp yan yana ölçmek

`Rihtim.dc.html` yalnızca okunacak bir metin değil — **çalıştırılabilir**. Yanındaki
`support.js` design-canvas motoru yerelde çalışıyor, yani tasarımın kendisi
tarayıcıda açılıp uygulamayla yan yana ölçülebilir.

```
cd r-ht-m-temeller-sayfas/project && python3 -m http.server 8899
# → http://localhost:8899/Rihtim.dc.html
```

`file://` çalışmaz (tarayıcı otomasyonu kabul etmiyor); HTTP sunucusu şart.

## Neden önemli

Metin karşılaştırması **renk, boşluk ve ton** farklarını göremiyor. 2026-08-22'de
başlık sayımı 155/155 "tamam" derken ana sayfanın **14 bölümünden 11'inde zemin
rengi yanlıştı**. Fark ancak iki sayfa aynı anda ölçülünce görüldü:

```js
// her iki sayfada da çalıştır, çıktıları karşılaştır
[...document.querySelectorAll('h1,h2')]
  .filter(e => parseFloat(getComputedStyle(e).fontSize) >= 29)
  .map(h => { const s = h.closest('section') || h.parentElement;
    const c = getComputedStyle(s);
    return [h.textContent.trim().slice(0,24),
            c.backgroundImage !== 'none' ? 'GRADYAN' : c.backgroundColor,
            c.paddingTop]; })
```

**Dikkat:** tasarım `<section>` etiketi kullanmıyor, iç içe `<div>`lerle kurulmuş.
Tasarım tarafında en yakın geniş kapsayıcıyı (`width > 1400`) yukarı doğru arayarak
bulmak gerekiyor.

## Ana sayfada bulunan farklar

| Bölüm | Tasarım | Yanlış hâli |
|---|---|---|
| Sistem nasıl çalışır | `#E4EAE5` | beyaz |
| Popüler bölgeler | beyaz | `#F8F9F8` |
| Öne çıkan tekneler | `#F1F4F1` | beyaz |
| Tur kategorileri | beyaz | `#F8F9F8` |
| Uygulamayı indir | `#10201C` koyu | beyaz |
| İskelede bekleyen | amber gradyan | koyu |
| Sezon başlamadan | `#E4EAE5` | koyu |
| Bölüm dolgusu | 72px | 120px |

`--surface-1` (`#F8F9F8`) tasarımda **hiç kullanılmıyor**; dönüşümlü zemin
`#F1F4F1` (`--surface-2`) ve `#E4EAE5` (`--surface-3`).

## Uydurulmuş içerik

Hero'nun altında "Aradığını bulamadın mı? Tüm tekneleri gör →" satırı vardı;
tasarımda **sıfır kez** geçiyor. Karşılaştırma yapılmadan yazılan içerik böyle
sızıyor → [[web-eksik-detay-ekranlari]]

## Metin karşılaştırması — `window.name` hilesi

İki farklı origin arasında veri taşımak için `window.name` kullanılabilir; sekme
gezinince bile korunur:

```js
// tasarım sayfasında
window.name = JSON.stringify(document.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean));
location.href = 'http://localhost:3000/';
// uygulama sayfasında
const design = JSON.parse(window.name);
```

**Karşılaştırmadan önce normalize et**, yoksa yanlış pozitif yağar:

| Gürültü | Sebep |
|---|---|
| `GÖRSELI` vs `GÖRSELİ` | Tasarımın `<html>`inde `lang` yok; Türkçe büyütme farkı |
| Yer tutucu metinleri | `innerText` `placeholder` içermez — ayrıca topla |
| `input` değerleri | Aynı şekilde ayrıca topla |
| Marka adı | Rıhtım ↔ Daily Cruising |

## İkinci turda bulunan farklar

Zemin renkleri düzeldikten **sonra** çıkanlar:

| Ne | Tasarım | Yanlış hâli |
|---|---|---|
| "Neden…" kart ikonları | 22px çizgi SVG | emoji (🛡⚡🔒🎧) |
| Adım kartları | yalnızca "Adım N" etiketi | ek numara rozeti |
| SSS | kartsız, çizgiyle ayrık, işaretçisiz | kart + `+` işaretçisi |
| İletişim bilgileri | tek başlık + düz liste | her satıra ayrı etiket |
| Görsel yer tutucu | etiket **yalnızca bölge kartlarında** görünür | hiçbirinde görünmüyor |
| Çerez bandı | emojisiz | 🍪 eklenmiş |
| Footer tur adı | "Haftalık Charter" | "Haftalık Tekne Turu" |
| Tüzel unvan | "<Marka> Turizm A.Ş." | "Bilgehan Denizcilik A.Ş." |

Tasarımda aynı tur tipi iki farklı adla geçiyor: menüde "Haftalık Tekne Turu",
vitrinde ve footer'da "Haftalık Charter" → `TourType.altLabel`.

## Kabul edilen farklar

Bunlar bilinçli, düzeltilmeyecek:

- Tasarımın statik kutuları yerine gerçek `<select>` / `<input>` kullanılıyor;
  `innerText` bu yüzden seçenekleri de sayıyor.
- Bültende ve arama alanında `sr-only` etiket var — tasarımda yok, erişilebilirlik
  için eklendi.
- Yıldız: tasarım `★★★★☆`, kodda dolu yıldız + soluk yıldız (görsel olarak aynı).

## Üçüncü tur — geometri karşılaştırması

Metin ve renk eşleşse bile **konum ve ölçü** tutmayabiliyor. Kesin yöntem: her metin
düğümünün kutusunu ölçüp iki sayfayı karşılaştırmak.

```js
// her iki sayfada çalıştır; metin düğümlerini Range ile ölç
const out=[]; const walk=el=>{ for(const n of el.childNodes){
  if(n.nodeType===3){ const t=n.textContent.replace(/\s+/g,' ').trim(); if(!t) continue;
    const r=document.createRange(); r.selectNodeContents(n); const b=r.getBoundingClientRect();
    if(b.width||b.height){ const s=getComputedStyle(el);
      out.push({t,x:Math.round(b.left),y:Math.round(b.top+scrollY),fs:parseFloat(s.fontSize),fw:s.fontWeight,c:s.color}); } }
  else if(n.nodeType===1 && getComputedStyle(n).display!=='none') walk(n); } };
walk(document.body);
```

**Zorunlu koşullar:**

| Koşul | Neden |
|---|---|
| İki sayfa da **aynı `innerWidth` ve `innerHeight`** | Hero `min-height:100vh`; yükseklik değişince her şey kayar |
| `document.fonts.ready` beklenmeli | Font yüklenmeden ölçüm yanlış |
| `getAnimations().forEach(a=>a.finish())` | Açılış animasyonları konumu bozar |
| Renkleri tuvale çizip karşılaştır | Tailwind v4 `oklab()` üretir, tasarım `rgb()` — aynı renk farklı yazılır |

`chrome-devtools` MCP'sinin `resize_page` aracı pencereden bağımsız görüntü alanı
verir; `claude-in-chrome`'un pencere boyutu ekranla sınırlı ve kayabiliyor.

### `resize_page` sessizce başarısız olabilir (2026-08-23)

Tasarım sekmesinde `resize_page` **hatasız döndü ama boyut değişmedi** — sekme
1280×730'da kaldı, uygulama 1440×900'deydi. Ölçüm yalan söyledi: kutu genişlikleri
doğru göründü ama tüm `x` değerleri tam **80px** kaydı — `(1440−1280)/2`. Sabit
genişlikli, ortalanmış bir düzende kayma her zaman bu formülü verir; gördüğünde ilk
şüphelenecek şey görüntü alanıdır.

Çözüm iki adımlı: (1) çevirmeyen sekmeyi zorlamak yerine **diğerini onun boyutuna**
indir, (2) ölçüm betiğinin ilk satırına kilit koy — kilit olmadan yanlış boyutta
ölçüp olmayan farkları kovalıyorsun:

```js
if (innerWidth !== 1280 || innerHeight !== 730) throw new Error('viewport ' + innerWidth);
```

### Her koşudan önce iki sekmeyi de yeniden yükle (2026-08-23)

Sayfa yeniden yüklenmedikçe hem React durumu hem tasarımın kendi `state`'i **önceki
ölçümden kalır**:

- Tasarımın yan menü grupları önceki koşuda açılmıştı; yeni koşuda "başlangıçta hepsi
  açık" gibi göründü. Tasarımın gerçek kuralı: grup, **etkin modülü içeriyorsa** açık
  gelir, kullanıcı elle değiştirene kadar (`Rihtim.dc.html` 8580).
- Destek panelinde `Gelen kutusu` 1180px fazla ölçüldü; sebep, önceki koşuda bir
  talebin açılmış olması ve detay ekranının açık kalmasıydı. Yeniden yükleyince fark
  +2px'e indi.

Tasarım sekmesi yeniden yüklenince oturum sıfırlanır: panellere ulaşmak için önce
`Giriş yap` → gönder, sonra kullanıcı menüsünden ilgili panel açılmalı.

## En büyük bulgu: font yanlıştı

`next/font/google` çağrısına `weight: ["400","500","600","700"]` verilince Next
**statik** kesitleri indiriyor. Tasarım ise DM Sans'ın `opsz 9..40` eksenli
**değişken** sürümünü kullanıyor. Sonuç: harfler **%10 geniş**, başlıklar farklı
sarıyor, her bölüm birkaç piksel kayıyor.

```ts
// yanlış: statik kesitler
DM_Sans({ weight: ["400","500","600","700"], subsets: [...] })
// doğru: değişken font, opsz ekseni açık
DM_Sans({ axes: ["opsz"], subsets: [...] })
```

Düzeltince başlığın satır genişliği tasarımla birebir oldu (956px / 338px).

## Bölüm dolgu ve boşlukları (ölçüm)

| Bölüm | padding | margin-top |
|---|---|---|
| Hero | 135px 0 0 | — |
| Ne tür bir gün | 72 0 0 | 0 |
| Neden | 72 0 | **72** |
| Sistem · Popüler · Öne çıkan | 72 0 | 0 |
| Tur kategorileri | 72 0 0 | 0 |
| Turdan dönenler | 72 0 | **72** |
| Uygulamayı indir · İskelede bekleyen · Bülten | 0 | 0 |
| Son eklenen bloglar | 72 0 | 0 |
| Sık sorulanlar | 72 0 56 | 0 |
| Bize ulaşın | 56 0 80 | 0 |

Bölüm arası **72px boşluk margin ile veriliyor, padding ile değil**. Zeminler farklı
olduğu için bu ikisi aynı şey değil.

## Izgara ölçüleri

Tüm ana sayfa ızgaralarında boşluk **30px** (bende 16–20 idi). Kart köşesi genelde
**12px** (40 kullanım), metin kartlarında 16px (20 kullanım).

| Izgara | Sütun | Kart |
|---|---|---|
| Ne tür bir gün | 4 × 250.5 | 251×97, dolgu 20 |
| Sistem | 4 × 250.5 | 251×212, dolgu 24, zemin `#FDF1E0` |
| Popüler bölgeler | 4 × 250.5 | 251×273 (görsel 178 + metin 93) |
| Öne çıkan tekneler | 4 × 250.5 | 251×345 (görsel 178 + metin 165) |
| Tur kategorileri | 4 × 250.5, satır 220 | geniş `span 2/2` 531×470; dar 251×220, **görselsiz** |
| Son eklenen bloglar | 3 × 344 | 344×391 (görsel 212 + metin 177) |
| Bize ulaşın | 2 × 531 | form kartı 531×604, dolgu 30 |

## Kabul edilen tek fark

Tasarımda kart başlıkları **saf siyah** (`rgb(0,0,0)`) çıkıyor; sebebi kartların
`<button>` olması ve butonun renk miras almaması. Bu bir tasarım kararı değil,
tarayıcı varsayılanı. Kodda marka rengi `#10201C` kullanılıyor — 14 metinde
görülen fark bundan.

## Ulaşılan sonuç (2026-08-22)

| Ölçüt | Başlangıç | Son |
|---|---|---|
| Gerçek stil farkı | 51 | **0** |
| Bölüm yüksekliği toplam sapma | 2894 px | **16 px** (13 bölüm, en fazla ±3) |
| Sayfa yüksekliği | 11271 / 8377 | 8240 / 8177 |

Kalan ±1–3 px, satır yüksekliği yuvarlamasından geliyor: tasarım 14px metinde
`line-height:1.6` → 22.4px, tarayıcı bunu satır başına farklı yuvarlıyor.

**Yanlış eşleşme tuzağı:** aynı metin sayfada birden çok yerde geçiyorsa
("Günlük Tekne Turu" hero seçiminde, tur kartında, tekne rozetinde ve footer'da)
eşleştirici yanlış çifti kurup sahte fark üretiyor. Kalan farklar tek tek
doğrulanmadan "fark var" denmemeli.

## Son turda düzeltilen ince ayrıntılar

- Yer tutucu etiketi sağ alt yerine **sol altta**, dolgu 16px
- Telefon maketi 260×405, dolgu `18px 18px 0`, köşe `24 24 0 0`, zemine değiyor
- Uygulama mağazası butonları 148×67, ikon 22×22 köşe 6, zemin beyaz %22
- Mobil bölüm ızgarası `652px 380px`, boşluk 60, **alta hizalı**; sol sütunun
  alt dolgusu 80px — satır yüksekliğini o belirliyor
- İletişim formu: kart 531×604, alan blokları 80, mesaj bloğu 152, buton 57
- `<textarea>` `block` yapılmazsa altında 8px taban çizgisi boşluğu kalıyor
- Adım kartlarında 1px çerçeve

İlgili: [[web-notlar]] · [[web-kararlar]] · [[durum]]

### 390px ölçmek: `chrome-devtools` yetmiyor (2026-08-23)

Mobil doğrulama için iki araç da başarısız oldu:

- `resize_page` pencereyi **500px'de kırpıyor** — yeni sekmede bile 390'a inmiyor.
- `emulate` aracı bozuk: `viewport` ne şekilde verilirse verilsin CDP'ye
  `width: null` gidiyor ve `Emulation.setDeviceMetricsOverride` hata veriyor.

Çalışan yol **Playwright MCP**: `browser_resize` gerçek `setViewportSize`
çağırıyor, 390×844 sorunsuz. Sayfa gezinmesi `browser_navigate` ile yapılmalı;
sayfa içinden `location.href` veya sentetik `<a>` tıklaması betiğin bağlamını
yok ediyor.

Tasarımı 390'da açmanın **anlamı yok**: tasarımın tek kırılımı 1180 ve 390'da
kendi ızgaraları taşıyor. Mobil referansı `isBreak` ekranındaki 390/834
maketleri → [[web-kararlar]]

