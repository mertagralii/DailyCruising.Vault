---
rol: not
kapsam: web
guncelleme: 2026-08-21
durum: guncel
---

# `create-next-app` tuzakları (Next.js 16)

## Dizin adı npm paket adı olur

Hedef dizinin adı doğrudan `package.json` → `name` alanına gidiyor ve npm kurallarına
uymak zorunda: **büyük harf kabul edilmiyor.** `DailyCruising.Front-End` bu yüzden
reddedildi.

Çözüm: geçici dizinde geçerli bir adla (`daily-cruising-web`) oluşturup içeriği hedef
klasöre taşımak. Gizli dosyalar unutulmasın:

```
mv "$SRC"/* "$SRC"/.[!.]* "$DEST"/
```

Karar olarak kayıtlı → [[web-kararlar]]

## Bayraklar sürüme göre değişiyor

Next.js 16'nın `create-next-app`'inde:

- `--turbopack` bayrağı **yok** (Turbopack artık varsayılan)
- `--disable-git` var (eski sürümlerdeki `--no-git` değil)
- `--rspack`, `--biome`, `--react-compiler`, `--api`, `--empty` mevcut
- `--agents-md` **varsayılan açık** → `AGENTS.md` üretir

Bayrakları ezberden yazma; `create-next-app@latest --help` ile doğrula.

## AI dosyaları varsayılan geliyor

`CLAUDE.md` ve `AGENTS.md` istenmese de üretiliyor. Repoya girmemeleri gerek →
ilk commit'ten önce silinmeli. Bu kurulumda silindi → [[durum]] delete-zone.

İlgili: [[web-notlar]] · [[web-kararlar]] · [[web-env-gitignore-tuzagi]]
