---
rol: status
kapsam: genel
guncelleme: 2026-08-24
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

- **Web:** tasarım uygulanmış, sayfaların tasarıma göre piksel denetimi sürüyor (W-01)
- **API:** iskelet var, yalnız `/api/health` çalışıyor. Domain görüşmesi bitti,
  sırada **şema** (A-01, sekiz bölüm)
- **Genel:** context havuzu yeniden düzenleniyor (G-09)

Aktif engeller (ayrıntı -> [[durum]]):
kimlik doğrulama yok, panel rotaları herkese açık · API yok, her şey mock ·
fiyat sunucuda doğrulanmıyor · 1 domain sorusu Mert'te (çevrimdışı biniş, G-12) ·
front-end'de 19 dosya commit'lenmemiş

## Okuma tetikleyicileri — koşulsuz

"İlgiliyse oku" değil. Tetikleyici oluştuysa **oku**.

| Tetikleyici | Oku |
|---|---|
| "Nerede kaldık" sorusu | [[durum]] — tek otorite |
| `Back-End/` altında dosya değiştirmeden ÖNCE | [[api-desenler]] + [[api-araclar]] + [[api-gorevler]] |
| `Front-End/` altında dosya değiştirmeden ÖNCE | [[web-desenler]] + [[web-araclar]] + [[web-gorevler]] |
| "Neden böyle yapmışız" sorusu | ilgili `*-kararlar.md` — gerekçe yalnız orada, git log'da yok |
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

İlgili: [[00-Index]] · [[durum]] · [[CLAUDE]] · [[genel-desenler]] · [[genel-gorevler]]
