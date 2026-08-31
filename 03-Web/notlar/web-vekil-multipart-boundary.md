---
rol: not
kapsam: web
guncelleme: 2026-08-28
durum: guncel
---

# Vekilde çok parçalı gövdenin `boundary`'si düşüyordu

`/api/dc/[...path]` vekili **her dosya yüklemesini bozuyordu.** Backend'in
kendisi sağlamdı; hata yalnız vekilden geçen istekte çıkıyordu.

## Belirti

```
400 ValidationFailed
Failed to read the request form.
Multipart header length limit 16384 exceeded.
Too much data before the first boundary.
```

Aynı dosya, aynı uç, **doğrudan backend'e** `curl -F` ile → `200`.
**Vekil üzerinden** → `400`.

## Sebep

Vekil gövdeyi böyle geçiriyordu:

```ts
body = await request.blob();
```

`Blob`'un `type` alanı içerik türünü taşır ama **parametrelerini taşımaz**.
`multipart/form-data; boundary=----WebKitFormBoundaryXyz` başlığı bu yoldan
geçerken `multipart/form-data`ya iniyor, `boundary` düşüyor. `fetch` gövdeyi
`Blob`'tan gönderdiğinde `Content-Type`'ı `blob.type`'tan üretiyor — yani
sunucuya sınırsız bir başlık gidiyor.

Sunucu sınırı bilmediği için gövdenin tamamını "ilk sınıra kadar olan başlık"
sanıyor ve 16 KB'lık başlık sınırına tosluyor. Hata mesajı bu yüzden dosya
boyutundan bahsediyor ama **sorun boyut değil**.

## Çözüm

Ham baytları geçir, başlığı **elle** kopyala:

```ts
body = await request.arrayBuffer();
if (ct) baslik = { "Content-Type": ct };
```

`@/lib/api/client` bunu taşıyabilsin diye `ApiIstek`'e `headers` alanı eklendi.

## Neden önemli

**`build`, `lint` ve `tsc` üçü de temiz geçiyordu.** Kod tip olarak doğruydu;
`Blob` geçerli bir `BodyInit`. Hata yalnız **gerçek bir dosya yüklenince**
ortaya çıktı — vault'taki "build temiz ≠ doğru" listesine dokuzuncu madde.

Bu yalnız tekne görsellerini değil **vekilden geçen bütün yüklemeleri**
etkiliyordu: belge yükleme de aynı yoldan geçiyor.

İlgili: [[web-notlar]] · [[web-desenler]] · [[web-kararlar]] · [[web-gorevler]]
