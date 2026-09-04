---
rol: gorev
kapsam: genel
guncelleme: 2026-08-31
durum: guncel
---

# Genel Görevler

İki repoyu birden ilgilendiren veya karar bekleyen işler. Kimlik öneki **`G-`**.

**Kurallar:** Yapılıyor'da en fazla 3 görev · Tamamlandı'ya taşımak `Kanıt:` satırı
ister. Biçim ve gerekçe -> [[genel-desenler]]

Karar bekleyenlerde "kimde" satırı vardır; **Mert'te olan işler Claude tarafından
tamamlanamaz.**

## 🔵 Yapılacak

- [ ] **G-16** SaaS / abonelik ürününe dönüştürme · öncelik: **EN SON**
      Mert: *"bu sistemi bir abonelik üzerinden satacağım"* — rezervasyon sistemi +
      AI entegrasyonları komple paket. **Şu anda buna göre hiçbir şey yapılmıyor.**
      Bugün hazırlık gerekmiyor: abone başına ayrı veritabanı yolu mevcut şemayla
      çalışır. Tek veritabanı + `TenantId` yolu seçilirse sonradan çok pahalı
      -> [[domain-gereksinimler]] 2026-08-24
      Bağımlı: bu sistemin canlıda çalıştığının kanıtlanması
- [ ] **G-15** Vault'un başka projelere taşınabilir şablona dönüştürülmesi
      Öncelik: bu proje kanıtlanınca · Kabul: boş bir projede kurulup çalışması,
      DailyCruising'e özgü içerik ile genel iskeletin ayrılmış olması
      Bağımlı: bu projede sistemin işe yaradığının kanıtlanması

      **Yakalanan hata defteri** — şablon ancak sistem gerçek hata yakaladıysa
      hak edilir. Yoksa şablon bir klasör düzenidir, sistem değil:
      1. Git durumu bayatlaması — vault oturumu "2 dosya commit'lenmemiş" yazdı,
         peer oturum saniyeler önce commit atmıştı
      2. `api-durum` çelişkisi — "domain modeli yok" yazıldı, backend o sırada
         şemanın 2. bölümünü onaylatıyordu
      3. `domain-gereksinimler` tablosu gövdesiyle çelişiyordu — 5 kapalı soru
         açık görünüyordu, iki oturum blocker sandı
      4. Geniş tablo kabı her ölçüde açık bırakıldı — kaydırma çubuğu masaüstü
         ölçümünü 18px'ten 55px'e çıkardı, bir saat kaybedildi
      5. Gövdenin sabit satır yüksekliği **dört ayrı yerde** aynı hatayı üretti;
         desen dosyasında olsa ilkinde biterdi
      6. Yazma hakkı kuralı fazla katı kuruldu — `01-Genel/*` tamamen kapalı
         ilan edilmişti, aynı gün pratikte kırıldı ve gevşetildi
      7. **Gerekçe ile uygulama ayrıştı** — `api-kararlar.md` "bölümlendirme
         yapılmadı, BRIN aynı işi görüyor" diyordu; `api-sema.md`'de saklama
         süresi kararının ertelenebilme gerekçesi ise **bölümlendirme sayesinde
         silmenin ucuz olması**ydı. BRIN sorgu hızını çözer, silme maliyetini
         çözmez. `database-reviewer` ajanı yakaladı (araç zincirinin 7. adımı),
         `A-11` görevi açıldı
      8. **Aynı çelişkinin üçüncü kopyası ilk düzeltmede kaçtı** — üç dosyada üç
         farklı terimle (`bölümlendirme` · `DROP` · `saklama süresi`) yazılmıştı,
         `grep` hiçbirini diğerine bağlamıyordu. Üçüncüsü özelliği **olmuş gibi**
         anlatıyordu. Yakalanma sebebi denetimin çift yön kurmaya zorlaması —
         kural doğrudan değil, **baktırarak** yakalattı
      9. **Panodan beş görev sessizce silindi** — "A-09'dan A-07'ye kadar sil"
         denmişti, panodaki gerçek sıra yüzünden aralık altı görevi kapsadı.
         `dogrula.py` **TEMİZ dedi**: biçim bozulmamış, link kırılmamıştı —
         *yazılı olan doğruydu, yazılmamış olan kayıptı.* Aynı oturumda verilen
         "A-09 tamamlandı" bildirimi de doğruydu; yanlış olan görünmeyen yan
         etkisiydi. Vault bir gün önce git'e alınmasaydı **kalıcı kayıptı**

- [ ] **G-13** Fatura modelinin mali müşavirle teyidi · kimde: **Mert**
      Aracılık modeli seçildi; teyit gelene kadar şema esnek kurulacak
- [ ] **G-07** Deploy, CI/CD ve ortam yönetimi
- [ ] **G-08** ECC Memory katmanının kalıp kalmayacağına karar verilmesi
      Kuruldu, kullanılmıyor. Başka harness planı yoksa kaldırılmalı -> [[genel-kararlar]]
- [ ] **G-10** `brand.ts` kurumsal verilerinin doğrulanması · kimde: **Mert**
      Telefon, e-posta, adres, TÜRSAB no tasarımdan geldi, yer tutucu

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

- [x] **G-03** Ödeme sağlayıcı kararı · **CEVAPLANDI** 2026-08-25
      Mert: **İyzico** — *"ama sonrasında bunu değiştirebilirim, ona göre bir yapı
      kuralım; Paratika, Param, PayTR veya benzeri sanal postlarla da çalışabilirim."*
      Kanıt: şema zaten sağlayıcı-bağımsız — `Payments.Provider` ·
      `ProviderTransactionId` · `RawResponse (jsonb)` · `IdempotencyKey` (benzersiz)
      ⚠️ Uygulama `A-29` olarak API panosunda; iki tuzak orada yazılı (eski
      ödemelerin iadesi eski sağlayıcıdan geçmek zorunda, ve pazaryeri
      bölüştürme semantiği sağlayıcılar arasında AYNI DEĞİL)

- [x] **G-04** E-posta ve SMS sağlayıcı kararı · **CEVAPLANDI** 2026-08-25
      Mert: e-posta **Postmark**, SMS **Netgsm**, yerel test **Mailpit**
      Verimor önerilmedi ve seçilmedi — eski sistemde canlıda IP whitelist
      hatası veriyordu
      Kanıt: Mailpit (Docker) ayakta, rezervasyon onayı gerçekten yakalandı —
      `musteri@ornek.com | Rezervasyonunuz alındı — Y4YABQ7N`
      Kanıt: SMS gövdesi de üretiliyor (geliştirmede günlüğe)
      ⚠️ Netgsm gönderici başlığı operatörden ÖNCEDEN onaylı olmalı, onay
      birkaç gün sürüyor — canlıya çıkmadan başlatılmalı
      ⚠️ Postmark'ta `FromEmail` DOĞRULANMIŞ olmak zorunda

- [x] **G-06** Veri göçü kararı · bitti: 2026-08-24
      Kanıt: Mert *"sıfırdan kuruyoruz zaten"* — göç YOK, dönüştürme betiği
      yazılmayacak. Bedelleri (35 işletme yeniden kayıt, puanlar sıfırlanır, eski
      URL'ler kırılır) bilinerek kabul edildi -> [[domain-gereksinimler]] 2026-08-24

- [x] **G-12** Çevrimdışı biniş kararı · bitti: 2026-08-24
      Kanıt: Mert **c** seçti — internet yoksa tekne sahibi sonradan panelden
      işaretler, `BoardingScans.Method = Manuel`. Çevrimdışı kuyruk (a) gelecek
      sürümde, mobil uygulamayla. Karar -> [[domain-gereksinimler]] 2026-08-24,
      şema -> [[api-sema]] bölüm 5

- [x] **G-14** Vault'un yedeklenmesi · bitti: 2026-08-24
      Kanıt: `mertagralii/DailyCruising.Vault` (private) oluşturuldu ve push edildi ·
      117 dosya, commit `db57a77` · `git status` origin/main ile eşit ·
      `.obsidian/workspace.json`, `graph.json` ve `.claude` symlink'i `.gitignore`'da

- [x] **G-01** Domain görüşmesi: iş kurallarının tamamının netleştirilmesi · bitti: 2026-08-24
      Kanıt: [[domain-gereksinimler]] 60+ karar, her biri gerekçeli · DÖNÜLECEK
      listesinin 5 maddesi de kapandı (D1–D5) · şemayı bloke eden madde kalmadı
      Arta kalan tek soru çevrimdışı biniş -> G-12
- [x] **G-02** Kimlik verisi (TCKN/adres) toplama amacı · bitti: 2026-08-24
      Kanıt: **aracılık** fatura modeli seçildi -> platform müşteriye fatura kesmiyor
      -> TC kimlik ve adrese ihtiyaç yok. Kimlik verisi yalnız teknenin "yolcu
      listesi ister" anahtarı açıkken, yolcu başına toplanacak. KVKK itirazı düştü
- [x] **G-05** i18n yöntemi · bitti: 2026-08-23
      Kanıt: ayrı **çeviri tabloları** (alan çifti değil). Diller TR/EN/DE/RU.
      Özellik ertelendi ama şema baştan kurulacak; AI ile otomatik çeviri planlı

- [x] **G-09** Context havuzu yeniden düzeni · bitti: 2026-08-24
      Kanıt: `dogrula.py` TEMIZ (42 not) · `acilis.md` 3.356/6.000 karakter ·
      6 yeni denetimin 6'sı kopya vault'ta bozularak sınandı, hepsi hata verdi ·
      `Stop` hook'u kusurlu dökümde uyardı, kurala uyan dökümde sustu ·
      `SessionStart` hook'u `acilis.md`'yi enjekte etti

- [x] **G-00** Obsidian vault tabanlı context hafızasının kurulması · bitti: 2026-08-21
      Kanıt: `python3 _araclar/dogrula.py` -> TEMIZ, 32 not, kırık link yok
- [x] **G-11** İki private repo oluşturulup push edilmesi · bitti: 2026-08-21
      Kanıt: `mertagralii/DailyCruising.API` ve `mertagralii/DailyCruising.Web`

İlgili: [[genel-desenler]] · [[genel-kararlar]] · [[durum]] · [[domain-gereksinimler]] · [[genel-notlar]]
