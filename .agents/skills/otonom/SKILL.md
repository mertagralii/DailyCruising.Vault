---
name: otonom
description: Use when Mert wants Codex to work through the DailyCruising task board unattended — "otonom çalış", "hepsini yap", "sormadan devam et", "loop'a al". Codex takes technical decisions itself, collects business decisions as numbered questions, and stops only when the board is exhausted or every remaining task is blocked on Mert.
---

# Otonom Çalışma

Mert onay vermeyi bırakıyor. Sen panoyu baştan sona götürüyorsun; **teknik
kararları kendin alıyorsun**, **iş kararlarını asla tahmin etmiyorsun** — onları
numaralı soru olarak biriktirip sonunda topluca soruyorsun.

## Duran kural: iki karar türü ayrıdır

Bu ayrım bu skill'in tamamıdır. Yanlış tarafa düşen bir karar ya seni gereksiz
durdurur ya da Mert'in adına uydurulmuş bir iş kuralı üretir.

| Tür | Örnek | Ne yaparsın |
|---|---|---|
| **Teknik** | indeks türü, katman yerleşimi, hata kodu, kilit sırası, test biçimi, kesme sınırı | **Kendin karar ver**, gerekçesiyle `<alan>-kararlar.md`'ye yaz, devam et |
| **İş** | komisyon/kupon/iptal politikası, hangi veri toplanacak, giriş zorunlu mu, para, KVKK kapsamı, müşteriye ne gösterilecek | **DURMA, TAHMİN ETME.** Belgelenmiş bir varsayımla ilerle, soruyu kuyruğa ekle, sıradaki göreve geç |

Emin olamadığın yerde **iş kararı say**. "Muhtemelen böyle istemiştir" cümlesi
kurduğun anda o bir iş kararıdır.

## Soru kuyruğu

Tek yer: `02-API/api-durum.md` -> "Mert'e sorulacaklar" (web tarafı için
`03-Web/web-durum.md`). Biçim:

| # | Konu | Şimdilik ne yapıldı |
|---|---|---|
| S-N | Sorunun kendisi + **neden önemli** (somut bedel: "€500'lük turda ~50 TL fark") | Hangi varsayımla ilerlendi ve **geri almanın maliyeti** |

- `N` = kullanılmış en büyük numara + 1. Numara geri kullanılmaz.
- Cevaplanan soru silinmez, "cevaplananlar" tablosuna taşınır.
- Soru sorarken **seçenekleri de yaz**. Mert'in işi karar vermek, seçenek üretmek değil.

## Görev döngüsü

Sıra `02-API/api-gorevler.md` "Yapılacak" bölümünden, **öncelik** alanına göre.
Elle liste taşıma yok — pano tek kaynak.

Her görev için, sırayla:

1. **Oku** — AGENTS.md tetikleyicileri koşulsuz: `api-desenler` + `api-araclar` +
   `api-gorevler`. Şema işi varsa `api-sema`.
2. **Yapılıyor'a taşı** (aynı anda en fazla 3).
3. **Yaz.** Onaysız şema kurulmaz: ilgili bölüm `api-sema`'da onaylı değilse o
   görev iş kararıdır, kuyruğa gider.
4. **Canlı doğrula.** ⛔ `dotnet build` temiz olması KANIT DEĞİLDİR. Uca istek at,
   **status kodunu ve gövdeyi gör**. Yetki gerektiren uçta yetkisiz istekle de
   dene. Migration varsa **geri al ve tekrar uygula**.
5. **Denetle** — `ecc:csharp-reviewer` + `ecc:security-reviewer`, şema/sorgu
   değiştiyse `ecc:database-reviewer`. Hata yutulmuş olabilirse
   `ecc:silent-failure-hunter`.
6. **Her bulguyu DOĞRULA, kabul etme.** Denetim yanılır. Bugüne kadar dört bulgu
   yanlış çıktı ve biri yanlış düzeltme öneriyordu. Doğruysa üret, düzelt, tekrar
   üret. Yanlışsa **neden yanlış olduğunu yaz**.
7. **Test.** Bugünkü elle doğrulamayı kalıcı teste çevir. Denetim "şu test eksik"
   diyorsa yaz — bugüne kadar o testlerin ikisi gerçek hata buldu.
8. **Commit + push.** Görev başına bir commit. Ara commit'in **derlenmesi şart**
   (bisect). Mesaj neyi değil **NEDEN** anlatır.
9. **Vault.** Görev `Kanıt:` satırıyla Tamamlandı'ya; `Kanıt:` canlı çıktı içerir,
   "derlendi" değil. Karar varsa `-kararlar.md` (`**Neden:**` zorunlu), tekrar
   eden kural varsa `-desenler.md`, tuzak varsa `notlar/` + hub linki.
   `dogrula.py` TEMİZ olmalı.

## Durma koşulu

Şunlardan biri olunca **dur ve raporla**:

- Panoda yapılabilir görev kalmadı,
- Kalan her görev ya Mert'e ya dış bir karara (`G-` görevleri) bağlı,
- Aynı görev **üç kez** başarısız oldu → park et, sebebini panoya yaz, sıradakine
  geç; hepsi parklandıysa dur.

Sonsuza kadar dönme. Yapacak iş kalmadığında döngüyü **bitir**.

## Bitiş raporu

Üç başlık, bu sırayla:

1. **Ne bitti** — görev + tek satır canlı kanıt + commit hash'i.
2. **Cevaplaman gereken sorular** — numaralı tablo, her birinde seçenekler ve
   şimdilik hangi varsayımla ilerlendiği.
3. **Neyi yanlış yapmış olabilirim** — ne yaptığın değil. Doğrulanmamış varsayım,
   kendi ürettiğin ve sonra bulduğun hata, atladığın kural, reddettiğin denetim
   bulgusu, geçmişe müdahale (`reset`, `amend`). **Bu başlık boş bırakılmaz;**
   boşsa yeterince aramamışsındır.

## Asla

- **Aralıkla silme.** Tam metin eşleştir — bir kez beş görev böyle silindi.
- **`01-Genel/durum.md`'ye yazma.** Oraya yalnız vault oturumu yazar; gereken
  bilgiyi `SendMessage` ile ilet.
- **Vault'a commit atma.** Alan oturumu yazar, commit'i vault oturumu atar.
- **Commit'e `Co-Authored-By` / "Generated with" ekleme.** Yazar daima
  `Mert Ağralı <mmertagrali@gmail.com>`.
- **Repolara `AGENTS.md`/`AGENTS.md` ekleme.**
- **Push edilmiş geçmişi değiştirme.** Push edilmemişte `reset`/`amend` serbest
  ama **raporda söylenir**.

## Bağlam dolduğunda — durma, devam et

Bağlam dolunca harness konuşmayı **kendiliğinden sıkıştırır** (auto-compact).
`/compact` senin çağırabileceğin bir araç DEĞİL; Mert'in yerel komutu. Yani
"bağlam doldu, ne yapayım" diye sorulacak bir an yok — sıkıştırma olur ve sen
özetle devam edersin.

Tehlike sıkıştırmanın kendisi değil, **ipin kopması**: özet, o sırada aklında
olan yarım kararı taşımayabilir. Buna karşı iki kural:

### 1. Kontrol noktası — panoya yaz, belleğe güvenme

Bağlam nerede olursa olsun, şu üç anda pano güncellenir:

| Ne zaman | Nereye |
|---|---|
| Görev Yapılıyor'a alınırken | `<alan>-gorevler.md` — **ne yapmaya çalıştığın** tek satır |
| Bir karar verildiğinde (teknik ya da varsayım) | `<alan>-kararlar.md` / soru kuyruğu — **anında**, görev bitince değil |
| Canlı doğrulama yapıldığında | görev satırına `Kanıt:` — o çıktı bir daha üretilemeyebilir |

Yarım kalmış bir iş, panodan **okunarak** devam ettirilebilmeli. "Aklımda tutarım"
diye bekletilen hiçbir şey sıkıştırmadan sağ çıkmaz.

### 2. Sıkıştırma sonrası: sormadan devam

Sıkıştırma olduğunda ya da oturum kesildiğinde, sıradaki iş **her zaman** şu:

1. `01-Genel/acilis.md` + `01-Genel/durum.md` oku (AGENTS.md tetikleyicisi).
2. Alan panosunu oku — `Yapılıyor` boş değilse oradan devam et.
3. Dokunacağın alanın `-desenler` + `-araclar` dosyalarını **yeniden** oku;
   özet onları taşımaz.
4. Son commit'i ve `git status`'u gör — nerede kaldığın orada yazıyor.
5. **Devam et.** Mert'e "devam edeyim mi" diye SORMA; otonom çalışma zaten
   onaylandı. Rapor yalnız durma koşulunda verilir.

Sıkıştırma bir kesinti değil, sayfa çevirmedir.

İlgili: [[api-gorevler]] · [[api-durum]] · [[api-desenler]] · [[api-araclar]]
