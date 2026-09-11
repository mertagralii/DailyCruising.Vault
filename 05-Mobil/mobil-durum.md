---
rol: status
kapsam: mobil
guncelleme: 2026-09-10
durum: guncel
---

# Mobil Durumu

> **Bu dosyanın sahibi `DailyCruising.Mobil/` içinde çalışan oturumdur.**
> Mobil tarafın güncel durumu buraya yazılır, `01-Genel/durum.md`'ye **yazılmaz**.
> Genel resmi vault oturumu derler → [[durum]]

## ➡️ Şu an nerede duruyoruz

**9 Eylül 2026:** Expo iskeleti kuruldu, vault'ta alan açıldı, private repo
açılıp push'landı. **Uygulama kodu yok** — `App.tsx` hâlâ şablonun varsayılan
ekranı. Bu satır, mobil tarafta iş
yapan ilk oturumun yazacağı ilk şeyle değişmeli.

**10 Eylül 2026 — dışarıdan gelen kısıt, mobil etkilenmedi.** Backend iptal
sözleşmesini değiştirdi (`reason` zorunlu). Mobilde iptal ekranı olmadığı için
kırılan bir şey yok; kısıt kaybolmasın diye
[[mobil-iptal-ucu-reason-zorunlu]]'ya yazıldı ve `M-05`'e okuma tetikleyicisi
bağlandı. **Kod değişmedi.**

| Ne | Durum |
|---|---|
| İskelet | Expo SDK 57 · RN 0.86 · TS 6 → [[mobil-mimari]] |
| Ekran | 0 |
| Navigasyon | seçilmedi (`M-04`) |
| API bağlantısı | yok (`M-05`) |
| Test / lint | yok |
| Uzak repo | `mertagralii/DailyCruising.Mobil` (private, 9 Eylül) |
| Ölçüm yolu | **yok** (`M-03`) — mobilde "doğru göründü" bugün kanıtlanamaz |

## ⛔ Mert'te bekleyen

- **Kapsam:** ⏸️ **2026-09-09'da ertelendi.** Mert: önce API, sonra web
  bitecek; kapsam ondan sonra konuşulacak. Tetikleyici tarih değil olay —
  iki panoda da Mert'e bağlı olmayan iş kalmaması → `M-02` · [[mobil-kararlar]]
- **Expo yönetilen akışta kalınacak mı?** İskeletin gerekçesi sorulmadı;
  yerel bildirim, harita veya ödeme SDK'sı gerektiğinde bağlayıcı olur →
  [[mobil-kararlar]]

**Bu bekleyiş bilinçlidir.** Kapsam cevaplanmadan yazılacak mobil kod, atılacak
koddur; `M-04` (klasör düzeni, navigasyon) ve `M-05` (API istemcisi) kapsamdan
türüyor. Mobil tarafta bugün yapılacak doğru iş **hiçbir şey yapmamaktır**.

## ⚠️ Bilinen boşluk — denetim burayı henüz ölçmüyor

`dogrula.py` bu alanı diğerleriyle aynı kurallara tabi tutuyor (bayatlık,
tetikleyici, kanıtsız görev). Ama **kontrol 15** mimari dosyasının kod gerisinde
kalmasını git geçmişinden ölçer; mobil repoda tek commit var, yani bugün ölçüm
anlamlı bir şey söylemiyor. İlk gerçek commit'lerden sonra anlam kazanır.

İlgili: [[mobil-mimari]] · [[mobil-gorevler]] · [[mobil-kararlar]] · [[durum]] · [[00-Index]]
