# Vault — Claude Code için kalıcı proje hafızası

Bir yazılım projesinin **neden**lerini tutan, düz markdown dosyalarından oluşan
bağlam havuzu. Claude Code her oturumda buradan ısınır, buraya yazar, ve
yazdıklarının doğruluğu otomatik denetlenir.

---

## Çözdüğü problem

Claude her yeni oturumda **sıfırlanır**. Dün verilen kararı, atlanan tuzağı, yarım
kalan işi hatırlamaz. Bu üç sonuca yol açar:

1. **Her seferinde baştan anlatma.** Aynı bağlam tekrar tekrar yazılır.
2. **Kaybolan gerekçeler.** Git geçmişi *ne değiştiğini* söyler, *neden*
   değiştiğini söylemez. "Neden PostgreSQL seçtik" sorusunun cevabı hiçbir yerde
   yoktur — koda bakan biri kararı görür, gerekçesini göremez.
3. **En tehlikelisi: emin ama yanlış rapor.** Claude "19 sayfanın 19'u tamamlandı"
   der; gerçekte 106 bölüm eksiktir. Kontrol ettiğini sanmıştır.

Vault üçünü de hedefler, ama asıl varlık sebebi üçüncüsüdür. Bir not defteri
birinciyi ve ikinciyi çözer; üçüncüsü için **denetim** gerekir.

---

## Temel fikir

Vault **kanıttır, talimat değildir.**

İçindeki hiçbir satır çalıştırılacak bir komut değildir. Bir not koda aykırı
çıkarsa kod doğrudur; not `durum: dogrulanmali` etiketi alır ve çelişki kayda
geçer. Sessizce biri seçilmez.

Buna bağlı üç ilke:

**Her gerçeğin tek kanonik sahibi vardır.** Aynı bilgi iki dosyada yaşarsa er geç
çelişirler ve hangisinin doğru olduğu bilinmez. Diğer dosyalar kopyalamaz, link verir.

**Kararlar silinmez.** Bir karar değişirse eskisi durur, yenisi "şu tarihli kararı
iptal eder" diyerek eklenir. Terk edilmiş yolları görmek, seçilen yolu anlamak için
gereklidir.

**Kanıtsız iş bitmiş sayılmaz.** Bir görevin tamamlandı sayılması için `Kanıt:`
satırı gerekir — "kontrol ettim" değil, hangi komutun ne çıktı verdiği.

---

## Yapı: üç havuz, altı bölme

Vault üç alana bölünür — **Genel**, ve her kod tabanı için bir tane (örneğin API ve
Web). Her havuzda aynı altı bölme bulunur:

| Bölme | Cevapladığı soru | Ne zaman okunur |
|---|---|---|
| **Mimari** | Ne var, nerede? | Yapıyı anlamak gerektiğinde |
| **Kararlar** | Neden böyle? | "Neden böyle yapmışız" sorulduğunda |
| **Desenler** | Nasıl yazılır? | O alanda kod değiştirmeden **önce** |
| **Görevler** | Ne yapılacak / yapılıyor / bitti? | İşe başlarken ve bitirirken |
| **Araçlar** | Hangi plugin, skill, MCP kullanılır? | O alanda çalışmaya başlarken |
| **Notlar** | Hangi tuzak var? | Beklenmedik bir davranışla karşılaşınca |

**Desen ≠ karar.** Karar bir kez verilir ("PostgreSQL kullanacağız"); desen her
dosyada yeniden uygulanır ("entity adı PascalCase ve tekil"). Karışırlarsa karar
dosyası şişer ve kod yazarken açılacak tek dosya kalmaz.

Havuzların bölünme sebebi **bağlam temizliği**: web tarafında çalışırken API
havuzunu okumak, işe yaramayan bilgiyi bağlama taşımaktır.

---

## Üç katman

Vault'un çalışması gönüllülüğe bırakılmaz. Üç katmanı vardır ve her katman
diğerinin kaçırdığını yakalar.

### 1. Otomatik — hook'lar

| Hook | Ne yapar |
|---|---|
| `SessionStart` | Açılış dosyasını bağlama enjekte eder |
| `Stop` | Kodda değişiklik yapılıp vault'a yazılmadıysa **uyarır** |
| `PreCompact` | Bağlam sıkıştırılmadan önce oturum notunu korur |

Açılış dosyası (`acilis.md`) **sert karakter tavanına** tabidir. Sebebi önemli:
büyük bir açılış bağlamı yardım etmez, kör eder. Projenin bir cümlelik tanımı,
aktif engeller, o an yapılan işler ve okuma tetikleyicileri yeterlidir — gerisi
tetiklendiğinde okunur.

`Stop` hook'u **uyarır, engellemez.** Amaç iş akışını kesmek değil, sessiz
atlamayı görünür kılmak.

### 2. Kural — `CLAUDE.md`

Okuma kuralları **koşulludur, isteğe bağlı değildir**: "ilgiliyse oku" değil,
"tetikleyici oluştuysa oku". En kritik olanı şudur:

> Bir kod tabanında dosya değiştirmeden **ÖNCE** o alanın desen, araç ve görev
> dosyaları okunur.

Yazma kuralları izin sormaz: karar verildiği anda yazılır, sonra tek satır
bildirilir. Sorulan izin, alınmayan not demektir.

Bir de dürüstlük kuralı vardır: **bir okuma kuralı atlanırsa fark edildiği anda
söylenmek zorundadır.** Sistemin zayıf halkası budur ve gizlenirse ölçülemez.

### 3. Denetim — doğrulama betiği

`_araclar/dogrula.py` şunları tarar:

- Kırık wikilink, aynı adlı not, yetim not (hiçbir yerden linklenmemiş)
- Eksik frontmatter, bayat not
- **Gerekçesiz karar** — `**Neden:**` satırı olmayan karar girişi
- **Kanıtsız tamamlanmış görev**
- Aynı görev kimliğinin iki panoda kullanılması
- "Yapılıyor" bölümünde eşzamanlı görev üst sınırının aşılması
- Açılış dosyasının karakter tavanını aşması
- Araç tablosunda gerekçesi boş satır

**Betiğin göremediği:** semantik çelişki. Kırık linki bulur, *yalan söyleyen doğru
linki* bulamaz. Bu boşluk bilinçli olarak kabul edilir ve kurallarla kapatılır —
aşağıya bakınız.

---

## Kritik kurallar

Bunların her biri gerçek bir hatadan doğmuştur.

### Tek otorite

"Nerede kaldık" sorusunun cevabı **tek bir dosyadadır**. Oturum arşivleri o günün
kaydını tutar ama otorite değildir; çeliştiklerinde durum dosyası doğrudur.

Bu ayrım, iki dosyanın aynı soruya farklı cevap verdiği ve yanlış olanın
okunduğu bir olaydan sonra konmuştur.

### Gövde doğrudur, özet tablo türevdir

Uzun dosyalarda baştaki veya sondaki özet tablo, gövdeden **bağımsız bayatlar**.
Bir "cevap bekleyenler" tablosu beş soruyu açık gösterirken beşinin de cevabı aynı
dosyanın içinde durabilir — ve iki ayrı oturum bunları engel sanabilir.

Kural: çeliştiklerinde tabloyu gövdeye göre düzelt; bir soru cevaplandığında
tablo **aynı turda** düşürülür.

### Çıkarım, karar değildir

Claude'un doldurduğu boşluklar `*(çıkarım)*` etiketiyle işaretlenir ve kullanıcının
söyledikleriyle **aynı paragrafta karışmaz**. Karışırsa altı ay sonra hangisinin
kimden geldiği bilinmez.

Etiketli bir maddeye sonradan itiraz edilebilir — ama tek taraflı silinmez, gerekçe
kullanıcının önüne konur.

### Asla yazılmayacaklar

- Koddan okunabilen şeyler (klasör yapısı, kurulu paketler, dosya listesi)
- Git geçmişinde zaten bulunan bilgiler
- Tek oturumluk geçici detay

Bunlar kod değişince **yalan söyler**, ve yalan söyleyen bir not, notun hiç
olmamasından kötüdür.

---

## Aynı anda birden fazla oturum

Birden fazla Claude Code oturumu aynı projede paralel çalışabilir; birbirlerini
görebilir ve mesajlaşabilirler. Bu güçlüdür ama iki risk taşır.

**Çakışma.** İki oturum aynı dosyaya yazarsa biri diğerini sessizce siler. Çözüm:
yazma hakkının alanlara bölünmesi. Ölçüt **çalışma dizini değil, üzerinde
çalışılan alandır** — bir oturumun `pwd`'si, ne üzerinde çalıştığını göstermez.

Kapalı olan tek dosya genel durum dosyasıdır. Ortak dosyalarda (domain
gereksinimleri, görev panoları) kural şudur: **risk dosyada değil, aynı bölüme aynı
anda yazmaktadır.**

**Bayat okuma.** Başka bir oturum çalışırken okunan git durumu, dosya sayısı veya
"şu an ne yapılıyor" bilgisi **anında bayatlar**. Ölçüldüğü anda doğru olan, birkaç
saniye sonra yalan olabilir. Böyle bir bilgi vault'a yazılacaksa önce ilgili oturuma
sorulur.

Paralel oturumların beklenmedik faydası: **birbirlerinin hatalarını yakalarlar.**
Tek oturumda çalışan bir Claude'un yanlış kaydı vault'ta yalan olarak kalır;
üç oturumda ikisi diğerini düzeltir.

---

## Projeye özel skill'ler

Tekrar eden ve adımı atlanan işler skill haline getirilir. Örnek üçlü:

| Skill | Ne zaman |
|---|---|
| Not ekleme | Frontmatter, hub bağlantısı ve çıkan linki birlikte zorlar |
| Karar kaydı | Bir soru cevaplandığında güncellenmesi gereken dosyaları senkron tutar |
| Bitti denetimi | "Tamamlandı" demeden önceki ölçüm sırasını zorlar |

Skill yazma ölçütü nettir: **birden fazla kez yapılan ve en az bir kez yanlış
yapılmış** iş. Onun dışındaki skill, kullanılmayan skill'dir.

---

## Araç seçimi de kayda geçer

Her havuzun araç dosyası bir envanter değil **eşleme**dir: hangi durumda hangi
plugin, skill veya MCP kullanılacağı, **gerekçesiyle** yazılır.

Gerekçesiz bir araç satırı eklenmez — çünkü gerekçesi yazılmayan araç, kullanılmayan
araçtır. Aynı ölçüt yeni araç önerilerine de uygulanır:

> Bir araç ancak vault'un bilinen arıza modunu (atlanan adım, kanıtsız "bitti",
> senkronsuz dosya) **ölçülebilir şekilde azaltıyorsa** alınır. Ölçüt yeni yetenek
> değil, **yakalanan hata**dır.

---

## Vault'un kendisi neden sürüm kontrolünde

Vault'un varlık sebebi "hafıza kaybolmasın"dır; kendisi kaybolmaya açık olamaz.
Ama asıl sebep yedek değil **geri alma**: birden fazla oturum yazıyorsa, yanlış bir
yazma işlemi sürüm kontrolü olmadan telafi edilemez.

Kural: alan oturumları vault'a **yazar ama commit atmaz**; commit'i tek bir oturum
atar. Yoksa üç oturum aynı anda hepsini birden commit'ler ve birbirinin yarım işini
kayda geçirir.

---

## Sistem ne zaman gerçekten çalışıyor sayılır

Klasör düzeni kurmak kolaydır; sistem kurmak değil. Ölçüt şudur:

> **Sistem, en az bir kez gerçek bir hata yakalamış olmalı.**

Bu yüzden yakalanan hatalar sayılır ve kayda geçirilir. Örnekler:

- Bir ölçüm alındığı anda doğruydu, saniyeler sonra yalan oldu
- Bir dosya kendi kendisiyle çelişiyordu, iki oturum aynı yanlışa düştü
- Aynı kök neden **dört ayrı yerde** ayrı ayrı keşfedildi — desen dosyasında olsa
  ilkinde bitecekti
- Bir kural fazla katı kuruldu, aynı gün kırıldı ve gevşetildi

Sonuncusu en önemlisidir: **sistemin kendi kurallarını da yakalaması.** Kendi
kuralını denetlemeyen bir vault, dışarıdan gelen kurala körü körüne uyar — ve
klasör iskeletinden ibaret kalır.

Yakalanan hata kaydı boşsa, elinizde bir sistem değil bir klasör düzeni vardır.

---

## Parçalar

```
00-Index.md              tam dosya listesi ve rol haritası
CLAUDE.md                anayasa — okuma ve yazma kuralları
01-Genel/
  acilis.md              oturum açılışında otomatik yüklenen çekirdek
  durum.md               "nerede kaldık" — tek otorite
  <alan>-kararlar.md     append-only, gerekçe zorunlu
  <alan>-desenler.md     her dosyada uygulanan kurallar
  <alan>-gorevler.md     yapılacak / yapılıyor / bitti panosu
  <alan>-araclar.md      durum → araç eşlemesi
  notlar/                serbest biçim gözlemler, tuzaklar
02-.../ 03-.../          kod tabanı başına bir havuz, aynı altı bölme
04-Oturumlar/            günlük arşiv — otorite değil
_araclar/dogrula.py      doğrulayıcı
```

Hook betikleri Claude Code'un yapılandırma dizininde yaşar; proje düzeyinde
`settings.json` ile bağlanır, böylece küresel ayarlar kirletilmez.

---

## Kurulum

1. Bu yapıyı yeni projeye kopyala, içerikleri boşalt
2. `CLAUDE.md`'yi projenin klasör yerleşimine göre düzenle
3. Kod tabanı başına bir havuz aç, altı bölmeyi oluştur
4. `acilis.md`'yi yaz — tavanı aşma
5. Hook'ları proje düzeyinde bağla
6. İlk gerçek kararı verdiğinde yaz. Boş bir vault, olmayan bir vaulttur.

Kurmak bir saat sürer. Değerini görmek birkaç hafta — çünkü değeri, ilk yakaladığı
hatada ortaya çıkar.
