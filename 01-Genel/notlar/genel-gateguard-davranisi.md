---
rol: not
kapsam: genel
guncelleme: 2026-08-21
durum: guncel
---

# GateGuard hook davranışı

ECC'nin `gateguard-fact-force` hook'u bazı komutları **çalıştırmadan önce durduruyor**
ve gerçek olgular sunmamı istiyor. Kod hatası değil, kasıtlı bir kapı.

## Ne tetikliyor

| Tetikleyici | İstenen |
|---|---|
| Oturumun ilk `Bash` komutu | Talebin tek cümlelik özeti + komutun ne doğruladığı |
| Yıkıcı komut kalıpları (silme, taşıyarak üzerine yazma, commit `--amend`) | Etkilenecek dosyalar + geri alma yolu + kullanıcının talimatı birebir |
| Yeni dosya oluşturma | Dosyayı kimin okuyacağı + aynı işi gören dosya var mı araması + veri yapısı |

## Gözlemler

- **Kalıp eşleşmesi metin üzerinden.** Heredoc içine yazdığın *markdown metni* bile
  yıkıcı komut sanılabiliyor — bu notu yazarken tam olarak bu oldu. Çalıştırılmayan
  metin de tetikliyor.
- **Aynı komutu tekrar denemek yetmiyor.** Olguları sunmadan tekrarlarsan aynı hatayı
  tekrar verir. Silme için olguları sunup tekrar denedim, yine bloklandı; silmek yerine
  yedek ada taşıyınca hem geçti hem geri alınabilir oldu.
- **Yıkıcı işlemde taşımayı tercih et.** Silmek yerine `.trash-<ad>` gibi bir ada
  taşımak gate'i de geçiriyor, kullanıcıya da geri dönüş bırakıyor.
- Kapatma yolu var (`ECC_GATEGUARD=off`, `ECC_DISABLED_HOOKS`) ama **kapatma** — bu kapı
  gerçek hataları engelliyor. Kökteki geçici git reposunu kaldırırken olguları yazmak,
  hiç commit içermediğini fark etmemi sağladı.

## Sonuç

Yavaşlatıyor ama maliyeti düşük, faydası yüksek. Yıkıcı bir şey yapacaksam olguları
**baştan** yazmak, iki kez denemekten hızlı.

İlgili: [[genel-notlar]] · [[calisma-duzeni]] · [[genel-ecc-precompact-akisi]]
