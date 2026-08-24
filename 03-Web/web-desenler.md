---
rol: map
kapsam: web
guncelleme: 2026-08-24
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
