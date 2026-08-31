---
rol: not
kapsam: web
guncelleme: 2026-08-28
durum: guncel
---

# Elle yazılan yanıt tipi sessizce yalan söyler

`openapi.json` **85 işlemin hiçbiri için yanıt şeması taşımıyor**, bu yüzden
bütün yanıt tipleri elle yazılıyor. Elle yazılan tip, uçla uyuşmadığında
**hiçbir araç uyarmıyor**: `tsc` temiz, `lint` temiz, `build` temiz.

## 2026-08-28'de iki örneği aynı dosyada çıktı

`GET /api/reviews/invitation` için yazdığım tip şuydu:

```ts
type Davet = {
  boatName; boatSlug; reservationCode; startsAt; usedAt; expiresAt;
};
```

Ucun gerçek yanıtı:

```ts
{ boatName, boatSlug, departureDate, criteria[], alreadyUsed }
```

**Dördü uydurma.** Sonuçları:

1. `davet.usedAt` her zaman `undefined` okunuyordu →
   `davet.usedAt ? ... : ...` hiçbir zaman doğru olmuyordu →
   **"bu bağlantı zaten kullanılmış" ekranı hiç görünmedi.** Kullanıcı
   kullanılmış bir jetonla forma giriyor, dolduruyor, gönderirken hata
   alıyordu.
2. `reservationCode` ekranda **`Rezervasyon undefined`** olarak basılıyordu.

Aynı ekranda ikinci bir kusur: alt puanların anahtarları koda gömülüydü
(`cleanliness`, `crew`, `value`, `comfort`) ve uç **kriter kimliği** (`Guid`)
bekliyordu. Bu hiç fark edilmemişti çünkü alt puanlar **isteğe bağlı**:
kimse doldurmadan gönderdiğinde `scores: null` gidiyor ve istek geçiyor.
Yani kusur yalnız formu **tam dolduran** kullanıcıda ortaya çıkacaktı — ve
o sırada (backend doğrulamayı öne almadan önce) jeton çoktan harcanmış
olacaktı, yani o müşteri yorumunu bir daha hiç yazamayacaktı.

## Kural

**Elle yazılan her yanıt tipi, uca bir istek atılarak doğrulanır.** Kaynak
kodu okumak yeterli değil (sözleşme sınıfı ile serileştirilen ad ayrışabilir);
`curl` ya da tarayıcıdan `fetch` ile **gerçek gövde** görülür.

Özellikle şu üç durumda:

- Tip **ilk kez** yazılırken,
- Backend o uca dokunduğunu söylediğinde,
- Alan **isteğe bağlıysa** — çünkü isteğe bağlı alanın yanlışlığı normal
  kullanımda görünmez, yalnız formu tam dolduran kullanıcıda patlar.

İlgili: [[web-notlar]] · [[web-desenler]] · [[web-kararlar]] · [[web-gorevler]]
