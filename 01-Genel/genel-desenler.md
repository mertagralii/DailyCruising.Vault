---
rol: map
kapsam: genel
guncelleme: 2026-08-27
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


İlgili: [[genel-notlar]] · [[genel-kararlar]] · [[calisma-duzeni]] · [[genel-gorevler]] · [[genel-araclar]]
