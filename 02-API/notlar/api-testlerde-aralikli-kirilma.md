---
rol: not
kapsam: api
guncelleme: 2026-09-08
durum: guncel
---

# "Aralıklı" sandığım kırılma aslında kesindi

⚠️ **Bu notun ilk hâli yanlıştı ve ders o yanlışta.**

2026-09-08'de `dotnet test` bir kez `701/702` verdi, ardından dört tur üst
üste geçti. "Aralıklı kırılma, tekrar üretilemedi" diye yazdım ve
`dogrulanmali` etiketledim.

**Kırılma aralıklı değildi. Kesindi ve sebebi benim komutumdu:**

```bash
dotnet test && bash araclar/openapi-uret.sh
```

Yeni bir uç eklemiştim. `Every_controller_action_appears_in_the_document`
testi `openapi.json`'ı koddaki eylemlerle karşılaştırıyor ve belge henüz
üretilmediği için haklı olarak kırıldı. Sonra **aynı komutun ikinci yarısı
belgeyi üretti** — yani kusuru ben, ölçtükten hemen sonra, farkında olmadan
düzelttim. Sonraki turlar bu yüzden yeşildi.

**Ders: "tekrar üretemedim" ile "tekrar üretmeyi denerken düzelttim" farklı
şeyler.** İkincisi birincisi gibi görünür ve daha tehlikelidir, çünkü kusuru
"anlaşılmaz" diye kaydeder ve bir sonraki görülüşünde de öyle sayılmasına
zemin hazırlar.

**İşe yarayan yöntem** (ilk notta yazmıştım, sonra kendim uyguladım):

```bash
dotnet test --logger "trx;LogFileName=/tmp/tam.trx"
```

Konsol çıktısı test adını vermiyor, `trx` veriyor. Üç turda üçünde de aynı
adı verdi — kesin olduğunun kanıtı da bu oldu.

**Kural:** uç eklendiğinde `openapi.json` yeniden üretilmeden takım
çalıştırılmaz. Test doğru çalışıyor; kırılması bir kusur değil, eksik adımın
bildirimi.

İlgili: [[api-notlar]] · [[api-launchsettings-ortami-eziyor]]
