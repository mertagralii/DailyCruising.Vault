---
rol: map
kapsam: genel
guncelleme: 2026-09-05
durum: guncel
---

# Genel Desenler

İki repoyu birden ilgilendiren, her oturumda tekrar uygulanan kurallar.
Gerekçeler [[genel-kararlar]] içinde.

## Dil

| Nerede | Dil |
|---|---|
| Konuşma, vault notları | Türkçe |
| Kod, dosya/sınıf/endpoint adları | İngilizce |
| Commit mesajları | İngilizce |

## Commit

- Yazar daima `Mert Ağralı <mmertagrali@gmail.com>`
- **AI atfı yasak:** `Co-Authored-By: Claude` trailer'ı, "Generated with Claude Code"
  benzeri ibare, repoya `CLAUDE.md`/`AGENTS.md` konulması — hiçbiri olmaz
- Mesaj İngilizce ve emir kipinde ("add", "fix"); gövdede **neden** anlatılır
- Commit ve push **yalnızca Mert isteyince**
- Kökte repo yok; her git komutu ilgili alt klasörde çalışır

## Doğrulama

| Taraf | Komut | Beklenen |
|---|---|---|
| API | `dotnet build` | 0 uyarı, 0 hata |
| API | `curl localhost:5163/api/health` | `{"status":"healthy"}` |
| Web | `npm run build` | başarılı |
| Web görünüm | tarayıcıda karşılaştırma | -> [[web-desenler]] |
| Vault | `python3 _araclar/dogrula.py` | TEMIZ |

Portlar: API 5163 (http) / 7070 (https), Web 3000.

## Nereye yazılır

Aynı bilgi iki yere yazılmaz. Sınır şudur:

| Bilgi türü | Dosya |
|---|---|
| Bir daha aynı **kararı** vermemek için | `*-kararlar.md` (append-only, `**Neden:**` zorunlu) |
| Bir daha aynı **tuzağa** düşmemek için | `<alan>/notlar/` |
| Her dosyada tekrar uygulanan **kural** | `*-desenler.md` |
| Yapılacak / yapılıyor / biten **iş** | `*-gorevler.md` |
| Hangi **araç** ne zaman kullanılır | `*-araclar.md` |
| Proje seviyesi **engel**, açık uç, çelişki | [[durum]] |
| O günün çalışma kaydı (arşiv) | `04-Oturumlar/` |

**Asla yazılmaz:** koddan okunabilen şeyler (klasör yapısı, kurulu paketler), git
geçmişindeki bilgiler, tek oturumluk geçici detay.

**Karar değişirse eskisi silinmez** — yeni giriş eklenir, "<tarih> kararını iptal
eder" yazılır.

## Özet tablo ile gövde çelişirse

Uzun dosyalarda (`domain-gereksinimler.md` 1.200+ satır) baştaki veya sondaki
**özet tablo, gövdeden bağımsız bayatlıyor**. 2026-08-24'te "Cevap bekleyenler"
tablosu beş soruyu açık gösteriyordu; beşinin de cevabı aynı dosyanın içindeydi.
İki ayrı oturum bunları blocker sandı.

- **Gövde doğrudur, tablo türevdir.** Çeliştiklerinde tabloyu gövdeye göre düzelt
- **Bir soru cevaplandığında tablo aynı turda düşürülür** — sonraya bırakılmaz.
  `domain-karari` skill'i bu adımı zorunlu tutar
- `dogrula.py` bunu **yakalayamaz**; semantik çelişki, biçim hatası değil.
  Tek korunma disiplin ve skill


## Yazılı olan doğru, yazılmamış olan kayıp

Denetlenebilir hataların iki türü var ve ikincisi çok daha sinsi:

| Tür | Örnek | Betik görebilir mi |
|---|---|---|
| İki yazılı şey çelişiyor | Tablo gövdeyle uyuşmuyor, gerekçe uygulamayla | Kısmen — **kıyaslayacak referans var** |
| Yazılı olan doğru, **bir şey yok olmuş** | Panodan beş görev silindi | Hayır — **kıyaslayacak referans yok** |

2026-08-24'te ikinci tür yaşandı: aralıkla silme beş görevi yok etti, `dogrula.py`
TEMİZ dedi çünkü kalan her şey biçim olarak kusursuzdu.

**Bu türün tek panzehiri sürüm geçmişidir.** Referans yoksa üretilir: `dogrula.py`
14. denetimi panonun **tüm git geçmişini** tarar; bir görev kimliği bir kez
göründüyse bir daha kaybolamaz.

- **Aralıkla silme kullanılmaz.** "X'ten Y'ye kadar sil" komutunun kapsamı, dosyadaki
  **gerçek sıraya** bağlıdır ve o sıra beklendiği gibi olmayabilir. Silinecekler
  tek tek adlandırılır
- **Bildirimin doğru olması yan etkinin doğru olduğunu göstermez.** O oturumda
  "A-09 tamamlandı" bildirimi doğruydu; yanlış olan söylenmeyen kısımdı
- Geçmiş **`HEAD` değil tüm log** olmalı: kayıp bir kez commit'lenirse `HEAD` onu
  normal sayar. Bugün tam bu oldu — silinmiş hâl commit'lendi

## Gerekçe ile uygulama ayrışabilir

Özet tablo kuralının kardeşi, ama daha sinsi: orada **iki yer** çelişir, burada
**bir kararın gerekçesi ile o kararın sonucu** çelişir.

2026-08-24 örneği: bir karar *"bölümlendirme yapılmadı, BRIN aynı işi görüyor"*
diyordu. Aynı şemada saklama süresi kararının ertelenebilme gerekçesi ise
*"bölümlendirme sayesinde silmek ucuz olacak"*tı. BRIN sorgu hızını çözer, **silme
maliyetini çözmez** — iki farklı problem tek çözüme bağlanmıştı.

**Bu dikkatle çözülmez.** Gerekçeyi yazan ile uygulayan **aynı oturumdu** ve yine
de ayrıştı. Dikkat eksikliği olsaydı daha dikkatli olmak çözerdi; yapısal bir
boşluk olduğu için yapısal bir kontrol gerekiyor.

### Taşıyıcı gerekçe çift yönlü linklenir — zorunlu biçim

Bir karar **"X ucuz/mümkün, çünkü Y var"** biçimindeyse Y **taşıyıcı gerekçedir**.
İki satır zorunludur:

Kararın olduğu yerde:

```
**Dayanak:** [[hedef-not]] — hangi özelliğe dayanıyor
```

Dayanılan yerde:

```
**Buna dayananlar:** [[karar-notu]] — hangi karar
```

**Tek yön yetmez.** Kırılma **Y tarafında** olur: bölümlendirme hiç yapılmadı ve
ona dayanan saklama süresi kararı bundan habersizdi. Y'yi değiştiren kişinin,
neyin çöktüğünü görmesi gerekir.

*(Örnek satırlar kod bloğunda yazılır. Denetim eklendiği gün bu kuralın kendi
belgesini yakaladı — girintili örnek gerçek link sayılmıştı. Betik ``` bloklarını
ve satır içi kodu ayıklıyor, dört boşluk girintisini ayıklamıyor.)*

**`dogrula.py` bunu denetler** (13. kontrol): `**Dayanak:**` satırı link vermiyorsa
veya hedefte geri referans yoksa **hata verir**.

### Aynı gerekçe ikiden fazla yerde olabilir

`**Dayanak:**` biçimi **ilk yazımda** dağılmayı önler; **zaten dağılmış** kopyaları
bulmaz. 2026-08-24'te aynı çelişkinin **üç** kopyası vardı ve ilk düzeltmede ikisi
görülüp üçüncüsü kaçtı. Üçüncüsü en tehlikelisiydi: bölümlendirmeyi **olmuş bitmiş**
gibi anlatıyordu (*"aylık bölümlere ayrılmış olarak kuruluyor"*), oysa yapılmamıştı.

- Bir taşıyıcı gerekçe düzeltilirken **iki kopya bulununca durulmaz**, üçüncü aranır
- Arama **anahtar kelimeyle yapılamaz**: o örnekte "bölümlendirme", "DROP" ve
  "saklama süresi" üç ayrı terimdi, hiçbiri diğerini `grep` ile bulmuyordu
- **Bir özelliğin geniş zamanla anlatılması uyarı işaretidir** — *"kuruluyor"*,
  *"tutuluyor"*, *"sağlanıyor"* cümleleri yapılmış olduğunu ima eder; koda bakılır

### Kuralın asıl işleyiş biçimi

Üçüncü kopyayı `dogrula.py` **yakalamadı**. Yakalanmasının sebebi, denetimin
çift yön kurmaya zorlaması ve o sırada **bakılmış olmasıydı**.

Bir kuralın değeri yalnız doğrudan yakaladığında değil, **bakmaya zorladığında** da
oluşur. Bu, "daha dikkatli ol" demekten farklıdır: dikkat isteği bir niyettir,
zorunlu biçim bir eylemdir.

Denetimin göremediği kısım kalıyor: BRIN'in silme maliyetini çözmediğini anlamak
teknik muhakeme gerektirir; onu `database-reviewer` ajanı yakaladı — **araç
zincirinin inceleme adımı** → [[genel-araclar]]. Yani biçimi betik, anlamı ajan
denetler. İnceleme adımı bu yüzden atlanmaz: *"kod çalışıyor"* ile *"gerekçe
tutarlı"* farklı şeylerdir.

## Tetikleyicisi olmayan dosya çürür

Bir bölme açarken iki soruya cevap zorunlu: **ne zaman okunur, ne zaman yazılır?**
İkisinin de cevabı yoksa bölme açılmaz — çünkü açılırsa bayatlamaktan başka bir şey
yapamaz.

2026-08-26'da ölçüldü: `*-mimari.md` ne okuma ne yazma tablosundaydı. API'de on
commit boyunca beş dosya **her görevde** güncellendi, `api-mimari.md` hiç
güncellenmedi; "iş uç noktası hâlâ yok" derken sekiz controller yazılmıştı. Aynı
tarama `web-mimari.md`'yi de bayat buldu (87 dosya).

**Bunu disiplin hatası saymak yanlış olurdu.** İki dosyanın ortak özelliği tetikleyicisiz
olmalarıydı; aynı oturum tetikleyicisi olan dosyaları düzenli güncelledi. Ayrım önemli:

| Sınıf | Belirti | Çözüm |
|---|---|---|
| **Kural boşluğu** | tetikleyicisi olan dosya güncel, olmayan bayat | kuralı değiştir |
| **Disiplin** | aynı kural altındaki dosyaların bir kısmı güncel, bir kısmı değil | hatırlat |

İkisini karıştırmak pahalıdır: kural boşluğuna "daha dikkatli ol" demek hiçbir şeyi
düzeltmez, çünkü dikkat edilecek bir kural yoktur.

**Ölçüt beyandır, dosya damgası değil.** `dogrula.py` kontrol 15 bayatlığı
frontmatter'daki `guncelleme` ile kod reposundaki yapısal değişimi karşılaştırarak
ölçer — `mtime` değil. Dosyaya dokunmak onu doğru yapmaz; beyan edilen tarih ile
kodun gerçeği karşılaştırılır. Aynı sebeple yalnız **eklenen/silinen** dosyalar sayılır:
içerik değişikliği yapıyı değiştirmez.

İlgili: [[genel-esszamanli-oturumlar]]

### Koşullu geçici şeyin koşulu panoya yazılır

"Geçici" diye yazılan kodun kaldırılmasını tetikleyen hiçbir şey yoktur. Kod
çalışır, test geçer, kimse rahatsız olmaz — kaldırılması gerektiğini yalnız onu
yazan bilir ve o bilgi oturumla birlikte kaybolur.

2026-08-26'da bulundu: `GET /api/auth/yetki-denemesi` ucu *"geçici, A-03 bitince
gerçek uçlar aynı kalıbı kullanacak"* yorumuyla yazılmıştı. A-03'ün ilgili dilimi
bitti, `PartnerStaffController` o kalıbı üretimde kullanıyordu — ucun işi bitmişti
ama aylarca ayakta kaldı. Kimliği doğrulanmamış bir deneme ucu olarak.

**Kural:** koşulu yazılı geçici bir şey (`X bitince kaldırılacak`) üretiliyorsa,
o kaldırma işi **panoya görev olarak girer** — `Bağımlı: X` satırıyla.

Buna yeni bir denetim yazılmadı ve bilerek yazılmadı: iki kod reposunda toplam
**bir** geçici işaret var, yani nüfus denetim yazmayı hak etmiyor. Bunun yerine iş
zaten denetlenen mekanizmaya bağlanıyor — pano `dogrula.py` kontrol 9 ve 14
tarafından korunuyor, kimlik kaybı yakalanıyor, `Kanıt:` zorunlu. **Yeni makine
kurmak yerine, korunmayan şeyi korunan yere taşı.**

Yorumdaki koşul yeterli değildir; yorumu okuyacak bir tetikleyici yok →
[[genel-desenler]] "Tetikleyicisi olmayan dosya çürür" ile aynı sınıf.

### Yardımcıya çıkarılan kod, çıkarılırken alan kaybedebilir

Bir sonuç nesnesini ortak yardımcıya taşırken alanlardan biri sabit değere
(`null`, `0`, `false`) yazılırsa derleyici susar, tipler tutar, testlerin çoğu geçer.
Kayıp yalnız o alanı **okuyan** bir test varsa görülür.

2026-08-26: `PricingService`'te sonuç nesnesi yardımcıya çıkarılırken
`CouponRejectionReason` sabit `null` yazıldı — kuponu reddedilen müşteri sebebini
göremiyordu. Mevcut bir test yakaladı. Refactor'ün kendisi doğruydu, taşıma sırasında
bir alan düştü.

**Bunu yakalayan şey inceleme değil, var olan testlerdir.** Sonuç: davranışı olan her
alanın onu **okuyan** bir testi olmalı; yoksa refactor sırasında sessizce düşer ve
tip sistemi haber vermez — `null` geçerli bir `string?` değeridir.

Aynı sınıftan: [[genel-desenler]] "Yazılı olan doğru, yazılmamış olan kayıp" —
doğru rapor, doğru yan etki anlamına gelmez.

### Denetim, öğrettiği davranışı cezalandırmamalı

Bir kontrol yanlış pozitif veriyorsa asıl zarar gürültü değildir — **doğru davranan
oturumun cezalandırılmasıdır.** Ceza öğreniliyor: iki kez boşuna kırmızı gören
oturum üçüncüde ya eşiği yükseltir ya kontrolü kapatır. Denetim o an ölür.

2026-08-27, kontrol 15'in ilk sürümü: ölçüt `guncelleme` beyanıydı ve o bir
**tarih** (`YYYY-AA-GG`), kod commit'i ise bir **zaman damgası**. Aynı gün hem kod
yazıp hem mimariyi güncelleyen oturum ertesi gün kırmızı görüyordu — ölçüldü,
`web-mimari.md` koddan **23 saat sonra** güncellenmişti ve kontrol bunu göremedi.
Yani kontrol, tam da kendi öğrettiği davranışı cezalandırıyordu.

**Düzeltme çözünürlükte, ölçütte değil.** Ölçüt artık dosyanın **vault'taki commit
zaman damgası**. Bu `mtime` değildir: dosyaya dokunmak commit üretmez, içerik
değişmeden git kayıt tutmaz. *"Beyan ölçülür, dokunma ölçülmez"* ilkesi duruyor,
yalnız saniyeye iniyor. Henüz commit'lenmemiş dosya **taze sayılır** — az önce
yazılmıştır, vault commit'i bekliyordur.

**Genel kural:** yanlış pozitif veren denetim susturulmaz ama **düzeltilmeden de
bırakılmaz**. Üçüncü seçenek yok; bırakılırsa kendini iptal ettirir.

Bunu kontrolü yazan değil, **cezalandırılan oturum** yakaladı. Ölçüsünü koyanın
kendi ölçüsünün fazla kaba olduğunu görmesi zordur → [[genel-esszamanli-oturumlar]]

### Denetimden geçen düzenleme doğru olmayabilir

`dogrula.py` biçim ve bağlantı denetler; **tablo bütünlüğünü denetlemez.**
2026-08-27: bir düzenleme betiğinde `eski2` yerine `eski` yazdım. Sonuç: "Deploy"
satırı **silindi** ve `## 🟢 Tamamlananlar` başlığı tablonun ortasına girdi. Doğrulayıcı
**TEMİZ** dedi, commit'lendi, push edildi. Hatayı bir sonraki düzenlemede tabloya
bakınca gördüm.

Aynı sınıftan üçüncü olay: 2026-08-24'te aralıkla silme beş görevi yok etmiş ve
doğrulayıcı yine TEMİZ demişti (kontrol 14 o yüzden yazıldı).

**Kural: metin bloğu taşıyan her betik, yazdıktan sonra taşıdığı şeyi geri saymalı.**
Görev taşırken kimlik kümesini saydım ve kayıp olmadığını kanıtladım — bu doğruydu.
Tabloya satır eklerken saymadım — bu yanlıştı. Ölçüm alışkanlığı **iş türüne göre
değil, işlem türüne göre** uygulanır: dosyaya çok satırlı blok yazan her işlem
sayılır.

Değişken adı hatası derleyicisiz dillerde sessizdir; `eski`/`eski2` gibi ardışık
adlar bu hatayı davet eder. Ayrı ve anlamlı ad kullan.

### Okunup yazılmayan dosya, hiç okunmayandan kötüdür

Tetikleyicisiz dosya çürür — ama çürümenin iki farklı ağırlığı var:

| Durum | Sonuç | Örnek |
|---|---|---|
| Ne okunur ne yazılır | **Sessizce** yalan söyler; ancak biri açınca görülür | `api-mimari.md` |
| **Okunur ama yazılmaz** | Yalanı **her oturuma enjekte eder** | `acilis.md` |

2026-08-27'de ölçüldü: `acilis.md` her oturumda `SessionStart` hook'uyla otomatik
yükleniyordu ve *"API: yalnız `/api/health` çalışıyor, sırada şema"* diyordu — o an
21 controller, 69 yol, 106 tablo vardı. **Beş iddiasının beşi de yanlıştı.**

Okuma tetikleyicisi vardı (en güçlüsü: otomatik), yazma tetikleyicisi yoktu. Yani
dosya sıcaktı ama beslenmiyordu. Her yeni oturum bayat bilgiyle başlıyor, ilk
kararlarını ona göre veriyordu.

**Kural: bir dosyanın okunma sıklığı arttıkça yazma tetikleyicisinin sıkılığı da
artmalı.** En sıcak dosya en sıkı tetikleyiciyi ister; tersi felakettir.
`acilis.md` artık `durum.md` her değiştiğinde aynı oturumda güncellenir ve
`dogrula.py` kontrol 16 aradaki açığı ölçer.

Aynı sınıftan: [[genel-desenler]] "Tetikleyicisi olmayan dosya çürür"

## Kendi çıkarımım, karar değildir

`domain-gereksinimler.md`'de `*(çıkarım)*` etiketli maddeler var — Mert'in söylediği
değil, benim doldurduğum boşluklar. Bunlar zamanla karar gibi okunmaya başlıyor.

- **Etiketli bir maddeye sonradan itiraz edebilirim ve etmeliyim.** Daha iyi
  muhakeme ettiğimde eski çıkarımım bağlayıcı değildir
- **Ama tek taraflı silmem.** İtirazı gerekçesiyle Mert'in önüne koyarım; kararı o
  verir. 2026-08-24'te backend oturumu "müsaitlik yazma anında hesaplanıp
  saklanmalı" maddesine böyle itiraz etti — silmeden, sorarak
- Mert'in söylediği ile benim çıkarımım **aynı paragrafta karışmaz**; karışırsa
  altı ay sonra hangisinin kim olduğu bilinmez

## Gevşek ölçüt, ölçmemekten kötüdür

**Ölçüt yanlışsa ölçüm "temiz" der ve aramayı durdurur.** Hiç ölçmemek en azından
soruyu açık bırakır.

2026-08-28'de web oturumu "API yollarının front-end'de karşılığı var mı" sorusunu
ölçtü. İlk ölçüt **uç adının kaynakta geçip geçmediğiydi** — o kadar gevşekti ki
`rental-types` diye bir *bileşen adı* bile eşleşme sayıldı. Sonuç: **"hepsi bağlı".**
Doğru ölçüt — `api()`/`dcFetch()` çağrısında **yolun kendisi** — 24 boşluk buldu;
üçü elle elendi (dinamik değişkenle kurulan yollar, `offers/${id}/${eylem}`), geriye
**21 bağlanmamış yol** kaldı. Beşinin ekranı zaten vardı, mock veriyle çalışıyordu.

İlk sonuç raporlansaydı `durum.md`'ye o gün yalan girecekti — ve "hepsi bağlı"
cümlesi kimseyi bir daha bakmaya itmezdi.

**Kural:** bir ölçüt ilk kez kullanılıyorsa, ölçümden önce **negatif kontrol**
çalıştırılır — bilerek eşleşmemesi gereken bir örnek verilir. Eşleşirse ölçüt
gevşektir. Ve **"hepsi temiz" çıkan ilk ölçüm şüphelidir**: bu alanda temiz sonuç
kuraldır değil istisnadır, çünkü kimse daha önce bakmamıştır.

Bu, [[genel-kararlar]]'daki "ölçüt kopyalanmaz, yeniden ölçülür" kuralının
tamamlayıcısıdır: kopyalanan ölçüt yanlış olabilir, **kendi kurduğum ölçüt de**.

## Panonun boş olması işin bittiğini göstermez

`03-Web/web-durum.md` 2026-08-28'e kadar **"web tarafında yapılabilir iş kalmadı"**
diyordu. Cümle yanlış değildi, **ölçülmemişti** — pano boştu, o yüzden iş yok
sanılmıştı; oysa 21 API yolunun karşılığı hiç panoya girmemişti.

Boş pano iki şeyden birini gösterir: iş bitti, ya da **iş panoya yazılmadı**.
İkisini ayırmanın tek yolu panoya değil **kaynağa** bakmaktır. "Yapılacak iş
kalmadı" cümlesi, ancak son ölçümün tarihi ve ölçütü yanına yazılırsa bir iddiadır;
yalnız başına bir tahmindir.

## Başarılı yanıt, doğru yazdığının kanıtı değil

2026-08-31'de iki oturum aynı hatayı **yapısal olarak** aynı biçimde yaşadı:

- **Web:** kısa tarih biçimi yılı atlıyordu. Ekran çalışıyordu, hata görünmüyordu.
- **Backend:** olay günlüğü ucu `200` dönüyordu, ama yük boş kaydediliyordu.

İkisinde de "işlem başarılı" sinyali vardı ve ikisi de yanlıştı. Doğrulama her iki
durumda da **yazdığın şeyi başka bir yerden okumayı** gerektirdi — ekranı değil
listeyi, yanıt kodunu değil kaydı.

**Kural:** bir yazma işlemi, yazılanı **ayrı bir yoldan geri okumadan** doğrulanmış
sayılmaz. `200`, `build temiz` ve `ekran açılıyor` üçü de aynı sınıfta: gerekli
koşul, yeterli değil → [[web-mock-hatayi-gizler]]

## Sahte veri, kodun kendi hatasını gizler

Yukarıdaki web hatasının **neden aylarca görünmediği** ayrı bir derstir: tasarımdan
gelen mock kayıtların **hepsi aynı yıldaydı**. Yılı atlayan biçimlendirici o veri
kümesinde asla yanlış çıktı üretemezdi. Hata koddaydı, ama **veri onu ifade
edilemez kılıyordu**.

Mock veri iki zarar verir, ikincisi daha sinsi: (1) ekranda yanlış bilgi gösterir,
(2) **kodun hatalarını görünmez yapar**. Birincisi gerçek uca bağlanınca kendiliğinden
biter; ikincisi **o güne kadar biriken hataların hepsini aynı anda** ortaya döker.

**Kural:** mock veri, gerçeğin *dar* bir örneği olmamalı — tek yıl, tek şehir, tek
durum değeri, hepsi aynı uzunlukta ad. Çeşitliliği olmayan sahte veri test değil,
**körlük üreticisidir**.

## Muafiyet kalıcı olduğu yerde kör nokta olur

`dogrula.py` kontrol 15, mimari dosyasının kodun gerisinde kalıp kalmadığını
ölçer. İçinde bir muafiyet vardı: *dosya çalışma ağacında kirliyse atla — az önce
yazılmış, commit bekliyor, taze say.*

Bu muafiyet **vault oturumunun bakış açısıyla** yazılmıştı: yaz, hemen commit'le,
kirlilik saniyeler sürer. Ama vault'un kendi kuralı şunu söylüyor: **alan oturumları
vault'a yazar ve commit atmaz** — commit'i vault oturumu atar. Yani `api-mimari.md`
ve `web-mimari.md` günlerce kirli durur.

Sonuç: kontrol, izlemesi gereken iki dosya için **kalıcı olarak sustu.**
`api-mimari.md` "21 controller" derken 28 vardı, *"katalog, arama, mesajlaşma HÂLÂ
YOK"* derken sekizi de yazılmıştı. Kontrol 15 her gün çalıştı ve hiçbir şey demedi;
çürümeyi bulan, kontrol 17'nin bir yan etkisi oldu.

**Muafiyet yanlış değildi — eksikti.** Vault oturumu için doğruydu, alan
oturumları için hiç doğru olmadı. Hata muafiyetin kendisinde değil, **muafiyeti
yazarken kullanıcının tek tip sanılmasındaydı**.

Bu, aynı gün mock veride bulunan şeyle **aynı hata**: mock'un tüm kayıtları aynı
yıldaydı, muafiyetin tüm kullanıcıları aynı oturum tipiydi. İkisi de *dar bir
örnekten genel kural çıkarmak*. Sahte veride bu körlük üretiyor, muafiyette
sessizlik.

**Kural:** bir denetime muafiyet yazarken tek soru sorulur — *"bu koşul kimde
kalıcı hâle gelir?"* — ve bu soru **"kimde" kısmı çoğul kabul edilerek** sorulur:
muafiyeti yazan oturum tipi, muafiyetin geçerli olduğu tek tip olabilir. Muafiyetin varsayımı (kirlilik geçicidir) sistemin bir
bölümünde yanlışsa, denetim orada yok demektir. Ve muafiyetler **denetimin en çok
gerektiği yerde** kalıcılaşma eğilimindedir: en çok yazılan dosya, en uzun kirli
kalandır.

İkinci ders: **denetimin sessizliği kanıt değildir.** Kontrol 15 iki kez yanıldı —
önce gün çözünürlüğüyle yanlış pozitif verdi (bunu fark ettik, çünkü konuştu),
sonra muafiyetle yanlış negatif verdi (bunu üç gün fark etmedik, çünkü sustu).
**Konuşan denetim denetlenir, susan denetim denetlenmez** → [[genel-kararlar]]

## Bir kontrolün varlığı, çalıştığının kanıtı değil

2026-08-31 haftasında **beş** örnek çıktı, üç ayrı katmandan:

| Kontrol | Vardı ama | Nasıl bulundu |
|---|---|---|
| `dogrula.py` kontrol 15 | muafiyet yüzünden izlediği iki dosya için kalıcı olarak susuyordu | kontrol 17'nin yan etkisi |
| `Coupon_below_the_share_can_be_created` | iddiası **örtük**ti: "patlamadıysa geçmiştir" | 484 testin taranması |
| `publiclyReadable` | — | *"çalışmasaydı ne farklı görünürdü?"* |
| Hız sınırı bölümlemesi | — | aynı soru |
| Üretim kapıları | — | aynı soru |

Beşi de aynı aileden: **kontrol yazılmıştı, doğru soruyu soruyordu, ve cevabı
hiçbir yere ulaşmıyordu.** Yeşil bir test, sessiz bir denetim ve var olmayan bir
kontrol dışarıdan **birbirinin aynısı** görünür.

**Teşhis sorusu — beşini de bu buldu:**

> *Bu kontrol çalışmasaydı, ne farklı görünürdü?*

Cevap **"hiçbir şey"** ise kontrol zaten susuyordur. Bu soru bir kontrolü yazarken
de sorulmalı, yazıldıktan sonra da: kontrol 15 doğru yazılmıştı, **sonradan**
sustu — vault'un kuralı (alan oturumları commit atmaz) muafiyetin varsayımını
geçersiz kıldı. Yani cevap zamanla değişebilir.

**İki alt biçimi ayırt et**, çünkü fark ediliş süreleri farklı:

- **Örtük iddia** — "istisna atmadıysa geçmiştir". Satırın gerçekten yazılmasını,
  yazma çağrısının sessizce hiçbir şey yapmamasından ayırt edemez. Testi taramakla
  bulunur.
- **Kalıcılaşmış muafiyet** — kontrol çalışır, koşula takılır, atlar. Testte
  görünmez, çıktıda görünmez; **yalnızca beklediğin bir uyarının gelmediğini fark
  etmekle** bulunur. Kontrol 15'te üç gün sürdü.

Bu, [[genel-kararlar]]'daki "araç gerekli koşuldur, yeterli değildir" kuralının en
sert hâli: burada araç gerekli koşulu bile sağlamıyor, yalnız sağlıyor **gibi**
görünüyor.

## Aynı olguyu iki yerde tutan dosya, birinde bayatlar

`durum.md` hem pano sayılarını hem de *"21 controller · 69 yol"* ölçü tablosunu
taşıyordu; `acilis.md` aynı ölçüyü *28 · 93 · 42* diye yazıyordu. İkisi de vault
dosyası, ikisi de "güncel" etiketliydi. Çelişkiyi ne kontrol yakaladı ne ben — alan
oturumu okurken gördü.

**Kural:** bir olgunun **tek yazım yeri** olur; diğer dosyalar ona link verir,
kopyalamaz. Kopyalanan sayı, kopyalandığı anda ikinci bir bakım yükü doğurur ve
o yük hiç kimseye atanmaz.

**Bu kuralın uygulanışı görünmezdir** ve bu onu kırılgan yapar. Web oturumu pano
sayısını `web-durum.md`'ye **bilerek yazmıyor**; doğru davranış burada *yazılmayan
bir şey*, dolayısıyla dosyaya bakan biri kuralın uygulandığını göremez — yalnızca
bir boşluk görür ve iyi niyetle doldurur. Bu yüzden kaçınma **gerekçesiyle** kayda
geçer: eksik değil, karar.

**İstisna — arşiv satırı bayatlamaz:** tarihli bir kanıt cümlesi ("27 Ağustos'ta
kapatıldı, o gün 21 controller vardı") güncel iddia değildir, **o tarihe ait bir
ölçümdür** ve güncellenmez; güncellenirse kanıt olmaktan çıkar. Ayrım şudur:
*şu an böyle* diyen bayatlar, *o gün böyleydi* diyen bayatlamaz.

## Kontrol içeriğe bakıyorsa yapıya da bakmalı

`dogrula.py` kontrol 17 pano maddelerini denetliyordu: bitmiş görev Yapılacak'ta mı.
Ama **bölümün kendisine** bakmıyordu. 2026-08-31'de `genel-gorevler.md`'de iki adet
`## 🔵 Yapılacak` başlığı bulundu — biri boştu, artığı bir taşıma betiği bırakmıştı.
İkincisine yazılan bir görev panodan **sessizce düşerdi** ve hiçbir kontrol
konuşmazdı.

**Kural:** bir dosyanın içeriğini denetleyen kontrol, o içeriğin **oturduğu yapıyı**
da denetlemek zorundadır — yinelenen başlık, kayıp bölüm, yanlış sıra. İçerik
doğru olabilir ve yanlış yerde durabilir; okuyan da denetleyen de onu göremez.

Bu, bugünün diğer dersiyle aynı kökten: kontrol 15 **muafiyet** yüzünden sustu,
kontrol 17 **kapsam** yüzünden. İkisi de yazıldıkları soruya doğru cevap veriyordu;
sorun sorunun dar olmasıydı → [[genel-desenler]]

## Para kuralını tek dilim üzerinden sorma

2026-09-05'te `S-12`'ye (müşteri kaynaklı iptalde iade oranı) *"komisyon tam
alınsın"* cevabı geldi. Soru **tek dilim** üzerinden sorulmuştu ve o dilimde cevap
doğruydu. Backend uygulamadan önce sayılaştırdı: **%100 iade diliminde** kural
işletmeyi komisyon kadar **eksiye** düşürüyor, `CK_Payouts_Amount >= 0` kısıtı da
**sonraki turun hakedişini kilitliyordu**. Geri soruldu, cevap *(c) orantılı*
olarak değişti, kod hiç yazılmadı.

**Kural:** bir para kuralı sorulmadan önce **uç değerlerle sayılaştırılır** — %0,
%100, iade > tahsilat, iki iptal üst üste. Soru "hangi oran" değil, *"şu dört
senaryoda kim ne alır"* biçiminde sorulur. Tek dilimlik soru, cevabı veren kişiye
diğer dilimleri **göstermez**; yanlış cevabı veren soru olur.

Bu, uygulamadan önce sayılaştırmanın da gerekçesi: kural yazılıp test edilseydi
hata testte değil, **ilk %100 iadede** — yani bir işletmenin parasında ortaya
çıkardı.

## Kendi notun da başkasının notu kadar bayatlar

`api-benim-kararlarim.md`'de 26 Ağustos tarihli *"reddetme ucu YOK"* notu duruyordu.
Ölçüldüğünde **uç ve yedi testi vardı** — arada başka bir oturum yazmıştı.

Vault'un "not koda aykırıysa kod doğrudur" kuralı **kendi notların için de
geçerlidir** ve eşzamanlı oturumlarda daha sık geçerlidir: notu yazan sen olsan da,
o notu geçersiz kılan değişikliği yapan sen olmayabilirsin. **Tarih tazelik değil,
yalnızca yazılma anıdır** → [[genel-esszamanli-oturumlar]]

## Beyan ölçülen şeyse, beyanı güncellemek işin parçasıdır

`durum.md` dört gün içinde **üç kez** düzenlendi; `guncelleme` alanı hiç
değişmedi. İçerik güncel, beyan bayattı.

Bu vault'ta zararsız bir tutarsızlık değil: **beyan ölçülen şeydir.** Kontrol 7
(durum bayatlığı) ve kontrol 15 (mimari bayatlığı) frontmatter'daki tarihe bakar.
Yanlış beyan yalnızca insanı değil, **diğer kontrolleri de** yanıltır — ve onları
yanlış yönde yanıltır: dosya bayat sanılıp gereksiz uyarı çıkar, ya da taze sanılıp
gerçek bayatlık gizlenir.

Bu bir dikkat sorunu değildi, **eksik kapıydı**: dosyayı düzenlemek frontmatter'a
dokunmayı gerektirmiyordu. `dogrula.py` **kontrol 19** artık beyanı dosyanın gerçek
son yazımıyla karşılaştırıyor.

**Kontrol aynı gün iki kez dar çıktı, ikisi de öğreticiydi.** Önce sabit altı
dosyalık listeyle yazıldı — backend "iki değil altı dosyaydı" dedi; kontrol doğru
söylüyordu ama **eksik** söylüyordu. Çözüm listeyi büyütmek değil **kaldırmak**
oldu: `guncelleme` beyan eden her dosya ölçülüyor — *beyanda bulunmak izlenmeyi
kabul etmektir.*

Sonra tersine kaydı: liste kalkınca **55 dosya** bildirdi ve neredeyse hepsi toplu
commit artefaktıydı. Sebep vault'un **kendi kuralı**: alan oturumları yazar, vault
oturumu commit'ler — bir not 24'ünde yazılıp 27'sinde commit'lenir, **beyan doğru,
commit geçtir**. 55 uyarı veren denetim okunmaz, kapatılır.

Ölçüt bu yüzden dosyanın durumuna göre ayrıldı:

| Dosya | Ölçüt | Tolerans | Neden |
|---|---|---|---|
| Kirli | `mtime` | yok | bu makinedeki gerçek yazım anı; **düzeltmenin mümkün olduğu tek an** — commit'lenmeden önce |
| Temiz | son commit | 7 gün | commit tarihi yazım tarihi değildir; yalnız belirgin ihmal bildirilir |

55 → 5, ve beşi de gerçek çıktı. **Bir denetimin doğru eşiği, ürettiği uyarıların
okunup okunmadığıyla ölçülür** → "Denetim, öğrettiği davranışı cezalandırmamalı"

## Okunmadan verilen atıf, belgesiz koddan kötüdür

2026-09-05'te web oturumu kendi kodunu ölçtü: içinde **onlarca** `→ [[web-desenler]]`,
`→ [[web-kararlar]]` atıfı vardı ve o oturumda **hiçbiri açılmamıştı**. Atıflar
oturum başında yüklenen özetten ve hafızadan yazılmıştı.

Bu, kaynak göstermenin en kötü biçimi. Belgesiz kod okuyana *"dayanağı yok"* der
ve okuyan kendi doğrular. Okunmadan verilen atıf ise *"dayanağı var"* der ve
**doğrulamayı durdurur**. Belgedeki kural değişmiş olsa koddaki atıf yine oraya
işaret eder ve kimse fark etmez.

**Kural:** bir `[[dosya]]` atıfı yazmak, o dosyayı **bu oturumda açmış olmayı**
gerektirir. Açmadıysan atıf yazma — ya aç, ya *"hatırladığım kadarıyla"* diye yaz.

`dogrula.py` **kontrol 21** bunun ölçülebilen yarısını ölçüyor: koddaki atıf
vault'ta **var olan** bir dosyayı gösteriyor mu (bugün: 77 atıf, 0 ölü hedef).
İçeriğin doğruluğunu ölçemez ve bu **bilinerek** kabul edildi — alternatifi hiçbir
şeyin ölçülmemesiydi. Ölü atıf, adı değişmiş bir dosyaya sessizce işaret eder.

## Kural bir kapıdır, başlangıç okuması değil

*"Bir alanda dosya değiştirmeden önce desenler + araçlar + görevler oku"* kuralı
2026-09-05'te ölçüldü: web oturumu `gorevler` dışında ikisini de açmadı ve
**bunun hiçbir bedeli olmadı**. Bir kez itiraf edip sessizce devam etti.

Bu, kuralın en tehlikeli hâli: **delinen kural yalnız kendini götürmez, yanındaki
kuralların ağırlığını da götürür.** Uyulmadığı fark edilen ama sonucu olmayan bir
kural, diğerlerinin de isteğe bağlı olduğunu öğretir.

Sebep şuydu: o oturumdaki her gerçek kusuru **ölçüm** yakaladı, hiçbirini **okuma**
yakalamadı. Her dosya değişikliğinde okunması istenen bir belge, üçüncü dosyada
okunmamaya başlar.

**Kural:** bir belge, ne zaman *okunacağıyla* değil, **hangi anda karar
değiştireceğiyle** bağlanır. Desen belgesinin doğru anı işin başı değil, **deseni
çiğnemek üzere olduğun an**dır — mock veri basmadan, boş tablo göstermeden, elle
tip yazmadan hemen önce. Orada belge bir kapıdır ve kapı atlanmaz.

⚠️ **Bunun bedeli var:** web aynı vekil izin listesi tuzağına **üç kez** düştü;
ikisinden sonra `web-mimari`'ye yazmıştı ama **okuma tetikleyicisi olmadığı için**
üçüncüsünde yine düştü. **Yazmak yetmiyor** — dar kural, tetikleyicinin doğru yere
konmasını daha da kritik yapar.

## Gidecek yeri olmayan bilgi sohbette kalır

Web oturumu tek bir oturumda **yedi** *"yayına çıkmadan önce mutlaka"* maddesi
üretti ve **hiçbiri vault'a girmedi**. Disiplin sorunu değildi: bu maddeler görev
değil (yapılacak iş yok), blocker değil (bugün kimseyi durdurmuyor), karar değil
(tartışılmadı). **Gidecek yerleri yoktu.**

Vault'un bölmeleri bir bilgi türünü değil, bir **hayat döngüsünü** temsil eder.
Döngüsü olmayan bilgi — doğduğu an geçerli, bir tarihte kritik, arada uykuda —
hiçbir bölmeye uymaz ve sohbette kalır.

**Kural:** *"bu bilgi nereye yazılır?"* sorusunun cevabı yoksa, cevap "hiçbir yere"
değil **"yeni bir bölme"**dir — yeter ki iki tetikleyicisi olsun. `yayin-oncesi.md`
böyle doğdu → [[yayin-oncesi]]

İkinci ders, bu maddelerin **yan ürün** olmasından geliyor: hepsi başka bir işi
yaparken doğdu. Sonradan hatırlanarak toplanamazlar — bu yüzden yazma tetikleyicisi
"iş bitince" değil, **"cümleyi kurduğun an"**dır.

## Araç bilgisi eskimez, durum bilgisi eskir

2026-09-05'te backend vault'un o günkü **net bilançosunu** çıkardı ve iki uç
gerçek olaydı:

**Kazanç.** `A-97` migration'ı `permission denied to set role "dailycruising"`
verdi. `api-araclar`'da tam komut duruyordu — ve yalnız komut değil **gerekçesi**:
`ALTER DEFAULT PRIVILEGES` o role bağlı, başka rolle koşarsan tablo o rolün malı
olur ve *"uygulama açılışta değil İLK KULLANIMDA patlar."* O not okunmasaydı süper
kullanıcıyla koşulup geçildi sanılacaktı.

**Kayıp.** `api-durum`'daki `S-23` notu *"tekne detayında donanım ataması yok,
aramada süzgeç yok"* diyordu. **İkisi de yanlıştı**, uçlar aylardır vardı. Nota
güvenilip iş planlandı, sonra ölçülüp notun bayat olduğu bulundu. Web aynı gün
aynı şeyi yaşadı (*"süzgeç konamaz, parametre yok"* — parametre vardı).

İkisinin farkı yazarın disiplini değil, **bilginin türü**: bir aracın nasıl
çalıştığı eskimez, bir şeyin var olup olmadığı eskir.

**Kural:** vault'a **durum taşıyan** bir cümle yazarken — "X yok", "Y henüz
yapılmadı", "Z eksik" — cümle **ölçüm tarihiyle** yazılır. Tarihsiz bir yokluk
iddiası, yazıldığı gün doğru olsa bile ertesi gün yalana dönüşebilir ve **hiçbir
uyarı vermez**. Yokluk iddiası en hızlı bayatlayan bilgi türüdür, çünkü onu
geçersiz kılmak için birinin sadece o şeyi yazması yeterlidir.

Bunun pratik sonucu: *"X yok"* değil, *"5 Eylül'de ölçüldü, X yoktu"* yaz. İkincisi
yanlış olduğunda bile **kendini ele verir**.

## Kural okunmaz, hikâye akılda kalır

Backend'in kendi ölçümü: on beş dosya değiştirdi, `api-desenler`'i **bir kez bile**
baştan açmadı. Web'inki: aynı. İkisinde de kural delindi ve **bedeli olmadı**.

Ama bir karşı örnek var ve öğretici: `api-desenler`'e yazılan *"yorumun iddiası da
ölçülmek zorunda"* dersi backend'i **aynı gün yakaladı** — bir testin yorumunda
*"işin konuşmayı kapatabilmesini ölçüyor"* yazıyordu, oysa test yalnız satırın
varlığına bakıyordu. Yorumu düzeltmek yerine **testi iddiaya eşitledi**.

Fark şu: o dersi okuduğu için değil, **bir kez yazdığı için** davranışı değişti.
Ödenen bedel hatırlanıyor; okunan kural hatırlanmıyor.

**Kural:** `*-desenler.md` bir *kural listesi* değil, **bir kez ödenmiş bedellerin
kaydı** olarak yazılır. Her madde bir olaya bağlanır: ne oldu, ne kaybettik, ne
öğrendik. Kural gibi değil hikâye gibi dursun — çünkü belge bir **refleks kaynağı**
olarak işe yarıyor, bir *başvuru listesi* olarak yaramıyor.

Bu, "kural bir kapıdır" desenini tamamlıyor: kapı **ne zaman** okunacağını söyler,
bu da **nasıl yazılacağını**.

## "Testi var" ile "doğrulandı" aynı şey değil

2026-09-05'te backend Paratika sağlayıcısını yazdı: dört yöntem, yedi test, beş
mutasyon yakalanıyor. Pano **"tamamlandı"** gösterdi. Ama testlerin **hiçbiri
gerçek sağlayıcıyla konuşmamıştı** — `QUERYTRANSACTION` cevabının tam biçimi
sözleşme belgesinden yazılmıştı, gerçek yanıtla karşılaştırılmamıştı.

Bu ne "bitti" ne "yapılmadı"; **üçüncü bir hâl**. Ve panoda görünmediği için
tehlikeli: panoya bakan biri doğrulanmış sanır.

**Kural:** dış bir servise, hesaba veya kimlik bilgisine bağlı kod
**🔬 doğrulanmamış** olarak işaretlenir ve [[yayin-oncesi]]'ne girer. Okuma
tetikleyicisi nettir: **hesap geldiği an ilk iş o listeyi açmaktır.**

Bu, "başarılı yanıt doğru yazdığının kanıtı değil" deseninin bir üst katmanı:
orada yanıtın kendisi yalan söyleyebiliyordu, burada **yanıtı hiç görmedik** ve
testler onun yerine bizim varsayımımızı ölçüyor.

## "Testler yeşil" demeden önce değiştirdiğin satırın koştuğunu ölç

Yukarıdakinin bir adım kötüsü: yanıtı görmemek değil, **kodun hiç çalışmamış
olması.**

2026-09-05'te backend `ForcePathStyle`'ı yalnız AWS **dışı** sağlayıcılarda açık
kalacak biçimde değiştirdi ve *"600 test yeşil"* diye raporladı. Doğruydu ve
**yanıltıcıydı**. Ölçtüğünde:

- Testler MinIO'ya koşuyordu → `ServiceUrl` dolu → yol-tarzı **hâlâ açık**; yani
  değiştirilen dal testlerde hiç girilmiyordu.
- Üstelik testler `Program.cs`'i **hiç kullanmıyordu**: iki test sınıfı kendi
  `AmazonS3Config`'ini kuruyor ve içinde `ForcePathStyle = true` **elle yazılı**.

Değiştirilen satır ne testte ne geliştirmede, **hiçbir yerde çalışmadı** — ve pano
"tamamlandı", testler yeşil gösteriyordu.

**Kural:** *"testler yeşil"* cümlesini kurmadan önce, **değiştirdiğin satırın o
testlerde gerçekten çalıştığını** ölç. Yeşil bir paket, değişikliğinin doğru
olduğunu değil, yalnızca **var olanın bozulmadığını** kanıtlar. En hızlı ölçüm:
satırı bilerek boz, testin kırmızıya döndüğünü gör — dönmüyorsa o satır ölçülmüyor
demektir.

⚠️ **En tehlikeli hâli kendi raporun hakkında olanıdır.** Bayat bir *başkasının*
notuna güvenmek yakalanabilir; kendi az önce yazdığın rapora güvenmek yakalanmaz,
çünkü onu doğrulamak aklına gelmez. Backend aynı gün ikisini de yaşadı: `S-23`'te
başkasının notuna güvenip yanıldı, `Y-14`'te kendi raporuna güvenseydi yanılacaktı.
İkincisini yakalayan şey nota bakmak değil, **iddiayı ölçmek** oldu
→ [[yayin-oncesi]]


## Denetimin kendisi de denetlenir — susan kontrol ölçülmeden aklanmaz

`dogrula.py` 21 kontrol taşıyor ve çoğu aylardır hiç konuşmadı. Sessizlik iki
şeyin işareti olabilir: kontrol doğru çalışıyor ve ortada sorun yok, **ya da**
kontrol bozuk ve hiçbir şey görmüyor. Dışarıdan ikisi aynı görünür.

Bunun bedeli iki kez ödendi: **kontrol 15** `if kirli: continue` muafiyeti
yüzünden dokuz gün boyunca tam da izlediği dosyalarda kör kaldı; **kontrol 17**
yalnız maddelere bakıp bölüm yapısına bakmadığı için boş yinelenen başlığı
görmedi. İkisi de "TEMİZ" yazarken kördü.

`_araclar/kontrol-testi.py` bunu ölçüyor: her kontrol için gerçek bir kusuru
taklit eden bir bozma senaryosu var; vault kopyalanıp bozuluyor ve o kontrolün
**kırmızıya döndüğü** görülüyor. Dönmüyorsa kontrol yazılıdır ama ölçmüyordur.

⚠️ **Aracın kendisi de yalan söyleyebilir — ve ilk sürümde söyledi.** Kopyayı
senaryolar arasında `git reset --hard` ile sıfırlıyordum; bu, kopyadaki
`dogrula.py`'yi de HEAD'e döndürüyordu. Yani araç **commit'lenmiş** sürümü
ölçüyor, çalışma ağacındakini hiç çalıştırmıyordu. Meta-testte yakalandı:
kontrol 18 bilerek kör edildi, araç yine "hepsi kırmızıya döndü" dedi.
Sıfırlama `rsync`'e çevrildi; aynı meta-test artık `SESSIZ` diyor.

**Ders:** bir ölçüm aracının yeşil vermesi, ölçtüğünün kanıtı değildir; kendisi
de bozulup kırmızıya döndürülmelidir. Bu, aşağıdaki *"testler yeşil demeden önce
değiştirdiğin satırın koştuğunu ölç"* kuralının denetim katmanına uygulanmış
hâli — oradaki kural koda bakıyor, buradaki kurala bakana bakıyor.

## Yazılan not okunuyor sayılmaz — hangisinin karşılığını ödediği ölçülür

2026-09-05'e kadar vault'ta 83 notun **yazıldığını** biliyorduk (git söylüyor),
**okunduğunu** hiç bilmiyorduk. `_araclar/okunma.py` 108 oturum kaydını taradı.
Ölçüt kasten dar: *notu yazan oturumların dışında kaç oturumda açıldı?* Kendi
yazıldığı oturumda görünmek, bir notun işe yaradığını göstermez.

| Bölüm | Dışarıdan okunan |
|---|---|
| `notlar/` — gözlem notları | **5 / 41** |
| Ana bölmeler (mimari · kararlar · desenler · görevler · araçlar · durum) | **13 / 28** |
| `04-Oturumlar/` arşivi | 3 / 11 |

**Ana bölmeler karşılığını ödüyor, `notlar/` katmanı ödemiyor.** Sebep disiplin
değil yine tetikleyici: ana bölmelerin tetikleyicisi bir *olaydır* ("yapıya
dokunacağım", "işe başlıyorum"), `notlar/` katmanınınki ise bir *duygudur*
("tekrar eden bir soruna takıldım"). Olay ölçülebilir biçimde olur; takılmak
fark edilmeden geçer.

⚠️ **Bu, notları silmek için gerekçe değildir.** Bir tuzak notu yılda bir kez
okunur ama okunduğunda saatler kazandırır — düşük okunma, düşük değer demek
değil. Ölçümün söylediği tek şey şu: **hangi katmanın kendini taşıdığını
tahminle değil sayıyla biliyoruz artık**, ve şablona ne gireceğine bu karar
verecek (`G-15`).

⚠️ **Ölçümün kendi sınırları — susmasın diye yazılıyor:** açılma ölçülür,
okunup anlaşılma değil. Yalnız diskte duran oturum kayıtları taranır, yani
sayılar bir **alt sınırdır**. Sınıflandırılamayan Bash dokunuşları ayrıca
raporlanır. Ve ilk sürüm yanlış ölçüyordu: yol ayıklayan düzenli ifade `/`
karakterini yasaklıyor, böylece **tam da ölçmek istediği mutlak yolları
eliyordu**; araç "4 oturum" derken bağımsız `grep -l` 73 dosya buldu. Aynı
dersin üçüncü tekrarı — bkz. bu dosyadaki *"denetimin kendisi de denetlenir"*.

## Makine taşınır, içerik taşınmaz

Vault'un iki ayrı parçası var ve 2026-09-05'e kadar iç içe duruyorlardı:

- **Makine** — `dogrula.py`, `kontrol-testi.py`, `okunma.py`; roller, tetikleyici
  disiplini, yazma hakkı bölüşümü, pano biçimi. Bunlar DailyCruising'e ait değil.
- **İçerik** — 83 not, kararlar, desenler, ölçülen sayılar. Bunlar bu projeye ait.

Betiklerdeki 31 satır proje sabiti ikisini birbirine yapıştırıyordu.
`_araclar/vault.json` çıkarıldı: alan adları, önekler, kod repoları, pano bölüm
adları (`Yapılacak`/`Todo`), işaretler (`Kanıt:`/`Proof:`) ve dokuz eşik oraya
taşındı. Üç betikte kalan proje sabiti sayısı: **0**.

**Kanıt tahminle değil ölçümle:** `Belgeler`/`Urun` alanlı, `Todo`/`Doing`/`Done`
panolu, `Proof:`/`**Why` işaretli bambaşka bir vault kuruldu ve aynı `dogrula.py`
üzerinde çalıştı — hem de o vault'un gerçek bir kusurunu bularak.

⚠️ **Şablona içerik konmaz.** Yeni bir projeye 83 not kopyalanırsa, o proje hiç
sormadığı soruların cevaplarıyla başlar; bu boş vault'tan kötüdür, çünkü bayat
cevap "vault'ta var" hissi verip aynı bilginin yeniden üretilmesini engeller.
Taşınacak olan iskelet ve disiplindir, cevaplar değil.

⚠️ **Taşıma sırasında en olası kusur sessiz atlamadır.** Yapılandırmada yazan bir
kod reposu yolu yanlışsa kontrol 15 ve 21 eskiden hiçbir şey demeden körleşiyordu.
Artık `OLCULEMEDI` diye konuşuyorlar — yanlış yol, yeni projede en kolay yapılan
hatadır ve sessiz kalırsa denetim var sanılır.

İlgili: [[genel-notlar]] · [[genel-kararlar]] · [[calisma-duzeni]] · [[genel-gorevler]] · [[genel-araclar]]
