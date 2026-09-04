#!/usr/bin/env python3
"""
DailyCruising Vault saglik kontrolu.

Tarar:
  1. Eksik/bozuk frontmatter
  2. Ayni adli notlar (Obsidian wikilink'i belirsizlestirir)
  3. Kirik wikilink
  4. Bayat guncelleme tarihi (mutable notlar icin)
  5. Yetim not (hicbir yerden link verilmemis)
  6. Gerekcesiz karar girisi ("Neden:" satiri yok)
  7. notlar/ klasoru kurallari (ad oneki, hub baglantisi, cikan link)
  8. Her alanda desenler/gorevler/araclar dosyasi var mi
  9. Gorev panosu kurallari (Yapiliyor <= 3, Tamamlandi'da Kanit, kimlik cakismasi)
 10. acilis.md karakter tavani
 11. durum.md tazeligi
 12. Arac tablosunda bos "Neden" hucresi
 13. Tek yonlu tasiyici gerekce (Dayanak var, geri referans yok)
 14. Gorev kimligi kaybi (tum git gecmisine karsi)
 15. Mimari bayatligi (kod reposundaki yapisal degisime karsi)
 16. acilis.md durum.md'nin gerisinde mi

Kullanim: python3 _araclar/dogrula.py
Cikis kodu: 0 temiz, 1 sorun var
"""
import re
import sys
import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
BAYAT_GUN = 60                      # mutable notlar icin esik
MUTABLE_ROLLER = {"map", "status", "not"}  # kararlar/gorev/arsiv bayatlamaz

sorunlar = []
# 2026-08-31: susan denetim gorunmez oldugu icin susar. Her olcum, sorun
# uretmese de yazilir — "0/10" ile hicbir satir ayni sey degildir.
olcumler = []


def kodu_ayikla(text):
    """Kod bloklarini ve satir ici kodu cikar — icindeki [[ornek]] link sayilmaz."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    alanlar = {}
    for satir in m.group(1).splitlines():
        if ":" in satir:
            k, _, v = satir.partition(":")
            alanlar[k.strip()] = v.strip()
    return alanlar


# Vault notu olmayan repo belgeleri denetim disi: README GitHub icin yazilir,
# frontmatter ve hub bagi kurallari ona uygulanmaz.
DENETIM_DISI = {"README.md"}
notlar = sorted(p for p in VAULT.rglob("*.md") if p.name not in DENETIM_DISI)
adlar = {}
for p in notlar:
    adlar.setdefault(p.stem, []).append(p.relative_to(VAULT))

# 1 + 4: frontmatter ve bayatlik
bugun = datetime.date.today()
for p in notlar:
    metin = p.read_text(encoding="utf-8")
    fm = frontmatter(metin)
    rel = p.relative_to(VAULT)
    if fm is None:
        sorunlar.append(f"[frontmatter] {rel}: yok veya bozuk")
        continue
    for alan in ("rol", "kapsam", "guncelleme", "durum"):
        if alan not in fm:
            sorunlar.append(f"[frontmatter] {rel}: '{alan}' alani eksik")
    if fm.get("durum") == "dogrulanmali":
        sorunlar.append(f"[dogrulanmali] {rel}: koda karsi dogrulanmayi bekliyor")
    if fm.get("rol") in MUTABLE_ROLLER and "guncelleme" in fm:
        try:
            g = datetime.date.fromisoformat(fm["guncelleme"])
            yas = (bugun - g).days
            if yas > BAYAT_GUN:
                sorunlar.append(
                    f"[bayat] {rel}: {yas} gundur guncellenmedi (rol={fm['rol']}) "
                    f"— koda karsi dogrula")
        except ValueError:
            sorunlar.append(f"[frontmatter] {rel}: guncelleme tarihi gecersiz")

# 2: ayni adli notlar
for ad, yollar in adlar.items():
    if len(yollar) > 1:
        sorunlar.append(f"[belirsiz ad] '{ad}' {len(yollar)} dosyada: "
                        + ", ".join(str(y) for y in yollar))

# 3 + 5: linkler
gelen = {ad: 0 for ad in adlar}
for p in notlar:
    govde = kodu_ayikla(p.read_text(encoding="utf-8"))
    for ham in re.findall(r"\[\[([^\]]+)\]\]", govde):
        hedef = ham.split("|")[0].strip()
        if hedef not in adlar:
            sorunlar.append(f"[kirik link] {p.relative_to(VAULT)} -> [[{hedef}]]")
        elif hedef != p.stem:
            gelen[hedef] += 1

for ad, sayi in gelen.items():
    if sayi == 0 and ad not in ("00-Index", "CLAUDE"):
        yol = adlar[ad][0]
        # oturum notlari yetim olabilir, sorun degil
        if not str(yol).startswith("04-Oturumlar"):
            sorunlar.append(f"[yetim] {yol}: hicbir nottan link verilmemis")

# 7: notlar/ klasoru kurallari — ad oneki, hub baglantisi, cikan link
ALAN_ONEK = {"01-Genel": "genel-", "02-API": "api-", "03-Web": "web-"}
ALAN_HUB = {"01-Genel": "genel-notlar", "02-API": "api-notlar", "03-Web": "web-notlar"}

hub_linkleri = {}
for alan, hub in ALAN_HUB.items():
    hub_yol = VAULT / alan / f"{hub}.md"
    if not hub_yol.exists():
        sorunlar.append(f"[hub yok] {alan}/{hub}.md bulunamadi")
        hub_linkleri[alan] = set()
        continue
    govde = kodu_ayikla(hub_yol.read_text(encoding="utf-8"))
    hub_linkleri[alan] = {m.split("|")[0].strip()
                          for m in re.findall(r"\[\[([^\]]+)\]\]", govde)}

for p2 in notlar:
    rel = p2.relative_to(VAULT)
    parcalar = rel.parts
    if len(parcalar) < 3 or parcalar[1] != "notlar":
        continue
    alan = parcalar[0]
    onek = ALAN_ONEK.get(alan)
    if onek and not p2.stem.startswith(onek):
        sorunlar.append(f"[not adi] {rel}: '{onek}' onekiyle baslamali")
    if p2.stem not in hub_linkleri.get(alan, set()):
        sorunlar.append(
            f"[baglanmamis not] {rel}: {ALAN_HUB[alan]}.md icinden linklenmemis")
    govde = kodu_ayikla(p2.read_text(encoding="utf-8"))
    cikan = [m for m in re.findall(r"\[\[([^\]]+)\]\]", govde)
             if m.split("|")[0].strip() != p2.stem]
    if not cikan:
        sorunlar.append(f"[yalitilmis not] {rel}: hicbir nota link vermiyor")

# 6: gerekcesiz karar girisi
for p in notlar:
    if not p.name.endswith("kararlar.md"):
        continue
    metin = p.read_text(encoding="utf-8")
    bloklar = re.split(r"\n## ", metin)[1:]
    for blok in bloklar:
        baslik = blok.splitlines()[0].strip()
        # "**Neden:**" ya da "**Neden — ...:**" gibi varyantlar kabul
        if "**Neden" not in blok:
            sorunlar.append(
                f"[gerekcesiz karar] {p.relative_to(VAULT)}: '{baslik}' "
                f"icinde **Neden:** yok")


# 8: her alanda desenler / gorevler / araclar var mi
ALAN_BOLME = {"01-Genel": "genel", "02-API": "api", "03-Web": "web"}
for alan, onek in ALAN_BOLME.items():
    for bolme in ("desenler", "gorevler", "araclar"):
        yol = VAULT / alan / f"{onek}-{bolme}.md"
        if not yol.exists():
            sorunlar.append(f"[bolme yok] {alan}/{onek}-{bolme}.md bulunamadi")

# 9: gorev panosu kurallari
GOREV_SATIRI = re.compile(r"^\s*-\s*\[( |~|x)\]\s*\*\*([A-Z]-\d+)\*\*")
tum_kimlikler = {}
for alan, onek in ALAN_BOLME.items():
    yol = VAULT / alan / f"{onek}-gorevler.md"
    if not yol.exists():
        continue
    rel = yol.relative_to(VAULT)
    metin = yol.read_text(encoding="utf-8")
    bolum = None
    yapiliyor = 0
    for satir in metin.splitlines():
        b = satir.strip()
        if b.startswith("## "):
            if "Yapılacak" in b:
                bolum = "yapilacak"
            elif "Yapılıyor" in b:
                bolum = "yapiliyor"
            elif "Tamamlandı" in b:
                bolum = "tamamlandi"
            else:
                bolum = None
            continue
        m = GOREV_SATIRI.match(satir)
        if not m:
            continue
        isaret, kimlik = m.group(1), m.group(2)
        if kimlik in tum_kimlikler:
            sorunlar.append(
                f"[gorev kimligi] {rel}: '{kimlik}' zaten {tum_kimlikler[kimlik]} icinde")
        else:
            tum_kimlikler[kimlik] = rel
        if bolum == "yapiliyor":
            yapiliyor += 1
        if bolum == "tamamlandi" and isaret != "x":
            sorunlar.append(f"[gorev] {rel}: '{kimlik}' Tamamlandi'da ama [x] degil")
    if yapiliyor > 3:
        sorunlar.append(
            f"[odak] {rel}: Yapiliyor bolumunde {yapiliyor} gorev var, en fazla 3 olmali")
    # Tamamlandi bolumundeki her gorevin Kanit satiri olmali
    if "## 🟢 Tamamlandı" in metin:
        kuyruk = metin.split("## 🟢 Tamamlandı", 1)[1]
        kuyruk = kuyruk.split("\nİlgili:", 1)[0]
        bloklar = re.split(r"\n(?=\s*-\s*\[)", kuyruk)
        for blok in bloklar:
            m = GOREV_SATIRI.match(blok.strip("\n"))
            if m and "Kanıt:" not in blok:
                sorunlar.append(
                    f"[kanitsiz gorev] {rel}: '{m.group(2)}' Tamamlandi'da ama "
                    f"'Kanıt:' satiri yok")

# 10: acilis.md tavani
acilis = VAULT / "01-Genel" / "acilis.md"
if not acilis.exists():
    sorunlar.append("[acilis yok] 01-Genel/acilis.md bulunamadi")
else:
    boy = len(acilis.read_text(encoding="utf-8"))
    if boy > 6000:
        sorunlar.append(
            f"[acilis sisti] 01-Genel/acilis.md {boy} karakter, tavan 6000 — budanmali")

# 11: durum.md tazeligi
durum = VAULT / "01-Genel" / "durum.md"
if durum.exists():
    fm = frontmatter(durum.read_text(encoding="utf-8")) or {}
    try:
        yas = (bugun - datetime.date.fromisoformat(fm.get("guncelleme", ""))).days
        if yas > 7:
            sorunlar.append(
                f"[durum bayat] 01-Genel/durum.md {yas} gundur guncellenmedi — "
                f"'nerede kaldik' cevabi burada yasiyor")
    except ValueError:
        pass

# 12: arac tablosunda bos gerekce
for alan, onek in ALAN_BOLME.items():
    yol = VAULT / alan / f"{onek}-araclar.md"
    if not yol.exists():
        continue
    for no, satir in enumerate(yol.read_text(encoding="utf-8").splitlines(), 1):
        b = satir.strip()
        if not b.startswith("|") or b.startswith("|---") or "Tetikleyici" in b:
            continue
        hucreler = [h.strip() for h in b.strip("|").split("|")]
        if len(hucreler) >= 3 and not hucreler[2]:
            sorunlar.append(
                f"[gerekcesiz arac] {yol.relative_to(VAULT)}:{no}: "
                f"'{hucreler[1]}' icin 'Neden' bos")


# 13: tasiyici gerekce cift yonlu mu
# "X ucuz cunku Y var" bicimindeki karar, Y'ye link vermeli; Y de geri referans
# tasimali. Kirilma Y tarafinda oldugu icin tek yon yetmez.
# 2026-08-24: BRIN/bolumlendirme celiskisi bu denetim olmadigi icin kacti.
DAYANAK = re.compile(r"\*\*Dayanak:\*\*(.+)")
DAYANANLAR = re.compile(r"\*\*Buna dayananlar:\*\*(.+)")
LINKLER = re.compile(r"\[\[([^\]|]+)")

geri_referans = {}   # hedef notun stem -> geri link verdigi notlarin stem kumesi
for p2 in notlar:
    metin = kodu_ayikla(p2.read_text(encoding="utf-8"))
    for m in DAYANANLAR.finditer(metin):
        geri_referans.setdefault(p2.stem, set()).update(
            h.strip() for h in LINKLER.findall(m.group(1)))

for p2 in notlar:
    metin = kodu_ayikla(p2.read_text(encoding="utf-8"))
    for no, satir in enumerate(metin.splitlines(), 1):
        m = DAYANAK.search(satir)
        if not m:
            continue
        hedefler = [h.strip() for h in LINKLER.findall(m.group(1))]
        if not hedefler:
            sorunlar.append(
                f"[dayanak linksiz] {p2.relative_to(VAULT)}:{no}: "
                f"'Dayanak' satiri hicbir nota link vermiyor")
            continue
        for hedef in hedefler:
            if p2.stem not in geri_referans.get(hedef, set()):
                sorunlar.append(
                    f"[dayanak tek yonlu] {p2.relative_to(VAULT)}:{no}: "
                    f"[[{hedef}]] icinde 'Buna dayananlar: [[{p2.stem}]]' yok — "
                    f"dayanak kalkarsa bu karar sessizce cokerdi")


# 14: gorev kimligi kaybi
# Vault kurali: iptal edilen gorev SILINMEZ, "iptal" olarak Tamamlandi'ya tasinir.
# Kural vardi, denetimi yoktu. 2026-08-24: bir aralikla-silme hatasi bes gorevi
# panodan yok etti; dogrula.py TEMIZ dedi cunku bicim bozulmamisti — yazili olan
# dogruydu, yazilmamis olan kayipti. Referans olarak git'teki son surum kullanilir.
import subprocess

def _git(args):
    try:
        r = subprocess.run(["git", "-C", str(VAULT)] + args,
                           capture_output=True, text=True, timeout=10)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None

KIMLIK = re.compile(r"\*\*([A-Z]-\d+)\*\*")

if _git(["rev-parse", "--git-dir"]) is not None:
    for alan, onek in ALAN_BOLME.items():
        yol = VAULT / alan / f"{onek}-gorevler.md"
        if not yol.exists():
            continue
        rel = yol.relative_to(VAULT).as_posix()
        # HEAD degil TUM gecmis taranir: kayip bir kez commit'lenirse HEAD onu
        # normal sayar. 2026-08-24'te tam bu oldu — silinmis hali commit'lendi.
        commitler = (_git(["log", "--format=%H", "-n", "50", "--", rel]) or "").split()
        gorulmus = set()
        for c in commitler:
            icerik = _git(["show", f"{c}:{rel}"])
            if icerik:
                gorulmus |= set(KIMLIK.findall(kodu_ayikla(icerik)))
        if not gorulmus:
            continue
        yeni_k = set(KIMLIK.findall(kodu_ayikla(yol.read_text(encoding="utf-8"))))
        kayip = sorted(gorulmus - yeni_k)
        if kayip:
            sorunlar.append(
                f"[gorev kimligi kayboldu] {rel}: {', '.join(kayip)} "
                f"panonun gecmisinde vardi, simdi yok — iptal edilen gorev silinmez, "
                f"'iptal' olarak Tamamlandi'ya tasinir")


# 15: mimari bayatligi — vault'a degil KODA karsi olculur
# 2026-08-26: `*-mimari.md` ne okuma ne yazma tablosundaydi. On commit boyunca
# api-mimari.md hic guncellenmedi ve "is uc noktasi hala yok" derken sekiz
# controller yazilmisti. Disiplin hatasi degildi — dosyanin bayatlamaktan baska
# yapabilecegi bir sey yoktu. Tetikleyici CLAUDE.md'ye eklendi; olcumu bu yapar.
#
# Olcut mtime DEGIL frontmatter'daki `guncelleme` — dosyaya dokunmak onu dogru
# yapmaz, beyan edilen tarih ile kodun gercegi karsilastirilir. Eklenen/silinen
# kaynak dosya sayilir: yeni dosya = yapi degisti. Icerik degisikligi yapiyi
# degistirmez, o yuzden --diff-filter=AD.
MIMARI_REPO = {
    "02-API": ("api-mimari.md", "DailyCruising.Back-End",
               (".cs", ".csproj", ".slnx")),
    "03-Web": ("web-mimari.md", "DailyCruising.Front-End",
               (".ts", ".tsx", ".js", ".jsx", ".css")),
}
YAPISAL_ESIK = 10
YOL_DISI = ("obj/", "bin/", "node_modules/", ".next/", "dist/", "Migrations/Designer")


def _git_repo(repo, args):
    try:
        r = subprocess.run(["git", "-C", str(repo)] + args,
                           capture_output=True, text=True, timeout=15)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


for alan, (dosya, repo_adi, uzantilar) in MIMARI_REPO.items():
    yol = VAULT / alan / dosya
    repo = VAULT.parent / repo_adi
    if not yol.exists() or not repo.exists():
        continue
    fm = frontmatter(yol.read_text(encoding="utf-8")) or {}
    tarih = fm.get("guncelleme")
    if not tarih or not re.match(r"^\d{4}-\d{2}-\d{2}$", tarih):
        sorunlar.append(f"[mimari tarihsiz] {alan}/{dosya}: frontmatter'da "
                        f"gecerli `guncelleme` yok — insan okuru icin gerekli")
    if _git_repo(repo, ["rev-parse", "--git-dir"]) is None:
        continue

    # Olcut: mimari dosyasinin VAULT'taki commit zaman damgasi.
    # 2026-08-27: ilk surum `guncelleme` beyanini (gun cozunurlugu) kullaniyordu ve
    # yanlis pozitif verdi — web-mimari.md 08-27 03:25'te commit'lenmisti, sayilan
    # 20 dosya 08-26 04:15'te eklenmisti, yani mimari koddan 23 saat SONRA
    # guncellenmisti. Gun cozunurlugu bunu goremiyor ve **kontrolun ogrettigi
    # davranisi cezalandiriyordu**: ayni gun hem kod yazip hem mimariyi guncelleyen
    # oturum ertesi gun kirmizi goruyordu.
    #
    # Commit zamani mtime DEGILDIR: dosyaya dokunmak commit uretmez, icerik
    # degismeden git kayit tutmaz. Yani "beyan olculur, dokunma olculmez" ilkesi
    # korunuyor, yalniz cozunurluk saniyeye iniyor.
    #
    # 2026-08-31: ikinci yanlis — `kirli` olan dosya "az once yazilmis" sayilip
    # ATLANIYORDU. Bu, vault oturumunun bakis acisiydi: yaz, hemen commit'le.
    # Ama KURAL GEREGI alan oturumlari vault'a yazar ve **commit atmaz** —
    # commit'i vault oturumu atar. Yani api-mimari.md ve web-mimari.md gunlerce
    # kirli durur ve kontrol tam da izlemesi gereken dosyalar icin **kalici olarak
    # susar**. Nitekim api-mimari.md "21 controller" derken 28 vardi, "katalog,
    # arama, mesajlasma HALA YOK" derken sekizi de yazilmisti — kontrol 15
    # calisiyordu ve hicbir sey demedi. Bulan, kontrol 17'nin yan etkisiydi.
    #
    # Duzeltme: kirli dosyada olcut **mtime**. Bu, "dokunma olculmez" ilkesini
    # bozmaz — `git status` dosyayi ancak ICERIGI HEAD'den farkliysa kirli
    # gosterir. Salt dokunma kirli uretmez, dolayisiyla mtime burada gercek bir
    # icerik degisikliginin zamanidir.
    kirli = (_git(["status", "--porcelain", "--", yol.relative_to(VAULT).as_posix()]) or "").strip()
    if kirli:
        zaman = datetime.datetime.fromtimestamp(
            yol.stat().st_mtime).astimezone().isoformat()
    else:
        zaman = (_git(["log", "-1", "--format=%cI", "--",
                       yol.relative_to(VAULT).as_posix()]) or "").strip()
    if not zaman:
        zaman = tarih     # hic commit'lenmemis: beyana geri dus
    cikti = _git_repo(repo, ["log", f"--since={zaman}", "--diff-filter=AD",
                             "--name-only", "--format="])
    if cikti is None:
        continue
    degisen = {
        s.strip() for s in cikti.splitlines()
        if s.strip() and s.strip().endswith(uzantilar)
        and not any(h in s for h in YOL_DISI)
    }
    olcumler.append(
        f"kontrol 15 · {alan}/{dosya}: olcut {zaman[:16]} "
        f"({'kirli, mtime' if kirli else 'commit'}) -> "
        f"{len(degisen)}/{YAPISAL_ESIK} yapisal dosya")
    if len(degisen) >= YAPISAL_ESIK:
        sorunlar.append(
            f"[mimari bayat] {alan}/{dosya}: son yazimindan ({zaman[:16]}) bu "
            f"yana {repo_adi} icinde {len(degisen)} kaynak dosya eklendi/silindi. "
            f"Yapi degisti, mimari yazilmadi — dosya 'ne var' sorusuna yanlis cevap veriyor")



# 16: acilis.md, durum.md'nin gerisinde kalmis mi
# acilis.md her oturuma OTOMATIK yuklenir; durum.md'nin ozetidir. 2026-08-27'de
# olculdu: "API: yalniz /api/health calisiyor, sirada sema" diyordu — o an 21
# controller, 69 yol, 106 tablo vardi. Bes iddiasinin besi de yanlisti.
#
# Bu, api-mimari.md'nin bayatlamasindan DAHA agir: o dosya ne okunuyor ne
# yaziliyordu, sessizce curudu. acilis.md **her oturumda okunuyor** ama hicbir
# tetikleyici onu yazmiyordu — yani bayat bilgi her oturumun baglamina
# enjekte ediliyordu. **Okunup yazilmayan dosya, hic okunmayandan kotudur.**
ACILIS_ESIK = 3
if _git(["rev-parse", "--git-dir"]) is not None:
    a_yol, d_yol = VAULT / "01-Genel/acilis.md", VAULT / "01-Genel/durum.md"
    if a_yol.exists() and d_yol.exists():
        a_rel, d_rel = "01-Genel/acilis.md", "01-Genel/durum.md"
        kirli_a = (_git(["status", "--porcelain", "--", a_rel]) or "").strip()
        a_zaman = (_git(["log", "-1", "--format=%cI", "--", a_rel]) or "").strip()
        if not kirli_a and a_zaman:
            n = len((_git(["log", f"--since={a_zaman}", "--format=%H",
                           "--", d_rel]) or "").split())
            if n >= ACILIS_ESIK:
                sorunlar.append(
                    f"[acilis geride] 01-Genel/acilis.md son commit'inden "
                    f"({a_zaman[:16]}) bu yana durum.md {n} kez degisti. "
                    f"acilis her oturuma otomatik yuklenir — bayat kalirsa yanlis "
                    f"bilgi her oturumun baglamina girer")


# ---------------------------------------------------------------------------
# 17: Yapilacak bolumunde bitmis gorev duruyor mu
#
# 2026-08-28'de api-gorevler.md'de 21 bitmis gorev Yapilacak bolumunde bulundu;
# 2026-08-31'de ayni sey uc panoda birden vardi. Sonuc sayim hatasi: web oturumu
# "5 kaldi" derken pano 9 gosteriyordu, aradaki 4 bitmis isti.
#
# Bu bir disiplin hatasi degil — gorevi bitirirken kanit satirini yazmak akilda
# kaliyor, bolumler arasi tasimak kalmiyor. Olculmedigi surece pano her gun biraz
# daha yaniltir: "yapilacak" sayisi isin degil, tasinmamis satirin sayisidir.
PANO_DOSYALARI = [
    "01-Genel/genel-gorevler.md",
    "02-API/api-gorevler.md",
    "03-Web/web-gorevler.md",
]
for rel in PANO_DOSYALARI:
    yol = VAULT / rel
    if not yol.exists():
        olcumler.append(f"kontrol 17 · {rel}: DOSYA YOK — taranmadi")
        continue
    _bakilan = 0
    metin = yol.read_text(encoding="utf-8")
    # Yalniz "Yapilacak" bolumunun govdesi
    bloklar = re.split(r"^## ", metin, flags=re.M)
    for blok in bloklar:
        if not blok.lstrip().startswith(("🔵", "Yapılacak")):
            continue
        for satir in blok.split("\n"):
            if not re.match(r"^- \[[ x~]\] \*\*", satir):
                continue
            _bakilan += 1
            kimlik = re.search(r"\*\*([A-ZĞÜŞİÖÇ]+-\d+[a-z]?)\*\*", satir)
            kimlik = kimlik.group(1) if kimlik else "?"
            if satir.startswith("- [x]") or "bitti:" in satir:
                sorunlar.append(
                    f"[pano kaymasi] {rel}: {kimlik} Yapilacak bolumunde ama "
                    f"bitmis gorunuyor — Tamamlandi'ya tasinmali")
    olcumler.append(f"kontrol 17 · {rel}: {_bakilan} acik gorev incelendi")

    # 18: ayni bolum basligi iki kez varsa biri sessizce gormezden gelinir.
    # 2026-08-31: genel-gorevler.md'de bos bir ikinci "🔵 Yapilacak" basligi
    # bulundu — G-03/G-04 tasima betiginin artigi. Kontrol 17 gormedi cunku
    # yalniz MADDELERE bakiyor, bolum YAPISINA bakmiyordu. Bir gorev yanlis
    # baslik altina yazilsaydi panodan dusecekti ve hicbir kontrol konusmayacakti.
    basliklar = [b.strip() for b in re.findall(r"^## (.+)$", metin, re.M)]
    for b in set(basliklar):
        if basliklar.count(b) > 1:
            sorunlar.append(
                f"[yinelenen baslik] {rel}: '{b}' {basliklar.count(b)} kez var — "
                f"birine yazilan gorev digerinde gorunmez, pano sessizce eksilir")



print(f"Vault: {VAULT}")
print(f"Not sayisi: {len(notlar)}")
if olcumler:
    print()
    print("OLCUM OZETI — sorun uretmeyen kontroller de burada:")
    for o in olcumler:
        print("  " + o)
print()
if sorunlar:
    print(f"SORUN: {len(sorunlar)}")
    for s in sorunlar:
        print("  " + s)
    sys.exit(1)
print("TEMIZ — sorun bulunamadi")
sys.exit(0)
