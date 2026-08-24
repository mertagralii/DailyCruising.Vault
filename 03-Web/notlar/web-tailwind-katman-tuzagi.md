---
rol: not
kapsam: web
guncelleme: 2026-08-21
durum: guncel
---

# Tailwind v4 katman tuzağı: katmansız CSS sınıfları ezer

`globals.css` içine yazdığım `a { color: var(--text-action) }` kuralı, bileşenlerdeki
`text-white/[.72]` gibi Tailwind sınıflarını **geçersiz kılıyordu**. Footer bağlantıları
beyaz yerine pembe çıktı, koyu zemindeki "Kayıt ol" butonunun yazısı okunmaz oldu.

## Sebep

`@import "tailwindcss"` yardımcı sınıfları `@layer utilities` içine koyar.
CSS kaskadında **katmansız (unlayered) kurallar, katmanlı olanları yener** —
seçici özgüllüğünden bağımsız olarak. Yani element seçicili sade bir `a { }` kuralı,
class seçicili bir Tailwind yardımcısını eziyor.

## Çözüm

Temel stiller `@layer base` içine alındı:

```css
@layer base {
  a { color: var(--text-action); text-decoration: none; }
}
```

## Ders

Tailwind v4'te `globals.css`'e yazılan **her** element seviyesi stil `@layer base`
içinde olmalı. Katman dışında bırakılan bir kural, sonradan yazılan hiçbir yardımcı
sınıfla düzeltilemez — `!important` istemeye başlarsan bu tuzağa düşmüşsündür.

**Nasıl yakalandı:** derleme ve lint temiz geçti, hata yalnızca tarayıcıda
görüldü. Görsel doğrulama olmasaydı fark edilmezdi.

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-env-gitignore-tuzagi]]
