---
rol: map
kapsam: genel
guncelleme: 2026-08-24
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
