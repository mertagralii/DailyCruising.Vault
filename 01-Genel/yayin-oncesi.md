---
rol: gate
kapsam: genel
guncelleme: 2026-09-11
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

## "Ne zaman patlar" da ölçülür — tahmin edilmez

Bir koşulu yazarken iki soru var ve **ikisinin de cevabı ölçülmeli**: *sağlanmazsa
ne olur* ve **ne zaman patlar**. İkincisi atlanırsa kayıt durur ama yanlış kişiyi
ve yanlış anı işaret eder — bu, sınırı hiç yazmamaya yakın bir sonuç verir.

**Ölçülen örnek (2026-09-10, `Y-15`).** Backend panelin tur adı sorgularının
dile sabitlendiğini gördü ve tetikleyiciyi *"panel bir gün İngilizce
desteklerse"* diye yazdı. Büyük ve uzak bir iş gibi duruyordu. Ön yüz tarafı
ölçüldüğünde gerçek tetikleyici çıktı: **ön yüzün `lang` göndermeye
başlaması** — tek satır, yarın olabilir.

⚠️ Ölçüm ikinci bir şeyi daha değiştirdi: hüküm *"bugün doğru davranıyor"*
değil, **"bugün yanlış davranmasının bir yolu yok"** oldu. İki taraf da uca dil
sormuyor, yani ikisi de aynı sunucu varsayılanında buluşuyor. Bu ikisi farklı
güçte cümleler ve hangisinin doğru olduğu ancak **iki tarafa birden** bakınca
görülüyor.

**Ders:** tetikleyiciyi yazan taraf, çoğu zaman onu göremeyen taraftır. Kendi
alanından bakıp tahmin etmek yerine **diğer alanın kodunu ölç** ya da o alandaki
oturuma sor → [[genel-esszamanli-oturumlar]]

## Koşullar

### 🔊 Gürültülü — sağlanmazsa uygulama açılmaz

| # | Koşul | Kimde | Not |
|---|---|---|---|
| Y-01 | **Postmark** hesabı ve API anahtarı | Mert | e-posta katmanı bunsuz başlamıyor · **Kabul: `Email__Provider=Postmark` ile uygulama açılıyor ve bir deneme e-postası **teslim** oluyor (Postmark panelinde görünür)** |
| Y-02 | **Netgsm** hesabı ve kimlik bilgileri | Mert | SMS katmanı · **Kabul: bir deneme SMS'i gerçek numaraya ulaşıyor; Netgsm panelinde teslim kaydı var** |
| Y-03 | **Paratika** üye iş yeri hesabı (`A-41`) | Mert | İyzico'dan geçildi; **para bugün işletmeye gitmiyor** · **Kabul: sandbox değil **gerçek** üye iş yeriyle bir ödeme alınıyor ve tutar işletme hesabına düşüyor** |
| Y-04 | `KnownProxies` **hem `127.0.0.1` hem `::1`** olmalı | Web | biri eksikse istemci IP'si yanlış okunur · **Kabul: dağıtımdan sonra bir istek at, `RefreshTokens.CreatedIp` **gerçek istemci IP'si** olsun (`::1` veya vekil adresi değil)** |

### ⚠️ Sessiz — uygulama açılır, yanlış çalışır

| # | Koşul | Kimde | Sağlanmazsa ne olur |
|---|---|---|---|
| Y-05 | **Amazon S3 kovasına açık okuma iki öneke** (`boat-media/*` **ve** `blog-media/*`) — `S-24` | Mert | blog kapakları **sessizce kırılır**; uygulama hiçbir hata üretmez, hata yalnız tarayıcıda ve nesne deposunda görünür · **2026-09-05: sağlayıcı Amazon S3 olarak kesinleşti** (Mert), belirsizlik kalktı · **Kabul: yayındaki bir blog kapağı ve bir tekne görseli tarayıcıda **açılıyor** (404 değil)** |
| Y-06 | `/payment/mock` rotası Paratika bağlanınca **kapatılmalı** | Web | açık kalırsa üretimde sahte ödeme yolu açık kalır · **Kabul: `curl -i <site>/payment/mock` → **404**** |
| Y-07 | Gerçek tekne fotoğrafları | Mert | yer tutucu görseller yayında müşteriye gider · **Kabul: rastgele üç tekne sayfasında yer tutucu görsel **yok**** |
| Y-08 | `brand.ts` kurumsal verisi: telefon, adres, TÜRSAB no (`W-06`/`G-10`) | Mert | **her sayfanın üst şeridinde** yanlış bilgi durur → `S-29` · **Kabul: üç ayrı sayfanın üst şeridinde telefon/adres/TÜRSAB no **gerçek** değerler** |
| Y-09 | E-posta şablonları **gerçek istemcide** denenmeli | Web | HTML e-posta istemcileri farklı işler; build ve test bunu yakalamaz · **Kabul: dört şablon Gmail + Outlook + bir mobil istemcide açılıp **gözle** doğrulanıyor** |
| Y-10 | `W-40` aydınlatma metni + saklama süresi | Mert | *"onu ben yazıcam en son"* — KVKK, blocker 7 · **Kabul: metin yayında ve onay ekranından **linkli**; saklama süresi yazılı** |
| Y-11 | Veri göçü | ertelendi | önce site ayağa kalksın · **Kabul: YAZILMADI — ertelendi, koşul netleşmeden ölçüt yazılamaz** |
| Y-12 | **Ters vekil `X-Forwarded-For` eklemeli VE adresi `ForwardedHeaders:KnownProxies` listesinde olmalı** — iki parçalı, `S-19` | Mert + Backend | kayıtlara kullanıcının IP'si değil **vekilin IP'si** yazılır ve uygulama **hiçbir hata üretmez**. Etkilenen alanlar: `Contracts.ApprovedIp` (sözleşme onayının delili), `RefreshTokens.CreatedIp` (oturum geçmişi). ⚠️ Sözleşme onay ekranında *"IP adresin kaydedilir"* yazacaksak bu koşul sağlanmadan **yazılamaz** — yazılırsa beyan yalan olur ve uyuşmazlıkta kaydımız `::1` der. **Kabul ölçütü:** dağıtımdan sonra bir kez giriş yap, `RefreshTokens` son satırındaki `CreatedIp`'ye bak; vekilin adresi çıkıyorsa koşul **sağlanmamıştır**. Aynı ölçüm iki parçayı birden yakalar · **2026-09-05 ölçümü:** yerelde `CreatedIp = ::1`, `UserAgent` **gerçek tarayıcı** (o taraf kapandı) |

| Y-15 | **Panel tek dilli kalmalı — ya da dört sorgu ve iki çağrı birden değişmeli** | Web + Backend | Bugün ekranlarda Türkçe çıkan her tur/bölge adı, uca **dil sorulmadığı** için çıkıyor: sunucu varsayılanı Türkçe. ⚠️ Ölçüldü (2026-09-10): uçta **9 işlem** dil parametresi kabul ediyor (`/api/lookups` dahil, adı `lang`), ön yüz bunu **yalnız iki yerde** kullanıyor ve ikisi de sabit `"tr"` — `boat-detail.ts:304` (yorumlar) ve `review/page.tsx:57` (davet). `lookups` **parametresiz** çağrılıyor (`reservations.tsx`, `staff.tsx`). Panelin tur türü/bölge adını basan dört sorgusu ise uçta `ContentLanguage.Default`'a **sabitlenmiş**, dil parametresi kabul etmiyor (back-end ölçümü, `440648e`). Sonuç: bugün ikisi aynı şeyi söylüyor ama **aynı sebepten değil** — biri soramadığı için, biri sormadığımız için. Panele dil seçimi eklenirse `lookups` seçilen dile geçer, o dört ekran Türkçe kalır ve kutuda "Day cruise" · tabloda "Günlük tekne turu" yazar. **Kabul ölçütü:** panele dil seçimi eklenmeden önce (a) o dört sorgu `lookups` gibi parametreli hâle gelmeli, (b) ön yüzdeki iki sabit `"tr"` seçili dile bağlanmalı. Biri eksikse ekran **sessizce iki dilli** olur |

### 🔬 Doğrulanmamış — yazıldı, gerçek hesap olmadan sınanamadı

Bu bölümün okuma tetikleyicisi ayrıdır: **hesap veya kimlik bilgisi geldiği anda
ilk iş bu listeyi açmaktır.** Yazma tetikleyicisi: bir kod için *"gerçek hesap
olmadan doğrulayamadım"* dediğin an.

| # | Ne | Doğrulanamayan kısım |
|---|---|---|
| Y-16 | **Paratika sağlayıcısı** — dört yöntem, yedi test, beş mutasyon yakalanıyor | `QUERYTRANSACTION` cevabının **tam biçimi**. Sözleşme belgesine göre yazıldı; gerçek yanıtla karşılaştırılmadı · **Kabul: gerçek `QUERYTRANSACTION` yanıtı kaydedilip sözleşme belgesiyle karşılaştırılıyor** |
| Y-13 | **Postmark e-posta şablonları** | HTML e-posta istemcilerinde görünüm (`Y-09` ile aynı kök) · **Kabul: `Y-09` ile aynı ölçüm** |
| Y-14 | **Gerçek AWS'ye S3 bağlantısı** — `ForcePathStyle` 2026-09-05'te yalnız AWS DIŞI sağlayıcılarda açık kalacak biçimde değiştirildi | **Değiştirilen dal hiç çalışmadı.** Testler MinIO'ya koşuyor (`ServiceUrl` dolu → yol-tarzı hâlâ açık) ve üstelik `Program.cs`'i hiç kullanmıyor, kendi `AmazonS3Config`'ini kuruyor. Yani gerçek AWS yolu ne testte ne geliştirmede çalıştı. İlk gerçek kova bağlandığında **ilk yükleme denemesi** bu maddeyi kapatır · **Kabul: gerçek kovaya **ilk yükleme** başarılı (test değil, üretim yolu)** |

⚠️ **Bu bölüm neden var:** 2026-09-05'te backend Paratika'yı yazdı ve pano
"tamamlandı" gösterdi. Testler geçiyordu, mutasyon testi de geçiyordu — ama
**hiçbiri gerçek sağlayıcıyla konuşmamıştı.** "Testi var" ile "doğrulandı" arasında
bu vault'ta artık bir fark var ve o fark burada duruyor.

### ✅ Kapanmış koşullar

| # | Koşul | Kapanış |
|---|---|---|
| ~~Y-00~~ | ~~`/design-system` yayında açık~~ | 2026-09-05'te kapatıldı |
| ~~`S-19`~~ | ~~ağ topolojisi belirsiz~~ | API ve Next aynı makinede, `127.0.0.1` yeterli |

## Her koşul KABUL ÖLÇÜTÜ taşır

2026-09-11'de ölçüldü: 15 koşuldan **13'ünde** *"sağlandığını nasıl anlarız"*
yazmıyordu. Yayın günü bu soruyu sormak için geç olur — o gün hepsi aynı anda
sorulacak.

**Kural:** her satır `Kabul:` ile biter ve ölçüt **gözlemlenebilir** olmalı —
"hesap açıldı" değil, *"deneme e-postası teslim oldu"*. Yazılamıyorsa
`Kabul: YAZILMADI` yazılır; `dogrula.py` **kontrol 26** eksikleri sayar.

⚠️ Aynı denetimde `Y-12` numarasının **iki koşulda birden** kullanıldığı da
çıktı (ters vekil ve Paratika). Sonra yazılan Paratika `Y-16` oldu.

## Buraya yazılmayacak şeyler

- **Yapılacak iş** → panolara (`*-gorevler.md`). Ayrım: burada yazan şey bir
  *koşuldur*, kod yazmakla kapanmaz; hesap açmak, metin yazmak, izin vermekle kapanır.
- **Bugün birini durduran şey** → [[durum]] blocker tablosu. Burası yalnız
  **yayın günü** durduranlar içindir.
- **Neden öyle olduğunun gerekçesi** → ilgili `*-kararlar.md`; buraya yalnız
  koşulun kendisi ve sağlanmazsa ne olacağı yazılır.

İlgili: [[durum]] · [[genel-gorevler]] · [[genel-desenler]] · [[domain-gereksinimler]]
