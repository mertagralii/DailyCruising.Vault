---
rol: not
kapsam: api
guncelleme: 2026-09-09
durum: guncel
---

# "Test artığı" sanılan kayıt — geliştirme veritabanına yazan kim

2026-09-09'da web oturumu panelde `Finans Personeli 920660` adlı bir rol
gördü ve şöyle bildirdi: *"ad ekini üreten bir kod sende yok, yani bu
çakışmayı önlemek için benzersiz ad kullanan bir testten kalmış ve paylaşılan
geliştirme veritabanına sızmış."*

**Teşhis yanlıştı ve yanlışlığı ölçülebilirdi.** Testler Testcontainers ile
**ayrı** bir konteynerde koşuyor; geliştirme veritabanına hiç bağlanmıyorlar.
Bir testin o kaydı yazması fiziksel olarak mümkün değildi.

Ölçüm:

```sql
SELECT "Key", "Name", "CreatedAt" FROM "Roles" WHERE "PartnerId" IS NULL;
-- platform.custom.7e13c86b…  Finans Personeli 920660  2026-09-09 05:24
SELECT u."Email" FROM "UserRoles" ur JOIN "Users" u ON …;
-- demo-zorunlu-920660@ornek.com  ("Zorunlu Personel")
```

Rolün yanında **aynı damgayı taşıyan bir kullanıcı** vardı. İkisi birlikte
`MustChangePassword` akışını canlı API üzerinde uçtan uca doğrulamak için
elle atılmış isteklerdi — yani **benim** kalıntım, testin değil.

## Ders

Bir kayıt "otomatik üretilmiş" görünüyor diye kaynağı otomatik değildir.
Ayırt eden üç soru:

1. **O yazarın o veritabanına erişimi var mı?** Test konteynerdeydi; yoktu.
2. **Kayıt tek mi, yoksa bir öbek mi?** Rolün yanındaki kullanıcı, kaydın
   bir **akış** doğrulamasından geldiğini söylüyordu.
3. **Zaman damgası ne diyor?** 05:24, o akışın yazıldığı oturumun içi.

Aynı aile: [[api-eszamanlilik-testi-yarismayabilir]] — orada da "test şunu
ölçüyor olmalı" varsayımı ölçümle çürümüştü.

## Kalıcı düzeltme

Elle doğrulama kalıntısı geliştirme veritabanında **gerçek kayıttan ayırt
edilemiyor**. İki seçenek var ve ikincisi seçildi:

- Kalıntıyı silmek — ama o kullanıcı `MustChangePassword` ekranını panelde
  görmenin tek yolu; silinseydi özelliğin gösterilebilir hâli giderdi.
- Adını **kendini açıklar** hâle getirmek: `Finans Personeli (deneme)`.
  `A-151` ile gelen `PUT /api/platform/staff/roles/{roleId}` üzerinden
  yapıldı, yani düzeltme aynı zamanda yeni ucun canlı kanıtı oldu.

⚠️ Kural: geliştirme veritabanına elle kayıt atarken **adı kendini
açıklamalı**. Rastgele damga benzersizliği sağlar ama okuyana bir şey
söylemez — ve panelde gerçek kayıttan ayırt edilemez.

İlgili: [[api-notlar]] · [[api-kararlar]] · [[api-gorevler]]
