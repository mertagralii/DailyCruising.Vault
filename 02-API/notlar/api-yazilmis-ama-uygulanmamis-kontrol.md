---
rol: not
kapsam: api
guncelleme: 2026-08-30
durum: guncel
---

# Yazılmış ama uygulanmamış kontrol — bir kusur sınıfı

Bu projede aynı biçimde ÜÇ kez ortaya çıktı. Ortak yanları: kod doğru
görünüyor, testler geçiyor, kimse yanlış bir şey yapmamış — ve kontrol
hiç çalışmıyor.

| Nerede | Yazılan | Gerçekte olan | Nasıl bulundu |
|---|---|---|---|
| `S3FileStorage` | `publiclyReadable` parametresi | hiç kullanılmıyordu; görünürlüğü yalnız kova politikası belirliyordu — tekne ruhsatı kimliksiz indirilebiliyordu | yan etki ölçüldü: adres kimliksiz istendi |
| `UseRateLimiter` sırası | "kullanıcıya göre böl" | `context.User` boş olduğu için HEPSİ IP'ye bölünüyordu | kimliksiz sel sonrası **kimlikli** istek de `429` aldı |
| Üretim kapıları | on dört açılış kontrolü | ateşledikleri hiç ölçülmemişti | test yazılınca görüldü |

## Ortak sebep

**Ayrımı görebilecek durum hiç kurulmamıştı.**

- Tek kullanıcıyla, kullanıcıya göre bölme ile IP'ye göre bölme **aynı görünür**.
- Tek okuma başarılıyken `null` ile `undefined` **aynı görünür** (arayüz tarafındaki
  kardeş kusur).
- Kova politikası zaten açıkken `publiclyReadable=false` **fark yaratmaz**.
- Kapı hiç denenmezse ateşleyip ateşlemediği **bilinemez**.

Yani testler yanlış değildi; **ayrımın iki tarafı da üretilmemişti.**

## Bunu yakalayan iki soru

1. Bu kontrolün çalışmadığı bir dünya ile çalıştığı dünya, elimdeki
   ölçümde **farklı görünür mü?** Görünmüyorsa ölçüm bu kontrolü
   sınamıyor.
2. Kontrolü **kaldırsam** hangi test kırılır? Hiçbiri kırılmıyorsa
   kontrol sınanmıyor demektir.

İkincisi doğrudan uygulanabilir ve iki kez uygulandı: `A-69` testi eski
ara katman sırasıyla, `A-70` testi kapı devre dışıyken çalıştırıldı —
ikisi de başarısız oldu, yani gerçekten ölçüyorlar.

## Nerede daha aranmalı

- Yapılandırmadan okunup hiçbir yere bağlanmayan ayarlar
- Denetleyici üstündeki özniteliklerin eylem üstündekini ezdiği yerler
- Ara katman sırasına bağlı her kontrol (sıra kaynakta görünmez)

→ [[api-notlar]] · [[api-kararlar]] · [[api-hiz-siniri-tetikleme]]
