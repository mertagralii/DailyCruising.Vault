---
rol: not
kapsam: api
guncelleme: 2026-09-11
durum: guncel
---

# Çalışan API: ayakta olması yetmiyor, SÜRÜMÜ de ölçülmeli

## Ne oldu

Web sabaha karşı bildirdi: `:5163` **kapalıydı**, panel her ekranda hata
verecekti. Ölçüm:

    lsof -iTCP:5163 -sTCP:LISTEN   → boş
    curl localhost:5163/api/health → 000

Sebep bendim. Belgeyi üretmek için gün içinde **altı kez** şu kalıbı koştum:

    pkill -f "DailyCruising.Api"; sleep 2; ./araclar/openapi-uret.sh

Beş kerede elle yeniden başlattım, altıncıda unuttum.

## ⚠️ Ve `pkill` hiç gerekli değildi

Bu notun **ilk hâlinde** şöyle yazmıştım: *"Betik kendi örneğini `:5199`'da
açıyor; `:5163`'te çalışan örnek dosya kilidini ve derleme çıktısını tuttuğu
için önce onu düşürmek gerekiyor. Yani `pkill` bir tercih değil, betiğin ön
koşulu."*

**Ölçmeden yazmıştım. Ölçtüm, yanlıştı:**

    curl :5163/api/health   → 200      (API ayakta)
    ./araclar/openapi-uret.sh          → uç sayısı: 166, yazıldı
    curl :5163/api/health   → 200      (hâlâ ayakta)

Betik `:5163`'e **hiç dokunmuyor**. Kendi örneğini `:5199`'da açıyor ve
`trap 'kill $PID' EXIT` ile yalnız onu kapatıyor (satır 39). `pkill`'i ben
uydurdum, sonra uydurduğum şeyi bu dosyaya **gerekçesiyle birlikte** kural
diye yazdım.

## Doğru kullanım

    ./araclar/openapi-uret.sh

Hepsi bu. Çalışan API'ye dokunmaya gerek yok; öldürmeye de.

## Neden kimse fark etmedi

⚠️ **Testler ve denetimler API'nin ayakta olmasını gerektirmiyor.**
`dotnet test` Testcontainers kullanıyor, `dogrula.py` dosyalara bakıyor,
`sema-cikar.py` doğrudan veritabanına bağlanıyor. Yani *"her şey yeşil"*
derken **yeşil olan hiçbir şey API'nin ayakta olduğunu ölçmüyordu.**

Web aynı şeyi kendi tarafında bildirdi: `build`, `lint`, `tsc` ve üç ölçüm
betiği — hiçbiri sunucuya bakmıyor.

## Asıl ders

Bu not, kendi konusunun örneği oldu. Bir varsayımı *"ön koşul"* diye yazmak,
onu belgeleyerek **kalıcılaştırıyor**: sonraki okuyan artık ölçmez, çünkü
yazılı. Yanlış bir kural, kuralsızlıktan pahalıdır.

⚠️ Kontrol edilebilir hâli: bir nota *"şunu yapmak zorunludur"* yazarken,
**yapmadan** ne olduğunu bir kez denemiş olmak. Burada tek bir koşu yeterdi.

İlgili: [[api-notlar]] · [[api-mutasyon-geri-alma]]

---

## İkinci kez: ayakta ama ESKİ

Aynı gün, birkaç saat sonra aynı sınıftan ikinci kusur. API bu kez
**ayaktaydı** (`/api/health` → 200) ama süreç `regionId` commit'inden
**eskiydi**. Sonuç: panelde on bölgenin onu da "0 tekne" gösterdi, sekiz
tekne varken.

    çalışan süreç : 09:12:05
    regionId      : 09:20:21   ← sonra

⚠️ **`curl /api/health` bunu göremez.** Sağlık ucu sürümü bilmiyor; eski bir
sürüm için de 200 döner. Yani "API ayakta" ölçümü, "doğru API ayakta"
sorusunu cevaplamıyor — ilk vakadaki dersin bir adım incelmiş hâli.

Yine web tarayıcıda buldu, yine ben fark etmedim, yine sebebi aynıydı: hiçbir
denetimim çalışan sürece bakmıyor.

**Ölçüm artık var:** `araclar/api-guncel-mi.sh` — çalışan sürecin başlangıcını
son commit'in zamanıyla karşılaştırıyor, son satırı `GUNCEL=1` ya da
`GUNCEL=0` basıyor ve eskiyse yeniden başlatma komutunu yazıyor.

⚠️ Kod değiştiren her turun sonunda koşulmalı; `dotnet test` yeşil olması
çalışan sürecin o kodu taşıdığını **söylemiyor.**
