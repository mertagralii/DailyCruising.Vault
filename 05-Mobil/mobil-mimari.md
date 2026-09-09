---
rol: map
kapsam: mobil
guncelleme: 2026-09-09
durum: guncel
---

# Mobil Mimari

`DailyCruising.Mobil/` — "ne var" sorusunun tek cevabı. **Yapıya dokunmadan önce
okunur, dokunduktan sonra yazılır** (yeni ekran, navigasyon, dış servis, paket).

⚠️ **Bugün burada anlatılacak yapı yok denecek kadar az** — iskelet 8 Eylül'de
kuruldu ve henüz tek ekran yazılmadı. Bu dosya boş görünüyorsa sebebi bu; kod
yazıldıkça buraya yazılır.

## Yığın (8 Eylül ölçümü, `package.json`)

| Ne | Sürüm |
|---|---|
| Expo | `~57.0.21` |
| React Native | `0.86.3` |
| React | `19.2.3` |
| TypeScript | `~6.0.3` |
| `expo-status-bar` | `~57.0.1` |

Başka bağımlılık **yok**: navigasyon, durum yönetimi, HTTP istemcisi, test
altyapısı, biçimlendirici — hiçbiri kurulu değil.

## Dosya düzeni

```
DailyCruising.Mobil/
  index.ts        # giris — registerRootComponent(App)
  App.tsx         # tek bilesen, Expo sablonunun varsayilan ekrani
  app.json        # Expo yapilandirmasi
  assets/         # ikonlar, splash
  tsconfig.json
```

`src/` klasörü **yok**; kaynak kökü şu an repo kökü. Klasör düzeni kararı
verilmedi → [[mobil-gorevler]] `M-04`.

## Expo yapılandırması (`app.json`)

- `name: DailyCruising` · `slug: dailycruising-mobil` · `version: 1.0.0`
- `orientation: portrait` · `userInterfaceStyle: light`
- iOS: `supportsTablet: true`
- Android: uyarlanabilir ikon üçlüsü (foreground/background/monochrome),
  `predictiveBackGestureEnabled: false`
- Web hedefi de açık (`favicon`) — Expo şablonunun varsayılanı, bilinçli bir
  karar değil

## Git

`mertagralii/DailyCruising.Mobil` (private, 9 Eylül 2026), dal `main`, `origin`
bağlı. Diğer iki repo ile aynı düzen → [[calisma-duzeni]].

**Repoda AI aracı dosyası yok.** Expo şablonu `AGENTS.md`, `CLAUDE.md` ve
`.claude/settings.json` ile geliyordu; üçü de düşürüldü ve `.gitignore`'a
yazıldı. Şablonun `AGENTS.md`'sindeki tek gerçek bilgi — *"Expo değişti, kod
yazmadan önce sürüme özel dokümanı oku"* — kaybolmadı, tetikleyici olarak
[[mobil-araclar]]'a taşındı. Aynı kural API ve Web repolarında da geçerli →
[[genel-kararlar]]

`.gitignore` ortam değişkeni kuralı Web ile hizalandı: `.env*` yok sayılır,
`!.env.example` muaf. Şablonda yalnız `.env*.local` yazıyordu — düz bir `.env`
içindeki anahtar fark edilmeden commit'lenirdi → [[web-env-gitignore-tuzagi]]

## Backend'e bağlanma

Henüz hiçbir bağ yok. API sözleşmesinin kanonik kaynağı mobil tarafında da
**backend'dir**: uç noktalar ve şemalar için [[api-mimari]] ve
`02-API/api-sema-guncel.md` okunur, mobil tarafta elle tip yazılmaz →
[[mobil-desenler]]

İlgili: [[mobil-kararlar]] · [[mobil-desenler]] · [[mobil-gorevler]] · [[mobil-araclar]] · [[mobil-durum]] · [[mobil-notlar]] · [[00-Index]]
