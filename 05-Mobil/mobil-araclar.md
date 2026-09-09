---
rol: map
kapsam: mobil
guncelleme: 2026-09-09
durum: guncel
---

# Mobil Araçları

`DailyCruising.Mobil/` altında çalışırken **hangi durumda hangi aracı**
kullanacağım. Envanter değil **eşleme**: gerekçesiz araç satırı eklenmez —
gerekçesi olmayan araç kullanılmayan araçtır.

⚠️ **Aşağıdaki satırların hiçbiri bu projede mobil tarafta denenmedi.** Araçların
kurulu olduğu doğrulandı (8 Eylül), işe yaradıkları doğrulanmadı. Denendikçe
"Neden" sütunu ölçümle değiştirilecek.

| Tetikleyici | Araç | Neden |
|---|---|---|
| **Mobilde kod yazacağım — ilk satır dahil** | Expo 57 sürüm dokümanı: https://docs.expo.dev/versions/v57.0.0/ | Expo şablonunun kendi `AGENTS.md`'si tek bir şey söylüyordu: *"Expo HAS CHANGED — kod yazmadan önce sürüme özel dokümanı oku."* Dosya repodan düşürüldü, **uyarı burada yaşıyor** → [[mobil-kararlar]] |
| React Native bileşeni yazacağım/değiştireceğim | `Skill: ecc:react-native-patterns` | RN'e özgü desenler web React'ten ayrı: liste sanallaştırma, dokunma hedefleri, platform ayrımı. Kurulu (`ecc` marketplace) |
| `.tsx` dosyası değişti | `ecc:react-reviewer` + `ecc:typescript-reviewer` ajanları | Hook doğruluğu ve tip güvenliği platformdan bağımsız; ikisi de kurulu |
| Expo veya RN API'si soruldu | `context7` MCP | **Expo 57 ve RN 0.86 yeni sürümler**, eğitim verim bayat olabilir. Web tarafında aynı gerekçe Next 16 için tuttu |
| Tip hatası aranıyor | `npx tsc --noEmit` | Projede test ve lint yok; bugün tek otomatik kapı bu |
| Bağımlılık/SDK uyumu şüpheli | `npx expo-doctor` | Expo SDK sürüm çakışmalarını `npm install` sessizce geçirir |
| Uygulamayı ayağa kaldırmam gerekiyor | `npx expo start` (tmux içinde) | ECC `pre:bash:auto-tmux-dev` hook'u dev sunucularını tmux dışında engelliyor → [[web-araclar]] |
| Yeni bir ekran/akış sıfırdan tasarlanacak | `frontend-design` skill'i + tasarım kaynağı | Tasarım kararlarını rastgele vermemek için; web'de aynı yol izlendi |
| Uygulama ikonu/splash üretilecek | `Skill: ecc:ios-icon-gen` | `assets/` altında ikon üçlüsü Expo şablonundan geliyor, gerçek marka ikonu yok |

## Sırayla çalıştırılacaklar — bir ekran/bileşen yazıldığında

Sıra rastgele değil: her adım öncekinin kaçırdığını yakalar. API ve Web'de aynı
iskelet var → [[api-araclar]] · [[web-araclar]]

| Sıra | Ne | Ne zaman | Neden |
|---|---|---|---|
| 1 | Sürüm dokümanı + [[mobil-desenler]] | Koda dokunmadan önce | Expo 57 / RN 0.86 yeni; ezberden yazılan API sessizce eskimiş olur |
| 2 | `Skill: ecc:react-native-patterns` | Bileşen yazarken | RN'e özgü olan web React'te yok: liste sanallaştırma, dokunma hedefi, platform ayrımı |
| 3 | Kodun kendi yorumu | Yazdıktan hemen sonra | Gerekçe **kod satırının yanına** yazılır; vault'a yazılan gerekçe koddan uzaklaşır → [[genel-desenler]] |
| 4 | `npx tsc --noEmit` | Her değişiklikten sonra | Bugün tek otomatik kapı bu; lint ve test yok |
| 5 | `ecc:react-reviewer` + `ecc:typescript-reviewer` | `.tsx` değişen her işten sonra | Hook doğruluğu ve tip güvenliği derleyicinin görmediği sınıf |
| 6 | **Cihaz/simülatör ölçümü** | Review temiz çıkınca | ⚠️ **Bu adımın yolu henüz kurulmadı** → `M-03`. Kurulana kadar mobilde "çalışıyor" denemez |
| 7 | Commit + push | Ölçüm geçince | Mesaj İngilizce, gövdede **neden**; AI atfı yok → [[tercihler]] |

**6. adım eksik olduğu için bu zincir bugün tam değil.** Bunu yazmak, boşluğu
kapatmaz ama **görünür** yapar: kapısı olmayan adım atlanır ve atlandığı fark
edilmez → [[genel-desenler]]

## Expo'nun resmî Claude eklentisi — kurulu, yalnız bu projede

`expo@claude-plugins-official` (kaynağı `github.com/expo/skills`, Anthropic'in
resmî pazarı üzerinden) 9 Eylül'de kuruldu. Etkinliği **yalnız**
`DailyCruising/.claude/settings.json` içinde — `ui-ux-pro-max` ve `seo-butler`
gibi; küresel ayar kirletilmedi → [[mobil-kararlar]]

Getirdiği 24 skill, kabaca üç öbek:

| Öbek | Skill'ler | Ne zaman |
|---|---|---|
| Uygulama | `expo-router` · `expo-project-structure` · `expo-ui` · `expo-native-ui` · `expo-design-system` · `expo-animation` · `expo-data-fetching` · `expo-dom` | Ekran, navigasyon, klasör düzeni ve veri katmanı yazılırken — `M-04` ve `M-05`'in tam konusu |
| EAS (Expo'nun bulut servisi) | `eas-app-stores` · `eas-update` · `eas-workflows` · `eas-hosting` · `eas-observe` · `eas-simulator` | Yayına çıkarken; App Store / Play Store adımları burada |
| Bakım | `expo-upgrade` · `expo-module` · `expo-brownfield` · `expo-web-to-native` · `expo-examples` | SDK yükseltme, yerel modül, mevcut uygulamaya gömme |

⚠️ **Hiçbiri bu projede denenmedi** — mobil kod yazılmadan denenemez. Skill'in
varlığı işe yaradığının kanıtı değildir; ilk kullanımda hangisi neyi yakaladı,
buraya ölçümle yazılacak.

## Web'in ölçüm araçları burada **çalışmaz**

`chrome-devtools`, `playwright`, `claude-in-chrome` — üçü de tarayıcı ölçer.
Expo'nun web hedefi açık olduğu için bunlar *çalışıyormuş gibi* görünebilir, ama
web derlemesi iOS/Android derlemesi değildir: dokunma davranışı, güvenli alan,
klavye ve yerel bileşenler orada görünmez.

**Mobilde ölçümün yolu henüz kurulmadı** → [[mobil-gorevler]] `M-03`. Bu boşluk
bilerek yazıldı: kapısı olmayan adım atlanır, atlandığı da fark edilmez →
[[genel-desenler]]

## Alakasız olanlar — yanlışlıkla çağırmamak için

- `ecc:android-clean-architecture`, `ecc:kotlin-*`, `ecc:swift-*` — bunlar
  **yerel (native)** Android/iOS projeleri içindir; burada React Native var
- `DesignSync` yazma çağrıları — tasarım projesi Mert'in, oraya yazılmaz

İlgili: [[mobil-desenler]] · [[mobil-mimari]] · [[mobil-gorevler]] · [[genel-araclar]] · [[web-araclar]] · [[00-Index]]
