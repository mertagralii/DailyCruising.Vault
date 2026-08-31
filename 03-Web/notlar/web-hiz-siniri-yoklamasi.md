---
rol: not
kapsam: web
guncelleme: 2026-08-28
durum: guncel
---

# Hız sınırına yoklama yapmak sınırı hiç boşaltmıyor

2026-08-28'de kimlik uçlarının hız sınırına takıldım (`15 dk / 10`, IP bazlı).
Sınırın geçmesini beklemek için her 25 saniyede bir giriş denedim.

**Sınır hiç açılmadı.** `Retry-After` her seferinde **900** döndü — azalmadı.
Yani **reddedilen istek de sayılıyor**: her yoklama pencereyi yeniden dolduruyor
ve kilit kalıcı hâle geliyor.

Yoklamayı tamamen kestikten ~15 dakika sonra giriş ilk denemede başarılı oldu.

## Sonucu — arayüzü doğrudan ilgilendiriyor

- **"Tekrar dene" düğmesi konulmayacak.** `429` gören kullanıcıya yeniden
  deneme imkânı vermek, beklemesi gereken süreyi uzatır
- **Otomatik yeniden deneme yazılmayacak.** Ağ hatasında makul olan davranış
  burada zararlı
- Kullanıcıya `Retry-After` başlığındaki **gerçek süre** yazılır (başlık
  2026-08-28'de eklendi); süre uydurulmaz

## Ölçüm yaparken

Sınırlı bir uçta bekleyeceksen **hiç dokunma.** Yoklama betiği yazmak, beklediğin
şeyi geciktiriyor. Bu, ölçüm aracının ölçtüğü şeyi bozmasının bir örneği —
[[web-olcum-yanlis-pozitifleri]] ile aynı aile.

Sıkışırsan backend `RateLimiting__Enabled=false` ile geçici olarak kapatabiliyor;
ama bu onun sunucusu, istemeden yeniden başlatılmaz.

İlgili: [[web-notlar]] · [[web-olcum-yanlis-pozitifleri]] · [[web-desenler]]
