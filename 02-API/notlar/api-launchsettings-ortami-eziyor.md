---
rol: not
kapsam: api
guncelleme: 2026-08-26
durum: guncel
---

# `launchSettings.json` üretim kapısı testini sessizce çürütüyor

`Program.cs`'te üretime özel kapılar var: sahte ödeme sağlayıcısı, sandbox
adresi, boş `AllowedHosts`, eksik kimlik bilgileri. Bunların gerçekten
ateşlediğini ölçmek için `ASPNETCORE_ENVIRONMENT=Production` ile açmayı
denersin:

```bash
ASPNETCORE_ENVIRONMENT=Production Payments__Iyzico__BaseUrl="https://sandbox-..." \
  dotnet run --project DailyCruising.Api
```

**Uygulama sorunsuz açılır ve sen "kapı çalışmıyor" sanırsın.** Çalışıyor:
`dotnet run` `Properties/launchSettings.json`'daki profili uyguluyor ve o profil
`ASPNETCORE_ENVIRONMENT=Development` yazıyor — **ortam değişkenini eziyor.**

Doğrusu:

```bash
ASPNETCORE_ENVIRONMENT=Production ASPNETCORE_URLS=http://localhost:5399 \
  ... dotnet run --project DailyCruising.Api --no-build --no-launch-profile
```

`--no-launch-profile` olmadan yapılan her üretim denemesi **Development'ı
ölçer**. `ASPNETCORE_URLS` de elle verilmeli, çünkü adres de profilden geliyordu.

## Neden tehlikeli

Yanlış yön veriyor. "Kapı ateşlemedi" gözlemi seni kodda olmayan bir hatayı
aramaya gönderiyor; ya da daha kötüsü, kapıyı "çalışmıyor" diye kaldırıyorsun.

2026-08-26'da tam bunun eşiğine gelindi: `A-29`'da iki yeni üretim kapısı
yazıldı, commit mesajında "üretimde açılmıyor" diye **iddia edildi**, sonra
ölçüldüğünde üçü de açıldı. Kapılar doğruydu, ölçüm yanlıştı.

Aynı koşuda ikinci bir ölçüm hatası daha oldu: macOS'ta `timeout` komutu yok,
`timeout 40 dotnet run ... | grep` hiçbir şey çalıştırmadan boş çıktı verdi ve
bu boşluk "hata yok" gibi okunabilirdi. **Boş çıktı, geçti demek değildir.**

İlgili: [[api-eszamanlilik-testi-yarismayabilir]] · [[api-desenler]] · [[api-kararlar]]
