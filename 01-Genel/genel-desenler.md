---
rol: map
kapsam: genel
guncelleme: 2026-08-24
durum: guncel
---

# Genel Desenler

İki repoyu birden ilgilendiren, her oturumda tekrar uygulanan kurallar.
Gerekçeler [[genel-kararlar]] içinde.

## Dil

| Nerede | Dil |
|---|---|
| Konuşma, vault notları | Türkçe |
| Kod, dosya/sınıf/endpoint adları | İngilizce |
| Commit mesajları | İngilizce |

## Commit

- Yazar daima `Mert Ağralı <mmertagrali@gmail.com>`
- **AI atfı yasak:** `Co-Authored-By: Claude` trailer'ı, "Generated with Claude Code"
  benzeri ibare, repoya `CLAUDE.md`/`AGENTS.md` konulması — hiçbiri olmaz
- Mesaj İngilizce ve emir kipinde ("add", "fix"); gövdede **neden** anlatılır
- Commit ve push **yalnızca Mert isteyince**
- Kökte repo yok; her git komutu ilgili alt klasörde çalışır

## Doğrulama

| Taraf | Komut | Beklenen |
|---|---|---|
| API | `dotnet build` | 0 uyarı, 0 hata |
| API | `curl localhost:5163/api/health` | `{"status":"healthy"}` |
| Web | `npm run build` | başarılı |
| Web görünüm | tarayıcıda karşılaştırma | -> [[web-desenler]] |
| Vault | `python3 _araclar/dogrula.py` | TEMIZ |

Portlar: API 5163 (http) / 7070 (https), Web 3000.

## Nereye yazılır

Aynı bilgi iki yere yazılmaz. Sınır şudur:

| Bilgi türü | Dosya |
|---|---|
| Bir daha aynı **kararı** vermemek için | `*-kararlar.md` (append-only, `**Neden:**` zorunlu) |
| Bir daha aynı **tuzağa** düşmemek için | `<alan>/notlar/` |
| Her dosyada tekrar uygulanan **kural** | `*-desenler.md` |
| Yapılacak / yapılıyor / biten **iş** | `*-gorevler.md` |
| Hangi **araç** ne zaman kullanılır | `*-araclar.md` |
| Proje seviyesi **engel**, açık uç, çelişki | [[durum]] |
| O günün çalışma kaydı (arşiv) | `04-Oturumlar/` |

**Asla yazılmaz:** koddan okunabilen şeyler (klasör yapısı, kurulu paketler), git
geçmişindeki bilgiler, tek oturumluk geçici detay.

**Karar değişirse eskisi silinmez** — yeni giriş eklenir, "<tarih> kararını iptal
eder" yazılır.

## Özet tablo ile gövde çelişirse

Uzun dosyalarda (`domain-gereksinimler.md` 1.200+ satır) baştaki veya sondaki
**özet tablo, gövdeden bağımsız bayatlıyor**. 2026-08-24'te "Cevap bekleyenler"
tablosu beş soruyu açık gösteriyordu; beşinin de cevabı aynı dosyanın içindeydi.
İki ayrı oturum bunları blocker sandı.

- **Gövde doğrudur, tablo türevdir.** Çeliştiklerinde tabloyu gövdeye göre düzelt
- **Bir soru cevaplandığında tablo aynı turda düşürülür** — sonraya bırakılmaz.
  `domain-karari` skill'i bu adımı zorunlu tutar
- `dogrula.py` bunu **yakalayamaz**; semantik çelişki, biçim hatası değil.
  Tek korunma disiplin ve skill


## Kendi çıkarımım, karar değildir

`domain-gereksinimler.md`'de `*(çıkarım)*` etiketli maddeler var — Mert'in söylediği
değil, benim doldurduğum boşluklar. Bunlar zamanla karar gibi okunmaya başlıyor.

- **Etiketli bir maddeye sonradan itiraz edebilirim ve etmeliyim.** Daha iyi
  muhakeme ettiğimde eski çıkarımım bağlayıcı değildir
- **Ama tek taraflı silmem.** İtirazı gerekçesiyle Mert'in önüne koyarım; kararı o
  verir. 2026-08-24'te backend oturumu "müsaitlik yazma anında hesaplanıp
  saklanmalı" maddesine böyle itiraz etti — silmeden, sorarak
- Mert'in söylediği ile benim çıkarımım **aynı paragrafta karışmaz**; karışırsa
  altı ay sonra hangisinin kim olduğu bilinmez


İlgili: [[genel-notlar]] · [[genel-kararlar]] · [[calisma-duzeni]] · [[genel-gorevler]] · [[genel-araclar]]
