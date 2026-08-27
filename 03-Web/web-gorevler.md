---
rol: gorev
kapsam: web
guncelleme: 2026-08-26
durum: guncel
---

# Web Görevleri

`DailyCruising.Front-End/` işleri. Kimlik öneki **`W-`**, numara geri kullanılmaz.

**Kurallar:** Yapılıyor'da en fazla 3 görev · Tamamlandı'ya taşımak `Kanıt:` satırı
ister. Biçim ve gerekçe -> [[genel-desenler]]

## 🔵 Yapılacak

- [ ] **W-03** Gerçek görsellerin konması
      Kabul: `Placeholder` bileşeni yalnız gerçekten görseli olmayan yerde kalır
- [ ] **W-04** API bağlantısı, mock verinin ayıklanması · öncelik: yüksek
      Bağımlı: A-01, A-07 · Kabul: `src/lib/data/*.ts` yerine gerçek uçlar
- [ ] **W-06** `brand.ts` kurumsal verilerinin gerçekleriyle değişmesi
      Kabul: telefon, e-posta, adres, TÜRSAB no Mert tarafından onaylanmış değerler
      Bağımlı: G-10

## 🟡 Yapılıyor



## 🟢 Tamamlandı

- [x] **W-10** Geri bildirim katmanı: toast, modal, hata sayfaları, iskelet,
      boş durum, sayfalama, dosya yükleme, rezervasyon başarı ekranı, QR biniş
      belgesi, e-posta şablonları · bitti: 2026-08-26
      Kanıt: 25 rota derleniyor (öncesi 20), `npm run build` + `npm run lint`
      temiz. 1280×730'da modal 560px ortalı, perde `rgba(0,0,0,.5)`, kaydırma
      kilidi 15px telafiyle sıçramasız, ESC kapatıyor, odak çağırana dönüyor.
      Toast en fazla 3, hata `role="alert"` diğerleri `role="status"`.
      390px'te yedi yeni sayfada yatay taşma 0; modal alttan çıkan sayfaya
      dönüşüyor (üst köşe 16px, alt 0). 404 gerçekten HTTP 404 dönüyor.
      Baskı kuralları: 4 kural ayrıştı, seçiciler eşleşti, uygulandığında
      gezinme öğeleri gizlendi ve gölge kalktı.
      Bulunan ve düzeltilen hata: `rounded-circle` ölü sınıftı
      -> [[web-baglanmamis-token-tuzagi]]

- [x] **W-01** 19 sayfanın tasarıma göre piksel denetimi · bitti: 2026-08-24
      Kanıt: 16 misafir/hesap sayfasının 12'si birebir, kalanı ≤4px · yönetim
      24 modülün 19'u birebir, toplam 18px · destek 4 bölüm, toplam 12px ·
      işletme 10 bölümün 4'ü birebir, toplam 16px. Mobil 390px'te taşma yok.
      Kalan ortak +2px koyu banttaki kicker satırından, üç panelde de aynı.
- [x] **W-02** Kalan sayfaların tasarıma göre ölçülmesi · bitti: 2026-08-24
      Kanıt: W-01 ile aynı ölçüm; 1280×730'da tasarımla yan yana
- [x] **W-07** Front-end çalışmasının commit'lenmesi · bitti: 2026-08-23
      Kanıt: `76ac110` tasarımın 19 ekranı · `9009db3` kopan detaylar · `2b1dd35`
      işletme paneli hizalama · `d42b985` mobil kırılımlar · `2777132` İngilizce
      rotalar. Beşi de `origin/main`'de, AI atfı yok, yazar Mert.
- [x] **W-09** Rota klasörlerinin İngilizceye çevrilmesi · bitti: 2026-08-24
      Kanıt: 17 klasör `git mv` ile taşındı, 20 rota derleniyor; ana sayfada 26,
      hesap sayfasında 19 iç bağlantı 200 döndü, eski Türkçe yollar 404
      -> [[web-kararlar]]
- [x] **W-05** Mobil kırılımların doğrulanması · bitti: 2026-08-23
      Kanıt: 19 rota 390px'te tarandı, yatay taşma yok; 834px'te iki kart.
      Ölçüm Playwright ile — `chrome-devtools` 390'a inemiyor -> [[web-araclar]]
- [x] **W-08** Kopan detay ekranlarının geri bağlanması · bitti: 2026-08-23
      Kanıt: yönetimde 23, işletmede 3 ekran; 21 yönetim modülünde tek tek açılıp doğrulandı
- [x] **W-00** Next.js 16 iskeleti, Tailwind v4, tasarım sistemi katmanı · bitti: 2026-08-21
      Kanıt: `npm run build` başarılı

İlgili: [[web-desenler]] · [[web-kararlar]] · [[web-mimari]] · [[durum]] · [[web-notlar]]
