---
rol: status
kapsam: genel
guncelleme: 2026-09-11
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
| `DailyCruising.Mobil/` | Expo 57 + React Native 0.86 | `mertagralii/DailyCruising.Mobil` |
| `DailyCruising.Vault/` | bu notlar | repo değil |
| `r-ht-m-temeller-sayfas/` | tasarım kaynağı | repo değil |

Kök klasör git reposu **değil**; git komutları ilgili alt klasörde çalışır.

## Şu an ne oluyor

- **API:** pano 8/165 · **783 test yeşil** (9 Eylül, backend ölçümü). Ödeme uçtan uca
  çalışıyor (gerçek İyzico sandbox). Panoda **Mert'e bağlı olmayan iş kalmadı**
- **Web:** 41 rota · rota koruması `src/proxy.ts` ile çalışıyor (Next 16'da
  `middleware.ts` kaldırıldı, adı `proxy.ts`) · gerçek API'ye bağlandı (`W-04`).
  Pano **4 yapılacak / 80 tamamlandı** — kalanlar **Mert'in kararında**
- **Mobil:** iskelet + private repo var, **ekran yok** · kapsam (`M-02`) **API ve
  web bitene kadar ertelendi** — o zamana kadar mobil kod yazılmaz
- **Genel:** 103 not · `dogrula.py` 28 kontrol, hepsi mutasyonla kırmızıya döndürüldü ·
  makine `_araclar/vault.json` ile taşınabilir

Aktif engel tek (-> [[durum]]): **KVKK yolcu listesi dayanağı** — Mert'te.

**Mert'in önceliği: kendi makinesinde uçtan uca test** (5 Eylül); yayın adımları
bilinçli ertelendi.

⚠️ **"Karar bekliyor" ile "hesap bekliyor" ayrı şeydir.** Mert'te kalanların
hepsi hesap (mobil kapsamı ertelendi): Postmark/Netgsm · Paratika (`A-41`,
İyzico'dan geçildi) · S3 kovası (`S-24`) · `W-40` aydınlatma metni ·
`G-13` mali müşavir. Bunlar bugün kimseyi durdurmuyor, **yayın günü durduracak**.

## Yön: tasarımı backend gerçeği yönlendirir

2026-08-31 Mert talimatı, **kalıcı** → [[genel-kararlar]]:
uç var verisi eksikse **backend tamamlar** · uç ve veri var sayfada karşılığı
yoksa **sayfa o uca göre yapılır** · tasarım bir temeldir, **kısıt değil** —
çelişkide backend gerçeği kazanır. Sapma yasağı *var olan* ekranın görünümü
içindir, *olmayan* ekranı engellemez.

Mert'te bekleyenler: `S-18` (kupon kırpma çelişkisi) · `S-12` (iade oranı, iptal e-postasını kilitliyor) ·
testlerdeki iki ad değişikliği

## Burada NE YOK — ve neden

Okuma tetikleyicileri tablosu, "vault kanıttır" kuralı ve yazma hakkı bölüşümü
**bu dosyadan çıkarıldı** (2026-09-11). Üçü de [[CLAUDE]]'de yazılı ve o dosya da
her oturuma yükleniyor; ikisini birden taşımak aynı 1.400 karakteri iki kez
okutuyordu. Backend oturumu ölçtü ve bildirdi: *"vergi ödüyorum ama karşılığını
almıyorum."* Yerine aşağıdaki iki bölüm geldi — ikisi de tetikleyici gerektirmez,
çünkü her oturumda gerekir.

## Sıfırdan ayağa kaldırma

⚠️ Bunlar her oturumda yeniden keşfedilen komutlardı; üçü ölçülerek buraya kondu.

| Ne | Komut |
|---|---|
| API'yi başlat | `cd DailyCruising.Back-End/src && dotnet run --project DailyCruising.Api` — **`src/` içinden**; kökten koşmak `ConnectionStrings:Default tanımlı değil` verir (user-secrets proje dizinine bağlı) |
| Sağlık | `curl localhost:5163/api/health` — `/health` ve `/healthz` **yok** |
| Şema envanteri | `PSQL_URI=<bağlantı> python3 araclar/sema-cikar.py` — değişkenin adı budur |
| OpenAPI | `DailyCruising.Back-End/araclar/openapi-uret.sh` |
| Web mimari envanteri | `cd DailyCruising.Front-End && python3 araclar/mimari-cikar.py` |
| Vault denetimi | `python3 DailyCruising.Vault/_araclar/dogrula.py` → TEMIZ |
| acilis sayıları | `python3 _araclar/acilis-guncelle.py` — elle yazma |
| Web | `npm run build` · görünüm için **tarayıcıda ölçüm** → [[web-desenler]] |

**`build` ve `lint` görünüm hatasını yakalamaz** — sekiz web tuzağı ikisinden de
temiz geçti, yalnız tarayıcıda görüldü. Bugün beş kusurun beşi de aynı yoldan.

## Her oturum yeniden keşfedilenler

Tetikleyicisi yok ama bedeli yüksek üç şey — ikisi bugün ısırdı:

1. **Vekil izin listesi:** yeni bir uç öneki çağıracaksan `src/app/api/dc/[...path]/route.ts`
   içindeki izin listesine ekle. Web bu tuzağa **dört kez** düştü → [[web-desenler]]
2. **Tasarım belirteci var mı:** `globals.css`'te tanımlı olmayan bir belirteç
   sessizce hiçbir şey çizmez. Bugün 4 üretim dosyasında kenarlığı olmayan rozet
   bulundu → [[web-desenler]]
3. **Migration `dailycruising` rolüyle koşar**, uygulama rolüyle değil →
   [[api-araclar]]
4. **Kabukta sözcük bölme:** `set -- $cift`, `for x in $liste` gibi tek satırlar
   zsh'ta sessizce yanlış sonuç veriyor. Ölçüm alıyorsan Python kullan —
   web bu tuzağa iki kez, backend bir kez düştü; üçünde de sayı **makul**
   göründü → [[genel-desenler]]

## Ölçüm almadan önce — üç soru

Vault kodun doğruluğunu denetliyor, **ölçümün doğruluğunu denetlemiyor.** İki
oturum da bunu aynı gün bildirdi (biri dört kez yaşadı):

1. Beklediğim kadar satır/alan geldi mi? **Sayıyla** doğrula
2. Ölçtüğüm süreç, ölçmek istediğim kodu mu çalıştırıyor? (uptime, commit zamanı)
3. Testin kurulumu, sınanan kodun işini önceden yapıyor mu? Yapıyorsa test o
   davranışı **ölçmez, varsayar** → [[genel-desenler]]

İlgili: [[00-Index]] · [[durum]] · [[CLAUDE]] · [[genel-desenler]] · [[genel-gorevler]]
