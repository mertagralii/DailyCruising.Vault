---
rol: not
kapsam: genel
guncelleme: 2026-08-21
durum: guncel
---

# ECC PreCompact akışı ve bizim hook'umuz

`/compact` anında iki hook çalışıyor. Kim ne yapıyor — canlı testte gözlemlendi.

## Zincir

```
/compact
  ├─ ECC pre-compact.js      LLM özeti üretir
  │                          ~/.claude/session-data/<ad>-session.tmp içine
  │                          ECC:SUMMARY:START / END işaretleri arasına yazar
  └─ vault-precompact.js     o özeti bulup 04-Oturumlar/<bugün>.md'ye kopyalar
     (bizim)                 bulamazsa işaretleyici satır yazar
```

## Gözlemler

- **Oturum dosyası worktree ile eşleştiriliyor.** `session-data/` tüm projeler için
  ortak; en yeni `.tmp` başka bir projeye ait olabilir. ECC bunu `**Worktree:**`
  başlığıyla çözüyor, bizim hook da aynı yöntemi kullanıyor. Canlı testte doğru
  dosyayı buldu.
- **Sıra garanti değil.** Bizimki önce çalışırsa özet henüz yazılmamış olur. Bu yüzden
  hook her hâlükârda bir satır yazıyor, özeti best-effort kopyalıyor.
- **ECC özetinin kalitesi sınırlı** — kullanıcı mesajlarını kırpılmış halde listeliyor,
  gerekçeleri taşımıyor.

## Sonuç

Compact öncesi kritik bilgi **hook'a bırakılmamalı.** Karar netleştiği anda
`*-kararlar.md`'ye yazmak asıl güvence; hook yalnızca emniyet ağı.

İlgili: [[genel-notlar]] · [[genel-kararlar]] · [[genel-gateguard-davranisi]]
