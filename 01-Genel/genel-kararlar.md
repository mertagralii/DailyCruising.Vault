---
rol: history
kapsam: genel
guncelleme: 2026-09-11
durum: guncel
---

# Genel Kararlar

İki repoyu birden ilgilendiren kalıcı kararlar. **Append-only** — eski giriş silinmez;
karar değişirse yeni giriş eklenir ve eskisini iptal ettiği yazılır.

---

## 2026-09-11 — `ECC_MEMORY_PROJECT_ROOT` de küresel ayardan proje ayarına taşındı

**Karar:** Küresel `~/.claude/settings.json` içindeki `env` bloğu kaldırıldı,
aynı blok `DailyCruising/.claude/settings.json` içine alındı. Küresel ayarda
artık ne hook ne env var; yalnız makine geneli tercihler (model, tema, bildirim,
eklentiler) duruyor.

**Neden:** Değişken küreseldi ve **bu projenin** klasörünü gösteriyordu
(`DailyCruising/.ecc/memory`). Başka bir projede ECC memory kullanıldığında o
projenin belleği bu projenin klasörüne yazılırdı — aynı gün kaldırılan
`PreCompact` kancasıyla **aynı sızıntı sınıfı**: küresel ayara konmuş,
proje-özel bir yol.

**Davranış değişmiyor, koddan doğrulandı:** `ecc/scripts/lib/memory-vault.js:66`
— değişken yoksa ECC `findNearestProjectRoot(cwd)/.ecc/memory` kullanıyor, yani
en yakın `.git` klasörünün yanına yazıyor. Bu projede değişken proje ayarında
kaldığı için yol aynı; başka projede artık o projenin kendi klasörü kullanılır.

⚠️ **Değişkenin bu projede gerekli olma sebebi ayrı ve önemli:** proje kökü git
reposu **değil**. Yani değişken tamamen silinse, vault içinden çalışan bir
oturumda "en yakın `.git`" **vault'un kendisi** olur ve bellek
`DailyCruising.Vault/.ecc/memory` altına düşerdi. Bu yüzden silinmedi, taşındı.

**Sonucu:** ECC eklentisi küreselde kurulu ve etkin kalmaya devam ediyor —
taşınan şey eklenti değil, yalnız "belleği nereye yaz" ipucu.

## 2026-09-11 — `PreCompact` hook'u küresel ayardan proje ayarına taşındı

**Karar:** `~/.claude/settings.json` içindeki `PreCompact` kancası kaldırıldı ve
`DailyCruising/.claude/settings.json` içine alındı. Küresel ayarda artık **hiç
hook yok**; yedek `~/.claude/settings.json.yedek-20260911-035133`.

**Neden:** Hook küresel olduğu için **her projede** tetikleniyordu ve bağlı olduğu
betik yalnızca *"DailyCruising vault klasörü diskte var mı"* diye bakıyor, oturumun
hangi projeye ait olduğuna bakmıyor. Yazacağı yer de sabit (`04-Oturumlar`). Yani
başka bir projede compact olduğunda o oturumun özeti **bu vault'un arşivine**
düşecekti. Kusuru `test-a9` oturumu bildirdi (kendi vault'unu kurarken hook'u
bilerek bağlamamış); arşiv tarandı, kirlenme **henüz olmamıştı**.

Mert'in talimatı (2026-09-11): *"bunu sadece bu proje için kullanacağız, küresel
Claude Code'umun bozulmasını istemiyorum."* Aynı gerekçe `ui-ux-pro-max`,
`seo-butler` ve Expo eklentisi için de uygulanmıştı — **küresel ayar
kirletilmez**; proje ayarı, projeye ait olanın yeridir.

**Sonucu:** Hook yalnız bu projede çalışır; başka projede compact olursa arşive
hiçbir şey yazılmaz. Bedeli: `04-Oturumlar` artık bu proje dışındaki çalışmayı
hiç kaydetmiyor — bilinçli, çünkü o kayıtlar buraya ait değil.

Betiğin içindeki yol hâlâ sabit yazılı; kapsam daraltıldığı için bugün zararsız,
ama makine başka bir projeye taşınırken **üç hook dosyasının da yolu elle
düzeltilmek zorunda** → [[genel-notlar]]

## 2026-08-21 — İki ayrı private repo

**Karar:** Backend ve frontend ayrı GitHub repolarında, ikisi de private.
`DailyCruising.Back-End/` → `mertagralii/DailyCruising.API`,
`DailyCruising.Front-End/` → `mertagralii/DailyCruising.Web`.

**Neden:** Mert açıkça istedi.

**Alternatif:** Monorepo (tek repo, iki klasör) — ortak sürümleme ve atomik değişiklik
sağlardı, seçilmedi.

**Sonucu:** Kök klasörde git reposu **yok**. git komutları ilgili alt klasörde
çalıştırılmalı. İki repoyu birden ilgilendiren değişiklikler atomik değil.

---

## 2026-08-21 — Commit'lerde AI atfı yasak

**Karar:** Commit mesajlarına `Co-Authored-By: Claude` trailer'ı, "Generated with
Claude Code" / "Created by Anthropic" benzeri ibareler eklenmez. Repolara AI araç
dosyası (`CLAUDE.md`, `AGENTS.md`) konmaz.

**Neden:** Mert repolarının AI izi taşımasını istemiyor.

**Sonucu:** Claude Code'un varsayılan commit trailer davranışı geçersiz kılınır.
create-next-app'in ürettiği `CLAUDE.md`/`AGENTS.md` ilk commit'ten önce silindi.

---

## 2026-08-21 — Obsidian vault tabanlı context hafızası

**Karar:** Kalıcı proje bilgisi `DailyCruising.Vault/` içinde markdown notlarda
tutulur. Kökteki `CLAUDE.md` (vault'a symlink) her oturumda otomatik yüklenip
okuma/yazma kurallarını taşır. Yapı ECC `living-docs-governance` dört rolüne
(Constitution/Map/Status/History) göre düzenlenir.

**Neden:** `/compact` sonrası ve yeni oturumda bağlam kaybı; aynı kararın tekrar
tartışılması. ECC `strategic-compact` dokümanına göre compact'tan sağ çıkanlar:
CLAUDE.md talimatları ve disk üzerindeki dosyalar.

**Alternatif 1:** Her şeyi tek `CLAUDE.md`'de tutmak — her oturumda artan token
maliyeti nedeniyle elendi.
**Alternatif 2:** Notları repoların `docs/` klasörüne koymak — repolarda AI dosyası
istenmemesi ve iki repoyu birden ilgilendiren notların sahipsiz kalması nedeniyle elendi.

**Sonucu:** Vault git'e alınmaz (Mert'in kararı) → yedekleme kullanıcının
sorumluluğunda; disk arızasında karar gerekçeleri geri türetilemez.

---

## 2026-08-21 — ECC Memory Vault ikinci katman olarak

**Karar:** ECC'nin `.ecc/memory/` vault'u da devreye alınır. Akış **tek yönlü**:
ECC memory (ham, `trust: unreviewed`) → gözden geçirme → Obsidian vault (kanonik).

**Neden:** Harness'lar arası (Codex, Cursor) devir teslim imkânı. ECC `unified-memory`
skill'i ham hafızanın doğrudan karara terfi ettirilmesini yasaklıyor, bu yüzden akış
ters yönde işlemez.

**Sonucu:** `ecc-universal` global npm paketi bağımlılığı. `ECC_MEMORY_PROJECT_ROOT`
kök klasöre ayarlanır (kök git reposu olmadığı için gerekli).

İlgili: [[durum]] · [[calisma-duzeni]] · [[proje]] · [[00-Index]]

---

## 2026-08-21 — Vault dosya adları benzersiz olmalı

**Karar:** Aynı adı taşıyan not dosyası olmaz. `kararlar.md` yerine
`genel-kararlar.md` / `api-kararlar.md` / `web-kararlar.md`; `mimari.md` yerine
`api-mimari.md` / `web-mimari.md`.

**Neden:** İlk kurulumda klasör adına güvenilip dosyalar aynı adla oluşturuldu.
Doğrulamada çıktı: Obsidian'da `[[kararlar]]` üç dosya arasında belirsiz kalıyor,
grep ile de ayırt edilemiyor. Klasör yapısı bağlamı insana anlatır, wikilink
çözümleyicisine anlatmaz.

**Sonucu:** Yeni not eklerken ad benzersiz olmalı. Doğrulama scripti hem kırık hem
belirsiz linkleri tarıyor.

---

## 2026-08-21 — ECC_MEMORY_PROJECT_ROOT hafıza kökünü gösterir

**Karar:** `ECC_MEMORY_PROJECT_ROOT=/Users/mertagrali/Desktop/DailyCruising/.ecc/memory`

**Neden:** Değişken repo kökü sanılıp `.../DailyCruising` verildi; `ecc memory init`
kökte çorak bir `project/` klasörü oluşturdu. Değişken **hafıza kökünü** gösteriyor,
repo kökünü değil. Doğru değer `.ecc/memory` ile bitmeli ki dokümandaki
`<repo>/.ecc/memory/project/` düzeni oluşsun.

**Sonucu:** `.ecc/memory/project/` kendi fail-closed `.gitignore`'una (`*` + `!.gitignore`)
sahip; repolara sızmaz. Zaten kök git reposu da değil.

---

## 2026-08-21 — Proje bir yeniden inşa (rewrite), yeşil alan değil

**Karar:** DailyCruising sıfırdan bir fikir değil; `dailycruising.com.tr` adresinde
**canlı çalışan** bir platformun yeniden yazımı. Mert tersine mühendislikle çıkarılmış
tam bir şartname (PRD) verdi: veri modeli, enum değerleri, rota haritası, sayfa
içerikleri, fiyat algoritması, 22 panel modülü, 29 maddelik iş kuralı listesi.

**Neden:** Mevcut sistem çalışıyor ama veri modeli ve ürün tarafında bilinen kusurları
var; PRD bunları da listeliyor ve düzeltilmesini istiyor.

**Alternatifler:** Mevcut sistemi kademeli iyileştirmek — Mert yeniden yazımı seçti,
tartışılmadı.

**Sonucu:**
1. Belirsizlik düşük — davranış zaten tanımlı. Tasarım işi "ne yapmalı"dan çok
   "nasıl daha iyi yapmalı"ya kayıyor.
2. **PRD'nin veri modeli birebir kopyalanmayacak.** O, *eski sistemin* modeli;
   PRD'nin kendi "iyileştirme önerileri" bölümü onu düzeltiyor (User/Partner ayrımı,
   bölgenin enum yerine tablo olması, tur tipinin slug'a taşınması, TR/EN alan
   çiftleri yerine çeviri tablosu, ölçü alanlarının decimal olması).
3. Mobil uygulamalar mevcut → **API-önce** tasarım zorunlu. Bu bizim iki repoluk
   (.NET API + Next.js) kurgumuzla örtüşüyor.
4. Kabul kriteri hazır: PRD'deki 29 maddelik iş kuralı listesi.

**Risk:** PRD kaynak koda erişmeden yazıldı; ödeme callback detayı, satır bazlı
yetki kurgusu ve tam durum makinesi **çıkarım** olarak işaretlenmiş. Bu üçü
tasarlanırken doğrulanmalı, PRD'ye kesin gerçek gibi güvenilmemeli.

---

## 2026-08-21 — Marka: Rıhtım tasarımı, DailyCruising adı

**Karar:** claude.ai/design'daki "Rıhtım" projesinin **görsel kimliği ve tasarımı**
benimsenir; **görünen marka adı DailyCruising olarak kalır.** Tasarımdaki "Rıhtım"
yazıları, `rihtim.com.tr` e-postaları ve "Rıhtım Turizm A.Ş." ünvanı değiştirilir.

**Neden:** Mert tasarımı beğendi ama marka adını değiştirmek istemiyor. Repolar,
alan adı ve TÜRSAB kaydı DailyCruising üzerine.

**Alternatifler:** Tamamen Rıhtım'a geçmek (reddedildi) · eski Daily Cruising
görselini korumak (reddedildi).

**Sonucu:** Marka adı kodda **tek bir sabitte** tutulur, her yerde o okunur —
yazımı (bitişik/ayrık) sonradan tek satırda değişebilsin. Tasarımdan gelen
kurumsal veriler (TÜRSAB no, şirket ünvanı, adres, telefon, e-posta) yer tutucudur;
gerçek değerlerle doğrulanmadan yayına çıkmamalı → [[durum]]


---

## 2026-08-22 — `next dev`in ürettiği AI dosyaları git'te yok sayılıyor

**Karar:** `DailyCruising.Front-End/.gitignore` içine `/AGENTS.md` ve `/CLAUDE.md`
eklendi.

**Neden:** Next.js 16'nın `next dev` komutu her çalıştırmada bu iki dosyayı
`node_modules/next/dist/server/lib/generate-agent-files.js` üzerinden yeniden
üretiyor. Repoda AI aracı dosyası istenmiyor; silmek çözüm değil, `next dev` geri
koyuyor.

**Alternatif:** Dosyaları commit'lemek — kural gereği reddedildi.

**Sonucu:** Dosyalar diskte kalıyor (Next.js'in çalışması için), git'e girmiyor.

---

## 2026-08-24 — Obsidian Claude plugin'leri eklenmiyor, projeye özel skill'ler yazılıyor

**Karar:** `claude-code-ide`, `claude-obsidian` (AgriciDaniel) ve `claude-code-skills`
Obsidian eklentilerinin hiçbiri kurulmaz. Yerine üç projeye özel skill yazıldı:
`vault-not`, `domain-karari`, `sayfa-denetimi` → `DailyCruising/.claude/skills/`.

**Neden:** Üçünün de akış yönü **Obsidian → Claude**; yani Obsidian'da otururken
Claude'u çağırmak için. Bizim ihtiyacımız ters yönde — **Claude → vault** — ve bu
zaten doğrudan dosya yazımıyla çalışıyor. Vault sıradan markdown; araya Obsidian
katmanı koymak, Obsidian'ın açık olmasını şart koşar ve hiçbir şey kazandırmaz.

**Alternatifler:**
- `claude-code-ide` — Obsidian'da açık dosyayı ve seçili metni Claude'a bildirir.
  Tek somut faydası Obsidian CLI ile link bütünlüğü; ama `dogrula.py` kırık
  wikilink'i ve yetim notu zaten yakalıyor (denetim 3 ve 5). Elendi.
- `claude-obsidian` — kaynak yakalama, iddia defteri, provenance. Araştırma vault'u
  için tasarlanmış; bizimki proje çalışma vault'u, kaynağı yok kodu var. Ayrıca
  kendi taksonomisini (PARA / Zettelkasten / LYT) dayatıyor, üç havuz altı bölme
  yapısını bozardı. Elendi.
- `claude-code-skills` — Obsidian sidebar'ında metin seçip skill çalıştırma. Bizim
  skill'ler `playwright`, `npm run build`, `dotnet build` çalıştırıyor; sidebar'da
  değil terminalde yaşarlar. Elendi.

- `avenoxbeyin` (avenoxai) — Obsidian + Claude Code kalıcı hafıza sistemi.
  **Mimarisi bizimkiyle aynı:** SessionStart hook'u önceki bağlamı enjekte ediyor,
  kapanış hook'u hafızayı yazıyor, `Last-Session.md` + `Threads.md` durum taşıyor.
  Yani bizde `acilis.md` + `durum.md` + panolar ne yapıyorsa onu yapıyor. Kurulursa
  ikinci ve rakip bir "nerede kaldık" otoritesi doğar — tek otorite kuralını doğrudan
  bozar. Ayrıca **doğrulama katmanı yok**: kanıtsız "bitti" iddiasını engelleyen
  hiçbir mekanizması yok, bizim asıl arıza modumuz tam olarak bu. Elendi.

**Ölçüt — sonraki eklenti önerileri için:** bir araç ancak vault'un bilinen arıza
modunu (atlanan adım, kanıtsız "bitti", senkronsuz dosya) ölçülebilir şekilde
azaltıyorsa alınır. Yeni yetenek değil, **yakalanan hata** ölçüsüdür.

**Yan karar:** Skill'lerin cwd vault iken de bulunabilmesi için
`DailyCruising.Vault/.claude -> ../.claude` symlink'i kuruldu.

İlgili: [[genel-araclar]] · [[calisma-duzeni]] · [[durum]]

---

## 2026-08-24 — Eşzamanlı oturumlarda yazma hakkı bölündü

**Karar (Mert):** Aynı anda birden fazla Claude oturumu açık çalışıyor. Her oturum
yalnız **kendi alanının** dosyalarına yazar; `01-Genel/durum.md`'ye yalnız vault
oturumu yazar. Alanlar kendi durumlarını `02-API/api-durum.md` ve
`03-Web/web-durum.md` dosyalarında tutar.

**Neden:** Üç oturum aynı dosyaya yazarsa biri diğerinin yazdığını **sessizce
siler**. Vault git reposu olmadığı için geri alınamaz. Ayrıca `durum.md` "tek
otorite" olarak kurgulanmıştı; üç yazar o kuralı fiilen bozardı.

**Ölçüt cwd değil, üzerinde çalışılan alan.** 2026-08-24 testinde frontend işi
yapan oturumun `pwd`'si `DailyCruising.Vault` çıktı — klasör güvenilir bir işaret
değil.

**Alternatifler:**
- Tek dosyada bölüm ayrımı (herkes `durum.md`'nin kendi başlığına yazar) — aynı
  dosyaya eşzamanlı yazma riski sürerdi, elendi.
- Yalnız vault oturumunun yazması, diğerlerinin her şeyi mesajla iletmesi — her
  küçük güncelleme için tur bekletirdi, elendi.

**Kanıt — 2026-08-24 canlı testi:** `migrate-design-to-frontend` oturumuna
`SendMessage` ile dört soru soruldu, dördüne de cevap geldi. Test üç şey ortaya
çıkardı: (1) `SessionStart` hook'u açık oturumları ısıtmıyor, (2) `pwd` alanı
göstermiyor, (3) başka oturum çalışırken okunan git durumu saniyeler içinde
bayatlıyor — vault oturumu Front-End'i "2 dosya değişik" diye okudu, peer o sırada
commit attı, doğru cevap "temiz, `eb40c7e`" çıktı. Ayrıntı →
[[genel-esszamanli-oturumlar]]

İlgili: [[durum]] · [[api-durum]] · [[web-durum]] · [[calisma-duzeni]]

---

## 2026-08-24 — Vault sürüm kontrolüne alındı

**Karar:** Vault `mertagralii/DailyCruising.Vault` private reposunda tutulur.

**Neden:** 47 notun tek kopyası tek diskteydi — git reposu değil, Obsidian Sync
kapalı, bulut yolunda değil, Time Machine hedefi bağlanamıyor. Vault'un varlık
sebebi "hafıza kaybolmasın" iken kendisi kaybolmaya açıktı. İkinci ve daha sinsi
sebep: geri alma. Vault'a üç oturum yazıyor; yanlış bir `Write` sürüm kontrolü
olmadan **geri alınamaz**.

**Kapsam dışı:** `.obsidian/workspace.json` ve `graph.json` (makineye özgü),
`.claude` symlink'i (repo dışına gider, klonlandığında kırık olur).

**Not — CLAUDE.md bu repoda var.** "Repolara AI araç dosyası ekleme" kuralı
**ürün kod repoları** içindir (`DailyCruising.API`, `DailyCruising.Web`). Vault'un
tamamı zaten bağlam dosyası; `CLAUDE.md` onun anayasası, çıkarılırsa vault anlamsız
kalır.

---

## 2026-08-24 — Vault'un uzun vadeli hedefi: taşınabilir şablon

**Karar (Mert):** Bu vault DailyCruising'de kanıtlanırsa, yeni projelerde ve
**başka yazılımcılar tarafından** kullanılabilecek bir şablona dönüştürülecek.
Görev `G-15`.

**Neden:** Mert'in kendi ifadesi — iki gün sonra yeni bir projeye başladığında aynı
hafıza sistemini kurmak, ve başkalarının da kurabilmesini sağlamak istiyor.

**Bu hedefin bugünden getirdiği kısıt:** Yazarken **DailyCruising'e özgü olan** ile
**her projede geçerli olan** ayrılabilir kalmalı.

| Genel iskelet (şablona girer) | Projeye özgü (girmez) |
|---|---|
| Üç havuz, altı bölme düzeni | Tekne, sefer, rezervasyon domaini |
| `acilis.md` + karakter tavanı | DailyCruising'in blocker'ları |
| Pano biçimi, `Kanıt:` zorunluluğu | `A-`/`W-`/`G-` görev içerikleri |
| `dogrula.py` denetimleri | Postgres/Next.js'e özgü desenler |
| Hook'lar, yazma hakkı bölünmesi | `r-ht-m-temeller-sayfas` tasarım kaynağı |

**Kanıt ölçütü — şablonlaştırma ne zaman hak edilir:** Sistem bu projede en az bir
kez **yakalanmış hata** üretmiş olmalı. 2026-08-24 itibarıyla üç tane var: git
durumu bayatlaması, `api-durum` çelişkisi, `domain-gereksinimler` tablosunun
gövdesiyle çelişmesi. Yakalanan hata yoksa şablon yalnızca dosya düzenidir, sistem
değil.

İlgili: [[durum]] · [[genel-gorevler]] · [[calisma-duzeni]] · [[00-Index]]

---

## 2026-08-24 — Alt ajan ve orkestrasyon serbest bırakıldı

**Karar (Mert):** `Agent` (alt ajan) ve `Workflow` (çok ajanlı orkestrasyon) her
seferinde izin sormadan kullanılabilir. Ölçüt izin değil, **araç dosyalarındaki
tetikleyici eşlemesi**.

**Neden — Mert'in ifadesi:** *"ben pluginleri ve skilleri sana veriyorum, sen de
araçlara yerleştiriyorsun; ben demeden de kullanabilsinler."* Yani izin kapısı
gereksiz bir tur bekletiyordu; araç dosyaları zaten hangi durumda ne kullanılacağını
tanımlıyor.

**Bu karar bir çelişkiyi de kapattı.** `api-araclar.md` ve `web-araclar.md`
`ecc:csharp-reviewer`, `ecc:database-reviewer`, `ecc:react-reviewer` öneriyordu —
bunların üçü de **alt ajandır**. Aynı anda `genel-araclar.md` "alt ajan çağrısı
Mert açıkça istemedikçe kullanılmaz" diyordu. Vault kendi içinde çelişiyordu ve
bu, önerilen inceleme ajanlarının hiç çağrılmaması demekti.

**Serbest ≠ gelişigüzel.** Yerine üç kapı kondu → [[genel-araclar]]:
1. İş tek bilinen dosyadaysa doğrudan yapılır
2. Darboğaz paralellik değilse (cevap bekleniyorsa) ajan işe yaramaz
3. Çıktısı doğrulanamayacak ajan çağrısı, doğrulanmamış iddia üretir

**Maliyet uyarısı:** `Workflow` onlarca ajan çalıştırabilir. Kapsamlı bir denetim
öncesi kapsam ve tahmini boyut tek satırla bildirilir — izin için değil, görünürlük
için.

**Alternatif:** Her çağrıda sormaya devam etmek — Mert'in ret gerekçesi, aracı
verip kullandırmamanın anlamsızlığıydı. Elendi.

İlgili: [[genel-araclar]] · [[api-araclar]] · [[web-araclar]] · [[durum]]

---

## 2026-08-24 — İki eklenti proje bazlı kuruldu, küresel ayar kirletilmedi

**Karar (Mert):** `ui-ux-pro-max` (nextlevelbuilder) ve `seo-butler` (mertagralii)
**yalnız bu projede** etkin olacak. Tanımları `DailyCruising/.claude/settings.json`
içinde; `~/.claude/settings.json` değiştirilmedi.

**Neden:** Mert'in açık talebi — *"benim user scope'uma kurma"*. Küresel kurulum
her projede menüyü şişirir; DailyCruising'e özgü bir SEO eklentisinin başka bir
projede görünmesi gürültüdür.

**Nasıl:** `extraKnownMarketplaces` + `enabledPlugins` anahtarları proje düzeyi
`settings.json`'a yazıldı:

| Eklenti | Marketplace | Gereksinim |
|---|---|---|
| `ui-ux-pro-max` | `ui-ux-pro-max-skill` | Python 3 |
| `seo-butler` | `seo-butler-marketplace` | Node 18+ |

Küresel kalanlar: `ecc`, `superpowers`, `context7`, `playwright`,
`frontend-design` — bunlar her projede geçerli.

**Etkin olması için yeni oturum gerekir.** Eklentiler oturum açılışında yüklenir;
çalışan oturumlar bu ikisini görmez → [[genel-esszamanli-oturumlar]]

**Kullanım eşlemeleri** gerekçeleriyle [[web-araclar]] içinde. Özellikle iki uyarı
oraya yazıldı: `ui-ux-pro-max` **tasarımı olmayan** yeni iş içindir, var olan ekranı
"iyileştirmek" tasarımdan sapmadır; `seo-butler`'ın canlı komutları yayın öncesi
anlamsızdır ve `/seo` yer tutucu kurumsal veriyle çalıştırılırsa yanlış bilgi arama
motoruna işlenir.

İlgili: [[web-araclar]] · [[genel-araclar]] · [[durum]]

## 2026-08-28 — Yön tersine çevrildi: tasarımı backend gerçeği yönlendirir

Mert'in talimatı, üç durum:

1. **Uç var, verisi eksik** → backend tamamlar. Boş dönen bir uç "bitti" sayılmaz.
2. **Uç var, verisi var, sayfada karşılığı yok** → web sayfayı o uca göre yapar
   veya var olanı uca bağlar.
3. **Tasarım eksik olabilir** — bir temel olsun diye yapıldı, kısıt değil. Çelişki
   çıkarsa **backend gerçeği kazanır**, tasarım ona göre genişletilir.

**Neden:** Tasarım 22 Ağustos'ta, API'nin çoğu ondan sonra yazıldı — tasarım
yazıldığı gün doğruydu, bugün API'nin gerisinde. Yön "tasarım → kod" kaldığı
sürece 69 yolun karşılığı olmayan kısmı görünmez kalıyor ve iş, kimsenin
ölçmediği bir taslağa göre budanıyor. Kaynağın hangisi olduğu yazılmazsa her
oturum kendi kaynağını seçer.

Bu, [[web-kararlar]]'daki "tasarımdan sapma yasağı" kuralını **iptal etmez**:
sapma yasağı var olan ekranın görünümü içindir; bu karar **olmayan ekranın** var
edilmesi içindir. İkisi çakışırsa: var olan ekranın görünümü tasarıma sadık kalır,
eksik ekran API'ye göre yeni yazılır.

Ölçüm ve dağıtım: `03-Web/web-gorevler.md` içinde karşılığı olmayan uçlar için
görev açılır; veri boşlukları `02-API/api-gorevler.md`'ye düşer.

İlgili: [[web-kararlar]] · [[web-gorevler]] · [[api-gorevler]] · [[durum]]

## 2026-09-05 — Vault şablonu proje bitimine ertelendi

**Karar:** vault genel bir şablona **şimdi** çevrilmiyor. Şablon, proje
bitiminde backend ve frontend oturumlarıyla konuşularak çıkarılacak. Bugünkü
çalışma bu projede işe yarayacak şekilde uygulanır.

**Neden:** Mert'in kendi cümlesi — *"Şuanlık bizim projemizde çalışacak şekilde
yapalım en son projeyi bitirdiğimizde sen front-end ve back-end'le konuşursun.
Ona göre bu Vaultumuzu en uygun şekilde ayarlarız."* Gerekçe teknik olarak da
güçlü: backend'in tespitiyle, **gerekçesini yaşamadığın kural ilk yoğun günde
delinen kuraldır.** Şablon bugün çıkarılsaydı, projenin son ayında öğrenilecek
her şey dışarıda kalırdı.

**Alternatifler:** (a) şablonu şimdi çıkarıp proje ilerledikçe güncellemek —
elendi, çünkü şablon güncellenmeyen bir dosya olur ve iki yerde bakım gerektirir;
(b) yalnız iskeleti şimdi dondurmak — elendi, iskeletin kendisi hâlâ değişiyor
(bu hafta üç yeni araç ve iki yeni bölme eklendi).

**Sonucu:** `G-15` açık kalır ve tetikleyicisi *"proje bitti"* olur. Bugünkü
tasarım konuşmasından çıkan **bu projeye bugün uygulanabilir** üç bulgu
uygulandı → [[genel-desenler]]. Şablona girmeyecekler listesi de kayıtlıdır:
sayılar, domain, üç oturumlu yazma hakkı bölüşümü ve CLAUDE.md'deki yara izi
anlatıları.
