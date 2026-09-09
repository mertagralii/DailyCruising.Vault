---
rol: constitution
kapsam: genel
guncelleme: 2026-09-09
durum: guncel
---

# Çalışma Düzeni

Kuralların özeti [[CLAUDE]]'de; buradakiler detay.

⚠️ **Bu dosya PROJEYE özeldir** — portlar, repolar, doğrulama komutları.
Projeden bağımsız çalışma tercihleri (dil, cevap uzunluğu, commit kuralları,
tasarım sadakati) [[tercihler]] içine taşındı; başka bir projeye taşınacak olan odur.

## Git

Kökte repo **yok**. Her komut ilgili alt klasörde:

```bash
cd DailyCruising.Back-End  && git ...   # → DailyCruising.API
cd DailyCruising.Front-End && git ...   # → DailyCruising.Web
cd DailyCruising.Mobil     && git ...   # → DailyCruising.Mobil
```

- Varsayılan dal: `main`
- Commit mesajı: İngilizce, imperative ("add", "fix"), gövdede **neden** anlatılır
- AI atfı yasağı, yazar kuralı, "yalnız istenince commit" → [[tercihler]]

## Dil

Dil kuralı [[tercihler]] içinde — projeden bağımsızdır.

## Doğrulama

| Taraf | Komut | Beklenen |
|---|---|---|
| API | `dotnet build` | 0 uyarı, 0 hata |
| API | `curl localhost:5163/api/health` | `{"status":"healthy"}` |
| Web | `npm run build` | başarılı |
| Mobil | `npx tsc --noEmit` · `npx expo-doctor` | 0 hata · **görünüm kanıtı değildir** → [[mobil-desenler]] |

| API | `dotnet test` | 706 test yeşil (2026-09-09 backend ölçümü → [[api-durum]]) |

⚠️ **Düzeltme 2026-09-05:** bu satırda 21 Ağustos'tan beri *"test altyapısı henüz
yok"* yazıyordu. Yanlıştı ve `rol: constitution` taşıyan bir dosyada durduğu için
okuyan kişiyi yanlış yönlendirirdi → [[durum]]

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

**Neden:** gerekçe. Bu satır atlanırsa not değersizdir — "ne" koddan okunur,
"neden" okunmaz. Değerlendirilip **elenen bir seçenek varsa adı ve elenme
sebebi bu satırın içinde geçer.**
```

⚠️ **2026-09-09'da iki zorunlu satır kaldırıldı** — ölçüldükleri için:

| Satır | Kararlarda bulunma oranı | Karar |
|---|---|---|
| `**Sonucu:**` | **%0** (225 kararın hiçbirinde) | **silindi** |
| `**Alternatifler:**` | %7 başlık olarak, ama içeriği düzyazıda çok daha sık | **başlık silindi, içerik `Neden`e taşındı** |

`Sonucu` unutulduğu için değil **yazılamadığı** için boştu: "bu kararın sonucu
ne oldu" ancak haftalar sonra bilinir ve o an kimse eski karara dönmüyor.

⚠️ Asıl bedeli şuydu: **%0'da duran zorunlu satır, yanındakinin ağırlığını da
götürdü** — `**Neden:**` aynı dosyada %61'de kaldı. Ölü kural, yanındaki canlı
kuralı öldürür → [[genel-desenler]]

### Kısıtlayıcı karar bedelini yazar

Bir şeyi **yasaklayan, kapatan veya tek yol bırakan** karar, bedelini de söyler:
neyi zorlaştırdı, hangi borcu doğurdu.

Koşulludur, zorunlu satır değildir — ve bu bilinçli: bedel bugün kararların
yalnız beşte birinde yazılıyor. Koşulsuz zorunlu yapmak, geriye dönük yüzlerce
karara borç yazar ve üçüncü bir ölü satır üretirdi.

**Denetim:** `dogrula.py` yalnız `**Neden:**`i zorunlu tutar (kontrol 6); elenen
seçenek ve bedel **ölçülür, dayatılmaz** — her koşumda oranları basar. Oran
düşerse görünür olur; sessizce çürümez.

## Claude'un not klasörleri

Karar sayılmayan gözlemler `notlar/` altına gider. Serbest biçim; karar şablonu
zorunlu değil, istenildiği kadar dosya açılabilir.

| Alan | Klasör | Ad öneki | Hub |
|---|---|---|---|
| Genel | `01-Genel/notlar/` | `genel-` | [[genel-notlar]] |
| API | `02-API/notlar/` | `api-` | [[api-notlar]] |
| Web | `03-Web/notlar/` | `web-` | [[web-notlar]] |
| Mobil | `05-Mobil/notlar/` | `mobil-` | [[mobil-notlar]] |

**Zorunlu üç kural** (üçü de `dogrula.py` tarafından denetlenir):
1. Dosya adı alan önekiyle başlar — vault genelinde benzersizliği bu sağlar
2. Not, kendi hub'ından linklenir
3. Not, en az bir başka nota link verir — yalıtılmış not birikinti olur

Not ile karar arasındaki sınır: **bir daha aynı kararı vermemek için** yazılan şey
karardır (`*-kararlar.md`); **bir daha aynı tuzağa düşmemek için** yazılan şey nottur.

## Oturum notlarının ömrü

`04-Oturumlar/` sınırsız büyür. Kural:

- ⚠️ **Düzeltme 2026-09-05:** burada *"son dosya kutsaldır, her oturumun ilk
  okuduğu şey odur"* yazıyordu. Bu hüküm **2026-08-24'te iptal edildi**: her
  oturumun ilk okuduğu şey [[acilis]], "nerede kaldık"ın tek otoritesi [[durum]].
  `04-Oturumlar/` arşivdir, otorite değil → [[CLAUDE]]
- Bir oturum notundaki **kalıcı** bilgi ilgili `*-kararlar.md` veya [[durum]] içine
  taşınmalıdır; oturum notu geçicidir
- 30 günden eski oturum notları, kalıcı içeriği taşınmışsa silinebilir
- Silmeden önce kontrol: içinde hiçbir yerde kayıtlı olmayan bir gerekçe var mı?

## Vault sağlık kontrolü

```bash
python3 DailyCruising.Vault/_araclar/dogrula.py        # denetler
python3 DailyCruising.Vault/_araclar/acilis-guncelle.py  # acilis sayilarini URETIR
```

23 kontrol çalıştırır. Kontrollerin kendisi `_araclar/kontrol-testi.py` ile
ölçülür, notların okunma oranı `_araclar/okunma.py` ile; projeye bağlı sabitler
`_araclar/vault.json` içindedir → [[genel-desenler]]

## Cevap uzunluğu

→ [[tercihler]] (projeden bağımsız).
