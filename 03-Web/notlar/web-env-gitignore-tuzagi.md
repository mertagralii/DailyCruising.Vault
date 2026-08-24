---
rol: not
kapsam: web
guncelleme: 2026-08-21
durum: guncel
---

# `.env*` kuralı `.env.example`'ı yutuyor

`create-next-app`'in ürettiği `.gitignore` şu satırı içeriyor:

```
# env files (can opt-in for committing if needed)
.env*
```

Bu kalıp `.env.example` dosyasını **da** kapsıyor — yani paylaşılması gereken şablon
dosya sessizce repoya girmiyor. Fark edilmesi zor, çünkü hata vermiyor; dosya var,
`git status` göstermiyor.

## Çözüm

`.gitignore` sonuna istisna eklendi:

```
!.env.example
```

Sıra önemli: istisna, kapsayan kuralın **sonrasında** gelmeli.

## Doğrulama

```
git check-ignore -v .env.example   # cikti yoksa takip ediliyor demek
```

Bu kurulumda `.env.example` ilk commit'te yer aldı, `.env.local` yer almadı — doğru
davranış.

## Genel ders

Şablonların ürettiği `.gitignore` dosyalarını okumadan kabul etme. Geniş kalıplar
(`.env*`, `*.local`) paylaşılması gereken dosyaları da yutabilir.

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-create-next-app-tuzaklari]]
