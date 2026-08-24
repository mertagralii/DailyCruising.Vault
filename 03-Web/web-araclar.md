---
rol: map
kapsam: web
guncelleme: 2026-08-24
durum: guncel
---

# Web Araçları

`DailyCruising.Front-End/` altında çalışırken **hangi durumda hangi aracı** kullanacağım.

Bu bir envanter değil **eşleme**. Gerekçesiz araç satırı eklenmez — gerekçesi
olmayan araç kullanılmayan araçtır.

| Tetikleyici | Araç | Neden |
|---|---|---|
| Tasarımı koda geçirdim, görünüm doğrulanacak | `chrome-devtools` MCP (`take_snapshot`, `evaluate_script`, `resize_page`) | Ölçüm için kullanılan araç bu. Hesaplanmış stil ve sınır kutusu okumanın en güvenilir yolu -> [[web-tasarimi-tarayicida-acmak]] |
| Sayfayı gerçekten gezip tıklamam gerekiyor | `claude-in-chrome` MCP | Kullanıcının kendi Chrome oturumunda çalışır; giriş gerektiren akışlar için |
| Tasarım kaynağı okunacak | Yerel dosya (`r-ht-m-temeller-sayfas/project/`) | `DesignSync` MCP `get_file` dosyanın yalnız %19,6'sını veriyor (256 KiB kesme). MCP yalnız okuma; tasarım projesine yazılmaz |
| React/Next bileşeni yazdım veya değiştirdim | `ecc:react-reviewer` ajanı | Hook doğruluğu, server/client sınırı, render performansı — build'in yakalamadığı sınıf |
| Build veya tip hatası aldım | `ecc:react-build` skill'i | Next/Tailwind/TS hatalarına dönük dar kapsamlı düzeltme |
| Next, Tailwind veya bir kütüphanenin API'si soruldu | `context7` MCP | Next.js 16 ve Tailwind v4 yeni; eğitim verim bayat olabilir, önce dokümana bakılır |
| Sıfırdan yeni bir ekran/akış tasarlanacak | `frontend-design` skill'i | Tasarım kararlarını rastgele vermemek için |
| Grafik, gösterge, istatistik kartı yapılacak | `dataviz` skill'i | Panellerde çok sayıda grafik var; renk ve biçim tutarlılığı |
| Mobil kırılım (390px) ölçülecek | `playwright` MCP (`browser_resize`) | **`chrome-devtools` `resize_page` 390px'e inemiyor.** 2026-08-23 mobil taraması bu yüzden Playwright ile yapıldı -> [[web-tasarimi-tarayicida-acmak]] |
| Uygulamayı ayağa kaldırıp bakmam gerekiyor | `run` skill'i | Dev sunucusu zaten 3000'de olabilir; körlemesine `npm run dev` açmadan önce bakılır |
| Bir token/bileşenin kaç sayfada kullanıldığı sorulacak | `Explore` ajanı | 19 ekran ve 38 modülde elle tarama bağlamı doldurur → [[genel-araclar]] |
| Tüm sayfaların toplu yeniden ölçümü gerekecek | `Workflow` | 19 ekran birbirinden bağımsız; sıralı ölçüm saatler alır → [[genel-araclar]] |

## Araç seçimi — masaüstü mü mobil mi

Bu ayrım önemli, karıştırılırsa ölçüm sessizce yanlış çıkar:

- **Masaüstü (1280) ölçümü** -> `chrome-devtools`. İki sekme de aynı boyutta olmalı;
  `resize_page` sessizce başarısız olabiliyor, boyut doğrulanmadan ölçüm alınmaz
- **Mobil (390/834) ölçümü** -> `playwright`. `chrome-devtools` bu genişliklere inemiyor

## Kullanılmayacaklar

- `DesignSync` yazma çağrıları — tasarım projesi Mert'in, oraya yazılmaz

İlgili: [[web-notlar]] · [[web-desenler]] · [[web-mimari]] · [[web-gorevler]] · [[genel-araclar]]
