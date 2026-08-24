---
rol: constitution
kapsam: genel
guncelleme: 2026-08-21
durum: guncel
---

# Çalışma Düzeni

Kuralların özeti [[CLAUDE]]'de; buradakiler detay.

## Git

Kökte repo **yok**. Her komut ilgili alt klasörde:

```bash
cd DailyCruising.Back-End  && git ...   # → DailyCruising.API
cd DailyCruising.Front-End && git ...   # → DailyCruising.Web
```

- Varsayılan dal: `main`
- Commit mesajı: İngilizce, imperative ("add", "fix"), gövdede **neden** anlatılır
- AI atfı yasak → [[genel-kararlar]]
- Commit ve push **yalnızca Mert isteyince**

## Dil

| Nerede | Dil |
|---|---|
| Konuşma, vault notları | Türkçe |
| Kod, dosya/sınıf/endpoint adları | İngilizce |
| Commit mesajları | İngilizce |

## Doğrulama

| Taraf | Komut | Beklenen |
|---|---|---|
| API | `dotnet build` | 0 uyarı, 0 hata |
| API | `curl localhost:5163/api/health` | `{"status":"healthy"}` |
| Web | `npm run build` | başarılı |

Test altyapısı **henüz yok** → [[durum]]. Test yazılacaksa önce çerçeve kararı gerekir.

## Portlar

| Servis | Port |
|---|---|
| API (http) | 5163 |
| API (https) | 7070 |
| Web | 3000 |

CORS, API tarafında `Cors:AllowedOrigins` yapılandırmasından okunur; `http://localhost:3000`
kayıtlı.

İlgili: [[genel-kararlar]] · [[durum]] · [[00-Index]]

## Not formatı

Her not frontmatter ile başlar:

```yaml
---
rol: constitution | map | status | history | oturum
kapsam: genel | api | web
guncelleme: YYYY-AA-GG
durum: guncel | dogrulanmali
---
```

**Dosya adları benzersiz olmalı** — klasör adına güvenme. `[[kararlar]]` üç dosya
arasında belirsiz kalır; `[[api-kararlar]]` kalmaz → [[genel-kararlar]]

Her not `İlgili: [[x]] · [[y]]` satırıyla biter.

### Karar girişi şablonu

`*-kararlar.md` dosyalarına eklenen her giriş bu biçimde olmalı:

```markdown
## YYYY-AA-GG — <kararın tek cümlelik özeti>

**Karar:** ne yapılacağı, net ve ölçülebilir.

**Neden:** gerekçe. Bu satır atlanırsa not değersizdir — "ne" koddan okunur, "neden" okunmaz.

**Alternatifler:** değerlendirilip elenenler ve eleme sebepleri.

**Sonucu:** bu kararın yarattığı kısıt, borç veya risk.
```

`Alternatifler` ve `Sonucu` boşsa satırı yaz ve "yok" de — atlama. Eksik satır,
sonradan "bunu neden böyle yapmıştık" sorusunu cevapsız bırakır.

## Claude'un not klasörleri

Karar sayılmayan gözlemler `notlar/` altına gider. Serbest biçim; karar şablonu
zorunlu değil, istenildiği kadar dosya açılabilir.

| Alan | Klasör | Ad öneki | Hub |
|---|---|---|---|
| Genel | `01-Genel/notlar/` | `genel-` | [[genel-notlar]] |
| API | `02-API/notlar/` | `api-` | [[api-notlar]] |
| Web | `03-Web/notlar/` | `web-` | [[web-notlar]] |

**Zorunlu üç kural** (üçü de `dogrula.py` tarafından denetlenir):
1. Dosya adı alan önekiyle başlar — vault genelinde benzersizliği bu sağlar
2. Not, kendi hub'ından linklenir
3. Not, en az bir başka nota link verir — yalıtılmış not birikinti olur

Not ile karar arasındaki sınır: **bir daha aynı kararı vermemek için** yazılan şey
karardır (`*-kararlar.md`); **bir daha aynı tuzağa düşmemek için** yazılan şey nottur.

## Oturum notlarının ömrü

`04-Oturumlar/` sınırsız büyür. Kural:

- **Son dosya kutsaldır** — her oturumun ilk okuduğu şey odur, asla silinmez
- Bir oturum notundaki **kalıcı** bilgi ilgili `*-kararlar.md` veya [[durum]] içine
  taşınmalıdır; oturum notu geçicidir
- 30 günden eski oturum notları, kalıcı içeriği taşınmışsa silinebilir
- Silmeden önce kontrol: içinde hiçbir yerde kayıtlı olmayan bir gerekçe var mı?

## Vault sağlık kontrolü

```bash
python3 DailyCruising.Vault/_araclar/dogrula.py
```

Kırık wikilink, aynı adlı not, eksik frontmatter ve bayat `guncelleme` tarihlerini
tarar. Vault'a not eklendikten sonra çalıştırılmalı.

## Cevap uzunluğu

Kısa yaz. Varsayılan ~10 satır; uzun analiz gerekiyorsa önce tek paragraflık özet
ver, detayı ayrıca iste. Mert uzun yanıtları okumuyor — okunmayan yanıt verilmemiş
sayılır.
