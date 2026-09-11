---
rol: not
kapsam: web
guncelleme: 2026-09-12
durum: guncel
---

# API'ye ulaşılamayınca panel "çıkış yapmış" gibi görünüyor

## Ölçülen

2026-09-12 00:35'te yönetim panelinde iki modül (`rezervasyonlar`,
`musaitlik`) **oturum kapalıymış gibi** açıldı:

- başlıkta "Giriş yap / Kayıt ol",
- kenar menüde yalnız *"Genel bakış"* ve *"Siteye dön"*,
- gövdede `Sunucuya ulaşılamadı. Bağlantını kontrol et.`

Aynı adresler bir dakika sonra **tam** açıldı (60 rezervasyon · 6 kapatma).
Arada tek fark API'nin o an yeniden başlıyor olmasıydı — back-end oturumu
derleme yapıyordu.

⚠️ Oturum **hiç kapanmamıştı**. Çerezler yerindeydi; yalnız
`GET /api/auth/me` isteği bağlantı hatası aldı.

## Sebep — ölçüldü, tahmin değil

`src/lib/auth/session.ts`:

```ts
export async function kimlik(yazabilir = false): Promise<Identity | null> {
  const token = await erisimJetonu(yazabilir);
  if (!token) return null;
  try {
    return await me(token);
  } catch (e) {
    if (yazabilir && e instanceof AuthFailure && e.detail.status === 401) await sessionSil();
    return null;               // ← her hata buraya düşüyor
  }
}
```

`catch` **her** hatayı yutuyor ve `null` dönüyor. `null`'ın tek okuması
var: *"oturum yok"*. Yani üç ayrı durum aynı değere iniyor:

| Gerçek durum | Dönen | Ekranın söylediği |
|---|---|---|
| Çerez yok — misafir | `null` | doğru |
| Jeton geçersiz — `401` | `null` | doğru |
| **Sunucuya ulaşılamadı** | `null` | **yanlış: "çıkış yaptın"** |

Bu projede tekrar eden kalıbın aynısı: **sıfırın üç anlamı** ve üçünün tek
bir değere indirgenmesi → [[web-desenler]]

`kimlik()`'in tek çağıranı `oturumKullanicisi()`, o da bütün site tarafından
kullanılıyor — yani yarıçap yönetim paneli değil, **her sayfa**.

## Neden bu gece düzeltilmedi

Düzeltmenin şekli bir **ürün kararına** bağlı:

**(a) Oturumlu kullanıcı hata sınırına düşsün.** `kimlik()` taşıma hatasını
yutmasın; `error.tsx` *"sunucuya ulaşılamadı, tekrar dene"* göstersin.
Panel için doğru. Ama halka açık sayfalarda da geçerli olur: tekne
listesine bakan oturumlu bir ziyaretçi, API bir saniye takılınca sayfa
yerine hata ekranı görür — bugün sayfayı misafir gibi görüyor ve o daha iyi.

**(b) Yalnız panel katı olsun.** `oturumKullanicisi()` bugünkü gibi kalsın,
`/admin` taşıma hatasını ayrı okusun. Yarıçap dar ama **iki kod yolu**
doğar ve ayrışmaları an meselesi.

**(c) Hiçbir şey yapılmasın.** Belirti geliştirmede back-end yeniden
başlarken çıkıyor; üretimde API kesintisi zaten daha büyük bir sorun.
Bedeli: gerçek bir kesintide personel *"atıldım"* sanıp tekrar giriş
yapmaya çalışır ve sebebi hiçbir yerde okuyamaz.

⚠️ **Eğilimim (b)** — panelin operatörü ile sitenin ziyaretçisi farklı şeye
ihtiyaç duyuyor ve tek davranışla ikisini birden doğru yapmak mümkün değil.
Ama bu auth yolu; gece gözetimsiz değiştirilmedi, Mert'e soruldu.

İlgili: [[web-notlar]] · [[web-sunucu-render-401]] · [[web-durum]]
