---
rol: map
kapsam: genel
guncelleme: 2026-08-21
durum: guncel
---

# DailyCruising Vault — Ana Harita

Kalıcı proje bilgisinin kanonik kaynağı. Kurallar için [[CLAUDE]].

## Roller

Bu vault, ECC `living-docs-governance` skill'inin dört rolüne göre düzenlenmiştir.
**Her gerçeğin tek kanonik sahibi vardır**; diğer notlar kopyalamaz, link verir.

| Rol | Görevi | Dosyalar |
|---|---|---|
| Constitution | Uyulması zorunlu kurallar | [[CLAUDE]], [[calisma-duzeni]] |
| Map | Ne var, nerede | bu dosya, [[proje]], [[api-mimari|API mimari]], [[web-mimari|Web mimari]] |
| Status | Şu anki durum, blocker, açık uç | [[durum]] (genel) · [[api-durum]] · [[web-durum]] |
| History | Kalıcı kararlar ve gerekçeleri | [[genel-kararlar]] (genel / API / Web) |
| Notlar | Claude'un serbest gözlemleri | [[genel-notlar]] · [[api-notlar]] · [[web-notlar]] |

## Şunu yapacaksan buraya bak

| İhtiyaç | Git | Doğrula |
|---|---|---|
| API'de kod değiştir | `02-API/api-kararlar.md` → `02-API/api-mimari.md` | `dotnet build` |
| Web'de kod değiştir | `03-Web/web-kararlar.md` → `03-Web/web-mimari.md` | `npm run build` |
| Domain / iş kuralı konuş | `01-Genel/proje.md` → `01-Genel/durum.md` | — (henüz kod yok) |
| Bir tuzağa/tekrar eden soruna takıldım | ilgili `*-notlar.md` hub'ı | notu oku, yoksa yaz |
| "Neden böyle yapmıştık" | ilgili `*-kararlar.md` | — gerekçe **yalnızca** burada, git log'da yok |
| Nerede kalmıştık | `01-Genel/durum.md` — **tek otorite**. Alan ayrıntısı: [[api-durum]] · [[web-durum]] | — |

## Dosya listesi

**01-Genel**
- [[domain-gereksinimler]] — **iş kurallarının kanonik kaynağı**, Mert'le görüşmeden
- [[proje]] — DailyCruising ne yapar, kim kullanır ⚠️ davranış atıfları doğrulanmamış
- [[durum]] — açık uçlar, blocker'lar, delete-zone
- [[genel-kararlar]] — iki repoyu birden ilgilendiren kararlar
- [[calisma-duzeni]] — commit, dal, test, iletişim kuralları
- [[acilis]] — **oturum açılışında otomatik yüklenen çekirdek** (tavan 6.000 karakter)
- [[genel-desenler]] — dil, commit, doğrulama, nereye yazılır
- [[genel-gorevler]] — genel görev panosu (`G-`)
- [[genel-araclar]] — hangi durumda hangi plugin/skill/MCP
- [[genel-notlar]] — Claude'un genel gözlemleri (hub) → `01-Genel/notlar/`

**02-API** (`DailyCruising.Back-End/`)
- [[api-sema]] — veritabanı şeması, sekiz bölüm (A-01 çıktısı)
- [[api-mimari]] — Clean Architecture katmanları, bağımlılık yönü
- [[api-kararlar]] — .NET ve mimari kararları
- [[api-desenler]] — katman, isimlendirme, HTTP, veritabanı kuralları
- [[api-gorevler]] — API görev panosu (`A-`)
- [[api-araclar]] — API tarafında hangi araç ne zaman
- [[api-durum]] — API'nin güncel durumu — **backend oturumu yazar**
- [[api-notlar]] — Claude'un API gözlemleri (hub) → `02-API/notlar/`

**03-Web** (`DailyCruising.Front-End/`)
- [[web-mimari]] — App Router düzeni, API erişimi
- [[web-kararlar]] — Next.js kararları
- [[web-desenler]] — renk/token, tek kaynaklar, zorunlu görsel doğrulama
- [[web-gorevler]] — Web görev panosu (`W-`)
- [[web-araclar]] — Web tarafında hangi araç ne zaman
- [[web-durum]] — Web'in güncel durumu — **frontend oturumu yazar**
- [[web-notlar]] — Claude'un Web gözlemleri (hub) → `03-Web/notlar/`

**04-Oturumlar** — günlük çalışma notları, compact öncesi anlık görüntüler
**Arşivdir, otorite değildir.** "Nerede kaldık" cevabı yalnızca [[durum]] içindedir.

**_araclar** — `dogrula.py`: kırık link, belirsiz ad, eksik frontmatter, bayat not,
gerekçesiz karar taraması. Not eklendikten sonra çalıştır.

## Web notları (tuzaklar)
- [[web-tasarimi-tarayicida-acmak]] — **tasarımı localhost'ta açıp hesaplanmış stilleri karşılaştırma; sayfa geçirmeden önce oku**

`03-Web/notlar/` altında altı tuzak kayıtlı. **Altısı da `build` ve `lint`'ten temiz
geçti, yalnızca tarayıcıda görüldü** — bu yüzden görsel doğrulama zorunlu:

[[web-tailwind-katman-tuzagi]] · [[web-grid-row-span-tuzagi]] ·
[[web-animasyon-gizli-sekme]] · [[web-gizli-sekmede-scroll-olayi]] ·
[[web-yuzde-yukseklik-grafik]] · [[web-imza-oge-dalga-dikisi]]

## Henüz oluşturulmayanlar

Bilerek yok — içeriksiz dosya boşuna okutur:
- `02-API/veri-modeli.md` — API tasarımına başlanınca
- `03-Web/tasarim-dili.md` — token'lar ve bileşenler zaten `web-mimari.md`'de
