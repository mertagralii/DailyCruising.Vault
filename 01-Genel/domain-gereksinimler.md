---
rol: map
kapsam: genel
guncelleme: 2026-09-05
durum: guncel
---

# Domain Gereksinimleri

**Kanonik kaynak.** Mert'le yapılan soru–cevap görüşmesinde netleşen iş kuralları.
[[proje]] eski sistemi tarif eder ve davranış atıfları **doğrulanmamıştır**
([[durum]] çelişki tablosu); yeni sistemin dayanağı bu dosyadır.

**Append-only.** Kural değişirse eskisi silinmez; yeni giriş "<tarih> kuralını
iptal eder" notuyla eklenir. Kaynak daima Mert'in doğrudan cevabıdır — Claude'un
çıkarımı ise açıkça *(çıkarım)* diye işaretlenir.

---

## Kapsam kararları

### 2026-08-22 — Yalnızca Türkiye pazarı

Tek saat dilimi `Europe/Istanbul` (Türkiye 2016'dan beri kalıcı UTC+3, yaz saati
yok).

> ⚠️ **Bu maddenin para birimi kısmı 2026-08-23'te İPTAL EDİLDİ.** Aşağıdaki
> "Para birimi — 2026-08-23 DÜZELTMESİ" bölümü geçerlidir: tekne sahibi fiyatını
> TL/USD/EUR/GBP cinsinden girebilir, tahsilat daima TL'dir.

Yurt dışı açılımı *bugün için* kapsam dışı — ama müşteri kitlesi zaten yabancı
turist olduğu için **çok dillilik kapsam içinde kalır**. "Türkiye pazarı" ≠
"yalnızca Türkçe".

---

## Müşteri ve rezervasyon kimliği

### 2026-08-22 — Üyeliksiz (misafir) rezervasyon desteklenecek

Müşteri **iki yolla** rezervasyon yapabilir:
1. Siteye kayıt olup giriş yaparak,
2. **Hiç kayıt olmadan / giriş yapmadan.**

İkisi de birinci sınıf senaryo; misafir rezervasyonu ikincil bir kolaylık değil.

**Şemaya etkisi** *(çıkarım — Mert onaylamadı)*: `Rezervasyon` kaydı bir
kullanıcıya **zorunlu bağlı olamaz**. `KullaniciId` nullable olmalı ve iletişim
bilgisi (ad, e-posta, telefon) rezervasyonun kendi üzerinde taşınmalı. Giriş
yapmış kullanıcıda bu alanlar profilden kopyalanır — referansla değil **kopyayla**,
çünkü kullanıcı sonradan e-postasını değiştirse geçmiş rezervasyonun o günkü
iletişim bilgisi bozulmamalı.

Açık uçlar → aşağıdaki "Cevap bekleyenler".

---

### 2026-08-22 — Rezervasyon kodu ve bildirim akışı

Rezervasyon tamamlanınca müşteriye **hem e-posta hem SMS** gider; ikisinde de
rezervasyon bilgileri ve bir **rezervasyon kodu** bulunur. Müşteri bu kodu sitede
aratarak rezervasyonunu görüntüleyebilir.

Sonuç: **telefon zorunlu alan.** SMS gönderilecekse boş geçilemez.

QR kod müşterinin elinde; tur günü **tekne sahibine gösterilir**, biniş böyle
doğrulanır.

### 2026-08-22 — Yorum, e-postayla gönderilen linkten yapılır

Tur sonrası müşterinin e-postasına "turunuzu değerlendirin" linki gider; yorum o
linkten yazılır. **Üyelik gerekmez** — misafir de yorum yazabilir.

*(çıkarım)* Link, rezervasyona bağlı **tek kullanımlık ve süreli bir jeton**
taşımalı. Yorum hakkı rezervasyona bağlıdır, kullanıcıya değil.

### 2026-08-22 — Aynı e-postayla üye olan, geçmiş misafir rezervasyonlarını görür

Misafir olarak rezervasyon yapan biri sonradan **aynı e-posta ile** üye olursa,
eski rezervasyonları hesabına bağlanır ve "geçmiş rezervasyonlarım"da görünür.

*(çıkarım — güvenlik şartı)* Bu kural e-postayı kimlik anahtarı yapar. Dolayısıyla
kayıtta **e-posta doğrulaması zorunludur**; doğrulanmamış e-postayla üye olmak,
başkasının rezervasyonlarını devralmaya açık kapı bırakır.

### 2026-08-22 — Toplanan müşteri bilgileri

Ad soyad, telefon, **TC kimlik numarası**, adres ve benzeri bilgiler alınacak.

⚠️ **İki açık sorun var, çözülmeden şema kurulamaz:**

1. **Yabancı turistin TC kimlik numarası yok.** Müşteri kitlesinin ağırlığı yabancı
   turist ([[domain-gereksinimler]] kapsam kararı). Alan "TC kimlik no" olarak
   modellenirse ana müşteri segmenti rezervasyon yapamaz. Kimlik, *tür + numara*
   çifti olarak modellenmeli (TCKN / pasaport / yabancı kimlik no).
2. **Kod tek başına yeterli değil.** Rezervasyon sorgulaması yalnız rezervasyon
   koduyla yapılırsa, kodu tahmin eden herkes ad–telefon–kimlik–adres görür.
   Sorgulama **kod + e-posta** (veya kod + telefon) olmalı.

---

### 2026-08-22 — Rezervasyon sorgulama iki faktörlü

Rezervasyon **kod + e-posta** veya **kod + telefon** ile sorgulanır. Kod tek başına
yeterli değildir. *(çıkarım)* Kod rastgele üretilmeli, sıralı olmamalı.

### 2026-08-22 — Kimlik: TCKN veya pasaport

Yabancı müşteriden **pasaport numarası** kabul edilir. Kimlik tek kolon değil,
**tür + numara** çifti olarak modellenir (TCKN / Pasaport / Yabancı Kimlik No);
doğrulama kuralı türe göre değişir.

### 2026-08-22 — Mobil uygulama web'den sonra gelecek

Önce web bitirilecek, ardından **kesinlikle** mobil uygulama yapılacak. QR
doğrulama akışı web'e göre kurulup mobil sonradan uyarlanabilir.

*(çıkarım)* Biniş doğrulaması bir API uç noktası olmalı; kodun kameradan mı
klavyeden mi geldiği istemci detayıdır. Böylece web paneli bugün, mobil uygulama
yarın aynı uçtan çalışır.

---

## Rezervasyon akışı

### 2026-08-22 — Misafir rezervasyon akışı (Mert'in tarifi)

1. Müşteri siteye girer, **kayıt/giriş yapmadan** tekneleri gezer
2. Bir tekne beğenir
3. **Rezervasyon (tur) türünü seçer** → bir tekne birden çok tur türü satar
4. **Yetişkin / çocuk / bebek sayılarını** girer → fiyat bunlardan hesaplanır
5. Ödeme ekranına gelir
6. **Yalnızca ödemeyi yapan kişi kendi bilgilerini girer** — yolcuların bilgileri
   bu aşamada **istenmez**
7. Ödemeyi yapar

### 2026-08-22 — Yolcu listesi: tekne bazlı anahtar, ödemeden sonra doldurulur

`Yolcu` tablosu **girecek**, ama her rezervasyonda değil: teknenin
**"yolcu listesi ister"** anahtarı açıksa. Kapalıysa yalnızca sayılar tutulur.

Böylece kimlik verisi "lazım olur diye" değil, **tekne sahibinin beyan ettiği yasal
yükümlülük** gerekçesiyle toplanır — KVKK m.4'ün istediği belirli/açık/meşru amaç.

**Yolcu başına alanlar** (anahtar açıkken zorunlu): ad soyad, doğum tarihi, kimlik
türü, kimlik numarası. Uyruk isteğe bağlı.

Doğum tarihi zorunlu çünkü çocuk/yetişkin ayrımını **kanıtlanabilir** kılar;
iskeledeki yaş tartışmasını bitirir ve kimlik numarasından daha az hassastır.

**Zamanlama:** ödeme sırasında **istenmez**. Ödemeden sonra e-postaya giden linkten
doldurulur; kalkıştan 24 saat önce eksikse hatırlatma gider (süre tekne bazlı).
Tekne sahibi panelinde "eksik" rozeti görür.

**Kritik kural: eksik yolcu bilgisi binişi ENGELLEMEZ.** Ödemiş müşteriyi form
yüzünden tekneye almamak iade talebi ve kötü yorum üretir. Tekne sahibi eksik
bilgiyi biniş sırasında panelden girebilir.

*(çıkarım)* Rezervasyonu yapan kişi **mutlaka yolcu değildir** (anne–babası için
bilet alabilir). Yolcu listesi rezervasyon sahibinden bağımsız; formu onun
bilgisiyle önden doldur ama silinebilir bırak.

*(çıkarım)* Yolcu satır sayısı ödenen toplam kişi sayısıyla uyuşmalı. Doğum tarihi
ödenen kategoriyle çelişirse **engelleme, tekne sahibine göster** — ticari mesele,
ama komisyon eksik hesaplanmasın diye görünür olmalı.

---

## Fiyatlandırma

### 2026-08-27 — Fiyatlara KDV **dahildir**

**Karar (Mert):** *"Fiyatlarda KDV dahil olsun."*

Tekne sahibinin girdiği fiyat, müşterinin gördüğü fiyat ve tahsil edilen tutar
**aynı sayıdır**; üstüne vergi eklenmez.

**Neden soruldu:** 2026-08-27'de backend ve web oturumları bağımsız olarak aynı
boşluğa çarptı — şemada KDV alanı yok, fiyat tek sayı. İkisi de "bilmiyorum"
dedi ve tahmin etmedi. Karar Mert'e soruldu.

**Tasarım zaten bunu varsaymış ve matematiği tutuyor.** Rezervasyon ekranında
`KDV dahil` yazıyor (`booking-form.tsx`), fatura dökümünde `KDV (%20, dahil)
₺1.087` satırı var. ₺6.525 üzerinden %20 **dahil** KDV = 6.525 × 20/120 =
**₺1.087,50**. Yani tasarımcı içermeli varsaymış, hesabı da doğru yapmış —
karar tasarımı değiştirmiyor, **doğruluyor**.

**Sonuçları:**
- Arayüzde fiyatın yanına "KDV dahil" yazılır; ayrı bir vergi satırı **eklenmez**
- Fatura dökümünde KDV **ayrıştırılarak gösterilir** (dahil tutardan geriye
  hesapla: `tutar × oran / (100 + oran)`), çünkü fatura yasal olarak ayrımı ister
- API'nin döndürdüğü `grandTotalTry` ve `fromPrice` **KDV dahil** tutarlardır;
  istemci üstüne bir şey eklemez

**⚠️ Açık kalan — cevaplanmadı, çıkarım yapılmadı:**

1. **KDV oranı sabit %20 mi?** Tasarım %20 yazıyor ama bu bir tasarım
   yer tutucusu olabilir. Turizm hizmetlerinde farklı oran uygulanan kalemler
   olabilir (konaklamalı turlar, yiyecek-içecek menüsü). **Şemada oran alanı
   tutulmalı mı, sabit mi kabul edilecek** — sorulmadı
2. **Komisyon KDV dahil tutar üzerinden mi hesaplanıyor?** Bugün komisyon
   `grandTotal` üzerinden alınıyor; o tutar artık KDV dahil olduğuna göre
   platform, tekne sahibinin devlete ödeyeceği verginin üzerinden de komisyon
   almış oluyor. Bu **bilinçli bir tercih olabilir** ama teyit edilmedi
3. **Menü ve ek hizmetlerde oran aynı mı?** Yiyecek-içecek farklı orana tabi
   olabilir

Üçü de "Cevap bekleyenler"e eklendi. *(Bunlar çıkarım değil, sorulmamış
sorulardır — cevapsız bırakmak, uydurmaktan iyidir.)*

### 2026-08-22 — Fiyatı tekne sahibi, kiralama tipi başına, mutlak değer olarak girer

Fiyat **(tekne × kiralama tipi)** kırılımında tanımlanır. Tekne sahibi kendi girer.

Her kırılımda **üç ayrı mutlak fiyat**: yetişkin, çocuk, bebek.

**Türetilmiş fiyat YOK.** "Çocuk = yetişkinin %50'si" gibi bir kural olmayacak;
üç fiyat da bağımsız ve elle girilir. Şemada oran/indirim kolonu tutulmaz.

### 2026-08-22 — Bir tekne birden çok kiralama tipi satar

Rezervasyon akışının 3. adımında müşteri tekne sayfasında tur/kiralama türünü
seçiyor → tekne ile kiralama tipi arasında **çoka-çok** ilişki var, fiyat da bu
ilişkinin üzerinde duruyor.

### 2026-08-22 *(çıkarım)* — Ödenen fiyat rezervasyona kopyalanır

Tekne sahibi fiyatı istediği zaman değiştirebildiği için, rezervasyon **o günkü
fiyatı kendi üzerinde saklamalı** (yetişkin/çocuk/bebek birim fiyatları + toplam).
Referansla bağlanırsa, sahibi fiyatı değiştirdiğinde geçmiş rezervasyonların
tutarı ve hesaplanan komisyon geriye dönük bozulur.

### 2026-08-22 — Rezervasyon, ödemeden ÖNCE oluşur ve kapasiteyi tutar

Müşteri ödeme ekranına geçtiği anda `Beklemede` durumunda rezervasyon açılır ve
koltuklar düşer; **15 dakika** ömrü vardır.

- Ödeme başarılı → `Ödendi`
- Ödeme başarısız / terk → süre dolar, **koltuklar iade edilir**

**Gerekçe:** aksi halde son iki koltuk için aynı anda ödeyen iki müşteri
oluşabilir — kapasite aşımı, iade ve kötü yorum. Yük gerektirmez, 100 kullanıcıyla
da olur. Ayrıca ödeme kaydının bağlanacağı bir rezervasyon baştan var olur.

**Durum makinesi:**
`Beklemede → Ödendi → Binildi → Tamamlandı`, yan dallar `Süresi doldu`,
`İptal`, `İade`.

### 2026-08-22 — Ödeme ekranında yalnız ödeyenin bilgisi alınır

`ad soyad + e-posta + telefon`. Yolcu bilgileri bu aşamada **istenmez**.
TC kimlik / adres yalnızca fatura isteyene sorulur.

### 2026-08-22 — Yaş sınırlarını her tekne sahibi kendi belirler

Bebek/çocuk/yetişkin yaş sınırları platform genelinde sabit **değil**; her tekne
sahibi kendi sınırını tanımlar.

*(çıkarım)* İki sonucu var:
1. Rezervasyon formunda sınırlar **açıkça yazılmalı** ("Çocuk: 3–12 yaş"), yoksa
   aynı sitede iki teknede farklı kural olması müşteriyi yanıltır.
2. Sınırlar da fiyat gibi **rezervasyona kopyalanmalı**. Sahibi sonradan "çocuk
   0–10" derse, geçmiş rezervasyonlardaki kategoriler kaymamalı.

### 2026-08-22 — Bebekler kapasiteden düşülmez

10 yetişkin + 2 bebek = 10 koltuk dolu, tekne 12 kişilikse 2 koltuk daha satılır.

⚠️ **Mert bunun tekrar açılabileceğini söyledi — geri dönülecek.** Muhtemel sebep:
yasal/liman kapasitesi ve can yeleği sayımı bebekleri dahil edebilir. O durumda
"ticari kapasite" ile "yasal kapasite" iki ayrı sayı olur.

### 2026-08-22 — Sezonluk fiyat OLACAK (kararı Mert Claude'a bıraktı)

**Karar: temel fiyat + tarih aralıklı istisna.**

- Tekne sahibi kiralama tipi başına bir **temel fiyat** girer (yetişkin/çocuk/bebek).
- İsterse üstüne **tarih aralıklı istisnalar** ekler: "1 Haziran–15 Eylül: 1800".
- Seçilen tarihte istisna varsa o, yoksa temel fiyat geçerlidir.
- Temel fiyat da yoksa tur **online satılamaz** → "fiyat için iletişime geçin".

**Neden sezonluk:** Türkiye kıyı turizmi yoğun sezonlu; tekne sahibi Ağustos'ta
Nisan fiyatına satmak istemez. Desteklenmezse ya platformdan ayrılır ya yıl boyu
yüksek fiyat verip sezon dışını kaybeder — ikisi de zarar.

**Neden şimdi:** Tarih boyutu tablonun *şekli*. Sonradan eklemek kolon eklemek
değil, **fiyat okuyan her sorgu ve her ekranın değişmesi** demek. Sistemin en sık
çalışan sorgusu bu.

**Neden temel + istisna (sadece aralık değil):** Yalnız aralıklarla çalışırsa,
sahibi aralıkları gelecek yıla uzatmayı unuttuğunda tekne sessizce satılamaz hale
gelir. Temel fiyat bu boşluğu kapatır; ilgilenmeyen sahip tek fiyat girip bir daha
düşünmez.

*(çıkarım)* Aynı (tekne, kiralama tipi) için **aralıklar çakışamaz** — veritabanı
kısıtıyla engellenmeli. PostgreSQL'in `daterange` + `EXCLUDE`/GIST kısıtı bunu
tam olarak yapar; veritabanı seçiminde ([[durum]]) somut bir Postgres argümanı.

### 2026-08-22 — "Tekneyi komple kirala" tipi olacak

Kişi başı olmayan, tekne bazlı fiyatlanan kiralama tipleri de bulunacak. Yani fiyat
modeli **iki strateji** taşımak zorunda: kişi başı ve tekne bazlı.

**Mert kiralama tiplerinin tam listesini ve her birinin nasıl çalıştığını
verecek.** Liste gelmeden fiyat şeması kesinleştirilmeyecek.

### 2026-08-22 — Kiralama tipleri (Mert'in tarifi, sekiz tip)

**Paylaşımlı — kişi başı fiyat, kapasite paylaşılır:**

| Tip | Nasıl çalışır |
|---|---|
| Günlük tekne turu | X saatinden Y saatine kadar normal tur |
| Günlük dalış turu | X saatinden Y saatine kadar dalış turu |

**Özel — tekne komple kiralanır, saat aralığı kapatılır:**

| Tip | Nasıl çalışır |
|---|---|
| Özel günlük tekne turu | Belirli saat aralığı; tekne yalnız sana ve getirdiğin yolculara ait |
| Özel balık turu | Aynı şekilde |
| Özel dalış turu | Aynı şekilde |
| Özel gün batımı turu | Aynı şekilde, belirli bir saat aralığında |

**Çok günlü — tekne komple:**

| Tip | Nasıl çalışır |
|---|---|
| Konaklamalı tur | Tekne bir gün boyunca komple senin. **Ama iki günlük fiyat yazılır** — teknenin günlüğü 1000 TL ise bir gün tutsan da 2000 TL ödersin. Sebep: tekne bir gün gezecek, ertesi günün sabahına sahile dönecek |
| Haftalık tekne turu | Tekne bir hafta boyunca komple kapatılır; kapasiteye kadar yolcu getirilebilir |

**Yapı** *(çıkarım)*: iki bağımsız eksen var —
- **Fiyat stratejisi:** kişi başı (2 tip) / tekne bazlı (6 tip)
- **Süre:** gün içi saat aralığı (6 tip) / çok günlü (2 tip)

⚠️ [[proje]] eski sistemde **paylaşımlı balık turu** olduğunu söylüyordu; Mert'in
yeni listesinde yok. Kasıtlı mı, atlama mı — soruldu.

### 2026-08-22 — Konaklamalı tur: kaç gün tutulursa **+1**

Kural: **ödenen gün = tutulan gün + 1**, her zaman. 1 gün tutan 2 gün öder, 3 gün
tutan 4 gün öder. Çarpan (×2) değil, sabit +1.

Sebep: tekne bir gün gezip geceyi denizde geçiriyor, ertesi sabah misafiri sahile
bırakıp limana çekiliyor. Ertesi gün fiilen çalışamıyor.

### 2026-08-22 — Konaklamalının ekstra günü takvimi de kapatır

Yalnız fiyat kuralı değil: **+1 gün müsaitlikte de kapalıdır**. 1 Ağustos'a
konaklamalı tur satılırsa 2 Ağustos'a başka tur satılamaz.

⚠️ **Mert buraya dönebileceğimizi söyledi.**

### 2026-08-22 — Özel turlarda kişi sayısı sorulur ama fiyatı etkilemez

Fiyat = tekneyi kapatma fiyatı. Kişi sayısının fiyata etkisi **yok**. Yine de
yetişkin / çocuk / bebek sayıları **sorulur** (kapasite kontrolü ve yolcu listesi
için).

### 2026-08-22 — Dalış turunda dalan/dalmayan ayrımı YOK

Dalış turunda herkes aynı ücreti öder; dalıp dalmaması fark etmez.

*(not)* [[proje]] eski sistemde "dalan ve dalmayan kişi sayısı sorulur" diyordu —
yeni sistemde **bu kural yok**, Mert doğrudan reddetti.

### 2026-08-22 — Haftalık tur sabit takvim kalıbında

Haftalık tur rastgele bir günde başlamaz; **sabit kalıp** vardır — Cumartesi'den
Cumartesi'ye, Cuma'dan Cuma'ya gibi. *(çıkarım)* Başlangıç günü tekne bazlı ayar
olmalı; her tekne kendi kalıbını seçer.

### 2026-08-22 — Paylaşımlı balık turu YOK

Kişi başı balık turu satılmıyor. Balık turu yalnız **özel** olarak var. Sekiz
tipin ikisi paylaşımlı (günlük tekne, günlük dalış), altısı tekne bazlı.

---

## Menü / ek hizmet

### 2026-08-22 — Teknelerin menüsü olacak, fiyatlı ve ayrı tabloda

Her teknenin bir **menü** bölümü olacak: hangi menüleri sunuyor, her menünün
fiyatı ne. **Hem özel turlarda hem günlük turlarda** geçerli.

Mert: "bunu da ayrı bir veritabanı tablosunda ayarlarız."

**Fiyatlama:** menü **kişi başı** fiyatlanır.

**Zorunluluk:** menü **zorunlu değil**; menüsüz rezervasyon yapılabilir.

**Çeşitlilik:** tek rezervasyonda **birden fazla menü** olabilir (grubun bir kısmı
balık, bir kısmı vejetaryen).

**Tanımlama:** tekne sahibi teknesini girerken menülerini ve fiyatlarını tanımlar.
Menü **kiralama tipine bağlıdır** — aynı teknenin farklı kiralama tiplerinde farklı
menüleri olur.

**Seçim anı:** müşteri kişi sayısını girdiği anda, o sayıya göre menü seçimi açılır.
Yani menü seçimi rezervasyon akışının içinde, **ödemeden önce** — çünkü toplamı
etkiliyor.

### 2026-08-22 — Komisyon, tur + menü TOPLAMI üzerinden alınır

Tur 10.000 + menü 2.000 = 12.000 ise komisyon **12.000 üzerinden** hesaplanır,
yalnız tur bedeli üzerinden değil.

### 2026-08-22 — Menü dışında ek hizmetler de olacak

Mert: "menü dışında ekstra satılan bir şey olabilir, bunu da ekleyelim."

*(çıkarım)* O halde menü tek başına modellenmez; **ek hizmet** diye genel bir yapı
kurulur, menü onun bir türü olur. Böylece transfer / ekipman / fotoğraf paketi
gibi kalemler şema değiştirmeden eklenir.

*(çıkarım)* Menü ve ek hizmet fiyatları da tur fiyatı gibi **rezervasyona
kopyalanır** — sonradan değişirse geçmiş rezervasyonun tutarı ve komisyonu
bozulmasın.

### 2026-08-22 — Menüde yaş kırılımı YOK, menü = sabit paket

Menü fiyatı yaşa göre değişmez. Menü bir **paket**tir, fiyatı neyse odur:

> Menü 1: köfte ekmek + kola + tatlı — X TL
> Menü 2: balık ekmek + pilav + ayran — Y TL

"Çocuk menüsü", "vejetaryen çocuk fiyatı" gibi kırılımlar **olmayacak**.

*(varsayım — Mert düzeltmedi)* Seçilen toplam menü adedi, rezervasyondaki toplam
kişi sayısını aşamaz. Bebeğe menü alınması müşterinin tercihi; sistem zorlamaz.

### 2026-08-22 — Ek hizmetler kişi başı ve komisyona dahil

Ek hizmetler de **kişi başı** fiyatlanır. Adet/sabit fiyatlama **yok**.

**Komisyon matrahı = tur bedeli + menü + ek hizmetler** — yani toplam satışın
tamamı. Mert bunu bilerek seçti (tekne sahibi yemeğin de komisyonunu öder).

*(çıkarım)* Menü ve ek hizmet aynı yapıya oturur: ikisi de tekneye bağlı, kişi
başı fiyatlı, komisyona dahil kalemler. Menü bu yapının bir **türü** olur.

---

## Komisyon, hakediş, iptal

### 2026-08-22 — Menüler her kiralama tipi için ayrı girilir

Menü tekneye bir kez tanımlanıp tiplere işaretlenmiyor; **her kiralama tipi için
baştan ayrı ayrı** giriliyor. Yani menü `(tekne, kiralama tipi)` kırılımına bağlı.

### 2026-08-22 — Komisyon oranı iş ortağına bağlı, yüzde

Oranı **platform (Mert) belirler** ve **iş ortağı bazındadır** — tekneye veya
kiralama tipine göre değişmez. Bir ortağın tüm tekneleri aynı oranı kullanır.

Biçim: **yüzde**. Sabit tutar veya "en az şu kadar" gibi karma kural yok.

*(çıkarım)* Oran değişebildiği için **rezervasyona kopyalanmalı**. Bir ortağın
oranı %15'ten %12'ye çekilirse geçmiş rezervasyonların komisyonu kaymamalı.

### 2026-08-22 — Hakediş periyodik, tur sonrası

Tekne sahibine ödeme rezervasyon anında değil, **belirli aralıklarla** yapılır —
haftalık veya aylık.

**Önemli sonucu:** iptal geldiğinde para hâlâ platformda olduğu için tekne
sahibinden komisyon geri istenmez; komisyon sadece **hiç kazanılmamış** olur.
Turdan önce ödeme yapılsaydı geri çağırma sorunu doğardı.

### 2026-08-22 — İptal ve iade kurallarını platform koyar

Kuralı tekne sahibi değil **platform** belirler.

### 2026-08-22 — Hava muhalefetinde tarih değişikliği teklif edilir

Kaptan/işletme hava nedeniyle turu iptal ederse müşteriye **tarih değişikliği**
teklif edilir. (Bu, müşteri kaynaklı iptalden ayrı bir sebep türüdür.)

### 2026-08-22 *(teyit bekliyor)* — Para ödeme sağlayıcısında duruyor

Mert'in cevabı yazım olarak eksik okundu; anlaşılan **para platformun hesabında
değil, ödeme sağlayıcısında bekliyor**. Doğruysa hakediş kaydı "platformun yaptığı
ödeme" değil, **"sağlayıcıya verilen bölüştürme talimatı"** olarak modellenir.

⚠️ Teyit edilmeden şemaya işlenmeyecek.

### 2026-08-22 — Hava iptali: tarih değişikliği reddedilirse %100 iade

Müşteri teklif edilen yeni tarihi kabul etmezse **tam iade** yapılır. Zorlama yok.

### 2026-08-22 — Hava iptalinde tarih farkı müşteriden istenmez

Yeni tarihin fiyatı daha yüksek olsa bile **aradaki fark müşteriden istenmez**;
rezervasyon eski fiyatıyla taşınır.

*(varsayım — Mert düzeltmedi)* Simetrik olarak, yeni tarih daha ucuzsa da fark
**iade edilmez**. Rezervasyon fiyatı hiç değişmez.

*(not)* Bu kural, rezervasyonun fiyatı kendi üzerinde taşıması kararıyla
kendiliğinden uyumlu: tarih değişince fiyat zaten sabit kalıyor, ek mantık gerekmiyor.

### 2026-08-22 — Hava iptali kaydı için alan bırakılacak

Hava iptalini kimin ilan ettiği ve kaç kez yapıldığı **kayıt altına alınacak**;
şemada baştan alan bırakılacak. Mert suistimal denetiminin nasıl işleyeceğinden
emin değil → DÖNÜLECEK listesine eklendi.

### 2026-08-22 — Para ödeme sağlayıcısında duruyor (teyit edildi)

Müşteriden alınan para platformun hesabında değil, **ödeme sağlayıcısında** bekler.
Hakediş, platformun yaptığı bir ödeme değil, sağlayıcıya verilen **bölüştürme
talimatı** olarak modellenir.

Hangi sağlayıcı olacağı **henüz belli değil** → soru 41 açık.

---

## İş ortağı kaydı ve sözleşme

### 2026-08-22 — İş ortağı başvuru → sözleşme → aktivasyon akışı

1. Tekne sahibi sitedeki **"Tekneni Ekle"** bölümüne gider
2. Formu doldurur: ad soyad, işletme bilgileri, **vergi numarası** vb.; ayrıca
   **parola + parola tekrar** alanları var. Çerez onayı, gizlilik sözleşmesi gibi
   **onay kutuları** da bu adımda
3. Başvuru kaydedilir → başvurudaki e-postaya **"Başvurunuzu aldık, inceleyip size
   sözleşme hazırlayacağız"** maili gider
4. **Platform yönetimi** panelden başvuruyu inceler; bilgileri ve evrakları kontrol
   eder
5. Onaylarsa **panelden bir sözleşme hazırlar** ve iş ortağına gönderir
6. Gönderimde iş ortağının **hem e-postasına hem SMS'ine** bildirim gider:
   *"Sözleşmeniz hazır, başvuruda kullandığınız e-posta ve şifreyle giriş yaparak
   onaylayabilirsiniz"*
7. İş ortağı giriş yapar → **giriş anında sözleşme ekranı açılır**
8. Sözleşmeyi okur; altında *"Sözleşmeyi onaylıyorum"* onay kutusu ve
   onayla / iptal seçenekleri vardır
9. **Onayladığı anda panele erişir** — artık tam kayıtlı iş ortağıdır

*(çıkarım)* Hesap **3. adımda** oluşuyor (parolayı orada belirliyor) ama panele
erişim **9. adıma** kadar kapalı. Yani "hesap var ama yetkisi yok" ara durumu
şemada gerçek bir durum olmalı.

**Durumlar** *(çıkarım)*: `Başvuru alındı → İnceleniyor → Sözleşme gönderildi →
Aktif`, yan dal `Reddedildi`.

### 2026-08-22 — İş ortağı istediği kadar tekne ekleyebilir

Tek tekne sınırı yok. Komisyon oranının iş ortağı bazında olması bununla uyumlu —
ortağın tüm tekneleri aynı oranı kullanır.

### 2026-08-22 — Sözleşme panelde şablondan hazırlanır

Panelde bir **sözleşme şablonu** vardır; platform yönetimi ilgili yerleri
değiştirip gönderir. Dışarıdan PDF yükleme değil.

### 2026-08-22 — Sözleşme onayının kanıtı saklanacak

Onayın **kim, ne zaman, hangi IP'den** yapıldığı kaydedilir. Ayrıca **onaylanan
sözleşme metninin o günkü hali** saklanır — şablon sonradan değişse bile iş
ortağının fiilen neyi onayladığı kaybolmaz.

Anlaşmazlıkta elde tutulacak tek kanıt budur.

### 2026-08-22 — Reddedilen başvuru silinmez

Başvuru reddedilirse kayıt **"Reddedildi" durumunda durur**; silinmez.

### 2026-08-22 — Komisyon oranı sözleşmede yazar

Oran sözleşme metninin parçasıdır.

*(çıkarım)* Bu, oranı sözleşmeye bağlar: **iş ortağının geçerli oranı = aktif
sözleşmesindeki orandır.** Oranı değiştirmek yeni sözleşme (ve yeni onay)
gerektirir. "Oran rezervasyona kopyalanır" kararıyla birleşince zincir tam olur:
sözleşme → oran → rezervasyona kopya → hakediş.

---

## Roller ve yetkiler

### 2026-08-22 — Roller sabit DEĞİL, veri olarak yönetilecek

Başlangıç rolleri: **platform yönetimi**, **tekne sahibi (iş ortağı)**,
**müşteri**, **destek personeli**.

Ama Mert açıkça şunu istedi: *"sen bunu iyi ayarla, çünkü ben daha sonrasında
farklı farklı roller ve farklı farklı yetkiler verebilirim — rol şunları yapabilir,
bunları yapamaz gibi."*

**Sonuç:** roller kodda sabit bir `enum` olamaz. Rol ve yetki **veritabanı kaydı**
olmalı; yeni rol açmak ve yetki eklemek/çıkarmak **kod değişikliği
gerektirmemeli**.

### 2026-08-22 — İş ortağı kendi çalışanlarını tanımlar ve yetkilerini kısar

Bir işletmenin sahibi vardır, altında rezervasyonlara bakan **çalışanları** vardır.
Çalışanlar da panele girebilir, ancak:

- Çalışan hesabını **işletme sahibi kendi panelinden tanımlar** (platform değil)
- Sahibi çalışanın yetkisini **kısabilir** — "şunu yapabilir, bunu yapamaz,
  şunu görebilir, bunu göremez"

*(çıkarım — kritik)* Bu, iki katmanlı bir yetki sistemi demek:
- **Platform yönetimi** platform rollerini yönetir
- **İş ortağı sahibi** kendi çalışanlarının yetkilerini yönetir (devredilmiş yönetim)

*(çıkarım — güvenlik)* Yetkinin iki ayrı boyutu var ve karıştırılırsa veri sızar:
- **Ne yapabilir** (rezervasyon görüntüle, fiyat değiştir, tekne ekle…)
- **Kimin verisi üzerinde** (yalnız kendi işletmesinin kayıtları)

"Rezervasyonları görebilir" yetkisi **tüm rezervasyonlar** anlamına gelmemeli.
Kapsam kullanıcının bağlı olduğu iş ortağından türetilmeli — [[durum]]'daki
"satır bazlı yetki şart" maddesi tam olarak bu.

---

## Katalog ve takvim

### 2026-08-22 — Tekne sahibi takvimde gün kapatabilir, açıklama girer

Bakım, kendi kullanımı, mürettebat yokluğu gibi sebeplerle **gün kapatabilir** ve
kapatırken **açıklama** yazar.

### 2026-08-22 — Yeni tekne doğrudan yayına girer

İş ortağı sözleşmesi onaylıysa eklediği tekne **platform onayı beklemeden**
satışa açılır.

### 2026-08-22 — Yorum yazmak için QR okutulmuş olmalı

Yorum hakkı rezervasyon yapmakla değil, **fiilen tekneye binmekle** doğar —
QR okutulmuş olmalı. Tekne sahibi yoruma **cevap yazabilir**.

Yorumlar **yayına girmeden önce platform onayından geçer**. Onaylanmayan yorum
sitede görünmez.

### 2026-08-22 *(Claude'un önerisi — onay bekliyor)* — Tekne kaydı alanları

Mert "sen ayarla, detaylı olsun" dedi. Önerilen kırılım:

**Kritik ayrım: hangi bilgi tekneye, hangisi `(tekne × kiralama tipi)` ikilisine
ait?** Karıştırılırsa aynı veri tekrar tekrar girilir veya yanlış yerde durur.

**Tekneye ait (bir kez girilir):**
- Kimlik: ad, URL adı, iş ortağı, durum (taslak/yayında/pasif), açıklama *(çok dilli)*
- Tekne tipi: gulet, katamaran, yelkenli, motoryat, sürat teknesi…
- Konum: bölge *(düz liste — il/ilçe hiyerarşisi YOK, Mert onayladı)*,
  marina/kalkış noktası, kalkış tarifi, koordinat
- Kapasite: azami yolcu (ticari) — *yasal kapasite için ayrı alan → D2*
- Konaklama: kabin, yatak, tuvalet/duş sayısı
- Teknik: boy, genişlik, yapım yılı, son yenileme, motor
- Belge: bayrak/sicil no, ruhsat, sigorta, turizm belgesi *(platform doğrulaması)*
- Donanım *(çoktan seçmeli, ayrı tablo)*: klima, şnorkel, müzik sistemi, mutfak,
  duş, wifi, güneş şemsiyesi, sualtı merdiveni, mikrofon…
- **Mürettebat: kaptan adı, mürettebat sayısı, konuşulan diller**
- Medya: fotoğraflar (sıralı, kapak seçili), video
- Kurallar: evcil hayvan, sigara, müzik saati vb.

**`(tekne × kiralama tipi)` ikilisine ait (her tip için ayrı):**
- Saat aralığı (başlangıç–bitiş) veya süre
- Fiyat: temel + tarih aralıklı istisnalar (yetişkin/çocuk/bebek veya tekne bedeli)
- **Menü listesi** — Mert: her tip için ayrı giriliyor
- Ek hizmetler
- Tur programı / gün akışı metni, uğranan koylar
- Fiyata dahil olanlar / hariç olanlar
- Yaş sınırları (bebek/çocuk üst yaşı)
- Haftalık tur için: hafta başlangıç günü

**Not:** "konuşulan diller" alanı özellikle önemli — müşteri kitlesi ağırlıklı
yabancı turist; mürettebatın İngilizce bilip bilmediği satın alma kararını
doğrudan etkiler.

---

## Arama, içerik, destek

### 2026-08-22 — Arama filtrelerinin tamamı olacak

Mert: "hepsi olabilir" — bölge, tarih, kişi sayısı, tur tipi, fiyat aralığı,
tekne tipi, puan.

*(çıkarım — performans)* ⚠️ **Bu madde 2026-08-24'te GERİ ÇEKİLDİ.** Claude
"müsaitlik yazma anında hesaplanıp `(tekne, kiralama tipi, tarih)` başına
saklanmalı" demişti; kendi önerisine 4. bölümde itiraz etti, Mert kabul etti.
Gerekçe ve ne zaman geri dönüleceği → "🔮 GELECEK SÜRÜM" altındaki
`AvailabilityDays` maddesi. Arama bugün canlı sorguyla çalışacak.

### 2026-08-22 — Blog olacak; hem platform hem tekne sahipleri yazabilir

Yazar hem platform yönetimi hem iş ortağı olabilir.

### 2026-08-22 — Destek talep sistemi olacak

Müşteri talep açabilecek; destek personeli rolü buna göre kurgulanacak.

### 2026-08-22 — Kupon/indirim olacak

İndirim kuponu satışta uygulanacak.

**Çelişki çözüldü — indirimi tamamen PLATFORM karşılar.**

İlk ifade iki ayrı kural içeriyordu ve matematiksel olarak bağdaşmıyordu
(1000 TL tur, %15 komisyon, %10 kupon → 850 + 135 = 985 ≠ 900). Mert **A**
seçeneğini seçti:

```
Tekne sahibinin hakedişi = LİSTE fiyatı × (1 − komisyon oranı)   ← indirimden etkilenmez
Platformun payı          = müşteriden tahsil edilen − hakediş
```

Örnek: 1000 TL tur, %15 komisyon, %10 kupon → müşteri 900 öder, tekne sahibi
**850** alır, platforma **50** kalır. İndirimin 100 TL'sinin tamamı platformdan.

**Gerekçe:** kupon platformun pazarlama kararıdır; tekne sahibi o kampanyaya rıza
göstermemiştir. Onun hakedişini platformun promosyonu için düşürmek iş ortağı
güvenini bozar.

### 2026-08-22 — Kupon oranı komisyon oranını AŞAMAZ (sistem engeller)

İndirim komisyonu geçerse platform o rezervasyondan zarar eder. Mert: **sistem
engellesin.** Kazara zarar edilmeyecek.

Komisyon oranı **iş ortağı bazında** olduğu için bu kontrol global yapılamaz.
%20'lik bir kupon, komisyonu %25 olan ortakta geçerli, %15 olan ortakta geçersizdir.
Doğrulama **kuponun uygulandığı an, o rezervasyonun iş ortağının oranına karşı**
yapılır.

**Aşan kupon ne olur:** o teknede **geçersiz sayılır** (kırpılmaz). Müşteriye
"bu kupon bu tekne için geçerli değil" denir — kırpılsaydı müşteri ilan edilen
oranla uygulanan oranın farkını şikayet ederdi.

*(çıkarım)* Kupon oluşturma ekranında uyarı gösterilmeli: "bu oran şu N iş
ortağının komisyonunu aşıyor, onlarda geçmeyecek".

---

## Müsaitlik modeli — D1 ÇÖZÜLDÜ

### 2026-08-22 — Teknenin TEK takvimi vardır; kiralama tipleri ayrı takvim değildir

**Reddedilen model:** müsaitliği `(tekne, kiralama tipi, tarih)` başına ayrı tutmak.

**Neden reddedildi (Mert'in senaryosu):** Mehmet 15 Eylül'e *günlük tur* alır.
Birkaç saat sonra Cemil aynı tekneye 15 Eylül için *konaklamalı tur* almak ister.
Ayrı takvimlerde konaklamalı satırı hâlâ boş görünür ve Cemil satın alabilir —
ama ortada **tek bir tekne** vardır ve aynı gün iki yerde olamaz.

**Kabul edilen model — Sefer:** her satış teknenin takviminde bir **zaman aralığı**
işgal eder.

| Kiralama tipi | Kapladığı zaman | Paylaşımlı |
|---|---|---|
| Günlük tekne / dalış turu | O günün saat aralığı | ✅ koltuklar paylaşılır |
| Özel turlar (tekne/balık/dalış/gün batımı) | O günün saat aralığı | ❌ tek müşteri |
| Konaklamalı | Tutulan gün **+1** | ❌ tek müşteri |
| Haftalık | 7 gün | ❌ tek müşteri |

**Tek kural: aynı teknede iki sefer zaman olarak çakışamaz.**

*(sonuç)* **D3 kendiliğinden çözüldü** — konaklamalının +1 günü seferin zaman
aralığına dahil olduğu için ayrı bir takvim kuralı gerekmiyor.

*(sonuç)* Paylaşımlı turda birden çok rezervasyonun **aynı sefere** bağlanması
zaten zorunlu (koltukların ortak havuzda toplanması için). Yani sefer kavramı
tercih değil, gereklilik.

### 2026-08-22 — Takvim modu: tekne sahibi günün ne olacağına ÖNCEDEN karar verir

İlk-gelen-alır modelinin sorunu: Mehmet'in 2 koltukluk rezervasyonu, o gün gelecek
20.000 TL'lik konaklamalı talebini engeller. Tekne sahibi parayı **tesadüfen**
kaybeder.

**Çözüm — mod bazlı takvim.** Tekne sahibi tarih aralıkları için mod tanımlar:

| Mod | Satılabilir | Satılamaz |
|---|---|---|
| **Paylaşımlı gün** | Günlük tekne turu, günlük dalış turu | Özel, konaklamalı, haftalık |
| **Özel'e açık gün** | Özel turlar, konaklamalı, haftalık | Paylaşımlı |

Gün gün değil **kuralla** tanımlanır: *"1 Haziran–30 Eylül paylaşımlı"*,
*"1 Ekim–31 Mayıs özel'e açık"*, istisna günler tek tek işaretlenebilir.

**Neden bu çözüm:** ödemiş müşterinin rezervasyonu **asla iptal edilmez** (Mert'in
şartı). Dolayısıyla koruma satıştan sonra olamaz, satıştan **önce** olmalı.
Mod bazlı takvimde Cemil 15 Eylül'ü konaklamalı olarak **hiç görmez** — hayal
kırıklığı yok, iptal yok, kayıp yok.

**Kritik nokta:** tekne sahibi yine de o 20.000 TL'yi almıyor — ama artık
*tesadüfen kaybetmiyor*, **kendi seçiyor**. İnsan kendi kararına kızmaz.

### 2026-08-22 — Paylaşımlı turda asgari kişi sayısı OPSİYONEL

Tekne sahibi isterse asgari kişi girer ("6 kişi dolmazsa sefer kalkmaz"), girmezse
kural yoktur.

Panelde açıkça uyarılır: **asgari koyarsanız dolmadığında turu iptal etmek zorunda
kalırsınız.** Böylece iki riski de sahibin kendisi seçer:
- Asgari yok → az kişiyle çıkma riski, **sıfır iptal**
- Asgari var → dolu sefer, **iptal riski**

Platform hiçbirini dayatmaz.

---

## 🔮 GELECEK SÜRÜM — kesinlikle yapılacak, ilk sürümde değil

### 2026-08-24 — Sezonluk AI analiz raporları (Mert)

Sezon başı ve sonu arasında sitede olan **tüm işlemlerin** AI ile analiz edilip
**dört ayrı kitleye** rapor üretilmesi. Mert: *"bunu ilerde kesin yapacağımız için
bizim önceden bu sistemi de hazırlamamız gerekiyor ki elimizde bir veri havuzu
oluşsun."*

| Kitle | Rapor neyi cevaplar | Ne işe yarar |
|---|---|---|
| **Müşteri** | Sezon boyunca neler yaptı, neyi sevdi/sevmedi, değerlendirme yaptı mı, en çok sevdiği tekne | Kişiye özel destek, kupon ve reklam hedeflemesi |
| **Tekne sahibi** | En çok kullanılan / en sevilen / en çok yorum alan tekne, müşteriler neyi sevdi–sevmedi | Sonraki sezon hangi iyileştirmeler yapılmalı |
| **Site sahibi** | Sezonda ne oldu, en iyi işletmeci ve destek personeli kim, kâr–zarar, kullanılan kupon, cevaplanan destek mesajı, memnuniyet | Sonraki sezon için aksiyon planı |
| **Destek personeli** | Aynı kırılım, destek tarafı | Nelere dikkat edilmeli, hangi aksiyonlar alınmalı |

### 2026-08-24 — Diğer planlanan otomasyonlar (Mert)

- Gelen e-postalara **kişiye göre otomatik cevap** veren entegrasyon
- **Haftalık blog yazılarını otomatik yazan** otomasyon

Mert: *"bu projenin diğer rezervasyon sitelerinden farkı bu yönde de olsun."*

---

### 2026-08-24 — AI entegrasyonları: 1–5 KABUL EDİLDİ (Claude önerdi, Mert onayladı)

Mert: *"1, 2, 3, 4 ve 5 sonrasında ekleyeceğiz."* İlk sürümde değil, ama
**yapılacak** — şema bunlara kapatılmayacak.

**1 — Hava durumu ön uyarısı** ⭐ *(Claude'un birinci önceliği)*
Sistem hava tahminini izler, tekne sahibini **48–72 saat önceden** uyarır:
*"15 Eylül için 6 Bft rüzgar bekleniyor, o gün 3 rezervasyonun var."*
**Neden ilk sırada:** hava iptali bu işin en can sıkıcı sorunu. Müşteri 3 saat
değil 3 gün önce haber alır; tarih değişikliği erken teklif edilir, iade ve kötü
yorum önlenir. **AI bile gerekmez** — hava API'si + kural. Ucuz, hızlı, rakiplerde
yok.

**2 — Mesajlaşmada anlık çeviri**
Turist Almanca yazar, tekne sahibi Türkçe okur ve Türkçe cevaplar, turist Almanca
okur. **Özellik değil, pazar açıcı:** bugün yabancı turist yalnız İngilizce bilen
mürettebatı olan tekneyi seçebiliyor. Çeviriyle **İngilizce bilmeyen tekne
sahipleri de yabancı turiste satabilir** — arzın ve talebin önündeki en büyük
engel kalkar. Mesajlaşma zaten sistemde olduğu için o katmana takılır.

**3 — Yorum özeti**
Müşteriye: *"misafirler yemeği ve kaptanı övüyor; tekrar eden tek şikayet dönüşte
müzik sesi."* Tekne sahibine aksiyon olarak: *"12 yorumda gölge alanı yetersizliği
geçti, tente değerlendir."* Ucuz, görünür; hem satışa hem arz kalitesine yarar.

**4 — İlan kalite koçu**
*"Açıklaman 40 kelime, benzer guletler 180 yazıyor. 3 fotoğrafın var, ortalama 18.
Tur programı ve fiyata dahil olanlar boş."* Fotoğraf kalite kontrolü de dahil
(bulanık, karanlık, tekne görünmüyor, filigranlı). Arz kalitesi yükselince her şey
yükselir.

**5 — Fiyat önerisi**
*"15 Ağustos hafta sonu Bodrum'da 12 kişilik guletler ortalama 1.850 istiyor, sen
1.200 yazmışsın."* Doğru fiyatlama hem tekne sahibinin gelirini hem platformun
komisyonunu artırır. **Olay günlüğü olmadan çalışmaz** — geçmiş arama ve satış
verisi gerekir.

### 2026-08-24 *(önerildi, karar verilmedi)* — Suistimal tespiti ve D5 bağlantısı

Claude'un 6. önerisi. Mert 1–5'i saydı, bunu ayrıca onaylamadı.

Yakalayabilecekleri: bir teknenin hava iptali oranının bölge ortalamasının çok
üstünde olması · iptal edilen rezervasyonların hep düşük tutarlı olması ·
mesajlarda platform dışına çıkma girişimi (maskeleme *"beni dışarıdan halledelim"*
cümlesini yakalamaz) · sahte yorum örüntüleri.

**D5 ile bağı:** hava iptali suistimal denetimi *"bir sezon veri toplansın, sonra
bakılsın"* diye ertelenmişti. Bu, o kararın uygulanma biçimi olabilir.

### 2026-08-24 — AI entegrasyonları 7–16 (hepsi kabul edildi)

Mert: *"hepsini ekle."* Amaç üç taraflı: **tekne sahibini, destek ekibini ve site
sahibini dertten kurtarmak** — ve daha fazla kazanmak.

**Güven ve sorumluluk**

- **7 — Belge ve sigorta doğrulama** ⭐ AI yüklenen ruhsat/sigorta/turizm belgesini
  okur, **bitiş tarihini çıkarır**, dolmadan uyarır, dolduğunda tekneyi satıştan
  düşürür. *Sigortası bitmiş tekne müşteri taşıyorsa sorumluluk platformdadır.*
  35 teknede elle zor, 500 teknede imkânsız.
- **8 — Yorum ön-moderasyonu** Yorumlar platform onayından geçiyor (2026-08-22
  kararı). Bu bugün kolay, 500 teknede tam zamanlı iş. AI önce elesin (küfür,
  alakasız, kişisel bilgi, rakip reklamı, sahte örüntü); insan yalnız işaretlenene
  baksın.
- **9 — Yorum ↔ ilan tutarsızlığı** İlanda "klima var", yorumlarda "klima
  çalışmıyordu" → çelişki platforma bildirilir. İlan doğruluğunun sessiz çürümesini
  durdurur.

**Satış ve dönüşüm**

- **10 — Terk edilen ödemeyi kurtarma** ⭐ `Beklemede → Süresi doldu` tetikleyicisi
  **zaten şemada var**. Bir saat sonra otomatik e-posta: aynı tekne, tarih, fiyat,
  tek tıkla devam. AI bile gerekmez.
- **11 — Doğal dilde arama** *"Ağustos'ta 6 kişiyiz, iki çocuk var, Bodrum'dan
  kalkan, yemek dahil sakin bir tekne"* → filtrelere çevrilir. Yabancı turistin
  platformun taksonomisini bilmesi gerekmemeli.
- **12 — Kapak fotoğrafı seçimi** Kapak fotoğrafı bir ilanın en büyük dönüşüm
  kaldıracı; sahibi rastgele seçiyor. AI en iyisini seçsin.
- **13 — Boş gün uyarısı** *"2 haftada 6 günün boş, geçen yıl %80 doluydun."*
  Boş gün ölü envanterdir.

**Arz kalitesi**

- **14 — Tekne açıklamasını AI yazsın** 4 numaralı "ilan kalite koçu" *azarlıyor*;
  bu *işi yapıyor*. Sahibi fotoğraf ve birkaç alan verir, AI taslağı yazar.

**Operasyon yükü**

- **15 — Rezervasyon sonrası bilgi kartı** Tur öncesi otomatik: buluşma yeri, saat,
  hava, ne getirmeli. Mesajlaşmaya ve desteğe gelen soruların çoğunu **sorulmadan**
  cevaplar.
- **16 — Destek talebi sınıflandırma + taslak cevap** Etiket (iade/bilgi/şikayet/
  teknik) + **tur tarihine göre öncelik**: turu 2 gün sonra olan iade talebi geçen
  ayki sorudan acildir. Üstüne taslak cevap.

### 2026-08-24 ⚠️ TASARIM İLKESİ — veri önce, entegrasyon sonra

Mert: *"bu entegrasyonları yapabilmem için yapay zekalara doğru veriyi vermem
gerekiyor, bu verilerin de öncesinde hazır olması gerekiyor. Belli bir zamandan
sonra bunu yapalım dediğimde veritabanında aradığımız veriyi bulamazsak bizim için
sıkıntı olur."*

**Bu, şemanın tasarımına uygulanacak bir kuraldır.** Her varlık tasarlanırken
sorulacak: *bu varlığın başına hangi olaylar geliyor ve onları kaydediyor muyuz?*

Hangi entegrasyon olay günlüğüne bağlı:

| Bugünün verisiyle çalışır | **Olay günlüğü şart** |
|---|---|
| Belge doğrulama · yorum moderasyonu · yorum-ilan tutarsızlığı · kapak fotoğrafı · açıklama yazma · bilgi kartı · destek sınıflandırma · hava uyarısı | Terk edilen ödeme kurtarma · boş gün uyarısı · kişiselleştirilmiş arama · fiyat önerisi · sezon raporları |

### 2026-08-24 — Otomasyon platformu: muhtemelen n8n

Mert: *"büyük ihtimal bu entegrasyonları n8n'de yapabiliriz eğer gerekirse."*

⚠️ **Önemli ayrım:** n8n **otomasyon katmanıdır, veri katmanı değildir.**
Uygulamanın yaymadığı bir olayı n8n kaydedemez. Yani olayları **API üretecek**,
n8n yalnızca tetikleyip iş akışını yürütecek.

*(çıkarım)* Bunun şemaya etkisi: olay günlüğü **dışarıdan tüketilebilir** olmalı —
kararlı kimlikler, zaman damgası, olay türü, ve zaman aralığı + tür ile
sorgulanabilirlik. n8n iş akışlarının ihtiyacı tam olarak budur.

### 2026-08-24 — Uygulama sırası önerisi (Claude)

| Öncelik | Ne | Neden |
|---|---|---|
| **Şimdi** | Olay günlüğü | Ertelenemez, geriye dönük üretilemez |
| İlk sürümden sonra | Hava uyarısı · yorum özeti | Ucuz, hızlı, görünür fark |
| Sonra | Mesaj çevirisi · ilan koçu | Arzı ve talebi büyütür |
| Veri birikince | Fiyat önerisi · suistimal tespiti · sezon raporları | Geçmiş veri şart |

Mert'in kendi listesindeki **e-posta otomatik cevabı** ve **haftalık blog
otomasyonu** iç yükü azaltır; yukarıdakiler pazarda fark yaratır. İkisi de gerekli,
sıra böyle kurulmalı.

### 2026-08-24 ⚠️ ŞEMAYI BUGÜN ETKİLER — olay günlüğü (event log)

**Bu, ertelenebilir bir madde DEĞİL.** Analizin kendisi ertelenir; **veriyi
toplamak ertelenemez.**

Sebep: mevcut tablolar yalnızca **son durumu** tutar. `Reservation` tablosu
müşterinin rezervasyon yaptığını söyler; **20 kez arama yaptığını, 8 tekne
görüntülediğini, 2 kez ödeme ekranına gelip vazgeçtiğini söylemez.** Analizi
değerli kılan tam olarak bu veridir ve **geçmişe dönük üretilemez.** Geçen sezonun
olayları kaydedilmediyse sonsuza kadar yoktur.

**Toplanacak olaylar** *(çıkarım)*:
arama (filtreler, sonuç sayısı, tıklandı mı) · tekne görüntüleme · ödeme ekranına
gelip terk (`Beklemede → Süresi doldu`) · mesajlaşma (adet, ilk cevap süresi) ·
destek talebi (açılış, ilk cevap, çözüm süresi) · yorum ve puan · iptal (sebep ve
kim) · kupon kullanımı · teklif gönderimi ve kabul/ret.

**Tasarım ilkesi:** olay günlüğü **değişmez ve append-only** — para defteriyle aynı
mantık. Satır güncellenmez, silinmez.

⚠️ **KVKK:** müşteri profilleme ve **reklam hedeflemesi** ayrı bir hukuki dayanak
ister (açık rıza). Rapor üretmek ile pazarlama amaçlı kullanmak farklı şeylerdir;
kayıt altyapısı ortak olsa da izin ayrı yönetilmeli.



### 2026-08-24 — Çevrimdışı biniş: şimdilik elle işaretleme, kuyruk mobilde (G-12 KAPANDI)

İskelede internet çekmediğinde QR okutulamıyor. Mert **c** seçeneğini seçti,
**a**'yı gelecek sürüme aldı: *"1 soru içinde a kısmını ilerde yaparız, bunu da
kesinlikle ekle."*

**İlk sürüm (c):** tekne sahibi internet gelince panelden "bindi" işaretler.
`BoardingScans.Method` değerine `Manuel` eklenir. Şema bugün hazır, ek geliştirme yok.

**Gelecek sürüm (a) — çevrimdışı kuyruk:** mobil uygulamada tekne sahibi kodu
çevrimdışı okutur/girer, cihaz kaydı kuyruğa alır, bağlantı gelince eşitler.
Mobil uygulama web'den sonra geleceği için sırası da doğal.

**Neden ertelendi:** çevrimdışı kuyruk gerçek bir senkronizasyon problemidir —
aynı rezervasyon iki cihazda okutulabilir, saat kayabilir, çakışma çözümü gerekir.
Web-only ilk sürümde karşılığı yok.

**Şema buna bugünden hazır:** `BoardingScans` her okutmayı ayrı satır tutuyor ve
`ScannedAt` ile `DeviceInfo` taşıyor. Çevrimdışı kuyruk geldiğinde eklenecek tek
şey `ClientRecordedAt` (cihazın kendi saati) ve `SyncedAt`. Tek tablo, iki kolon.

⚠️ **Biniş sonrası tetiklenen iki şey** çevrimdışıda gecikir: yorum hakkı doğması
ve mesajlaşmanın kapanması. İkisi de gecikmeye tahammüllü — engel değil.

---

### 2026-08-24 — Rezervasyon değişikliği YOK, yalnız iptal (ilk sürüm)

Mert: *"değişiklik olmasın sadece iptal şimdilik ama bu özelliği de getiririz."*

**İlk sürümde:** müşteri kişi sayısını veya tarihi değiştiremez. İsterse iptal eder
ve yeniden alır. Hava muhalefetindeki tarih değişikliği **ayrıdır** ve durur —
onu platform teklif eder, müşteri talep etmez.

**Gelecek sürüm — `ReservationAmendments`:** her değişiklik ayrı satır olur; ne
değişti, fark tutarı, yeni komisyon, kim onayladı. Rezervasyonun kendisi
güncellenmez, üzerine değişiklik kaydı biner.

**Neden ertelendi:** değişiklik para farkı ve **yeni komisyon** üretir; kısmi
tahsilat, kısmi iade ve hakediş defterinde ek kayıt demek. 6. bölümdeki para
defteri oturmadan üstüne değişiklik akışı kurmak erken.

**Neden şemayı bozmuyor:** para defteri zaten değişmez ve append-only. Değişiklik
geldiğinde defterde yeni satırlar açılır, eskiler düzeltilmez — model aynı kalır.

---

### 2026-08-24 — `AvailabilityDays` özet tablosu ERTELENDİ (bakılacak)

Aynı gün içinde Claude kendi eski önerisini geri çekti, Mert kabul etti:
*"kabul şimdilik yapmayalım ama bunu da not al, ilerde yapılacaklar ya da
bakılacaklar diye."*

**Ne yapılmadı:** `(tekne, kiralama tipi, tarih)` başına tek satır tutan, fiyat +
kalan kontenjan + durum taşıyan özet tablo. Arama şimdilik canlı sorguyla çalışacak
(`Boats` ⋈ `BoatRentalTypes` ⋈ `Prices` ⋈ `Voyages`, indeksli).

**Neden ertelendi:**
- 35 tekne × 8 tip × 365 gün ölçeğinde indeksli join zaten hızlı
- Özet tablo **her fiyat değişikliğinde ~365 satır** yeniden yazmak demek; o
  güncellemeyi atlayan tek bir kod yolu müşteriye **yanlış fiyat** gösterir
- Redis "arama ölçülebilir şekilde yavaşlayınca gelir" diye elenmişti; bu tablo
  aynı kategoride — erken optimizasyon

**Ne zaman geri dönülür — somut eşik:** arama sorgusunun 95. yüzdelik gecikmesi
**300 ms**'i aştığında, ya da tekne sayısı **300**'ü geçtiğinde. Tahminle değil
ölçümle.

**Şema buna kapalı değil:** tablo türev veridir, kaynak tablolardan her zaman
yeniden üretilebilir. Sonradan eklemek migration + bir arka plan işi; mevcut veriyi
bozmaz.

---

### 2026-08-24 ⚠️ TASARIM İLKESİ — kararı platform değil TEKNE SAHİBİ verir

Mert: *"tekne sahibine kalsın bu ayar, hatta bazı böyle durumları biz tekne
sahibine bırakalım — o panelden kendisi yapsın."*

**Kural:** bir davranış tekne sahibinin işletme tarzına göre değişebiliyorsa,
platform onu **sabitlemez**; panelde ayar yapar. Zaten böyle kurulmuş olanlar:
yaş sınırları, asgari kişi sayısı, takvim modu, menü içerikleri, tekne kuralları.

**Neden:** platform 35 tekneyi değil, birbirine benzemeyen 35 işletmeyi barındırıyor.
Sabitlenen her kural, o kurala uymayan işletmeyi ya sistemden kaçırır ya da
yanlış veri girmeye zorlar.

**Sınırı:** para ve güven kuralları tekne sahibine bırakılmaz — komisyon oranı,
iptal-iade politikası, kupon kuralları, yorum onayı platformda kalır. Ayarlanabilir
olan **işletme tarzıdır**, platformun sözü değil.

**Şemaya etkisi:** böyle bir soru geldiğinde varsayılan cevap "kolon ekle, panele
koy" — kodda `if` yazmak değil.

---

### 2026-08-24 — Dile göre ayrı slug (SEO) — Mert: "kesinlikle yapacağız"

İlk sürümde tekne adresi **tek slug**: `/tekne/mavi-yolculuk`. İlerideki sürümde
her dil kendi adresini alacak: `/boat/blue-voyage`, `/boot/blaue-reise`.

**Neden ertelendi:** bugün yalnız Türkçe içerik var; dile göre slug ancak çeviriler
dolunca anlam kazanır.

**Neden şemayı bozmuyor:** slug kolonu çeviri tablosuna sonradan eklenir, mevcut
veriyi bozmaz. Tek slug `Boats` üzerinde durur, dile göre slug geldiğinde
`BoatTranslations.Slug` eklenip eskisi yönlendirmeye (301) dönüşür.

⚠️ Eski adresler **kırılmamalı** — SEO değeri yönlendirmeyle taşınır, silinerek değil.

---

### Sefer devri (charter için yer açma) — Mert: "bunu kesinlikle ekleyeceğiz"

**Senaryo:** Cemil 20.000 TL'lik konaklamalı tur istiyor, ama o günde Mehmet'in
2 koltukluk paylaşımlı rezervasyonu var.

**Fikir:** sistem Mehmet'e teklif götürür — **tam iade + indirim kuponu (%20 gibi)
+ başka teknede öncelik**. Mehmet kabul ederse sefer boşalır, Cemil charter'ı alır,
tekne sahibi 20.000 TL kazanır, Mehmet de kazançlı çıkar. Reddederse hiçbir şey
değişmez, Cemil alamaz.

**Neden ilk sürümde değil:** Cemil ödeme yaparken Mehmet'in cevabını beklemek
zorunda kalır — kötü bir ödeme deneyimi ve karmaşık bir bekleme akışı.

**Şema şartı:** sefer kaydı buna **kapatılmayacak**. Rezervasyonun sefere bağlanma
biçimi, ileride bir rezervasyonun seferden çıkarılıp yerine başkasının konmasına
izin verecek şekilde esnek kalacak.

⚠️ Mert bunu **unutulmaması gereken** madde olarak işaretledi. [[durum]] içine de
işlendi.

---

## Kapanış kararları (D2, D5, 35b, 41, 56)

### 2026-08-22 — Yasal kapasite ayrı alan olarak tutulur (D2 kapandı)

Teknede **iki kapasite** vardır:

| Alan | Ne sayar | Kullanımı |
|---|---|---|
| **Ticari kapasite** | Yetişkin + çocuk (bebek sayılmaz) | Satılabilir koltuk |
| **Yasal kapasite** | **Herkes — bebek dahil** | Belgede yazan azami kişi |

Doğrulama iki kademeli: `yetişkin + çocuk ≤ ticari` **ve**
`yetişkin + çocuk + bebek ≤ yasal`.

**Gerekçe (Mert):** denetimde ve kazada sorumluluk doğmasın. 12 koltuk satılıp
üstüne 3 bebek binerse teknede 15 can olur; belge 12 diyorsa bu platformun sorunu
olur.

### 2026-08-22 — Hava iptali: şimdilik yalnızca ölçülür (D5 kısmen kapandı)

Her hava iptalinde kaydedilir: **kim iptal etti, ne zaman, açıklaması, iptal edilen
rezervasyonun tutarı**. Panelde tekne ve iş ortağı bazında sayaç gösterilir.

**Otomatik eşik / ceza YOK.** Gerekçe: "normal" hava iptali sıklığının ne olduğu
henüz bilinmiyor — Kasım'da haftada üç iptal normalken Ağustos'ta bir iptal
şüpheli olabilir. Şimdi eşik koymak tahmin yürütmek ve dürüst iş ortaklarını
cezalandırmak olur.

⚠️ **Mert: "bundan sonrasında tekrardan bakacağız."** Bir sezon veri toplandıktan
sonra eşik kararı verilecek. Alan hazır olacak.

### 2026-08-22 — Kısmi iadede komisyon: A seçildi (35b kapandı)

Müşteride kalmayan tutar, **aynı komisyon oranıyla bölüşülür.**
1000 ödendi, 500 iade edildi → kalan 500'ün %15'i platformun, %85'i tekne sahibinin.

**Tek formül:** `komisyon = müşteride kalmayan tutar × oran`. Tam iade, kısmi iade,
no-show, hava iptali, indirim — hepsi bu kuralla çözülür; iptale özel komisyon
mantığı yazılmaz.

### 2026-08-22 — Ödeme sağlayıcı kararı ertelendi (41 beklemede)

Mert henüz hangi sanal POS'u kullanacağına karar vermedi. **Şemayı bloke etmiyor.**

Şema sağlayıcıdan **bağımsız** kurulur; ihtiyaç duyduğu alanlar her sağlayıcıda var:
- Ödeme: sağlayıcı adı, sağlayıcıdaki işlem no, tutar, durum, tarih
- Hakediş: dönem, tutar, sağlayıcıya verilen talimat referansı, durum
- İş ortağının sağlayıcıdaki **alt üye iş yeri** kimliği

Sağlayıcı seçilirken aranacaklar: **alt üye iş yeri (marketplace) desteği** (şart —
olmadan bölüştürme yapılamaz), kısmi iade API'si, hakediş talimatı, 3D Secure.

### 2026-08-22 — Fatura: genel tablo + aracılık modeli (56 kapandı)

**Aracılık modeli seçildi.** Hizmeti tekne sahibi verir; müşteriye faturayı o keser.
Platform, iş ortağına **komisyon faturası** keser (periyodik, hakedişle aynı ritim).

Şemada tek bir genel fatura kaydı: **kim kesti, kime, tutar, tür, numara, tarih.**
Yön bir alandır — model değişirse şema değişmez.

*(not)* Aracılık modeli seçildiği için platform müşteriye fatura kesmiyor →
**müşteriden TC kimlik ve adres toplanmasına gerek yok.** D4 böylece çözüldü;
KVKK itirazı da ortadan kalktı. Kimlik verisi yalnızca teknenin "yolcu listesi
ister" anahtarı açıkken, yolcu başına toplanır.

⚠️ Mali müşavir teyidi alınınca kesinleşecek.

---

## Para birimi — 2026-08-23 DÜZELTMESİ

### 2026-08-23 — Çoklu para birimi: liste ≠ tahsilat ≠ görüntüleme

**Önceki "her şey TL" varsayımı yanlıştı, Mert düzeltti.** Üç ayrı kavram var:

| Kavram | Nedir | Değer |
|---|---|---|
| **Liste para birimi** | Tekne sahibinin fiyatı girdiği birim | TL / USD / EUR / GBP |
| **Tahsilat para birimi** | Karttan çekilen | **Her zaman TL** |
| **Görüntüleme para birimi** | Müşterinin navbar'dan seçtiği | TL / USD / EUR / GBP |

Navbar'da güncel kurlar gösterilir. Tekne sahibi fiyatını dört birimden herhangi
birinde girebilir; müşteri **daima TL öder**.

### 2026-08-23 — Kur riski: tahsil edilen TL üzerinden (A seçildi)

Hakediş **fiilen tahsil edilen TL** üzerinden hesaplanır, liste para birimi
üzerinden değil.

Örnek: tekne €500 listelendi, 1 Temmuz'da kur 35 → müşteri 17.500 TL ödedi.
30 Eylül'de kur 40 olsa bile tekne sahibine **17.500 TL eksi komisyon** ödenir,
20.000 TL değil.

**Gerekçe:** aksi halde platform tahsil etmediği parayı ödemek zorunda kalır —
döviz spekülatörüne dönüşür. Tekne sahibi zaten **rezervasyon anındaki** kurdan
korunmuş olur; korunmadığı tek aralık satış–hakediş arasıdır (2–6 hafta), bu da
hakediş sıklığı kısaltılarak küçültülebilir.

### 2026-08-23 *(çıkarım)* — Kur kaynağı ve dondurulan alanlar

Kur kaynağı: **TCMB günlük kuru**. Kurlar günlük çekilip saklanır — hem hesaplama
hem "o gün kur neydi" sorusuna cevap için.

Rezervasyon **beş şeyi birden** dondurur: liste para birimi, liste tutarı,
kullanılan kur, kurun tarihi, TL karşılığı.

**TL eksendir.** Euro fiyatlı bir tekneyi sterlin görüntüleyen müşteri için
euro→TL→sterlin zinciri kurulmaz; her şey TL'ye normalize edilir, görüntüleme
oradan yapılır. Böylece görülen fiyatla ödenen fiyat tutarlı kalır.

*(bilinçli sonuç)* Euro fiyatlı teknenin TL fiyatı **her gün değişir**. Tekne
sahibi zaten bunun için euro giriyor.

---

## Çok dillilik — 2026-08-23

### 2026-08-23 — Diller: TR / EN / DE / RU — özellik SONRAYA ertelendi

Hedef dört dil. Ancak Mert **ilk sürümü yalnız Türkçe** yapmak istiyor.

⚠️ **Claude'un ayrımı:** *özellik* ertelenir, *şema şekli* ertelenmez. Çeviri
tabloları baştan kurulur, yalnız Türkçe satırlar doldurulur. Tek kolonla
başlanırsa dil eklemek migration + her okuma yolunun yeniden yazılması olur.

### 2026-08-23 — AI ile otomatik çeviri fikri (Mert)

Tekne sahibi bilgileri **Türkçe** girer; sistem bir AI API'sine bağlanıp diğer dil
kolonlarını otomatik doldurur. Tekne sahibinden dört dilde içerik beklenmez.

*(çıkarım)* Otomatik çeviri şemada iki alan gerektirir:
- **kaynak**: `manuel` / `otomatik` — tekne sahibinin düzeltmesi bir sonraki
  otomatik çeviriyle **ezilmemeli**
- **kaynak metin özeti (hash)** — Türkçe metin değişince çevirinin bayatladığı
  anlaşılsın ve yeniden üretilsin

---

## Fiyatsız satış / özel teklif akışı — 2026-08-23

### 2026-08-23 — "Fiyat için iletişime geçin" + özel teklif

Tekne sahibi kiralama tipini tanımlayıp **fiyat girmeyebilir**. O durumda:

1. Müşteri tekneyi görür; fiyat yerine **"fiyat için iletişime geçin"** yazar
2. Müşteri iletişime geçer, **telefonda** konuşurlar
3. Tekne sahibi panelden müşteriye **özel teklif** gönderir
4. Teklif müşteriye **hem SMS hem e-posta** ile ulaşır
5. Müşteri kabul edip **sistemden** öder — IBAN'a havale **kesinlikle yok**
6. Rezervasyon normal akıştaki gibi oluşur

**Netleşenler:**
- Teklif içinde **menü ve ek hizmetler de seçilebilir**
- Komisyon **normal oranla aynı**
- **Her kiralama tipinde** açık
- Platform dışına kaçışa karşı **kullanıcıya uyarı/bildiri**. Mert: *"platformumuzun
  ana amacı zaten müşteriyi ve tekne sahibini korumak"*

### 2026-08-23 — Teklif 48 saat geçerli ve o süre boyunca tarihi TUTAR

Gönderilen teklifin geçerlilik süresi **48 saat**. Bu süre boyunca ilgili tarih
rezerve edilir; başkası satın alamaz. Süre dolunca teklif **geçersiz** olur ve
tarih **serbest kalır**.

*(not)* Bu, rezervasyondaki 15 dakikalık `Beklemede` mekanizmasının uzun sürelisi —
aynı yapı, farklı süre. Ek karmaşıklık getirmez.

### 2026-08-23 — İletişim TELEFONLA DEĞİL, sistem içi mesajlaşmayla

**Aynı gün verilen "telefonda konuşurlar" ifadesini iptal eder.** Müşteri ile tekne
sahibi **sistem içinden mesajlaşır**; telefon üzerinden görüşme akışın parçası
değildir.

Mert: *"bütün bu konuşmalar bizim sistemimizin içerisinde olsun ki hem takip
edebilelim, hem kullanıcıyı hem tekne sahibini koruyabilelim."*

**Gerekçe:** platform dışına kaçışı önlemenin gerçek mekanizması budur — uyarı bir
kuraldır, mesajlaşma bir mekanizmadır. Ayrıca anlaşmazlıkta platformun elinde kayıt
kalır.

Uyarı metni de gösterilecek: platform dışında ödeme yapılırsa ödeme güvencesi, iade
hakkı, anlaşmazlık çözümü, QR ile kayıtlı biniş ve yorum hakkı **geçersizdir**.

### 2026-08-23 — Çeviri tabloları ŞİMDİ kurulur, yalnız Türkçe doldurulur

Mert Claude'un ayrımını kabul etti: **özellik ertelenir, şema şekli ertelenmez.**
Çeviri tabloları baştan kurulur; ilk sürümde yalnız `tr` satırları dolar.
Mert: *"sonrasında bizim haftalarımızı vesaire almasın hiç."*

### 2026-08-23 — Çeviride kaynak ve bayatlık takibi

- **kaynak**: `manuel` / `otomatik` — tekne sahibinin elle düzelttiği çeviri, bir
  sonraki otomatik çeviriyle **ezilmez**
- **bayatlık**: çeviri üretilirken kaynak metnin özeti (hash) saklanır; Türkçe metin
  değişince çevirinin güncellenmesi gerektiği anlaşılır

*(çıkarım)* Fiyatsız kiralama tipi arama sonuçlarında görünmeli ama fiyat
filtresine takılmamalı — "fiyat sorunuz" olarak listelenmeli.

---

## Sistem içi mesajlaşma — 2026-08-23

### 2026-08-23 — Mesajlaşma her tekneye, her zaman açık

Müşteri **herhangi bir tekneye istediği zaman** mesaj atabilir. Yalnız "fiyat
sorun" akışına bağlı değil — fiyatı belli bir tekneye de soru sorulabilir.

### 2026-08-23 — Mesajlaşma BİNİŞE kadar sürer (önceki maddeyi düzeltir)

**Düzeltme:** "rezervasyondan sonra mesajlaşma sürmez" ifadesi yanlış anlaşılmadan
doğmuştu. Doğrusu:

Konuşma rezervasyondan **sonra da devam eder**. Müşteri tur öncesi buluşma yeri,
saat, ne getireceği gibi soruları sorabilir.

**Konuşma, QR okutulup biniş resmileştiği anda kapanır** — yani rezervasyon
`Binildi` durumuna geçtiğinde.

*(çıkarım)* Konuşma **(müşteri × tekne)** bazındadır; rezervasyondan önce açıldığı
için rezervasyona bağlı olamaz. Rezervasyon bu konuşmanın bağlamına iliştirilir.

Biniş hiç gerçekleşmezse (no-show, iptal) konuşma **tur tarihi geçince otomatik
kapanır**.

### 2026-08-23 — Telefon ve e-posta MASKELENİR

Mesaj içinde telefon numarası veya e-posta adresi yazılırsa sistem gizler.
Mesajlaşmanın tek başına yetmediği durumu ("beni şu numaradan ara") kapatır.

### 2026-08-23 — Destek talepleri ayrı yapı

Mesajlaşma (**müşteri ↔ tekne sahibi**) ile destek talepleri (**müşteri ↔ platform**)
**ayrı** modellenir; ortak bir "konuşma" altyapısına birleştirilmez.

Mert'in tercihi: net sınır, birleşik kod değil.

---

## ✅ DÖNÜLECEK listesi — kapandı

| # | Konu | Sonuç |
|---|---|---|
| D1 | Aynı gün birden fazla tur | ✅ Sefer modeli + mod bazlı takvim |
| D2 | Bebek kapasitesi | ✅ Ticari + yasal kapasite, iki kademeli doğrulama |
| D3 | Konaklamalı +1 gün | ✅ Sefer zaman aralığına dahil, ayrı kural yok |
| D4 | TC kimlik / adres | ✅ Aracılık modeli → toplanmıyor |
| D5 | Hava iptali suistimali | 🟡 Ölçülüyor, eşik kararı bir sezon sonra |
| 35b | Kısmi iade komisyonu | ✅ A — orantılı bölüşüm |
| 41 | Ödeme sağlayıcı | 🟡 Ertelendi, şema bağımsız |
| 56 | Fatura modeli | ✅ Aracılık + genel fatura tablosu (mali müşavir teyidi bekliyor) |

**Şemayı bloke eden açık madde kalmadı.**

---

## 🔁 ESKİ DÖNÜLECEK KAYDI (arşiv) — Mert'in açıkça işaretlediği konular

Mert bunlara **kesinlikle geri dönüleceğini** söyledi. Veri tabanı
kesinleştirilmeden önce bu liste tek tek gözden geçirilecek.

| # | Konu | Durum |
|---|---|---|
| ~~**D1**~~ | Aynı tekne aynı gün birden fazla tur satabilir mi? | ✅ **ÇÖZÜLDÜ** — Sefer modeli + mod bazlı takvim |
| **D2** | Bebekler kapasiteden düşülmüyor — yasal kapasite vs ticari kapasite ayrımı gerekebilir | Karar verildi, gözden geçirilecek |
| ~~**D3**~~ | Konaklamalının +1 gününün takvimi kapatması | ✅ **ÇÖZÜLDÜ** — sefer zaman aralığına dahil, ayrı kural gerekmiyor |
| **D5** | Hava iptali suistimali — tekne sahibi düşük fiyatlı rezervasyonu "hava" diye iptal edip günü daha iyi bir talebe satabilir. Denetim nasıl işleyecek? Mert: *"bu konuda pek emin değilim"* | Alan bırakılacak, kural sonra |
| **D4** | TC kimlik / adres toplama amacı — Claude "lazım olur diye" gerekçesine itiraz etti (KVKK m.4) | Karara bağlanmadı |

---

## Cevap bekleyenler

⚠️ **2026-08-24'te temizlendi.** Bu tablo 35b/38/39/40/41'i açık gösteriyordu; beşi de
22–23 Ağustos'ta cevaplanmıştı ve cevapları bu dosyanın kendi içinde duruyordu.
Tablo güncellenmediği için başka oturumlar bunları blocker sanıyordu.

| # | Konu | Nerede kapandı |
|---|---|---|
| 35b | Kısmi iade komisyonu | ✅ A — orantılı bölüşüm, "Kapanış kararları" |
| 38 | Tarih değişikliği reddi | ✅ %100 iade, 2026-08-22 |
| 39 | Tarih farkı | ✅ Fark müşteriden istenmez, 2026-08-22 |
| 40 | Hava iptalini kim ilan eder | ✅ Alan bırakılıyor; eşik bir sezon sonra (D5) |
| 41 | Ödeme sağlayıcı | 🟡 Ertelendi — **şemayı bloke etmiyor**, sanal POS seçilince |
| 57 | KDV oranı sabit %20 mi, şemada oran alanı tutulacak mı | 🔴 Açık — 2026-08-27'de KDV dahil kararıyla doğdu |
| 58 | Komisyon KDV dahil tutar üzerinden mi alınıyor | 🔴 Açık — platform, verginin üzerinden de komisyon alıyor olabilir |
| 59 | Menü ve ek hizmetlerde KDV oranı aynı mı | 🔴 Açık — yiyecek-içecek farklı orana tabi olabilir |
| 60 | Front-end'deki 7 statik blog yazısı veritabanına girecek mi | ✅ **Silinsin** (2026-09-04) |
| 61 | Kupon kişiye bağlanacak mı | ✅ **Üç tür olacak** (2026-09-04) — kullandıklarım · bana özel · genel kampanya |
| 62 | Yolcu listesi kimlik verisinin KVKK dayanağı | ✅ **Açık rıza** (2026-09-04) — onay kutusu ve saklama süresi gerekiyor |
| 63 | `brand.ts` kurumsal verisi | 🟡 **Ertelendi** — demo bitince Mert gerçek veriyi verecek |
| 64 | Biniş belgesi kaybolursa QR yeniden basılabilsin mi (`S-25`) | ✅ **(b) ayrı kısa ömürlü bilet** (2026-09-04) |
| 65 | Yolcu aydınlatma metni ve saklama süresi | 🟡 **Mert yazacak, en son** — `W-40`/`A-81` park edildi |

**Şu an şemayı bloke eden açık madde yok.** ⚠️ 2026-08-27'de üç yeni soru
açıldı (57–59), üçü de KDV kararının **arkasından** doğdu ve şemayı
etkileyebilir — özellikle 57 (oran alanı tutulacak mı).


---

## Toplu kararlar — 2026-08-24

### 2026-08-24 — Olay günlüğü saklama süresi: ŞİMDİLİK sınırsız (döneceğiz)

Mert: *"şimdilik bi hep saklayalım, bunu düzelteceğiz zaten, not al sen yine bir
yere, bakacağız buna — buna süre vermeyelim ŞİMDİLİK."*

**Bugün:** olay günlüğü silinmiyor.

**Neden ertelenebilir:** süre kararı verildiğinde uygulamasının ucuz olması,
`EventLog` tablosunun aylık bölümlere ayrılmış olmasına bağlı — o zaman eski ayın
parçası tek komutla düşürülür, milyonlarca satır tek tek silinmez.

⚠️ **DÜZELTME 2026-08-24:** bölümlendirme **henüz yapılmadı**. Bu madde ilk
yazıldığında yapılmış varsayılmıştı; yanlıştı. Bölümlendirme olmadan bu erteleme
ucuz değil. Görev `A-11`, ilk ciddi veri girmeden önce yapılmalı.

**Dayanak:** [[api-sema]] — `EventLog` aylık bölümlendirmesi (bölüm 8)

⚠️ **Ne zaman dönülmeli:** KVKK süresiz saklamayı meşru görmüyor; kişisel veri
"işlendiği amaç için gerekli olan süre" kadar tutulur. Sezonluk AI raporları için
en az iki sezon lazım — yani 24 ay mantıklı bir alt sınır. Karar en geç **ikinci
sezon kapanışında** verilmeli, o zamana kadar veri birikmiş ama silme kararı hâlâ
ucuz olur.

### 2026-08-24 — Yorumlarda alt puanlar olacak

Mert: *"alt puanları da olsun."* Genel puan (1–5) zorunlu; üstüne kriter bazlı
puanlar: temizlik, mürettebat, yemek, fiyat/değer, güvenlik, tekne durumu.

**Alt puanlar opsiyonel** — menü almamış müşteri "yemek" puanı veremez.

**Kriterleri PLATFORM tanımlar, tekne sahibi değil.** Bu, "kararı tekne sahibi
verir" ilkesinin sınırıdır: tekneler ancak aynı ölçüyle puanlanırsa
karşılaştırılabilir. Her tekne kendi kriterini seçseydi puanlar anlamsızlaşırdı.

### 2026-08-24 — Mesajlaşma için giriş ZORUNLU

Rezervasyon misafir olarak yapılabilir ama **mesaj atmak için hesap gerekir.**

**Neden:** cevabın kime gideceği belli olmalı; ayrıca girişsiz mesajlaşmada spam ve
taciz yönetilemez. Rezervasyondaki misafir serbestliği burada geçerli değil, çünkü
rezervasyon tek yönlü bir işlem, mesajlaşma karşılıklı bir ilişkidir.

### 2026-08-24 — Tekne sahibinin blog yazısı platform onayından geçer

Yazı platformun adı altında yayınlanıyor. Platform yönetiminin kendi yazısı onay
beklemez.


İlgili: [[proje]] · [[durum]] · [[genel-kararlar]] · [[api-kararlar]] · [[api-sema]] · [[00-Index]]

---

## 🔮 SaaS / abonelik ürünü — 2026-08-24

### 2026-08-24 — Veri göçü YOK, sistem sıfırdan kuruluyor (G-06 kapandı)

Mert: *"sıfırdan kuruyoruz zaten bu bütün sistemi."*

Canlı `dailycruising.com.tr` içindeki 35 tekne, 104 kullanıcı, 120 rezervasyon ve
46 blog yazısı **yeni sisteme taşınmayacak**. Dönüştürme betiği yazılmayacak.

**Bilinerek kabul edilen bedeller:**
- Tekne sahipleri sisteme yeniden kaydolur ve teknelerini yeniden girer — 35 işletme
  için gerçek bir yük, bazıları geri gelmeyebilir
- Geçmiş yorumlar ve puanlar sıfırlanır; yeni tekneler puansız başlar
- Eski URL'ler kırılır — SEO değeri devredilmez

**Neden yine de doğru:** eski şemada sefer kavramı, mod bazlı takvim, para defteri ve
olay günlüğü yok. Bunları geçmiş veriden **üretmek** gerekirdi ve üretilen veri
uydurma olurdu — özellikle para defterinde. Yanlış geçmiş, hiç geçmiş olmamasından
kötüdür.

### 2026-08-24 — İLERİDE: sistem abonelikle satılacak (SaaS)

Mert: *"bu sistemi bir abonelik üzerinden satışını yapacağım. Satın alan işletme
sahipleri direkt olarak bu sistemi web sitelerinde kullanabilecekler + yanında diğer
yapay zeka entegrasyonları vesaire ile birlikte komple bir paket olarak."*

⚠️ **BU EN SON YAPILACAK İŞ.** Mert açıkça belirtti: *"şu anda buna göre bir şey
yapmayalım."* Bugün hiçbir tablo, hiçbir kolon bunun için eklenmiyor.

**Neden yine de bugün yazılıyor:** çok kiracılılık (multi-tenancy), sonradan
eklenmesi en pahalı özelliktir. Bilinmesi, bilinmemesinden iyidir.

**İyi haber — bugünkü şema bunu zaten kaldırıyor.** İki yol var ve **ucuz olanı
bugün hiçbir değişiklik istemiyor**:

| Yol | Bugün gereken |
|---|---|
| **Abone başına ayrı veritabanı** | **Hiçbir şey.** Aynı şema, ayrı veritabanı. Bağlantı dizesi aboneye göre seçilir |
| Tek veritabanı + `TenantId` kolonu | Her tabloya kolon, her sorguya filtre, her indekse ön ek — **sonradan eklenirse çok pahalı** |

Birinci yol bu ölçekte (abone sayısı yüzlerle ifade edilecek) hem daha basit hem daha
güvenli: bir abonenin verisi diğerininkiyle **fiziksel olarak** karışamaz, yanlış
yazılmış tek bir `WHERE` cümlesi veri sızdıramaz.

**Sonuç: SaaS kararı bugün alınmak zorunda değil.** İkinci yola geçilmek istenirse o
zaman konuşulur; birinci yol seçilirse hiçbir şey değişmez.

**Pakete dahil olacaklar** (Mert'in tarifi): rezervasyon sistemi + AI entegrasyonları
+ otomasyonlar. AI entegrasyonlarının listesi bu dosyada zaten var; SaaS bunları
ayrı bir ürün özelliği değil, **paketin parçası** yapıyor.


---

## Blog — 2026-09-04

### 2026-09-04 — Blog uç yazılacak; yazı SİTEDEN yazılabilecek (`S-30` kapandı)

Mert: *"bloglar bu arada uç yazılsın blog yazılabilecek çünkü siteden"*

**Karar (Mert):** Blog statik kalmıyor. API ucu yazılacak ve yazı **site üzerinden**
oluşturulacak — yani yazma arayüzü panelde olacak, dosyaya elle yazma değil.

Bu, 2026-08-22 (*"hem platform hem tekne sahipleri yazabilir"*) ve 2026-08-24
(*"tekne sahibinin yazısı platform onayından geçer"*) kararlarını **iptal etmez,
uygular**. Üçü birlikte akışı tamamlıyor:

| Kim | Ne yapar | Onay |
|---|---|---|
| Platform yönetimi | Yazar, yayınlar | Beklemez |
| İş ortağı (tekne sahibi) | Yazar, onaya gönderir | `blog.approve` yetkisi olan personel |

**Şema zaten var, sıfır satır ve sıfır kod eksik değildi — yalnız uç eksikti.**
Dört tablo kurulu: `BlogPosts` (13 kolon), `BlogPostTranslations`, `BlogCategories`,
`BlogCategoryTranslations`. Çeviri, kategori, kapak görseli, görüntülenme sayacı ve
onay akışı (`ApprovedByUserId`, `ApprovedAt` — 2026-08-24 kararından doğmuş) dahil.
Yetkiler katalogda hazır: `blog.write`, `blog.approve`.

**Bu yüzden alternatif "statik kalsın" elendi:** statik seçilseydi dört tablonun ya
düşürülmesi ya "bilerek boş" diye belgelenmesi gerekirdi — ikisi de bugün var olan
işi çöpe atmak olurdu.

⚠️ **Bugünkü 7 statik yazı ile ilişki kararlaşmadı.** 2026-08-24'te *"46 blog yazısı
yeni sisteme taşınmayacak"* denmişti; front-end'de duran 7 yazı o karardan sonra
tasarım verisi olarak yazıldı. Uç gelince bunlar veritabanına girecek mi, yoksa
statik olarak mı kalacak — **çıkarım yapılmadı**, "Cevap bekleyenler"e eklendi (60).

### 2026-09-04 — Kalan uç işleri backend'e devredildi

Mert: *"tamam yaptır hepsini back-end'e"*

Kalan beş web görevinin **uç tarafı** backend oturumuna geçti: blog (`W-38`), favori
ve bildirim tercihi tabloları + uçları (`W-39`), biniş QR'ı (`W-66`).

⚠️ **Üç kalem bu devirle kapanmıyor, çünkü backend'in üretebileceği şeyler değil:**

| Ne | Neden backend cevaplayamaz |
|---|---|
| `W-06` `brand.ts` — telefon, adres, TÜRSAB numarası | Mert'in kendi kurumsal verisi; uydurulamaz |
| `W-40` yolcu listesi KVKK dayanağı | Hukuki dayanak kararı |
| `W-39`'un "kuponlarım" yarısı | `Coupons` tablosunda `UserId` **yok** — kupon kişiye ait değil. Uç eksiği değil, **ürün sorusu**: kupon kişiye mi bağlanacak, yoksa bugünkü gibi kod olarak mı kalacak |

Bu üçü "Cevap bekleyenler"de kalıyor — yarım cevap tam gibi kaydedilmiyor.

---

## Mert'in 29 cevabı — 2026-09-04

Bir oturumda üç kuyruk birden boşaldı. Aşağıdakiler **Mert'in kendi
cevaplarıdır**; çıkarım yapılan yerler `*(çıkarım)*` işaretli.

### Çerçeveyi değiştiren cevap: fiyatı işletme koyar, biz aracıyız

> *"İşletmeler teknelerinin fiyatlarını kendileri belirler (KDV dahil ederek
> fiyatlarını koyarlar) bunları kendileri belirler, biz sadece aracı olduğumuz
> için ücreti alacağız."*

Bu, `S-21`'i cevaplamakla kalmıyor, **sorunun kurulusunu düzeltiyor.** Soru
*"platform verginin üzerinden de komisyon alıyor, kasıtlı mı"* diye
sorulmuştu. Doğru çerçeve şu: **liste fiyatı işletmenin koyduğu, KDV dahil
fiyattır**; platform o fiyatın yüzdesini alır. Ortada "verginin üzerinden
komisyon" diye ayrı bir olgu yok, tek bir fiyat var.

Sonuç: bugünkü `grandTotal` üzerinden hesap **doğru**, değişiklik gerekmiyor.

### KDV — üç soru tek karar

| # | Soru | Karar |
|---|---|---|
| `S-20`/57 | Oran rezervasyona dondurulsun mu | **Dondurulsun** ("doldursun") |
| 58 | Komisyon KDV dahilden mi | **Evet** — yukarıdaki çerçeve |
| 59 | Menü/ek hizmette ayrı oran mı | **Hayır, tek oran** |

> *"günün sonunda ne kadar ücret çıkarsa ona göre bir KDV oranı, her birisi
> için ayrı ayrı KDV oranları olmayacak"*

Yani ek hizmet satırı kendi oranını taşımıyor; oran **toplam üzerinden**.

### Para akışı

- **Ödeme sağlayıcı: PARATİKA.** *"Paratikaya geçelim, onda pazar yeri
  özelliği vardı."* İyzico pazaryeri başvurusu iptal — eski sistem zaten
  Paratika kullanıyordu ve alt üye iş yeri özelliği orada açıktı.
- **Alt üye iş yeri belgeleri başvuruda toplanacak ve IBAN ZORUNLU.**
- **Kademeli iadede komisyon tam alınır** (`S-12`'nin açık ucu). İptal
  maliyeti işletmede kalıyor, platform payını iade etmiyor.
- **Fatura modeli mali müşavire henüz sorulmadı** — *"biz ilk önce
  bitirelim, sonrasında soracağım."*

### 2026-09-04 — İşletme müşterinin iletişim bilgisini GÖRMEYECEK (`S-27`)

Karar (Mert): **hayır**, ve gerekçesi bizim düşünmediğimiz bir şeydi:

> *"amaç işletme müşterinin e-posta ve telefonunu görüp kendisi başka yerden
> rezervasyon yaptırabilir"*

**Neden:** mesele KVKK değil, **aracıdan kaçış**. İşletme müşteriye doğrudan
ulaşabilirse ikinci turu platform dışında satar ve komisyon kaybolur. Bu,
platformun varlık nedenine dokunan bir risk.

**Yerine konan akış:** işletme **destek talebi açar**, durumu anlatır,
**platform müşteriye haber verir**. Yani "hava muhalefetinde müşteriye
ulaşamama" sorunu çözülüyor ama kanal platformda kalıyor.

**Alternatif elendi:** "yalnız kalkışa 24 saat kala aç" önerisi de kaçışı
engellemiyordu — 24 saat, bir sonraki turu doğrudan satmak için fazlasıyla
yeterli.

Uygulama: `GET /api/partner/reservations` yanıtından **e-posta ve telefon
çıkarılacak**; ad kalıyor.

### 2026-09-04 — Kupon ÜÇ TÜR olacak (`61`)

> *"burada kullandığı kuponlar ve bana özel kuponlar ve genel kuponlar olsun.
> NOT: Genel kuponlar herkese açık olacak, sitede bazen böyle kampanyalar
> yapabileceğiz"*

| Tür | Ne | Bugünkü şema |
|---|---|---|
| Kullandığım kuponlar | Geçmiş | `CouponRedemptions` var, **yalnız uç** eksik |
| Bana özel kuponlar | Kişiye tanımlı | **Yok** |
| Genel kuponlar | Sitede listelenen kampanya | Kupon var ama **okunabilir değil** |

Üçüncüsü yeni bir gereksinim: müşteri kampanyayı **görmeden** kodu giremez,
yani genel kuponların herkese açık bir listesi olmalı.

⚠️ Backend'in itirazı kayda geçiyor ve hâlâ geçerli: `Coupons` bugün bir
**kampanya** tablosu. `UserId` eklemek onu hem kampanya hem kişisel kupon
yapar ve "bu kupon kime ait" sorusunun cevabı satırdan satıra değişir; kupon
kontrolü yazan her yeni kod yolu bu ayrımı hatırlamak zorunda kalır ve unutan
biri kişisel kuponu herkese açar — **hata sessizdir**. Tasarım backend'de.

### 2026-09-04 — Statik blog yazıları SİLİNDİ (`60`)

Karar: **silinsinler**, blog gerçek yazılarla sıfırdan dolacak. Front-end'deki
7 yazı uydurma yazar adları taşıyordu ("Deniz Aksoy"). `src/lib/data/blog.ts`
silindi. 2026-08-24'teki *"46 blog yazısı taşınmayacak"* kararıyla tutarlı.

### Kalan cevaplar

| # | Konu | Karar |
|---|---|---|
| `S-19` | Ters vekil | **Aynı makine**, `127.0.0.1` |
| — | E-posta / SMS | **Postmark + Netgsm** |
| `S-24` | Dosya deposu | **S3 ya da DigitalOcean**, başlangıçta **ücretsiz katman**; gerekince ücretliye geçilir |
| `S-18` | Bölge listesi | **Onaylandı** (10 mavi tur bölgesi) |
| — | Reddedilen başvuru | **Yeniden başvurabilir** |
| — | Yorum daveti | **Tur biter bitmez**, ve **hatırlatma gönderilsin** |
| `62`/`W-40` | Yolcu listesi KVKK | **Açık rıza** — ayrı onay kutusu ve saklama süresi gerekiyor |
| `S-28` | 10 yanlış damgalı rezervasyon | **Düzeltilsin** |
| `S-22` | `a04-*` tohum satırları | **Silinsin** |
| `A-07` | Yanıt şeması | **Hepsine yazılsın** (114 uç) |
| — | Backend'in 26 Ağustos kararları | **Toplu onaylandı** |
| — | Testlerdeki iki ad | **Kalsın** — demo aşaması |
| — | `/design-system` rotası | **Yayında kaldırılsın** |
| — | Veri göçü | **Ertelendi**, önce site ayağa kalksın |
| `S-26` | `/add-boat` vaatleri | **Rakam verme** |
| — | Gerçek fotoğraflar | **İşletmeler yükleyecek** |
| `63`/`W-06` · `S-29` | Kurumsal veri, "340+ tekne" | **Demo aşaması** — gerçek veriler sonra verilecek |

### 2026-09-04 ⚠️ ÖNCELİK — önce çalışan sistem, sonra gerçek veri

> *"Şu anda bize çalışan her şeyi ayarlanmış bir site lazım, ilk önce bir test
> edeceğim. Sonrasında artık her şey tamamlandığında sana zaten gerçek
> verileri vereceğim, sen de ona göre veritabanına ekleyeceksin ve sitedeki
> genel değerleri, TÜRSAB belgelerini falan ekleyeceğiz."*

**Bu, birkaç soruyu birden kapatıyor.** `W-06` (kurumsal veri), `S-29`
("340+ tekne"), ana sayfa fiyatları, veri göçü ve gerçek fotoğraflar —
beşi de **bugün cevaplanacak sorular değil**, teslim sırasına ait. Bunlar
"cevapsız" sayılmaz, **ertelenmiş** sayılır.

⚠️ Ama **uydurma sayı yayına çıkmaz**: bugün sitede duran rakamlar
kaldırıldı, yerlerine yer tutucu değil **doğru olduğu ölçülebilen ifade**
kondu. Gerçek veri gelince rakam eklenir; sıralamayı tersine çevirip
"şimdilik bir sayı yazalım" denmez.

### `S-25` — hâlâ cevapsız, soru kötü kurulmuştu

Mert *"anlamadım"* dedi ve haklı: soru "biniş jetonu geri üretilebilir olsun
mu" diye, iç terimle sorulmuştu. Ürün diliyle yeniden soruldu:
müşteri biniş belgesini kaybederse QR'ı yeniden basabilmeli miyiz, yoksa
QR'dan vazgeçip okunaklı kod mu kalsın. → soru **63'ten sonraki numarada**
açık kalıyor.

---

## 2026-09-04 (2) — dört cevap daha

### `S-12` iade komisyonu → (c) ORANTILI, yani bugünkü davranış korunuyor

Karar (Mert): **c**. Kademeli iadede komisyon da orantılı iade ediliyor.

**Neden bu satır ayrı yazılıyor:** 2026-09-04'te aynı gün *"komisyon tam
alınsın"* (b) cevabı verilmişti; backend kodu okuyup **sorunun dar
olduğunu** gösterdi ve cevap değişti. Bu giriş o cevabı **iptal eder**.

Soru %50 dilimi üzerinden kurulmuştu ve orada makuldü. Aynı kural %100
dilimine uygulanınca ₺1.000'lik turda işletme ₺850 kazanıp ₺1.000 geri
veriyor, yani **defterinde ₺150 eksi kalıyor** — hiç yapılmamış bir turdan
zarar ediyor. Backend ayrıca `CK_Payouts_Amount >= 0` yüzünden eksi
bakiyenin **sonraki turun hakedişini de kilitlediğini** ölçtü.

**Ders, karardan büyük:** bir iş kuralı sorusu **tek bir dilim üzerinden**
sorulursa cevap o dilimde doğru, sınırlarda yanlış olabilir. Para kuralı
sorarken **uç dilimler sayıyla gösterilmeli** → [[genel-desenler]]

`LedgerService.PostRefundAsync` değişmiyor.

### `S-31` blog gövdesi → zengin metin, **CKEditor** (`*(çıkarım)*` payı var)

Mert: *"b olabilir yada CKEditör de olabilir"* — ikisini de kabul etti,
seçim teknik tarafa bırakıldı.

**Seçilen: CKEditor.** **Neden:** yazarlar tekne işletmecisi ve kaptan,
yazılımcı değil. Markdown'da `**kalın**` yazmayı öğrenmek gerçek bir engel
ve blogun amacı işletmeyi yazmaya **teşvik etmek**. CKEditor'ün araç
çubuğu tanıdık.

**Bedeli ve ZORUNLU sırası:** CKEditor **HTML üretir** ve backend'de bugün
hiçbir HTML temizleyici yok (`BlogService.Clean()` yalnız `Trim()`).
Temizleme **sunucuda, izin listesiyle** yapılmadan HTML basılamaz — aksi
hâlde `blog.write` yetkisi olan bir işletme çalışanı herkese açık sayfaya
script gömer ve platform onayı bunu yakalamaz (onaylayan kişi metne bakar,
kaynağa değil).

Sıra bu yüzden tersine çevrilemez:
1. Backend yazma yolunda izin listeli temizleyici kurar,
2. Sonra editör ve HTML basımı açılır.

O güne kadar gövde **düz metin** kalıyor ve ekrandaki *"HTML etiketleri
olduğu gibi görünür"* ipucu doğru. Temizleyici geldiği gün o cümle
**yalan olur** ve aynı gün değişmeli.

### `S-25` biniş jetonu → (b) ayrı, kısa ömürlü biniş bileti

Karar (Mert): **b**. Asıl jetona dokunulmuyor; biniş belgesi açıldığında o
an için geçerli ayrı bir bilet üretiliyor. Böylece belge kaybolursa yenisi
basılabiliyor ve veritabanını okuyan biri biniş anahtarını **okuyamıyor**.

⚠️ Backend'in uyarısı karara dahil: **biletin ömrü tur bitişine değil,
kalkıştan makul bir süre SONRASINA kadar olmalı.** Bitişte ölen bilet, geç
kalkan ya da uzayan turda kaptanın elinde ölür ve o an kimse destek hattı
arayacak durumda olmaz.

`W-66` (QR ekranı) bu kararla açıldı.

### `W-40` yolcu listesi → aydınlatma metnini **Mert yazacak**, en son

Mert: *"onu ben yazıcam en son."* Metin gelmeden rıza kaydı boş bir sürüm
etiketi taşır; `W-40` ve `A-81` **park ediliyor**, tahmin edilmiyor.

⚠️ Saklama süresi de aynı pakette ve **silen bir iş** gerektiriyor: süre
yazılıp silme yazılmazsa yazılı bir vaat olur, uygulaması olmaz.

### 2026-09-05 — İşletme kendi kampanyasını KENDİSİ açabilir

Karar (Mert): **a**. İşletme kendi kuponunu/kampanyasını panelinden
oluşturabilecek.

**Neden bu bir soruydu:** şema bunu zaten ifade edebiliyordu
(`Coupon.PartnerId`, `FundedBy = Partner`) ama yetki katalogunda
`coupon.write` **işletmeye verilemiyordu** (`IsPartnerAssignable = false`).
Yani "bedelini işletmenin karşıladığı kupon" kavramı vardı, o kuponu
işletmenin **açması** yoktu. Backend tutarsızlığı bulup sordu.

**Bu karar 2026-08-24 ilkesiyle çelişmiyor.** O ilke *"kararı platform
değil tekne sahibi verir; ayarlanabilir olan işletme tarzıdır — komisyon,
iptal politikası ve kupon platformda kalır"* diyordu. Buradaki kupon
**platformun kupon politikası değil**, işletmenin kendi bütçesinden
verdiği indirim: `FundedBy = Partner` olduğu için bedeli hakedişinden
düşüyor, platformun payına dokunmuyor. Yani platformun elindeki kaldıraç
(komisyon, iptal, platform kuponu) yerinde duruyor.

⚠️ Açık kalan sınır: işletme **kendi teknesi dışında** geçerli kupon
açamamalı ve **platform kuponu** üretememeli. Kapsam ve finansman
alanlarının işletme isteğinde zorlanması gerekiyor — yetkiyi açmak tek
başına yetmez.
