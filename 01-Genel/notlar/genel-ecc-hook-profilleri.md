---
rol: not
kapsam: genel
guncelleme: 2026-08-24
durum: guncel
---

# ECC hook'ları — profiller ve kapatma anahtarları

ECC v2.2.0 yaklaşık **33 ayrı hook** çalıştırıyor. Çoğu sessiz; birkaçı işi
durduruyor. Bir hook beklenmedik şekilde işi tıkadığında buraya bakılır.

## Ana şalterler

| Değişken | Etki |
|---|---|
| `ECC_HOOKS_ENABLED=false` | **Tüm** ECC hook'larını kapatır |
| `ECC_HOOK_PROFILE=minimal\|standard\|strict` | Varsayılan `standard`. `minimal` = yalnız temel yaşam döngüsü + güvenlik |
| `ECC_DISABLED_HOOKS="id1,id2"` | Belirli hook'ları kapatır (virgülle, küçük harf) |
| `ECC_GATEGUARD=off` | Yalnız GateGuard kapısını kapatır |
| `ECC_SESSION_START_CONTEXT=off` | Açılış bağlam enjeksiyonunu kapatır |
| `ECC_CONTEXT_MONITOR_COST_WARNINGS=off` | Maliyet uyarılarını susturur, diğer uyarıları korur |

## İşi fiilen durduranlar

| Hook | Ne yapar | Kapatma |
|---|---|---|
| `pre:edit-write:gateguard-fact-force` | Her dosyaya **ilk** Edit/Write'ı bloklar, araştırma ister | `ECC_GATEGUARD=off` |
| `pre:bash:gateguard-fact-force` | Oturumun ilk Bash'ini bloklar | Aynı |
| `pre:bash:auto-tmux-dev` | `npm run dev`'i tmux dışında bloklar (exit 2) | `ECC_DISABLED_HOOKS=pre:bash:auto-tmux-dev` |
| `pre:config-protection` | Linter/formatter config dosyalarına yazmayı bloklar | `ECC_DISABLED_HOOKS=pre:config-protection` |
| `pre:mcp-health-check` | Sağlıksız MCP sunucusuna çağrıyı bloklar | ID ile |
| `pre:bash:block-no-verify` | `git --no-verify` ile hook atlamayı engeller — **tüm profillerde açık** | ID ile |

`pre:config-protection` kasıtlı bir tasarım: config'i gevşetip hatayı susturmak
yerine kodu düzeltmeye zorluyor. Kapatmadan önce iki kez düşünülür.

## Sessizce iş yapanlar — davranış şaşırtabilir

- `stop:format-typecheck` → yanıt sonunda düzenlenen tüm JS/TS dosyalarını
  **toplu** formatlar (Biome/Prettier) ve `tsc` çalıştırır. Beklenmedik biçim
  değişikliğinin sebebi genelde budur
- `post:edit:design-quality-check` → frontend düzenlemesi jenerik/şablon görünümlü
  UI'a kayarsa uyarır
- `pre:edit-write:suggest-compact` → ~50 tool çağrısında bir `/compact` önerir
- `pre:bash:commit-quality` ve `pre:bash:git-push-reminder` → yalnız `strict`
  profilde aktif

## Bu vault'un kendi hook'larıyla ilişkisi

Vault'un `SessionStart` ve `Stop` hook'ları **proje düzeyi** `settings.json`'da,
ECC'ninkiler küresel. İkisi çakışmıyor; ikisi de çalışıyor. `PreCompact` ise hem
ECC'de hem vault'ta var → [[genel-ecc-precompact-akisi]]

İlgili: [[genel-gateguard-davranisi]] · [[genel-araclar]] · [[genel-notlar]]
