---
rol: note
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# Denetim kaydını saldırganın kendisi sildiriyordu

`IEventLogger.LogAsync` bir `CancellationToken` alıyordu ve **her çağıran isteğin
kendi jetonunu geçiyordu**. ASP.NET, controller eylemine bağladığı
`CancellationToken`'ı `HttpContext.RequestAborted`'dan verir — yani istemci
bağlantıyı koparınca iptal olur.

Zincir şöyle kapanıyordu:

1. Saldırgan cevabı beklemeden bağlantıyı kopardı (kaba kuvvet ve kupon deneme
   betikleri tam olarak böyle davranır; cevabı okumak zaman kaybı).
2. `RequestAborted` tetiklendi.
3. `EventLogger` içindeki `db.SaveChangesAsync(ct)` `OperationCanceledException`
   fırlattı.
4. Aynı sınıftaki genel `catch (Exception)` onu **yuttu** — bu `catch` bilerek
   oradaydı: olay kaybı kabul edilebilir, müşterinin işlemini bozmak değil.
5. Kayıt hiç yazılmadı.

Sonuç: `auth.login.failed` ve `coupon.rejected` — yani saldırının **tek görünür
izi** — saldırganın kendi davranışıyla siliniyordu.

## Ölçüm

Aynı makinede, aynı gün, iki yönde de ölçüldü. Giriş isteği normalde ~100 ms
sürüyor (PBKDF2 100.000 tur); 30 ms'de kesilen istek kod akışına giriyor ama
tamamlanmıyor:

| Davranış | 3 kopan istek | Yazılan kayıt |
|---|---|---|
| Eski (`ct` geçiliyor) | `--max-time 0.03` | **0** |
| Yeni (jeton yok) | `--max-time 0.03` | **3** |

⚠️ **10 ms'de kesmek yanıltıcı:** istek daha veritabanı aramasına gelmeden
kopuyor, hiçbir davranışta kayıt yazılmıyor ve düzeltme çalışmıyormuş gibi
görünüyor. İlk denemem buydu ve yanlış sonuca götürecekti — kesme süresi
isteğin gerçek süresine göre seçilmeli.

## Düzeltme neden "None geçelim" değil

Parametre "artık `CancellationToken.None` geçin" diye belgelenip bırakılabilirdi.
Bırakılmadı, **kaldırıldı** — 13 çağrı yerinin hepsi `ct` geçiyordu, yani yanlış
kullanım istisna değil kuraldı. Bu projede tekrarlanan ilke:

> Yanlış geçilebilen bir alan er ya da geç yanlış geçilir. Var olmayan alan
> geçilemez.

Aynı ilkeyi `QuoteRequest`'te tutar alanının hiç bulunmaması da uyguluyor →
[[api-desenler]].

`OlayGunluguTests.Olay_yazimi_iptal_jetonu_almiyor` bunu **imza üzerinden**
sabitliyor. Davranış testi yetmezdi: parametreyi varsayılan değerle geri eklemek
mevcut çağrıları bozmaz, yani derleyici de bir davranış testi de uyarmaz.

İlgili: [[api-notlar]] · [[api-desenler]] · [[api-kararlar]] · [[api-hasindex-yutulmasi]]
