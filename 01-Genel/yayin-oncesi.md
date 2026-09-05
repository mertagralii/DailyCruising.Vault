---
rol: gate
kapsam: genel
guncelleme: 2026-09-05
durum: guncel
---

# Yayın Öncesi Koşullar

Bu dosya **görev listesi değil**. Buradaki maddeler yapılacak iş değil, *"üretimde
şu koşul sağlanmazsa bu özellik çalışmaz"* biçiminde **koşullardır**. Görev
panolarına, `durum.md` blocker tablosuna ve karar dosyalarına girmezler — hiçbiri
bugün kimseyi durdurmuyor, hepsi yayın günü durduracak.

## Neden ayrı dosya

2026-09-05'te web oturumu tek bir oturumda **yedi** böyle madde ürettiğini ve
**hiçbirinin vault'ta olmadığını** bildirdi; hepsi sohbette kalmıştı. Sebebi
yapısaldı: bu maddeler görev değil (yapılacak bir şey yok), blocker değil (kimseyi
durdurmuyor), karar değil (tartışılmadı). Gidecek yerleri yoktu.

Hepsi başka bir işin **yan ürünü** olarak doğuyor — bu yüzden sonradan
hatırlanarak toplanamazlar. Yazılma anı, doğdukları andır.

## Tetikleyiciler

| Ne zaman | Ne yapılır |
|---|---|
| Mert "yayına çıkalım" / "hazır mı" dediğinde · deploy konuşulduğunda | **oku** — tam liste burada |
| Bir iş biterken *"bu üretimde şu koşulla çalışır"* cümlesi kurulduğu **anda** | **yaz** — sonraya bırakma |

Yazma hakkı **ortaktır**: koşulu hangi oturum üretiyorsa o yazar
([[domain-gereksinimler]] ve [[genel-gorevler]] gibi). Çakışma riski dosyada
değil, aynı bölüme aynı anda yazmakta.

## Sessiz mi, gürültülü mü — en önemli ayrım

Bir koşulun **sağlanmadığında nasıl belli olduğu**, ne olduğundan daha önemlidir:

- **Gürültülü koşul** — sağlanmazsa uygulama **açılmaz**. Yayın günü fark
  edilmemesi mümkün değil. Bunlar risksizdir; unutulsalar bile kendilerini
  hatırlatırlar.
- **Sessiz koşul** — uygulama açılır ve **sessizce yanlış çalışır**. Hata
  tarayıcıda, günlükte ya da dış serviste kalır. **Asıl tehlike bunlardır** ve
  aşağıda ⚠️ ile işaretlidir.
- **🔬 Doğrulanmamış** — kod yazıldı, testleri var, ama **gerçek hesap olmadan
  doğrulanamadı**. Bu ne "bitti" ne "yapılmadı"; üçüncü bir hâl. Görev panosunda
  "tamamlandı" görünür ve bu **yanıltıcıdır** — panoya güvenen biri doğrulanmış
  sanır.

## Koşullar

### 🔊 Gürültülü — sağlanmazsa uygulama açılmaz

| # | Koşul | Kimde | Not |
|---|---|---|---|
| Y-01 | **Postmark** hesabı ve API anahtarı | Mert | e-posta katmanı bunsuz başlamıyor |
| Y-02 | **Netgsm** hesabı ve kimlik bilgileri | Mert | SMS katmanı |
| Y-03 | **Paratika** üye iş yeri hesabı (`A-41`) | Mert | İyzico'dan geçildi; **para bugün işletmeye gitmiyor** |
| Y-04 | `KnownProxies` **hem `127.0.0.1` hem `::1`** olmalı | Web | biri eksikse istemci IP'si yanlış okunur |

### ⚠️ Sessiz — uygulama açılır, yanlış çalışır

| # | Koşul | Kimde | Sağlanmazsa ne olur |
|---|---|---|---|
| Y-05 | **S3 / DO Spaces kovasına açık okuma iki öneke** (`boat-media/*` **ve** `blog-media/*`) — `S-24` | Mert | blog kapakları **sessizce kırılır**; uygulama hiçbir hata üretmez, hata yalnız tarayıcıda ve nesne deposunda görünür |
| Y-06 | `/payment/mock` rotası Paratika bağlanınca **kapatılmalı** | Web | açık kalırsa üretimde sahte ödeme yolu açık kalır |
| Y-07 | Gerçek tekne fotoğrafları | Mert | yer tutucu görseller yayında müşteriye gider |
| Y-08 | `brand.ts` kurumsal verisi: telefon, adres, TÜRSAB no (`W-06`/`G-10`) | Mert | **her sayfanın üst şeridinde** yanlış bilgi durur → `S-29` |
| Y-09 | E-posta şablonları **gerçek istemcide** denenmeli | Web | HTML e-posta istemcileri farklı işler; build ve test bunu yakalamaz |
| Y-10 | `W-40` aydınlatma metni + saklama süresi | Mert | *"onu ben yazıcam en son"* — KVKK, blocker 7 |
| Y-11 | Veri göçü | ertelendi | önce site ayağa kalksın |

### 🔬 Doğrulanmamış — yazıldı, gerçek hesap olmadan sınanamadı

Bu bölümün okuma tetikleyicisi ayrıdır: **hesap veya kimlik bilgisi geldiği anda
ilk iş bu listeyi açmaktır.** Yazma tetikleyicisi: bir kod için *"gerçek hesap
olmadan doğrulayamadım"* dediğin an.

| # | Ne | Doğrulanamayan kısım |
|---|---|---|
| Y-12 | **Paratika sağlayıcısı** — dört yöntem, yedi test, beş mutasyon yakalanıyor | `QUERYTRANSACTION` cevabının **tam biçimi**. Sözleşme belgesine göre yazıldı; gerçek yanıtla karşılaştırılmadı |
| Y-13 | **Postmark e-posta şablonları** | HTML e-posta istemcilerinde görünüm (`Y-09` ile aynı kök) |

⚠️ **Bu bölüm neden var:** 2026-09-05'te backend Paratika'yı yazdı ve pano
"tamamlandı" gösterdi. Testler geçiyordu, mutasyon testi de geçiyordu — ama
**hiçbiri gerçek sağlayıcıyla konuşmamıştı.** "Testi var" ile "doğrulandı" arasında
bu vault'ta artık bir fark var ve o fark burada duruyor.

### ✅ Kapanmış koşullar

| # | Koşul | Kapanış |
|---|---|---|
| ~~Y-00~~ | ~~`/design-system` yayında açık~~ | 2026-09-05'te kapatıldı |
| ~~`S-19`~~ | ~~ağ topolojisi belirsiz~~ | API ve Next aynı makinede, `127.0.0.1` yeterli |

## Buraya yazılmayacak şeyler

- **Yapılacak iş** → panolara (`*-gorevler.md`). Ayrım: burada yazan şey bir
  *koşuldur*, kod yazmakla kapanmaz; hesap açmak, metin yazmak, izin vermekle kapanır.
- **Bugün birini durduran şey** → [[durum]] blocker tablosu. Burası yalnız
  **yayın günü** durduranlar içindir.
- **Neden öyle olduğunun gerekçesi** → ilgili `*-kararlar.md`; buraya yalnız
  koşulun kendisi ve sağlanmazsa ne olacağı yazılır.

İlgili: [[durum]] · [[genel-gorevler]] · [[genel-desenler]] · [[domain-gereksinimler]]
