---
rol: not
kapsam: api
guncelleme: 2026-08-26
durum: guncel
---

# `mv` ile geri alınan mutasyon, eski DLL'i koşturuyor

Mutasyon testinde alışkanlık şu: dosyayı yedekle, boz, testi koş, geri al.

```bash
cp Dosya.cs Dosya.cs.bak
# ... boz, test koş ...
mv Dosya.cs.bak Dosya.cs      # ⚠️ TUZAK
```

`mv` yedeğin **değiştirilme zamanını korur** ve yedek, mutasyondan ÖNCE
alınmıştı. Yani geri alınan dosya, mutasyonla derlenmiş DLL'den **daha eski**
görünüyor; MSBuild "kaynak değişmemiş" deyip derlemeyi atlıyor ve test paketi
**hâlâ mutasyonlu ikiliyi** koşuyor.

Belirti kafa karıştırıcı: kaynak dosyada mutasyon yok, `grep` doğru satırı
gösteriyor, ama testler bozuk davranıyor.

## Doğrusu

`cp` kullan — hedef dosyanın zamanı **şimdi** olur:

```bash
cp Dosya.cs.bak Dosya.cs
```

`mv` kullandıysan zamanı tazele:

```bash
touch Dosya.cs
```

Emin olmak istiyorsan `dotnet test` yerine `dotnet build --no-incremental`.

## Neden tehlikeli

İki yönde de yalan söylüyor. 2026-08-26'da `A-41`'de mutasyon geri alındıktan
sonra dört test kırmızı kaldı ve bir an "kod bozuldu" sanıldı. Ters yönü daha
kötü: mutasyon uygulanırken de aynı şey olsaydı test **yeşil** kalır ve
"kural ölçülüyor" diye yanlış bir sonuç çıkarılırdı.

İlgili: [[api-eszamanlilik-testi-yarismayabilir]] · [[api-launchsettings-ortami-eziyor]] · [[api-desenler]]
