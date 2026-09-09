---
rol: constitution
kapsam: mobil
guncelleme: 2026-09-09
durum: guncel
---

# Mobil Desenleri

Her dosyada tekrar uygulanan kurallar. **Karar değil desen:** karar bir kez
verilir (→ [[mobil-kararlar]]), desen her ekranda yeniden uygulanır.

⚠️ **Bu dosya bugün büyük ölçüde devralınmıştır.** Mobil tarafta henüz tek satır
uygulama kodu yazılmadı; aşağıdaki kuralların hiçbiri *bu* platformda ölçülmüş
değil. Her satırın yanında nereden geldiği yazıyor. **Mobilde bedeli ödenmiş
kural yok** — ödendikçe buraya yazılacak ve kaynağı bu dosya olacak.

## Devralınan kurallar — kaynağıyla birlikte

| Kural | Nereden geldi |
|---|---|
| **Mock veri basılmaz.** Veri yoksa hata görünür kalır | [[web-mock-hatayi-gizler]] — mock'un asıl zararı yanlış bilgi göstermesi değil, **hatanın kendisini görünmez yapmasıdır** |
| **Uç noktanın tipi elle yazılmaz**, şemadan türetilir | [[web-elle-yazilan-tip-yalan-soyler]] — uydurulmuş alan adı derleyiciden sessizce geçer |
| **Renk/ölçü sabiti bileşene yazılmaz**, tek kaynaktan okunur | [[web-desenler]] — token'a bağlanmamış değer sessizce ölü kalır |
| **API sözleşmesinin sahibi backend'dir.** Uç eksikse backend tamamlar, mobil uydurmaz | [[genel-kararlar]] 2026-08-31, Mert talimatı |
| **`Kanıt:` satırı olmayan görev tamamlanmış sayılmaz** | [[genel-desenler]] |

## Mobilde henüz karşılığı olmayan kapı — ölçüm

Web tarafının en çok iş gören kuralı şuydu: **`build` ve `lint` görünüm hatasını
yakalamaz**; sekiz görsel tuzağın sekizi de ikisinden temiz geçti ve yalnız
tarayıcıda görüldü → [[web-tasarimi-tarayicida-acmak]]

Mobilde bu kapının **karşılığı yok**. `npx tsc --noEmit` temiz çıkması ekranın
doğru göründüğünü göstermez ve mobilde tarayıcı yerine simülatör/cihaz gerekir;
o yol henüz kurulmadı.

Bu yüzden buradaki kural bugün için şudur: **mobilde "çalışıyor" demeden önce
neyin ölçüldüğü yazılır.** Ölçüm yolu kurulana kadar hiçbir mobil görev
`Kanıt: build temiz` ile kapatılmaz — o cümle mobilde hiçbir şey kanıtlamaz →
[[mobil-gorevler]] `M-03`

## Bir iş "bitti" sayılmadan önce — mobil sırası

API ve Web'de aynı iskelet var; mobilde altıncı adım **eksik** ve bu bilerek
yazıldı → [[mobil-araclar]]

1. **Yorum:** gerekçe kodun yanına yazılır, vault'a değil — kod karşılığı olan
   gerekçe vault'ta bayatlar
2. **Sadeleştirme:** aynı işi yapan daha az parça var mı? Bu adımın hiçbir hata
   sinyali yoktur, o yüzden atlanan adım hep budur → [[genel-desenler]]
3. **Test ve güvenlik:** mobilde test altyapısı **yok**; kurulana kadar bu adım
   "atlandı" diye yazılır, "yapıldı" diye değil
4. **Gözden geçirme:** `ecc:react-reviewer` + `ecc:typescript-reviewer`
5. **Ölçüm:** cihaz/simülatörde görüldü mü — **yolu henüz yok** (`M-03`)
6. **Commit + push:** ölçüm geçtikten sonra; `Kanıt:` satırı panoya yazılır

**`Kanıt: tsc temiz` mobilde geçerli bir kanıt değildir.** Derleyici ekranın
göründüğünü ölçmez; web'de sekiz görsel tuzağın sekizi de `build`'den temiz
geçti → [[web-tasarimi-tarayicida-acmak]]

## Buraya ne zaman yazılır

- Aynı kuralı **ikinci ekranda** tekrar uyguladığımda
- Bir tuzağa düşüp çözdüğümde: kod karşılığı **varsa** gerekçe o satırın yanına,
  **yoksa** `05-Mobil/notlar/` altına; ikisinde de tekrarlanan bir kural doğduysa
  buraya
- Bir kuralı çiğnemek üzereyken bu dosya **okunur** — kapı burada

İlgili: [[mobil-mimari]] · [[mobil-kararlar]] · [[mobil-araclar]] · [[mobil-notlar]] · [[genel-desenler]] · [[00-Index]]
