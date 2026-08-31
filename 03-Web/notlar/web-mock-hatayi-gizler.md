---
rol: not
kapsam: web
guncelleme: 2026-08-31
durum: guncel
---

# Mock veri, hatanın kendisini gizler

Mock verinin bilinen zararı belli: ekranda yanlış bilgi durur. 2026-08-31'de
ikinci ve daha sinsi bir zararı ölçtüm — **mock, kodundaki hatayı da
görünmez yapıyor.**

## Ölçülen örnek

Rezervasyon listesinde kısa tarih biçimi kullanıyordum: `tarihSaat(iso, "kisa")`
gün ve ay basıyor, **yılı basmıyor**. Mock veriyle bu hiç sorun çıkarmadı,
çünkü uydurma kayıtların hepsi aynı yıldaydı — yıl yazılsa da yazılmasa da
ekran doğru okunuyordu.

Gerçek uca (`GET /api/partner/reservations`) bağlanır bağlanmaz ilk ölçümde
çıktı: `2027-06-17` kalkışlı bir tur listede **"17 Haz"** görünüyor ve bugünden
(30 Ağustos 2026) önceymiş gibi okunuyordu. İşletmeci onu geçmiş bir tur sanar.

Hata biçimlendiricideydi ve **mock veri onu tetikleyemiyordu.** Mock'u ne kadar
dikkatli incelesem bulamazdım; bulunması için verinin birden çok yıla yayılması
gerekiyordu.

## Kural

**Bir ekranı "mock'la çalışıyor" diye doğrulanmış sayma.** Mock, girdi uzayının
dar bir dilimidir ve o dilim genelde en kolay dilimdir: tek yıl, tek para birimi,
hep dolu alanlar, hep başarılı durum, hep kısa metin.

Gerçek uca bağlanınca ekranı **yeniden** ölç — "zaten çalışıyordu" deme.

## Kardeş gözlem: yanıtın başarılı olması kanıt değil

Aynı gün backend oturumu yapısal olarak aynı hatayı yaşadı: olay günlüğüne
değişen alanları dizi olarak gönderiyordu, satır yazılıyordu, uç `200`
dönüyordu — ama **yük boş kalıyordu**, çünkü yük politikası iç içe değerleri
kasten düşürüyor.

İkisinde de hata **yazma tarafındaydı ve okuma tarafından görünmüyordu**:
ben listeye baktığımda "17 Haz" doğru görünüyordu, o `200` aldığında satır
gerçekten yazılmıştı. Doğrulama ikimizde de **başka bir yerden** okumayı
gerektirdi — ben takvimden, o veritabanı satırından.

Kısacası: *yanıtın başarılı olması, yazdığın şeyin doğru olduğunun kanıtı
değildir.*

İlgili: [[web-notlar]] · [[web-elle-yazilan-tip-yalan-soyler]] ·
[[web-olcum-yanlis-pozitifleri]] · [[web-desenler]]
