---
rol: map
kapsam: genel
guncelleme: 2026-08-24
durum: guncel
---

# Genel Araçlar

Alandan bağımsız, her iki repoda da geçerli araç eşlemesi.
Alana özel olanlar -> [[api-araclar]] · [[web-araclar]]

| Tetikleyici | Araç | Neden |
|---|---|---|
| Yeni bir özellik veya sistem konuşulacak | `superpowers:brainstorming` | Kod yazmadan önce niyet ve kısıtları netleştirir; onay kapısı zorunlu |
| Bir hata avlanacak | `superpowers:systematic-debugging` | Tahminle değil kanıtla ilerlemek için |
| "Bitti" demeden önce | `superpowers:verification-before-completion` | Bu projenin bilinen arıza modu kanıtsız tamamlandı raporu |
| Yazılan kod gözden geçirilecek | `/code-review` | Yerel değişiklik veya PR üzerinde çalışır |
| Çok adımlı bir iş planlanacak | `superpowers:writing-plans` | Uzun işlerde adım kaybını önler |
| Kalıcı ayar, hook veya izin değişecek | `update-config` skill'i | `settings.json` elle kurcalanmaz |
| Vault'a yeni not eklenecek | `vault-not` skill'i (projeye özel) | Frontmatter, hub bağı ve çıkan link üçü birden unutuluyordu; `dogrula.py` hatasının en sık sebebi buydu |
| Bir domain sorusu cevaplandı, blocker çözüldü | `domain-karari` skill'i (projeye özel) | Dört dosya (`domain-gereksinimler`, `api-kararlar`, `durum`, pano) senkron güncellenmezse vault kendiyle çelişir |
| Bir web sayfası "bitti" denecek | `sayfa-denetimi` skill'i (projeye özel) | 2026-08-21'de 19/19 bitti denip 106 bölüm eksik çıktı; sıra atlanınca ölçüm yalan söylüyor |

Projeye özel skill'ler `DailyCruising/.claude/skills/` altında; vault'tan `.claude`
symlink'i ile de görünür.

## Ortam davranışları

- **GateGuard** (`ECC_GATEGUARD`) oturumun ilk Bash komutunu, yıkıcı kalıpları ve
  **her yeni dosya oluşturmayı** durdurup olgu ister. Yıkıcı işlemde silmek yerine
  `.trash-<ad>` gibi bir ada taşımak hem kapıyı geçirir hem geri dönüş bırakır
  -> [[genel-gateguard-davranisi]]
- **PreCompact** hook'u compact öncesi özeti oturum notuna yazar
  -> [[genel-ecc-precompact-akisi]]
- Oturum dökümleri `~/.claude/projects/` altında tutulur (~35 MB). **Okunmaz** —
  içlerinden damıtılan bilgi vault'a girer

## Kullanılmayacaklar

- `Workflow` / çok ajanlı orkestrasyon — Mert açıkça istemedikçe çalıştırılmaz
- Alt ajan (`Agent`) çağrısı — Mert açıkça istemedikçe kullanılmaz

İlgili: [[genel-notlar]] · [[genel-desenler]] · [[calisma-duzeni]] · [[genel-gorevler]] · [[api-araclar]] · [[web-araclar]]
