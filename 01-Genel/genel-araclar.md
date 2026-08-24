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

## Alt ajan ve orkestrasyon

**2026-08-24'te serbest bırakıldı** — Mert izin verdi, her seferinde sormaya gerek
yok. Ama serbest ≠ gelişigüzel: aşağıdaki tetikleyiciler dışında çağrılmaz.

| Tetikleyici | Ne | Neden |
|---|---|---|
| Cevabı çok dosyaya yayılmış bir soru (nerede kullanılıyor, kaç yerde geçiyor) | `Explore` ajanı | Onlarca dosya okumak ana bağlamı kirletir; ajan sadece sonucu getirir |
| Kod yazıldı veya değiştirildi, incelenecek | `ecc:*-reviewer` ajanları | Zaten alan araç dosyalarında eşlenmiş — bunlar birer alt ajandır |
| Birbirinden bağımsız 3+ iş kolu aynı anda ilerleyebiliyor | Paralel `Agent` çağrıları | Sıralı yapmanın tek kazancı yok |
| Kapsamlı denetim: çok sayıda dosyada tarama + bulguların ayrıca doğrulanması | `Workflow` | Bulan ile doğrulayanın ayrı olması, emin-ama-yanlış bulguyu eler |

**Ne zaman çağrılmaz — çağırmadan önce bu üçünü sor:**

1. **İş tek bir bilinen dosyada mı?** Öyleyse doğrudan yap. Ajan çağırmak yavaşlatır.
2. **İş bir cevabı mı bekliyor?** Domain sorusu cevaplanmadan şema yazılamaz;
   on ajan da o duvarı yıkmaz. Darboğaz paralellik değilse ajan işe yaramaz.
3. **Sonucu doğrulayabilir miyim?** Ajan emin bir dille yanlış cevap verebilir.
   Doğrulanamayacak bir çıktı, doğrulanmamış bir iddiadır → [[genel-desenler]]

⚠️ **Maliyet.** `Workflow` onlarca ajan çalıştırabilir. Kapsamlı bir denetim
başlatmadan önce ne kadar süreceği ve neyi kapsayacağı tek satırla bildirilir —
izin için değil, Mert görsün diye.

## ECC — alandan bağımsız olanlar

Komutlar `/ecc:<ad>`, skill'ler `Skill` aracıyla `ecc:<ad>`. Alan-özgü eşlemeler
[[api-araclar]] ve [[web-araclar]] içinde; burada yalnız her iki tarafta geçerli
olanlar var.

| Tetikleyici | Ne | Neden |
|---|---|---|
| Ciddi bir işe başlamadan önce | `/ecc:plan` | Riski değerlendirir, adım planı üretir ve **koda dokunmadan CONFIRM bekler** |
| Hangi komutları hangi sırayla çalıştıracağım belirsiz | `Skill: ecc:ecc-recipes` | İş akışını doğru komut **grubuna**, sırasıyla ve durma koşuluyla eşler |
| ECC'de ne var, ne yok | `/ecc:ecc-guide` | Canlı repo yüzeyinden ajan/skill/komut/hook listesi |
| Kod yazıldı, incelenecek | `/ecc:code-review` | Yerel commit edilmemiş değişiklik veya PR numarası/URL alır |
| "Bitti" denmeden önce | `Skill: ecc:verification-loop` | Bu projenin bilinen arıza modu kanıtsız tamamlandı raporu |
| Mimari karar verildi | `Skill: ecc:architecture-decision-records` | ADR üretir — ama bu projede kararlar `*-kararlar.md`'ye gider, ADR **ikinci bir otorite yaratmaz** |
| Yayın öncesi hazırlık | `Skill: ecc:production-audit` | Yerel kanıta dayalı "prod'da ne kırılır" denetimi |
| Bir hook veya kapı işi tıkadı | → [[genel-ecc-hook-profilleri]] | 33 hook'un hangisi ne yapıyor, nasıl kapatılıyor |

⚠️ **Kullanılmayacak ECC parçaları — bu projede ikinci otorite yaratırlar:**
`ecc:ck` ve `ecc:unified-memory` (kalıcı bellek katmanları) vault'un yerini almaya
çalışır; `durum.md` tek otorite kuralını bozar → [[genel-kararlar]] 2026-08-24.
`ecc:continuous-learning` **deprecated**, kullanılmaz.

## Kullanılmayacaklar

- (bu alanda şu an yok)

İlgili: [[genel-notlar]] · [[genel-desenler]] · [[calisma-duzeni]] · [[genel-gorevler]] · [[api-araclar]] · [[web-araclar]]
