---
rol: not
kapsam: web
guncelleme: 2026-08-28
durum: guncel
---

# Sunucu bileşeni render'ında çerez yazılamaz

2026-08-28'de her sayfa `500` vermeye başladı:

    Error: Cookies can only be modified in a Server Action or Route Handler.
      at sessionSil (src/lib/auth/session.ts)
      at async erisimJetonu → kimlik → oturumKullanicisi

**Sebep:** `erisimJetonu()` süresi dolmuş jetonu yeniliyor ve sonucu çereze
yazıyordu. Kök yerleşim onu render sırasında çağırıyor. Next'te
`cookies().set()` **yalnız** Server Action, Route Handler ve `proxy.ts` içinde
çalışır.

## Neden geç fark edildi

Hata **yalnız erişim jetonu ölünce** çıkıyor — yani girişten **15 dakika
sonra**. İlk 15 dakikada her şey çalışıyor. Geliştirme sırasında oturum hep
tazeydi; hata ancak bir oturum bekletilip geri dönülünce göründü.

Bu, "çalışıyor" ile "doğru" arasındaki farkın örneği: kod ilk 15 dakika
kusursuz çalışıyordu ve **her kullanıcıyı 16. dakikada 500'e düşürecekti.**

## Kural

- `erisimJetonu(yazabilir)` **varsayılan `false`**. Yenileme yalnız çerez
  yazabilen yerlerde denenir
- Rota işleyicileri `yazabilir: true` geçer
- Sayfa gezinmelerinde yenilemeyi **`proxy.ts` yapar**

## İkinci tuzak: yenileme bir istek geç kalıyor

Proxy jetonu **yanıta** yazar; aynı isteğin sunucu bileşenleri hâlâ **eski**
çerezi görür. Yani yenilemenin olduğu istekte sayfa oturumsuz render edilir ve
kullanıcı bir kez boş ya da 404 ekran görür — ikinci istekte düzelir.

Çözüm: `NextResponse.next({ request: { headers } })` ile `cookie` başlığını
**isteğe de** yazmak. Ölçüldü: `dc_at` silinip istek atıldığında sayfa aynı
render'da 200 ve gerçek veriyle döndü.

## Yenileme neden proxy'de, her yerde değil

Aynı yenileme jetonunu iki kez göndermek backend'de **oturum zincirini
kapatıyor**. Bu yüzden yenileme yalnız `sec-fetch-dest: document`
gezinmelerinde yapılıyor — belge istekleri kullanıcı tarafından sıralanır,
paralel veri istekleri bu yoldan geçmez.

İlgili: [[web-notlar]] · [[web-hiz-siniri-yoklamasi]] · [[web-kararlar]]
