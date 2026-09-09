---
rol: history
kapsam: mobil
guncelleme: 2026-09-09
durum: guncel
---

# Mobil Kararları

Kalıcı kararlar ve **gerekçeleri**. "Ne" koddan okunur, "neden" okunmaz — o yüzden
`**Neden:**` satırı olmayan giriş değersizdir ve `dogrula.py` hata verir.

Karar değişirse eskisi **silinmez**; yeni giriş eklenir ve "<tarih> kararını iptal
eder" yazılır.

---

## 2026-09-09 — Mobil kapsamı, backend ve frontend bitene kadar ERTELENDİ

**Karar:** *"Mobil hangi ekranları taşıyacak"* sorusu (`M-02`) bugün
cevaplanmayacak. Mert'in kararı: **önce API, sonra web bitecek**, kapsam ondan
sonra konuşulacak. `M-02`'nin tetikleyicisi artık bir tarih değil, bir **olay**:
API ve Web panolarında Mert'e bağlı olmayan iş kalmaması.

**Neden:** Mobilin taşıyacağı akışlar, web'de hangi akışların gerçekten
oturduğuna bağlı. Bugün verilecek kapsam kararı, web'in son iki haftada
değişmeye devam eden yüzeyine dayanır — yani ilk değişiklikte yeniden verilir.
Cevabı olmayan soruyu **cevapsız olarak işaretlemek**, uydurulmuş bir cevaptan
iyidir → [[genel-desenler]]

**Alternatifler:** Şimdiden misafir akışıyla başlamak — elendi: `M-04` (klasör
düzeni, navigasyon) ve `M-05` (API istemcisi) kapsamdan türüyor; yanlış kapsamla
kurulan iskelet atılır.

**Sonucu:** Mobil panosunda `M-02`, `M-04`, `M-05` **bilerek beklemede**. Bu
süre boyunca mobil tarafta kod yazılmaz; yazılırsa bu karara aykırıdır.

---

## 2026-09-09 — Expo'nun resmî Claude eklentisi kuruldu, YALNIZ bu projede etkin

**Karar:** `expo@claude-plugins-official` kuruldu ve **yalnız**
`DailyCruising/.claude/settings.json` içinde etkinleştirildi. Kurulum komutu
eklentiyi küresel ayara da yazmıştı; o satır **geri alındı** (yedek:
`~/.claude/settings.json.yedek-*`).

**Neden:** Eklenti Expo ekibinin kendi skill'lerini taşıyor (24 skill: Expo
Router, EAS Build/Update/Workflows, expo-ui, upgrade, project-structure…).
Expo 57 ve RN 0.86 yeni sürümler; eğitim verimin bayat olduğu yer tam burası.
Kaynağı `github.com/expo/skills`, Anthropic'in resmî pazarı üzerinden dağıtılıyor.
Yalnız bu projede etkin olmasının sebebi `ui-ux-pro-max` ve `seo-butler` ile
aynı: **küresel ayar kirletilmez**, başka projede Claude açıldığında görünmez.

**Alternatifler:** Şablonun yaptığı gibi kod reposunun içindeki
`.claude/settings.json` ile açmak — elendi: repoya AI aracı dosyası konmaz
(2026-09-09 kararı, aynı gün).

**Sonucu:** `M-06` kapandı. Eklentinin hangi tetikleyicide gerçekten işe
yaradığı **henüz ölçülmedi** — mobil kod yazılmadan ölçülemez → [[mobil-araclar]]


## 2026-09-09 — Repo `DailyCruising.Mobil`, private; AI aracı dosyaları repoda tutulmaz

**Karar:** `mertagralii/DailyCruising.Mobil` private reposu açıldı, iskelet
push'landı. Ad, klasör adıyla ve `DailyCruising.API` / `DailyCruising.Web` /
`DailyCruising.Vault` düzeniyle aynı hizada. Expo şablonunun `AGENTS.md`,
`CLAUDE.md` ve `.claude/settings.json` dosyaları repodan düşürüldü ve
`.gitignore`'a yazıldı.

**Neden:** Bağlam vault'ta yaşar, kod reposunda değil — üç repoda birden geçerli
kural bu ([[genel-kararlar]]). Repoya konan AI dosyası ikinci bir gerçek kaynağı
doğurur ve vault ile çelişmeye başlar; çeliştiğinde hangisinin doğru olduğunu
kimse bilmez.

**Alternatifler:** Şablonun `AGENTS.md`'sini bırakmak — elendi, ama içindeki tek
gerçek bilgi **atılmadı**: *"Expo değişti, kod yazmadan önce sürüme özel
dokümanı oku"* uyarısı tetikleyici olarak [[mobil-araclar]]'a taşındı. Bir
dosyayı silerken ölçüt, dosyanın kendisi değil **taşıdığı tetikleyicidir**.

**Sonucu:** Expo şablonu bu dosyaları yeniden üretirse (`npx expo start` gibi bir
komutta) `.gitignore` onları yakalar; Web'de `next dev` tam olarak bunu yapıyor.
Mobilde henüz gözlenmedi.

---

## 2026-09-09 — `.gitignore` ortam değişkeni kuralı Web ile hizalandı

**Karar:** `.env*.local` yerine `.env*` yok sayılır, `!.env.example` muaf tutulur.

**Neden:** Şablonun kuralı yalnız `.env*.local` dosyalarını yakalıyordu; mobil
uygulama API tabanı ve anahtar taşıyacağı için düz bir `.env` **fark edilmeden
commit'lenirdi**. Bu, sessiz sınıfa giren bir hata: hiçbir araç uyarmaz, yalnız
sızdıktan sonra görünür.

**Alternatifler:** Olduğu gibi bırakıp dikkatli olmak — elendi, dikkat bir kapı
değildir.

**Sonucu:** `.env.example` bilinçli olarak muaf; örnek dosya olmadan yeni geliştirici
hangi değişkenin gerektiğini bilemez → [[web-env-gitignore-tuzagi]]


## 2026-09-08 — Mobil, vault'ta ayrı bir alan olarak açıldı

**Karar:** `05-Mobil/` alanı açıldı. Dosya öneki `mobil-`, görev kimliği öneki
`M-`, not klasörü `05-Mobil/notlar/`. Alan `_araclar/vault.json` içine yazıldı;
betiklere elle sabit girilmedi.

**Neden:** Vault'ta yazma hakkı **alan bazlı** bölünmüştür, çünkü aynı anda birden
fazla oturum açık olabiliyor ve ikisi aynı dosyaya yazarsa biri diğerini sessizce
siler. Mobil işi `03-Web/*` altına yazılsaydı, mobil oturumu ile frontend oturumu
aynı panoya ve aynı durum dosyasına yazardı → [[genel-esszamanli-oturumlar]]

**Alternatifler:**
- `03-Web` altında alt bölüm — elendi: yazma hakkı çakışır, pano kimlikleri
  (`W-`) tek numara alanını paylaşır, "web durumu" iki platformu birden anlatır
- Mobil için ayrı bir vault — elendi: API sözleşmesi ortak, `[[api-sema-guncel]]`
  gibi çapraz linkler kopar, denetim iki yerde çalıştırılır

**Sonucu:** `dogrula.py` artık dört alan denetliyor. Bu bir bakım borcudur: boş
bölmeler de bayatlık ve tetikleyici taramasına girer. Alan açmanın bedeli
budur — bölme sayısı arttıkça denetimin sesi de artar.

---

## 2026-09-08 — Klasör adı `05-Mobil`; `04-Oturumlar` yeniden adlandırılmadı

**Karar:** Alanlar artık `01-Genel`, `02-API`, `03-Web`, `05-Mobil` — numaralar
bitişik değil. `04-Oturumlar` olduğu gibi bırakıldı.

**Neden:** `~/.claude/hooks/vault-precompact.js` içinde arşiv klasörünün adı
**sabit yazılı** ve klasör yoksa **yeniden yaratılıyor**. Yeniden adlandırılsaydı
hook hiçbir şey söylemeden yeni bir `04-Oturumlar` açar, arşiv sessizce ikiye
bölünürdü. Numara yalnızca sıralama önekidir; alanın kimliği `vault.json`
içindeki `onek` alanıdır, klasör numarası değil.

**Alternatifler:** `04-Mobil` + `05-Oturumlar` — elendi: küresel hook dosyasına
dokunmayı gerektiriyordu ve kazanç yalnızca görsel sıralamaydı. `04-Mobil` ile
`04-Oturumlar`'ı yan yana bırakmak — elendi: aynı numara iki klasörde, okuyanı
yanıltır.

**Sonucu:** Numara boşluğu (`04` arşivde) kalıcıdır. Yeni alan açılırsa `06`'dan
devam edilir.

---

## 2026-09-08 — Teknoloji yığını Expo/React Native, Mert'in iskeletiyle geldi

**Karar:** Mobil, Expo SDK 57 + React Native 0.86 + TypeScript 6 üzerine kurulu
şablonla başlıyor. Bu yığın **sorgulanmadan kabul edildi**.

**Neden:** İskeleti Mert kurdu; vault kanıttır, talimat değildir — var olan kodun
seçimini not düzeltmez. Yığının gerekçesi (Expo yönetilen akış mı, EAS Build
beklentisi mi, ileride bare workflow'a çıkılacak mı) **sorulmadı ve bilinmiyor**.

**Alternatifler:** Değerlendirilmedi — karar verildiğinde ben yoktum.

**Sonucu:** Açık soru olarak duruyor: yönetilen (managed) akışta kalınacak mı?
Cevap, yerel bildirim / harita / ödeme SDK'sı gerektiğinde bağlayıcı olur →
[[mobil-durum]]

İlgili: [[mobil-mimari]] · [[mobil-desenler]] · [[mobil-durum]] · [[genel-kararlar]] · [[00-Index]]
