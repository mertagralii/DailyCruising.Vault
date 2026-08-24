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

## Zincirler — genel tarafta hangi araç hangi sırayla

Web ve API'de zincirin çıktısı **kod**tur; burada çıktı **karar**dır. Yanlış kod
build'de patlar, yanlış karar altı ay sonra patlar — bu yüzden buradaki sıra daha
önemlidir, daha az görünür olduğu halde.

### Zincir A — yeni bir iş, özellik veya kural konuşulurken

| # | Ne | Komut / skill | Neden bu sırada |
|---|---|---|---|
| 1 | Niyeti netleştir | `Skill: superpowers:brainstorming` | Kod yazmadan önce amaç, kısıt ve başarı ölçütü. **Onay kapısı zorunlu** — onay alınmadan uygulamaya geçilmez |
| 2 | Birden çok geçerli yol varsa | `Skill: ecc:council` | Dört sesli konsey, yapılandırılmış anlaşmazlık. Tek bakış açısıyla verilen karar sonradan "başka türlü de olabilirmiş"e dönüşür |
| 3 | Karar netleşti | `Skill: domain-karari` (projeye özel) | Dört dosyayı senkron tutar: `domain-gereksinimler` · ilgili `*-kararlar` · `durum.md` · pano |
| 4 | Doğrula | `python3 _araclar/dogrula.py` | Gerekçesiz karar ve kopan bağ burada yakalanır |
| 5 | İşi panoya aç | ilgili `*-gorevler.md` | Kabul ölçütü **yazılır**. Ölçütsüz görev, "bitti" kararını yine bana bırakır |

⛔ **1. adım atlanamaz.** Bu projede alınmış her yanlış kararın ortak sebebi,
konuşulmadan uygulanmış olmasıdır. `brainstorming` skill'inin onay kapısı tam
bunun içindir.

⚠️ **Karar Mert'in mi benim çıkarımım mı — ayrılır.** Karışırsa altı ay sonra
hangisinin kim olduğu bilinmez → [[genel-desenler]]

### Zincir B — bir hata avlanırken

| # | Ne | Komut / skill | Neden |
|---|---|---|---|
| 1 | Yöntem | `Skill: superpowers:systematic-debugging` | Tahminle değil kanıtla ilerlemek. En pahalı hata, yanlış yeri düzeltmektir |
| 2 | Hata yutuluyor olabilir | `ecc:silent-failure-hunter` ajanı | Yutulmuş exception, kötü fallback, eksik hata yayılımı — belirti veren değil **sessiz** sınıf |
| 3 | Kök neden bulundu | Düzelt | — |
| 4 | Tekrarlanacak mı | `Skill: vault-not` (projeye özel) | Aynı tuzağa ikinci kez düşmemek için. **Aynı kök neden bu projede dört ayrı yerde yeniden keşfedildi** → [[genel-gorevler]] `G-15` |
| 5 | Doğrula | Alanın doğrulama komutu | Web → tarayıcı · API → uç noktaya istek · vault → `dogrula.py` |

⛔ **4. adım atlanamaz.** Düzeltilip yazılmayan tuzak, yeniden keşfedilecek tuzaktır.

### Zincir C — oturumu kapatırken

`Stop` hook'u ilk üçünü denetler ve eksikse uyarır; engellemez.

| # | Ne | Neden |
|---|---|---|
| 1 | Alanın havuzuna en az bir şey yazıldı mı | Karar yoksa desen, desen yoksa not, o da yoksa panoya satır |
| 2 | Görevler `Kanıt:` satırıyla kapatıldı mı | Kanıt "kontrol ettim" değil, **hangi komutun ne çıktı verdiği** |
| 3 | `durum.md` güncel mi | "Sırada ne var" cevabı orada yaşar, oturum notunda değil |
| 4 | `python3 _araclar/dogrula.py` | TEMIZ dönmeden iş bitmiş sayılmaz |
| 5 | Vault commit'lendi mi | Alanlar yazar, **commit'i vault oturumu atar** |

Kapsamlı bir iş bitiyorsa 4'ten önce `Skill: ecc:verification-loop` — "bitti"
iddiasını sıkılaştırır.

### ⛔ Üç alanın ortak kapısı

Her zincirin sonunda aynı kural var, yalnız biçimi değişiyor:

| Alan | "Bitti" için yetmeyen | Gereken |
|---|---|---|
| **Web** | `npm run build` temiz | Tarayıcıda ölçüm → [[web-araclar]] |
| **API** | `dotnet build` temiz | Uç noktaya istek, status + gövde → [[api-araclar]] |
| **Genel** | "Karar verildi" | Dört dosya senkron + `dogrula.py` TEMIZ |

Üçünde de araç **gerekli koşuldur, yeterli değildir.** Bu projenin bilinen arıza
modu, gerekli koşulu yeterli sanmaktır: 2026-08-21'de "19/19 sayfa tamamlandı"
denmesinin sebebi build'in temiz olmasıydı; 106 bölüm eksikti.

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
