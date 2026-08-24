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

## ECC — web tarafında hangi komut ne zaman

ECC v2.2.0 küresel kurulu. **Komutlar `/ecc:<ad>` biçiminde çağrılır**, skill'ler
`Skill` aracıyla `ecc:<ad>` olarak. Frontend tarafı ECC'de **tam desteklidir** —
aşağıdakiler 94 komut ve 285 skill içinden bu projeye uyanlardır.

### Sırayla çalıştırılacaklar — bir bileşen yazıldığında

| Sıra | Ne | Ne zaman | Neden |
|---|---|---|---|
| 1 | `/ecc:plan` | Ciddi bir işe **başlamadan önce** | Gereksinimi yeniden ifade eder, riski değerlendirir, adım planı üretir ve **koda dokunmadan CONFIRM bekler** |
| 2 | `Skill: ecc:react-patterns` | Bileşen yazarken | React 18/19 hook disiplini, server/client sınırı, Suspense, form actions |
| 3 | `/ecc:react-build` | Build veya tip hatası alınca | Next.js/Turbopack, JSX/TSX derleme, **hydration uyuşmazlığı**, server/client sınır hataları |
| 4 | `/ecc:react-review` | `.tsx`/`.jsx` değişen **her işten sonra** | Hook doğruluğu, render performansı, server/client sınırı, a11y. TSX'te `typescript-reviewer`'ı da paralel çağırır |
| 5 | Tarayıcı doğrulaması | Review temiz çıkınca | Build ve review **görsel hatayı görmez** → [[web-desenler]] |

**4. adım atlanamaz.** `npm run build` temiz olması bileşenin doğru olduğunu
göstermez; bu projede 6 görsel tuzak build'den geçip tarayıcıda yakalandı.

### Duruma göre çağrılacaklar

| Tetikleyici | Ne | Neden |
|---|---|---|
| **Next.js 16 / Turbopack** ayarı, dev hızı, cache sorunu | `Skill: ecc:nextjs-turbopack` | Bu projenin tam sürümü için yazılmış: artımlı bundling, FS cache, Turbopack–webpack farkı |
| Sayfa yavaş, render fazla | `Skill: ecc:react-performance` | Vercel'in React best practice'lerinden uyarlanmış |
| Erişilebilirlik işi | `Skill: ecc:frontend-a11y` veya `ecc:accessibility` | İlki React/Next odaklı; ikincisi WCAG 2.2 AA denetimi. `a11y-architect` ajanı da var |
| Bir düğme/akış beklenmedik davranıyor | `Skill: ecc:click-path-audit` | Her düğmeyi tam state değişim dizisi boyunca izler; birbirini iptal eden hataları bulur |
| API sözleşmesi değişiyor (mock → gerçek uç) | `Skill: ecc:contract-first` | `W-04` ve `A-07`'nin tam konusu: tüketici-üretici arasında alan kayması olmadan evrimleştirme |
| Animasyon/geçiş yazılacak | `Skill: ecc:motion-patterns` (temel: `ecc:motion-foundations`) | Buton, modal, toast, sayfa geçişi için hazır desen + SSR güvenliği |
| Ölü kod temizliği | `/ecc:refactor-clean` | knip, depcheck, ts-prune ile analiz eder, her silmeden sonra doğrular |
| Test altyapısı kurulacak | `/ecc:react-test` + `Skill: ecc:react-testing` | RTL + Vitest/Jest tespiti, davranış ve a11y odaklı. **Bu projede frontend testi hiç yok** → `G-07` |
| E2E testi | `Skill: ecc:e2e-testing` | Playwright Page Object Model, flaky test stratejileri |
| Deploy sonrası görsel QA | `Skill: ecc:browser-qa` | Yayın sonrası UI etkileşim doğrulaması |
| Yayın öncesi hazırlık | `Skill: ecc:production-audit` | Yerel kanıta dayalı "prod'da ne kırılır" denetimi |

### Ajanlar — komut çağırmadan doğrudan

| Ajan | Ne zaman |
|---|---|
| `ecc:react-reviewer` | `.tsx`/`.jsx` dokunan her değişiklikte |
| `ecc:typescript-reviewer` | Her TS/JS değişikliğinde |
| `ecc:react-build-resolver` | Build kırılınca (komut yerine doğrudan) |
| `ecc:performance-optimizer` | Bundle boyutu, render, memory |
| `ecc:a11y-architect` | Bileşen veya design system tasarlarken |

### ⚠️ ECC hook'u dev sunucusunu blokluyor

`pre:bash:auto-tmux-dev` hook'u **`npm run dev`'i tmux dışında engeller** (exit 2).
Sebep: log erişimi. Karşılaşınca yapılacaklar, sırayla:

1. Dev sunucusu **zaten 3000'de olabilir** — `lsof -i :3000` ile bak, körlemesine başlatma
2. tmux içinde başlat
3. Gerekiyorsa `ECC_DISABLED_HOOKS=pre:bash:auto-tmux-dev`

Ayrıca `stop:format-typecheck` hook'u yanıt sonunda düzenlenen JS/TS dosyalarını
**toplu** formatlar (Biome/Prettier) ve `tsc` çalıştırır — her düzenlemede değil,
bir kez. Beklenmedik biçim değişikliği görülürse sebebi budur.

## Kurulum kapsamı — proje bazlı

`ui-ux-pro-max` ve `seo-butler` **yalnız bu projede** etkin. Tanımları
`DailyCruising/.claude/settings.json` içinde; küresel `~/.claude/settings.json`
kirletilmedi. Başka bir projede Claude Code açıldığında bu ikisi görünmez.

`ecc`, `superpowers`, `context7`, `playwright`, `frontend-design` ise küresel
kurulu — onlar her projede var.

## `ui-ux-pro-max` — tasarım sistemi üretimi

Sıfırdan ekran veya akış tasarlanacağında kullanılır. 79 UI stili, 192 renk paleti,
74 font eşleşmesi, 119 UX kuralı ve 22 teknoloji yığını için rehber taşır.

| Tetikleyici | Nasıl | Neden |
|---|---|---|
| Tasarımı olmayan yeni bir ekran/akış gerekiyor | Doğrudan tarif et: *"şu iş için şu ekranı tasarla"* — skill kendiliğinden devreye girer | Tasarım kararlarını rastgele vermemek için |
| Renk, tipografi veya stil seçimi tıkandı | `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<sorgu>" --design-system` | Palet ve font eşleşmeleri hazır; sıfırdan uydurmaktan iyi |
| Grafik/gösterge tipi seçilecek | Aynı komut, sorguda grafik türü belirtilir | 25 grafik tipi için öneri taşıyor |

⚠️ **Bu projede öncelik yerel tasarım dosyasındadır.** DailyCruising'in 19 ekranı
zaten tasarlandı ve birebir uygulandı; `ui-ux-pro-max` **tasarımı olmayan** yeni iş
için vardır. Var olan bir ekranı "daha iyi" yapmak için kullanılmaz — o, tasarımdan
sapma olur → [[web-desenler]].

Python 3 gerektirir (yalnız standart kütüphane).

## `seo-butler` — teknik SEO ve GEO

Beş komutu var ve **sırası önemlidir**. Sıra bozulursa doğrulama anlamını kaybeder.

| Sıra | Komut | Ne zaman | Ne yapar |
|---|---|---|---|
| 1 | `/seo` | SEO işine başlarken veya periyodik iyileştirme turunda | Yığını keşfeder, 35 maddelik denetimi beş uzman ajanla yapar, **onay kapılı** plan sunar, git ile geri alınabilir şekilde uygular |
| 2 | `/seo-live` | **Dağıtımdan hemen sonra** | Kaynak koda değil **canlı siteye** bakar; Lighthouse çalıştırır, performans izi alır. Şablon bozulması, CDN sorunu ve yarım dağıtım yalnız burada görünür |
| 3 | `/seo-verify` | `/seo-live` sonrası | Dış araçlarla doğrular (Search Console, OpenSEO, Lighthouse). **Eklenti kendi ödevini kendi notlandırmaz** |
| 4 | `/seo-watch` | Haftalık | Canlı siteyi taban çizgisiyle karşılaştırır: `robots.txt` kayması, kırık rota, eksik canonical, performans gerilemesi. **Yalnız rapor eder, değiştirmez** |
| 5 | `/seo-report` | Dağıtımdan **en az 28 gün** sonra | Search Console verisini uygulama anına göre karşılaştırır. Erken çalıştırılırsa reddeder — uydurma trend üretmez |

**Kapsam daraltma:** `/seo skip analytics` veya `/seo only sitemap`.

**GEO ayrı bir şeydir.** Google sıralaması ile ChatGPT/Claude/Perplexity'nin
siteyi kaynak göstermesi farklı işler. `seo-butler` ikisini birden denetler —
alıntı botlarının `robots.txt` ile engellenmemesi ve kritik içeriğin sunucu
tarafında render edilmesi bu yüzden kontrol edilir.

⚠️ **Bu projede sırası henüz gelmedi.** Site yayında değil, dağıtım kararı yok
(`G-07`). `/seo` şimdi çalıştırılabilir ama `/seo-live`, `/seo-verify`,
`/seo-watch`, `/seo-report` **canlı URL ister** — yayın öncesi anlamsızdır.

`/seo` çalıştırılmadan önce hazır olması gerekenler: firma adı, iletişim bilgileri,
TÜRSAB numarası. Bunlar şu an `brand.ts`'te **yer tutucu** → `W-06`, `G-10`.
Yer tutucu veriyle SEO uygulanırsa yanlış bilgi arama motoruna işlenir.

**Getirdiği MCP sunucuları:** `chrome-devtools` (zaten var), `context7` (zaten var),
`openseo` (HTTP, dış denetim), `geodaddy` (GEO denetimi). Son ikisi bu eklentiyle
geliyor; `/seo-verify`'ın "kendi ödevini notlandırmama" ilkesi bunlara dayanıyor.

Node 18+ gerektirir.

## Kullanılmayacaklar

- `DesignSync` yazma çağrıları — tasarım projesi Mert'in, oraya yazılmaz

İlgili: [[web-notlar]] · [[web-desenler]] · [[web-mimari]] · [[web-gorevler]] · [[genel-araclar]]
