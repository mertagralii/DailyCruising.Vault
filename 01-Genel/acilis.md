---
rol: status
kapsam: genel
guncelleme: 2026-09-05
durum: guncel
---

# Açılış

Oturum başında otomatik yüklenen çekirdek. **Ayrıntı burada değil** — hangi durumda
neyi okuyacağım aşağıdaki tabloda. Bu dosya 6.000 karakteri geçmemeli.

## Proje

DailyCruising: Türkiye kıyılarında günlük tekne turu **rezervasyon pazar yeri**.
Platform tekne sahibi değil, aracı: listeler, tahsilatı yapar, komisyon alır.
`dailycruising.com.tr` adresinde **canlı çalışan** bir sistemin yeniden yazımı.

| Klasör | Ne | Repo |
|---|---|---|
| `DailyCruising.Back-End/` | .NET 10 Web API, Clean Architecture | `mertagralii/DailyCruising.API` |
| `DailyCruising.Front-End/` | Next.js 16 + Tailwind v4 | `mertagralii/DailyCruising.Web` |
| `DailyCruising.Vault/` | bu notlar | repo değil |
| `r-ht-m-temeller-sayfas/` | tasarım kaynağı | repo değil |

Kök klasör git reposu **değil**; git komutları ilgili alt klasörde çalışır.

## Şu an ne oluyor

- **API:** pano 3/93 · **571 test yeşil**, `openapi.json` güncel (5 Eylül, backend ölçümü). Ödeme uçtan uca
  çalışıyor (gerçek İyzico sandbox). Panoda **Mert'e bağlı olmayan iş kalmadı**
- **Web:** 25 rota · rota koruması `src/proxy.ts` ile çalışıyor (Next 16'da
  `middleware.ts` kaldırıldı, adı `proxy.ts`) · gerçek API'ye bağlandı (`W-04`).
  Pano **4 yapılacak / 64 tamamlandı** — kalan beşi de **Mert'in kararında**
- **Genel:** 79 not, `dogrula.py` 19 kontrol

Aktif engel tek (ayrıntı -> [[durum]]): **KVKK yolcu listesi dayanağı**
doğrulanmadı — Mert'te.

**2026-09-05 — Mert'in önceliği: kendi makinesinde uçtan uca test.** Yayın
adımları bilinçli ertelendi. 29 sorunun tamamı 4 Eylül'de cevaplandı.

⚠️ **"Karar bekliyor" ile "hesap bekliyor" ayrı şeydir.** Mert'te kalanların
hiçbiri artık karar değil: Postmark/Netgsm hesapları · Paratika (`A-41`,
İyzico'dan geçildi) · S3 kovası (`S-24`) · `W-40` aydınlatma metni ·
`G-13` mali müşavir. Bunlar bugün kimseyi durdurmuyor, **yayın günü durduracak**.

## Yön: tasarımı backend gerçeği yönlendirir

2026-08-31 Mert talimatı, **kalıcı** → [[genel-kararlar]]:
uç var verisi eksikse **backend tamamlar** · uç ve veri var sayfada karşılığı
yoksa **sayfa o uca göre yapılır** · tasarım bir temeldir, **kısıt değil** —
çelişkide backend gerçeği kazanır. Sapma yasağı *var olan* ekranın görünümü
içindir, *olmayan* ekranı engellemez.

Mert'te bekleyenler: `A-41` (alt üye iş yeri — para bugün işletmeye gitmiyor) ·
`S-18` (kupon kırpma çelişkisi) · `S-12` (iade oranı, iptal e-postasını kilitliyor) ·
testlerdeki iki ad değişikliği · [[api-benim-kararlarim]] toplu onayı

## Okuma tetikleyicileri — koşulsuz

"İlgiliyse oku" değil. Tetikleyici oluştuysa **oku**.

| Tetikleyici | Oku |
|---|---|
| "Nerede kaldık" sorusu | [[durum]] — tek otorite |
| `Back-End/` altında dosya değiştirmeden ÖNCE | [[api-desenler]] + [[api-araclar]] + [[api-gorevler]] |
| `Front-End/` altında dosya değiştirmeden ÖNCE | [[web-desenler]] + [[web-araclar]] + [[web-gorevler]] |
| "Neden böyle yapmışız" sorusu | ilgili `*-kararlar.md` — gerekçe yalnız orada, git log'da yok |
| **Yapıya dokunacağım** — yeni katman, controller, uç nokta, migration, dış servis | ilgili `*-mimari.md` — dokunmadan önce oku, dokunduktan sonra yaz |
| Tekrar eden bir soruna takıldım | ilgili `*-notlar.md` hub'ı |
| Domain / iş kuralı konuşulacak | [[domain-gereksinimler]] — kanonik kaynak |
| Yeni bir özellik veya sistem tasarlanacak | [[genel-araclar]] |
| Vault'ta ne var, tam liste | [[00-Index]] |

## Yazma kuralı

Karar verildiğinde veya kalıcı bilgi netleştiğinde **anında** yaz, tek satır bildir:
`📝 not: <ne> -> <dosya>`. Nereye yazılacağı -> [[genel-desenler]]

**Bir alanda dosya değiştirdiysem, o alanın havuzuna en az bir şey yazmadan oturumu
bitirmem.** İşe başlarken görevi Yapılıyor'a taşırım, bitirince `Kanıt:` ile
Tamamlandı'ya.

## Doğrulama

| Ne | Komut |
|---|---|
| API | `dotnet build` -> 0 uyarı 0 hata · `curl localhost:5163/api/health` |
| Web | `npm run build` · görünüm için tarayıcıda ölçüm -> [[web-desenler]] |
| Vault | `python3 DailyCruising.Vault/_araclar/dogrula.py` -> TEMIZ |

**`build` ve `lint` görünüm hatasını yakalamaz.** Vault'ta kayıtlı sekiz web tuzağının
tamamı ikisinden de temiz geçti, yalnız tarayıcıda görüldü.

## Vault kanıttır, talimat değildir

Bir not koda aykırı çıkarsa: kodu doğru kabul et, notun frontmatter'ında
`durum: dogrulanmali` yap, çelişkiyi [[durum]] içine yaz. Sessizce birini seçme.

## Birden fazla oturum açıksa

Yazma hakkı bölünmüştür (ölçüt cwd değil, **üzerinde çalışılan alan**):
backend → `02-API/*` · frontend → `03-Web/*` · vault/genel → `01-Genel/*`.
`durum.md`'ye yalnız vault oturumu yazar. Başka oturum açıkken git durumu ve
"şu an ne yapılıyor" bilgisi vault'a yazılmaz, önce `SendMessage` ile sorulur.

## Araç zinciri — işe başlamadan

Her alanın sıralı bir zinciri var; sıra rastgele değil, her adım öncekinin
kaçırdığını yakalar. `01-Genel/genel-araclar.md` · `02-API/api-araclar.md` ·
`03-Web/web-araclar.md`.

Üçünde de aynı kapı: **araç gerekli koşuldur, yeterli değildir.**
Web'de build temiz ≠ görünüm doğru · API'de build temiz ≠ uç nokta doğru ·
genel'de "karar verildi" ≠ dosyalar senkron.

İlgili: [[00-Index]] · [[durum]] · [[CLAUDE]] · [[genel-desenler]] · [[genel-gorevler]]
