---
rol: gorev
kapsam: genel
guncelleme: 2026-08-24
durum: guncel
---

# Genel Görevler

İki repoyu birden ilgilendiren veya karar bekleyen işler. Kimlik öneki **`G-`**.

**Kurallar:** Yapılıyor'da en fazla 3 görev · Tamamlandı'ya taşımak `Kanıt:` satırı
ister. Biçim ve gerekçe -> [[genel-desenler]]

Karar bekleyenlerde "kimde" satırı vardır; **Mert'te olan işler Claude tarafından
tamamlanamaz.**

## 🔵 Yapılacak

- [ ] **G-15** Vault'un başka projelere taşınabilir şablona dönüştürülmesi
      Öncelik: bu proje kanıtlanınca · Kabul: boş bir projede kurulup çalışması,
      DailyCruising'e özgü içerik ile genel iskeletin ayrılmış olması
      Bağımlı: bu projede sistemin işe yaradığının kanıtlanması

- [ ] **G-12** Çevrimdışı biniş · kimde: **Mert**
      İskelede internet çekmezse QR doğrulama ne olacak? G-01'den arta kalan tek soru
- [ ] **G-13** Fatura modelinin mali müşavirle teyidi · kimde: **Mert**
      Aracılık modeli seçildi; teyit gelene kadar şema esnek kurulacak
- [ ] **G-03** Ödeme sağlayıcı kararı · kimde: **Mert**
      Mert henüz sanal POS seçmedi. **Şart: alt üye iş yeri (marketplace) desteği** —
      olmadan bölüştürme yapılamaz. Şema sağlayıcı-bağımsız kurulacak, bloke etmiyor
- [ ] **G-04** SMS sağlayıcı kararı · kimde: **Mert**
      Eski sistem Verimor; canlıda IP whitelist hatası veriyordu
- [ ] **G-06** Veri göçü kararı · kimde: **Mert**
      35 tekne, 104 kullanıcı, 120 rezervasyon, 46 blog taşınacak mı
- [ ] **G-07** Deploy, CI/CD ve ortam yönetimi
- [ ] **G-08** ECC Memory katmanının kalıp kalmayacağına karar verilmesi
      Kuruldu, kullanılmıyor. Başka harness planı yoksa kaldırılmalı -> [[genel-kararlar]]
- [ ] **G-10** `brand.ts` kurumsal verilerinin doğrulanması · kimde: **Mert**
      Telefon, e-posta, adres, TÜRSAB no tasarımdan geldi, yer tutucu

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

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
