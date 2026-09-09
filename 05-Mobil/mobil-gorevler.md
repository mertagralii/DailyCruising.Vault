---
rol: gorev
kapsam: mobil
guncelleme: 2026-09-09
durum: guncel
---

# Mobil Görev Panosu

Kimlik öneki `M-`, numara geri kullanılmaz. **Yapılıyor'da aynı anda en fazla 3
görev.** Tamamlandı'ya taşımak `Kanıt:` satırı ister — kanıtsız görev tamamlanmış
sayılmaz.

⚠️ Aşağıdaki beş satır bu alan açılırken **iskeletten türetildi**, Mert'in verdiği
bir iş listesi değil. `M-02` (kapsam) kararı Mert'e bağlı; o netleşmeden
diğerleri anlamlı sırayla yapılamaz.

## 🔵 Yapılacak

- [ ] **M-02** Kapsam: mobil hangi işi yapacak · ⏸️ **BEKLEMEDE**
      Web'de 25 rota var. Mobil bunların tamamını mı taşıyacak, yalnız misafir
      akışını mı (arama → tekne → rezervasyon → biniş belgesi), yoksa işletme
      paneli de var mı?
      **Mert 2026-09-09'da erteledi:** önce API, sonra web bitecek; kapsam ondan
      sonra konuşulacak → [[mobil-kararlar]]
      **Tetikleyici tarih değil olay:** API ve Web panolarında Mert'e bağlı
      olmayan iş kalmadığında bu soru yeniden açılır
      Kabul: cevap [[mobil-kararlar]]'a gerekçesiyle yazılır; ekran listesi çıkar

- [ ] **M-03** Ölçüm yolu: mobilde "doğru göründü" nasıl kanıtlanır · öncelik: yüksek
      Bağımlı: yok — koddan önce kurulmalı
      Web'de kapı tarayıcı ölçümüydü; mobilde karşılığı yok. Simülatör mü, Expo Go
      ile cihaz mı, ekran görüntüsü karşılaştırması mı?
      Kabul: bir mobil değişiklik, kapatılmadan önce bu yolla ölçülür ve
      [[mobil-araclar]]'a tetikleyicisiyle yazılır

- [ ] **M-04** Klasör düzeni ve navigasyon kütüphanesi · öncelik: orta
      Bağımlı: M-02 · `src/` yok, navigasyon paketi yok. `expo-router` (dosya
      tabanlı, Web'deki App Router'a yakın) mı, `react-navigation` mı?
      Kabul: karar gerekçesiyle [[mobil-kararlar]]'a yazılır, iskelet kurulur,
      [[mobil-mimari]] güncellenir

- [ ] **M-05** API istemcisi ve oturum akışı · öncelik: orta
      Bağımlı: M-02, M-04 · Uçlar ve şemalar backend'de hazır (`openapi.json`).
      Tipler **üretilecek**, elle yazılmayacak → [[mobil-desenler]]
      Kabul: bir uç noktadan gerçek veri ekrana düşer; token saklama yeri
      [[mobil-kararlar]]'a yazılır

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

- [x] **M-06** Expo resmî Claude eklentisi kuruldu · bitti: 2026-09-09
      Kanıt: `DailyCruising/.claude/settings.json` → `expo@claude-plugins-official: true`;
      `~/.claude/settings.json` içinde **yok** (kurulum komutunun yazdığı satır geri
      alındı, yedeklendi) → yalnız bu projede etkin. 24 Expo skill'i kurulu

- [x] **M-01** Uzak repo açıldı · bitti: 2026-09-09
      Kanıt: `gh repo view mertagralii/DailyCruising.Mobil` → `visibility: PRIVATE`,
      `defaultBranchRef: main`; `git log origin/main` iki commit gösteriyor.
      Uzaktaki dosya listesinde `AGENTS.md`/`CLAUDE.md`/`.claude/` **yok**

- [x] **M-00** Vault'ta mobil alanı açıldı · bitti: 2026-09-08
      Kanıt: `05-Mobil/` altında altı bölme + hub, `_araclar/vault.json`'a alan
      eklendi, `python3 _araclar/dogrula.py` → TEMIZ

İlgili: [[mobil-durum]] · [[mobil-mimari]] · [[mobil-desenler]] · [[genel-gorevler]] · [[00-Index]]
