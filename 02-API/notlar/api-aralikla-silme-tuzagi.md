---
rol: not
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# Aralıkla silme tuzağı — beş görevi sessizce sildim

2026-08-24'te `api-gorevler.md`'den **`A-03`, `A-04`, `A-05`, `A-06`, `A-08`
görevlerini sildim ve fark etmedim.** Saatler sonra `A-03`'e geçmek isteyip
panoda bulamayınca ortaya çıktı.

## Ne yaptım

`A-09`'u Tamamlandı'ya taşırken:

```python
start = s.index("- [ ] **A-09**")
end   = s.index("- [ ] **A-07**")
s = s[:start] + s[end:]
```

Niyetim "A-09 bloğunu kaldır"dı. Panodaki gerçek sıra şuydu:

    A-09, A-03, A-04, A-05, A-06, A-08, A-07

Yani "A-09'dan A-07'ye kadar" **altı görevi** kapsıyordu.

## Neden hiçbir kontrol yakalamadı

- `dogrula.py` **temiz** dedi — biçim bozulmadı, link kırılmadı, frontmatter
  yerindeydi. Yalnız içerik yok oldu.
- Görev sayısını izleyen bir kontrol yok.
- Aynı oturumda `Kanıt:` satırı yazıp "A-09 tamamlandı" diye bildirdim; bildirim
  doğruydu, yan etkisi görünmezdi.
- Vault o sırada git'e alınmıştı, bu yüzden **geri getirilebildi**. Bir gün önce
  olsaydı kalıcı kayıptı.

## Kural

**Metinde "A'dan B'ye kadar sil" yazma.** İki sınır arasında ne olduğunu
varsayıyorsun; dosya değişince varsayım sessizce yanlış oluyor.

Bunun yerine **kaldırılacak bloğun tamamını birebir yaz ve değiştirerek kaldır** —
metin birebir eşleşmezse Python durur, yani yanlış şey silinemez:

```python
old = "- [ ] **A-09** ...tam metin...\n"
assert old in s          # eslesmezse durur
s = s.replace(old, "")
```

`index` ile aralık almak yalnız sınırların **bitişik olduğu kesinse** güvenli.

## Daha genel olan

Bu yalnız bir kod hatası değil: **silmenin doğruluğu, silinenin görünürlüğüne
bağlı.** Ekleme hatası göze çarpar (fazladan satır), silme hatası görünmez
(eksik satır). Bu yüzden silme her zaman daha dikkatli bir işlem ve tercihen
geri alınabilir bir yerde yapılmalı.

Vault'un sürüm kontrolüne alınmış olması bu olayı kurtardı → [[api-durum]].

İlgili: [[api-gorevler]] · [[api-notlar]] · [[api-durum]]
