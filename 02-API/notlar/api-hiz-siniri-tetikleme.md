---
rol: not
kapsam: api
guncelleme: 2026-08-28
durum: guncel
---

# Hız sınırını bilerek tetikleme — ölçülmüş tarif

Arayüz oturumu panel listelerinin **hata hâlini** ölçemedi: sunucuda render
ediliyor, `fetch` sahtekârlığı oraya işlemiyor, geçersiz jeton ise vekil
tarafından `/login`'e yönlendirildiği için hata yoluna hiç ulaşmıyor. Gerçek
tetikleyici `429` / `500` / zaman aşımı.

## Kovaların ömrü aynı değil

| Politika | Sınır | Pencere | Bölümleme |
|---|---|---|---|
| `panel` | 120 | **1 dakika** | kullanıcı, yoksa IP |
| `rezervasyon` · `hesap` | 10 | 15 dakika | IP |
| `rezervasyonSorgu` | 20 | 1 saat | kullanıcı, yoksa IP |
| `personelEkle` | 20 | 1 saat | kullanıcı, yoksa IP |
| `iptal` | — | — | **rezervasyon koduna göre** |

Bu ayrım pratikte önemli: `panel` kovasını yakmak bedavadır, altmış saniyede
kendiliğinden açılır. "Kova yakmayalım" endişesi `rezervasyon` kovasından
geliyor ve panel uçlarına taşınmamalı.

## Ölçülmüş tarif

`/api/conversations`'a 125 istek → 112'si geçti, **13'ü `429`**:

    HTTP/1.1 429 Too Many Requests
    Retry-After: 60
    (gövde BOŞ)

Gövdesiz olması arayüzü ilgilendiriyor: hata metni durum kodundan
üretilmeli, gövdeden okunamaz.

## Bu bulgu bir KUSURU açığa çıkardı (aynı gün düzeltildi)

O 112 istek `401` dönüyordu ve yine de sayılıyordu. İlk yorum "kimlik
çözülemeyince bölümleme IP'ye düşüyor, makul" oldu. **Yanlıştı.**

Arayüz oturumu kimlikli kullanıcıların da etkilendiğini fark etti. Kod
okunduğunda iki ayrı kova görünüyordu; ölçüldüğünde tek kova çıktı:
`UseRateLimiter`, `UseAuthentication`'dan ÖNCE çalışıyordu, yani
`context.User` her zaman boştu ve **kullanıcıya göre bölünmesi gereken
bütün politikalar IP'ye düşüyordu**.

Ölçüm: kimliksiz 130 istekten sonra GEÇERLİ jetonlu istek de `429` aldı.
Düzeltmeden sonra aynı sel sonrası `200`. → `A-69`, [[api-gorevler]]

**Tarif bu yüzden DEĞİŞTİ:** artık kimliksiz sel yalnız IP kovasını
doldurur. Oturumlu bir sayfanın hata hâlini ölçmek için istekleri
**oturumlu istemciyle** atmak ya da API sürecini kısa süre durdurmak
gerekiyor.

**Ders:** kaynak kodda iki ayrı bölüm görmek, çalışma zamanında iki ayrı
bölüm olduğu anlamına gelmez. Ara katman sırası, bölümleme anahtarının
okuduğu veriyi belirliyor ve kod bunu göstermiyor.

## Yapılmayan şey

Hata enjeksiyonu ucu **açılmadı**. Geliştirmede bile olsa kalıcı bir yüzey
demek ve `500` üretmenin bedelsiz yolu var: API sürecini kısa süre
durdurmak, SSR tarafında bağlantı hatası doğurur ve aynı `catch` dalını
çalıştırır → [[api-sessiz-yutulan-hatalar]] · [[api-durum]]
