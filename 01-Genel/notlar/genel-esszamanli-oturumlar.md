---
rol: not
kapsam: genel
guncelleme: 2026-08-24
durum: guncel
---

# Eşzamanlı Claude oturumları — gözlenen davranış

2026-08-24'te üç oturum aynı anda açıktı. `ListAgents` ile birbirlerini görüyor,
`SendMessage` ile konuşabiliyorlar. Bir test yapıldı; dört şey öğrenildi.

## 1. `SessionStart` hook'u yalnız yeni oturumda çalışır

Test edilen oturum hook kurulmadan **önce** başlamıştı; `acilis.md` içeriği o
oturumun bağlamına **hiç girmedi**. Oturum ortasında hook kurmak açık oturumları
ısıtmıyor.

**Sonuç:** hook ya da `acilis.md` değiştirildiğinde, etkisini görmek için o
oturumların yeniden açılması gerekir. Açık oturumlar eski açılış katmanıyla
çalışmaya devam eder ve bunu fark etmez.

## 2. `CLAUDE.md` değişikliği açık oturuma düşer

Açılış katmanının aksine, `CLAUDE.md` diskte değiştiğinde çalışan oturuma
`system-reminder` olarak iletiliyor. Yani **kurallar yayılıyor, açılış katmanı
yayılmıyor.** Acil bir kural değişikliği `CLAUDE.md`'ye yazılırsa hemen etki eder.

## 3. `pwd` oturumun alanını göstermez

Frontend işi yapan oturumun çalışma dizini `DailyCruising.Vault` çıktı. Yazma
hakkı ayrımı bu yüzden klasöre değil **işin alanına** bağlandı → [[durum]]

## 4. Başka oturum çalışıyorken okunan durum anında bayatlar

Front-End'de `git status` okundu: 2 dosya değişik, son commit `2777132`. Aynı
dakikalarda peer oturum commit attı; gerçek son commit `eb40c7e` ve ağaç temiz
oldu. **Ölçüm yanlış değildi, sadece bir saniye sonra yalan oldu.**

Bu, vault'un temel arıza modunun yeni bir biçimi: kanıt toplandığı anda doğruydu.

**Kural:** başka oturum açıkken git durumu, dosya sayısı ve "şu an ne yapılıyor"
bilgisi vault'a yazılmaz. Yazılacaksa önce `SendMessage` ile o oturuma sorulur —
o kendi durumunu bilir, ben tahmin ederim.

## Çakışma riski

Üç oturum aynı dosyaya yazarsa biri diğerini sessizce siler ve vault git reposu
olmadığı için geri alınamaz. Yazma hakkı ayrımı bunun içindir → [[genel-kararlar]]

İlgili: [[durum]] · [[genel-notlar]] · [[genel-araclar]]
