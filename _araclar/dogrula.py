#!/usr/bin/env python3
"""
Vault saglik kontrolu. Projeye bagli her sey `_araclar/vault.json`'da.

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
 17. Yapilacak bolumunde bitmis gorev
 18. Yinelenen bolum basligi
 19. Beyan (guncelleme) icerikten geride mi
 20. Cok linkli dosyanin tetikleyicisi var mi
 21. Kodun verdigi vault atiflari olu mu
 22. acilis.md'deki sayilar kaynagiyla celisiyor mu
 23. Alan durumu kod reposundaki commit'lerin gerisinde mi
 24. Yazili desen kodda cignenmis mi (cirnik: borc buyuyemez)

Kullanim: python3 _araclar/dogrula.py
Cikis kodu: 0 temiz, 1 sorun var
"""
import collections
from datetime import datetime
import re
import sys
import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

# 2026-09-05: proje adlari, klasor adlari ve esikler betikten cikarildi.
# Sebep sablonlastirma (`G-15`): makine tasinabilir olmali, icerik tasinmamali.
# Yapilandirma YOKSA sessizce varsayilana dusulmez — sessiz varsayilan, yanlis
# projeyi olcen bir denetim demektir; bu vault'ta en pahali kusur biçimi odur.
import json
_AYAR_YOLU = Path(__file__).resolve().parent / "vault.json"
if not _AYAR_YOLU.exists():
    sys.exit(f"vault.json yok ({_AYAR_YOLU}) — makine yapilandirmasiz calismaz")
AYAR = json.loads(_AYAR_YOLU.read_text(encoding="utf-8"))
ESIK = AYAR["esikler"]
PANO = AYAR["pano"]
OZEL = AYAR["ozel"]

BAYAT_GUN = ESIK["bayat_gun"]
MUTABLE_ROLLER = set(AYAR["mutable_roller"])

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
DENETIM_DISI = set(AYAR["denetim_disi"])
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
    if sayi == 0 and ad not in set(AYAR["yetim_muaf"]):
        yol = adlar[ad][0]
        # oturum notlari yetim olabilir, sorun degil
        if not str(yol).startswith(AYAR["arsiv_klasoru"]):
            sorunlar.append(f"[yetim] {yol}: hicbir nottan link verilmemis")

# 7: notlar/ klasoru kurallari — ad oneki, hub baglantisi, cikan link
ALAN_ONEK = {a: v["onek"] + "-" for a, v in AYAR["alanlar"].items()}
ALAN_HUB = {a: v["onek"] + "-notlar" for a, v in AYAR["alanlar"].items()}
NOTLAR_KLASORU = AYAR["notlar_klasoru"]

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
    if len(parcalar) < 3 or parcalar[1] != NOTLAR_KLASORU:
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
_karar_sayaci = collections.defaultdict(lambda: [0, 0, 0])
for p in notlar:
    if not p.name.endswith("kararlar.md"):
        continue
    metin = p.read_text(encoding="utf-8")
    bloklar = re.split(r"\n## ", metin)[1:]
    for blok in bloklar:
        baslik = blok.splitlines()[0].strip()
        # "**Neden:**" ya da "**Neden — ...:**" gibi varyantlar kabul
        if AYAR["isaretler"]["neden"] not in blok:
            sorunlar.append(
                f"[gerekcesiz karar] {p.relative_to(VAULT)}: '{baslik}' "
                f"icinde **Neden:** yok")
        # 2026-09-09: sablonun iki zorunlu satiri kaldirildi. `Sonucu` 225
        # kararin HICBIRINDE yoktu — unutuldugu icin degil, karar aninda var
        # olmayan bilgiyi istedigi icin. `Alternatifler` basligi %7'deydi ama
        # icerigi duzyazida cok daha sik geciyordu: ihtiyac gercek, kalip yanlis.
        #
        # Yerlerine DAYATMA degil OLCUM kondu. Sebebi olculmus: %0'da duran
        # zorunlu satir, yanindaki `**Neden:**`i de %61'de tutmustu. Ucuncu bir
        # olu satir eklemek ayni bedeli yeniden odemek olurdu.
        # Oran her kosumda basilir; dusesse gorunur, sessizce curumez.
        _karar_sayaci[p.name][0] += 1
        if re.search(AYAR["isaretler"]["elenen_deseni"], blok, re.I):
            _karar_sayaci[p.name][1] += 1
        if re.search(AYAR["isaretler"]["bedel_deseni"], blok, re.I):
            _karar_sayaci[p.name][2] += 1

for _ad, (_t, _e, _b) in sorted(_karar_sayaci.items()):
    if _t:
        olcumler.append(
            f"kontrol 6 · {_ad}: {_t} karar · elenen secenek {_e} "
            f"({_e * 100 // _t}%) · bedel {_b} ({_b * 100 // _t}%) "
            f"— OLCUM, dayatma degil · olcut: vault.json isaretler."
            f"elenen_deseni / bedel_deseni")

# 8: her alanda desenler / gorevler / araclar var mi
ALAN_BOLME = {a: v["onek"] for a, v in AYAR["alanlar"].items()}
for alan, onek in ALAN_BOLME.items():
    for bolme in AYAR["bolmeler"]:
        yol = VAULT / alan / f"{onek}-{bolme}.md"
        if not yol.exists():
            sorunlar.append(f"[bolme yok] {alan}/{onek}-{bolme}.md bulunamadi")

# 9: gorev panosu kurallari
GOREV_SATIRI = re.compile(PANO["gorev_deseni"])
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
            if PANO["yapilacak"] in b:
                bolum = "yapilacak"
            elif PANO["yapiliyor"] in b:
                bolum = "yapiliyor"
            elif PANO["tamamlandi"] in b:
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
    if yapiliyor > ESIK["yapiliyor_en_fazla"]:
        sorunlar.append(
            f"[odak] {rel}: Yapiliyor bolumunde {yapiliyor} gorev var, "
            f"en fazla {ESIK['yapiliyor_en_fazla']} olmali")
    # Tamamlandi bolumundeki her gorevin Kanit satiri olmali
    if PANO["tamamlandi_basligi"] in metin:
        kuyruk = metin.split(PANO["tamamlandi_basligi"], 1)[1]
        kuyruk = kuyruk.split("\nİlgili:", 1)[0]
        bloklar = re.split(r"\n(?=\s*-\s*\[)", kuyruk)
        for blok in bloklar:
            m = GOREV_SATIRI.match(blok.strip("\n"))
            if m and PANO["kanit"] not in blok:
                sorunlar.append(
                    f"[kanitsiz gorev] {rel}: '{m.group(2)}' Tamamlandi'da ama "
                    f"'{PANO['kanit']}' satiri yok")

# 10: acilis.md tavani
acilis = VAULT / OZEL["acilis"]
if not acilis.exists():
    sorunlar.append(f"[acilis yok] {OZEL['acilis']} bulunamadi")
else:
    boy = len(acilis.read_text(encoding="utf-8"))
    if boy > ESIK["acilis_tavan_karakter"]:
        sorunlar.append(
            f"[acilis sisti] {OZEL['acilis']} {boy} karakter, "
            f"tavan {ESIK['acilis_tavan_karakter']} — budanmali")

# 11: durum.md tazeligi
durum = VAULT / OZEL["durum"]
if durum.exists():
    fm = frontmatter(durum.read_text(encoding="utf-8")) or {}
    try:
        yas = (bugun - datetime.date.fromisoformat(fm.get("guncelleme", ""))).days
        if yas > ESIK["durum_bayat_gun"]:
            sorunlar.append(
                f"[durum bayat] {OZEL['durum']} {yas} gundur guncellenmedi — "
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
DAYANAK = re.compile(AYAR["isaretler"]["dayanak"])
DAYANANLAR = re.compile(AYAR["isaretler"]["dayananlar"])
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

KIMLIK = re.compile(PANO["kimlik_deseni"])

if _git(["rev-parse", "--git-dir"]) is not None:
    for alan, onek in ALAN_BOLME.items():
        yol = VAULT / alan / f"{onek}-gorevler.md"
        if not yol.exists():
            continue
        rel = yol.relative_to(VAULT).as_posix()
        # HEAD degil TUM gecmis taranir: kayip bir kez commit'lenirse HEAD onu
        # normal sayar. 2026-08-24'te tam bu oldu — silinmis hali commit'lendi.
        commitler = (_git(["log", "--format=%H", "-n", str(ESIK["gorev_gecmisi_commit"]), "--", rel]) or "").split()
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
    alan: (v["onek"] + OZEL["mimari_soneki"], v["kod_repo"], tuple(v["uzantilar"]))
    for alan, v in AYAR["alanlar"].items() if v.get("kod_repo")
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
    # Sessiz atlama YASAK: yapilandirmada kod reposu yazan bir alan icin repo
    # bulunamiyorsa bu bir olcum bosluğudur, "sorun yok" degildir. Baska bir
    # projeye tasindiginda en olasi kusur tam da budur — yol yanlis yazilir ve
    # denetim hicbir sey demeden korlesir.
    if not yol.exists():
        olcumler.append(f"kontrol 15 · {alan}/{dosya}: DOSYA YOK — OLCULEMEDI")
        continue
    if not repo.exists():
        olcumler.append(f"kontrol 15 · {alan}: kod reposu yok ({repo}) — OLCULEMEDI")
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
ACILIS_ESIK = ESIK["acilis_geride_commit"]
if _git(["rev-parse", "--git-dir"]) is not None:
    a_yol, d_yol = VAULT / OZEL["acilis"], VAULT / OZEL["durum"]
    if a_yol.exists() and d_yol.exists():
        a_rel, d_rel = OZEL["acilis"], OZEL["durum"]
        kirli_a = (_git(["status", "--porcelain", "--", a_rel]) or "").strip()
        a_zaman = (_git(["log", "-1", "--format=%cI", "--", a_rel]) or "").strip()
        if not kirli_a and a_zaman:
            n = len((_git(["log", f"--since={a_zaman}", "--format=%H",
                           "--", d_rel]) or "").split())
            if n >= ACILIS_ESIK:
                sorunlar.append(
                    f"[acilis geride] {OZEL['acilis']} son commit'inden "
                    f"({a_zaman[:16]}) bu yana {OZEL['durum']} {n} kez degisti. "
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
PANO_DOSYALARI = [f"{a}/{v['onek']}-gorevler.md" for a, v in AYAR["alanlar"].items()]
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
        if not blok.lstrip().startswith((PANO["yapilacak_isareti"], PANO["yapilacak"])):
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


# ---------------------------------------------------------------------------
# 19: beyan edilen `guncelleme` ile dosyanin gercek son yazimi ortusuyor mu
#
# 2026-09-05: durum.md dort gun boyunca UC KEZ duzenlendi, `guncelleme` hep
# 2026-08-28 kaldi. Icerik guncel, beyan bayatti — ve vault'ta beyan **olculen
# seydir**: kontrol 7 (durum bayatligi) ve kontrol 15 ona bakiyor. Yani yanlis
# beyan yalniz insani degil, diger kontrolleri de yaniltiyordu.
#
# Bu bir dikkatsizlik degil, eksik kapi: dosyayi duzenlemek frontmatter'a
# dokunmayi gerektirmiyordu. Simdi gerektiriyor.
# 2026-09-05, ayni gun: ilk surum SABIT ALTI DOSYALIK bir liste kullaniyordu.
# Backend "iki degil alti dosyaydi" diye bildirdi — kontrol dogruyu soyluyordu
# ama EKSIK soyluyordu. Bu, ayni hafta ucuncu kez cikan sey: kontrol 15 muafiyet
# yuzunden, kontrol 17 kapsam yuzunden, bu da liste yuzunden dar kaldi.
# Cozum listeyi buyutmek DEGIL, listeyi kaldirmaktir: `guncelleme` beyan eden
# HER dosya olculur. Beyanda bulunmak izlenmeyi kabul etmektir.
BEYAN_TOLERANS = ESIK["beyan_tolerans_gun"]
_b19 = 0
if _git(["rev-parse", "--git-dir"]) is not None:
    _beyanli = sorted(
        y for y in VAULT.rglob("*.md")
        if "_araclar" not in y.parts and ".git" not in y.parts
    )
    for yol in _beyanli:
        rel = yol.relative_to(VAULT).as_posix()
        fm = frontmatter(yol.read_text(encoding="utf-8")) or {}
        beyan = fm.get("guncelleme")
        if not beyan or not re.match(r"^\d{4}-\d{2}-\d{2}$", beyan):
            continue          # kontrol 15 zaten tarihsizligi bildiriyor
        # Olcut dosyanin durumuna gore DEGISIR ve bu kasitlidir:
        #
        # KIRLI dosya  -> `mtime` = bu makinedeki gercek yazim ani. Kesin olcum,
        #                 ve duzeltmenin mumkun oldugu tek an: dosya heniiz
        #                 commit'lenmeden once oturum beyani duzeltebilir.
        # TEMIZ dosya  -> yalniz commit tarihi bilinir, ama vault'un KENDI KURALI
        #                 yazmayi commit'ten ayirir (alan oturumlari yazar, vault
        #                 oturumu commit'ler). Bir not 24'unde yazilip 27'sinde
        #                 toplu commit'lenebilir; beyan DOGRU, commit gec olur.
        #                 Bu yuzden burada tolerans var: ancak belirgin ihmal
        #                 (BEYAN_TOLERANS gunden fazla) bildirilir.
        #
        # 2026-09-05: tolerans yokken kontrol 55 dosya bildirdi ve neredeyse hepsi
        # toplu commit artefaktiydi. 55 uyari veren bir denetim okunmaz, kapatilir
        # → [[genel-desenler]] "Denetim, ogrettigi davranisi cezalandirmamali".
        kirli = (_git(["status", "--porcelain", "--", rel]) or "").strip()
        if kirli:
            gercek = datetime.date.fromtimestamp(yol.stat().st_mtime).isoformat()
            kaynak, tolerans = "diskteki son yazim", 0
        else:
            zaman = (_git(["log", "-1", "--format=%cI", "--", rel]) or "").strip()
            if not zaman:
                continue
            gercek, kaynak, tolerans = zaman[:10], "son commit", BEYAN_TOLERANS
        _fark = (datetime.date.fromisoformat(gercek)
                 - datetime.date.fromisoformat(beyan)).days
        if _fark > tolerans:
            sorunlar.append(
                f"[beyan geride] {rel}: frontmatter `guncelleme: {beyan}` diyor ama "
                f"{kaynak} {gercek}. Beyan olculen seydir — yanlis beyan diger "
                f"kontrolleri de yaniltir")
        _b19 += 1
    olcumler.append(f"kontrol 19 · {_b19} dosyanin beyani olculdu "
                    f"(kirli: tolerans yok · temiz: {BEYAN_TOLERANS} gun)")


# ---------------------------------------------------------------------------
# 20: cok linklenen ama tetikleyicisi olmayan dosya
#
# "Tetikleyicisi olmayan dosya curur" kurali 2026-08-26'da yazildi ve o gun
# api-mimari.md icin elle bulundu. 2026-09-05'te AYNI SEY api-sema.md'de cikti:
# 40 gelen link, `durum: guncel`, son yazim 24 Agustos — arada 54 migration ve
# 66 entity dosyasi degismis. Yani kural yaziliydi ve ihlali gorunmuyordu.
#
# Olcut: gelen wikilink sayisi >= esik VE dosya adi CLAUDE.md / acilis.md
# tetikleyici tablolarinda gecmiyor (joker `*-kararlar.md` bicimleri dahil).
# Cok linklenmek "bu dosyaya guveniliyor" demektir; tetikleyicisi yoksa o guven
# bakimsiz bir dosyaya yoneliyordur — en pahali bayatlik budur.
LINK_ESIK = ESIK["link_esigi"]
_tetik_metin = ""
for _t in AYAR["tetikleyici_dosyalari"]:
    _ty = VAULT / _t
    if _ty.exists():
        _tetik_metin += _ty.read_text(encoding="utf-8")
if _tetik_metin:
    _joker = set(re.findall(r"\*-([a-z]+)\.md", _tetik_metin))
    _gelen = {}
    for _f in VAULT.rglob("*.md"):
        if ".git" in _f.parts or _f.parts[0] == AYAR["arsiv_klasoru"]:
            continue
        for _m in re.findall(r"\[\[([^\]|#]+)", _f.read_text(encoding="utf-8")):
            _ad = _m.strip()
            _gelen[_ad] = _gelen.get(_ad, 0) + 1
    _yetim = []
    for _ad, _n in sorted(_gelen.items(), key=lambda x: -x[1]):
        if _n < LINK_ESIK:
            continue
        if _ad.split("-")[-1] in _joker:
            continue          # `*-kararlar.md` gibi joker tetikleyici kapsiyor
        # `notlar/` altindaki bir notun tetikleyicisi KENDI HUB'IDIR
        # (`*-notlar.md`, tabloda var). Ilk surum bunlari da bildirdi — olcut
        # gevsekti: dosyanin adina bakip yolunu gormemek.
        if any(_p.parent.name == NOTLAR_KLASORU for _p in VAULT.rglob(f"{_ad}.md")):
            continue
        if re.search(re.escape(_ad), _tetik_metin):
            continue
        _yetim.append((_ad, _n))
        sorunlar.append(
            f"[tetikleyicisiz] {_ad}: {_n} yerden linkli ama "
            f"{' / '.join(AYAR['tetikleyici_dosyalari'])} tetikleyici tablolarinda yok. Cok linklenen dosyaya guvenilir; "
            f"tetikleyicisi yoksa bakimsiz kalir ve guven bos yere yonelir")
    olcumler.append(
        f"kontrol 20 · {len(_gelen)} hedef, {LINK_ESIK}+ linkli olanlarda "
        f"{len(_yetim)} tetikleyicisiz")


# ---------------------------------------------------------------------------
# 21: koddaki `[[...]]` atiflari vault'ta var olan bir dosyayi gosteriyor mu
#
# 2026-09-05, web oturumunun kendi itirafi: kodda onlarca `→ [[web-desenler]]`
# atifi var ve o dosya o oturumda **hic acilmadi**. Atiflar oturum basi ozetten
# ve hafizadan yazilmis. Bu, kaynak gostermenin en kotu bicimi: okuyan kisi
# satirin belgeye dayandigini sanir, oysa dayanagi yazarin hatirladigi halidir.
#
# Bu kontrol atifin **dogrulugunu** olcemez — yalnizca hedefin VAR oldugunu.
# Yetersiz oldugu bilinerek yaziliyor; alternatifi hicbir sey olculmemesiydi.
# Olu atif (adi degismis veya silinmis dosya) sessizce yanlis yonlendirir.
KOD_REPOLARI = [f"{v['kod_repo']}/{v['kaynak']}" for v in AYAR["alanlar"].values()
                if v.get("kod_repo")]
_hedefler = {y.stem for y in VAULT.rglob("*.md")}
_atif_toplam, _olu = 0, {}
for _rel in KOD_REPOLARI:
    _kok = VAULT.parent / _rel
    if not _kok.exists():
        olcumler.append(f"kontrol 21 · kod koku yok ({_kok}) — OLCULEMEDI")
        continue
    for _f in _kok.rglob("*"):
        if not _f.is_file() or _f.suffix not in (
                ".cs", ".ts", ".tsx", ".js", ".jsx", ".css", ".md"):
            continue
        if any(h in _f.parts for h in ("obj", "bin", "node_modules", ".next")):
            continue
        try:
            _ic = _f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for _m in re.findall(r"\[\[([^\]|#\n]{2,60})\]\]", _ic):
            _ad = _m.strip()
            _atif_toplam += 1
            if _ad not in _hedefler:
                _olu.setdefault(_ad, []).append(
                    _f.relative_to(VAULT.parent).as_posix())
for _ad, _yerler in sorted(_olu.items()):
    sorunlar.append(
        f"[olu atif] kodda [[{_ad}]] geciyor ama vault'ta boyle bir dosya yok "
        f"({len(_yerler)} yerde, orn. {_yerler[0]}) — atif sessizce yanlis "
        f"yonlendiriyor")
if _atif_toplam:
    olcumler.append(
        f"kontrol 21 · kodda {_atif_toplam} vault atifi, {len(_olu)} olu hedef "
        f"(NOT: yalniz hedefin varligi olculur, iceriginin dogrulugu DEGIL)")


# ---------------------------------------------------------------------------
# 22: acilis.md'deki sayilar kaynagiyla celisiyor mu
#
# 2026-09-09'da elle olculdu: acilis.md "pano 3/93", "571 test", "25 rota"
# diyordu. Gercek: 6/152, 706 test, 41 rota. DORT sayinin dordu de yanlisti ve
# bu dosya HER OTURUMUN baglamina otomatik yukleniyor — yani yanlis sayi her
# oturumda yeniden dagitiliyordu.
#
# Kontrol 16 bunu neden yakalamadi: o, acilis'in durum.md'nin kac COMMIT
# gerisinde kaldigini olcer. acilis o gun commit'lenmisti, yani TAZE gorunuyordu.
# **Tazelik dogruluk degildir.** Bir dosyaya dokunmak icindeki sayiyi
# duzeltmez; olculecek sey dosyanin yasi degil, iddiasinin kaynagiyla uyumudur.
#
# Olcut: acilis bir OZETTIR, kaynagi baska dosyadir. Iki sinif iddia denetlenir:
#   (a) pano sayimi  -> panolarin gercek sayimiyla birebir eslesmeli
#   (b) "<sayi> <birim>" -> o birimin kaynak dosyalarinda ayni sayi gecmeli
# Hangi birimin nerede dogrulanacagi vault.json'da; betikte proje sabiti yok.
_A22 = AYAR.get("acilis_sayilari")
_acilis_yol = VAULT / OZEL["acilis"]
if _A22 and _acilis_yol.exists():
    _a_metin = kodu_ayikla(_acilis_yol.read_text(encoding="utf-8"))
    _rel_a = OZEL["acilis"]
    _bakilan22 = 0

    # (a) panolarin gercek sayimi: (acik, bitmis)
    _gercek_panolar = {}
    for _alan, _v in AYAR["alanlar"].items():
        _pano = VAULT / _alan / f"{_v['onek']}-gorevler.md"
        if not _pano.exists():
            continue
        _acik = _bitmis = 0
        for _blok in re.split(r"^## ", _pano.read_text(encoding="utf-8"), flags=re.M):
            _bas = _blok.lstrip()
            _satirlar = [x for x in _blok.split("\n")
                         if re.match(r"^- \[[ x~]\] \*\*", x)]
            if _bas.startswith((PANO["yapilacak_isareti"], PANO["yapilacak"])):
                _acik = len(_satirlar)
            elif PANO["tamamlandi"] in _bas.split("\n")[0]:
                _bitmis = len(_satirlar)
        _gercek_panolar[_alan] = (_acik, _bitmis)

    for _desen in _A22.get("pano_desenleri", []):
        for _m in re.finditer(_desen, _a_metin, re.I):
            _bakilan22 += 1
            _cift = (int(_m.group(1)), int(_m.group(2)))
            if _cift not in _gercek_panolar.values():
                _dogrusu = " · ".join(f"{a}: {v[0]}/{v[1]}"
                                      for a, v in sorted(_gercek_panolar.items()))
                sorunlar.append(
                    f"[acilis sayisi] {_rel_a}: '{_m.group(0).strip()}' hicbir "
                    f"panonun gercek sayimiyla eslesmiyor. Panolar -> {_dogrusu}. "
                    f"Bu dosya her oturuma otomatik yuklenir; yanlis sayi her "
                    f"oturumda yeniden dagitilir")

    # (b) birim iddialari kaynak dosyalarinda geciyor mu
    for _b in _A22.get("birimler", []):
        _kaynak_metin = ""
        _eksik_kaynak = []
        for _k in _b.get("kaynaklar", []):
            _ky = VAULT / _k
            if _ky.exists():
                _kaynak_metin += _ky.read_text(encoding="utf-8")
            else:
                _eksik_kaynak.append(_k)
        if _eksik_kaynak and not _kaynak_metin:
            olcumler.append(
                f"kontrol 22 · birim '{_b['desen']}': kaynak dosya yok "
                f"({', '.join(_eksik_kaynak)}) — OLCULEMEDI")
            continue
        # Kaynakta ayni birimin GUNCEL beyanlari.
        #
        # Iki olcut de kor testte elendi:
        #   "sayi dosyada bir yerde geciyor mu" -> "25 rota" aylar once yazilmis
        #     bir satir yuzunden aklandi. Bu dosyalar append-only tarihce;
        #     gecmisteki her sayi hala icinde duruyor.
        #   "dosyanin ilk veya son gecisi" -> api-durum'un DOGRU 706 degeri
        #     kirmizi yandi (yanlis pozitif). Yanlis alarm veren denetim,
        #     susan denetimden kotudur: birkac kez bagirinca kimse bakmaz.
        #
        # Gecerli olan: kaynagin GUNCEL bolgesi. Iki bicim de destekleniyor
        # cunku iki dosya ters sirada yaziyor — api-durum en yeniyi dosyanin
        # basina, web-mimari en yeni TARIHLI bolume koyuyor:
        #   (1) ilk tarihli basliktan onceki bolge (acilis/ozet bolumu)
        #   (2) en yeni tarihli basligin bolumu
        _gecerli = set()
        for _k in _b.get("kaynaklar", []):
            _ky = VAULT / _k
            if not _ky.exists():
                continue
            _t = _ky.read_text(encoding="utf-8")
            _tarihli = list(re.finditer(r"^## .*?(\d{4}-\d{2}-\d{2})", _t, re.M))
            _bolgeler = [_t[:_tarihli[0].start()] if _tarihli else _t]
            if _tarihli:
                # AYNI gunde birden fazla bolum olabilir; hepsi guncel sayilir.
                # Ilk surum yalniz ilk maksimumu aliyordu ve web-mimari'de aynı
                # tarihli iki bolumden yanlisini secip DOGRU olan "41 rota"yi
                # kirmizi yakti. Yanlis alarm, susmaktan daha hizli guven yakar.
                _en_yeni_tarih = max(m.group(1) for m in _tarihli)
                for _m2 in _tarihli:
                    if _m2.group(1) != _en_yeni_tarih:
                        continue
                    _son = _t.find("\n## ", _m2.end())
                    _bolgeler.append(_t[_m2.start():_son if _son > 0 else len(_t)])
                # Kaynak taraf, acilis'le AYNI kalibi kullanamaz. acilis
                # "725 test yesil" yaziyor; api-durum ayni seyi
                # "`dotnet test` 706/706" diye yaziyor — sayi kelimeden ONCE
                # degil SONRA. Ilk surum bu yuzden hicbir eslesme bulamadi ve
                # sessizce OLCULEMEDI dedi: yazili, calisiyor gorunen, hicbir
                # sey olcmeyen bir kontrol. Kor test yakaladi.
                # Olcut bu yuzden kalip degil YAKINLIK: birim kelimesinin
                # gectigi satirdaki her sayi gecerli beyan sayilir.
                _kelime = _b.get("kelime")
                for _bolge in _bolgeler:
                    for _satir in _bolge.split("\n"):
                        if _kelime and _kelime.lower() in _satir.lower():
                            _gecerli.update(re.findall(r"\d+", _satir))
        for _m in re.finditer(_b["desen"], _a_metin):
            _bakilan22 += 1
            if not _gecerli:
                # Kaynagi dosya degil HESAP olan birimler (not sayisi, kontrol
                # sayisi). Bunlari asagidaki uretici kosumu dogruluyor.
                olcumler.append(
                    f"kontrol 22 · '{_m.group(0).strip()}': kaynagi hesap — "
                    f"uretici kosumuyla dogrulaniyor")
            elif _m.group(1) not in _gecerli:
                sorunlar.append(
                    f"[acilis sayisi] {_rel_a}: '{_m.group(0).strip()}' kaynagin "
                    f"guncel beyani degil ({', '.join(_b['kaynaklar'])} guncel "
                    f"bolgesinde {sorted(_gecerli)} geciyor) — ozet, ozetledigi "
                    f"dosyadan kopmus")
    olcumler.append(
        f"kontrol 22 · {_rel_a}: {_bakilan22} sayi iddiasi kaynagiyla karsilastirildi")

    # Uretici dogrulamasi: acilis'teki sayilar URETILEN degerle ayni mi.
    # Metin karsilastirmasinin ulasamadigi iki sayi var — not ve kontrol
    # sayisi, cunku kaynaklari bir dosya degil hesabin kendisi. Onlari
    # dogrulamanin tek yolu ayni hesabi tekrar yapmak: uretici --kuru
    # kosulur, "degisiklik istiyorum" derse acilis ya elle duzenlenmis ya
    # betik calistirilmamistir. Ikisi de hata.
    _uretici = VAULT / "_araclar" / "acilis-guncelle.py"
    if _uretici.exists():
        try:
            _u = subprocess.run([sys.executable, str(_uretici), "--kuru"],
                                capture_output=True, text=True, timeout=60)
        except Exception as _e:
            olcumler.append(f"kontrol 22 · uretici kosulamadi ({_e}) — OLCULEMEDI")
        else:
            if _u.returncode == 1:
                _istek = [x.strip() for x in _u.stdout.split("\n")
                          if x.startswith("  ")]
                sorunlar.append(
                    f"[acilis uretilmemis] {_rel_a}: uretici farkli deger "
                    f"hesapliyor ({'; '.join(_istek) or 'ayrinti yok'}). "
                    f"`python3 _araclar/acilis-guncelle.py` calistirilmali — "
                    f"elle yazilan sayi bir sonraki degisiklikte bayatlar")
            elif _u.returncode != 0:
                olcumler.append(
                    f"kontrol 22 · uretici hata verdi (kod {_u.returncode}) "
                    f"— OLCULEMEDI")
elif not _A22:
    olcumler.append("kontrol 22 · vault.json'da acilis_sayilari yok — OLCULEMEDI")


# ---------------------------------------------------------------------------
# 23: alan durumu, kod reposundaki commit'lerin gerisinde mi
#
# 2026-09-09'da backend oturumu kendi kusurunu bildirdi: o gun kod reposuna
# SEKIZ commit atti, `api-durum.md`'ye SIFIR kez yazdi. Sonuc, dosyanin tepesi
# "706/706 test" derken gercek 725'ti — ve o bayat sayi once acilis.md'ye,
# oradan her oturumun baglamina yayildi.
#
# Bu bir disiplin hatasi degildi: yazma tablosunda "alanin guncel durumu" satiri
# vardi ama NE ZAMAN yazilacagi yazmiyordu. Tetikleyicisi olmayan dosya curur —
# kuralin kendi ornegi, bu kez durum dosyasinda.
#
# Olcut mtime degil `guncelleme`: dosyaya dokunmak onu guncel yapmaz, beyan
# edilen tarih ile kodun gercegi karsilastirilir (kontrol 15 ile ayni ilke).
#
# ⚠️ SINIRI: bu kontrol TARIHE bakar, ICERIGE degil. Yesil olmasi dosyanin
# guncel oldugunu degil, TARIHININ guncel oldugunu soyler. 2026-09-09'da
# web-durum'un frontmatter'i bugunu, icerigi dunu anlatiyordu ve kontrol
# sustu. Sinir yazili olmazsa kontrol oldugundan guclu sanilir — bu vault'ta
# en pahali hata sinifi budur (kontrol 15 dokuz gun kor kalmisti).
for _alan, _v in AYAR["alanlar"].items():
    if not _v.get("kod_repo"):
        continue
    _dyol = VAULT / _alan / f"{_v['onek']}-durum.md"
    _repo = VAULT.parent / _v["kod_repo"]
    _rel_d = f"{_alan}/{_v['onek']}-durum.md"
    if not _dyol.exists():
        olcumler.append(f"kontrol 23 · {_rel_d}: DOSYA YOK — OLCULEMEDI")
        continue
    if not _repo.exists():
        olcumler.append(
            f"kontrol 23 · {_alan}: kod reposu yok ({_repo}) — OLCULEMEDI")
        continue
    _fm = frontmatter(_dyol.read_text(encoding="utf-8")) or {}
    _tarih = _fm.get("guncelleme")
    if not _tarih or not re.match(r"^\d{4}-\d{2}-\d{2}$", _tarih):
        olcumler.append(f"kontrol 23 · {_rel_d}: beyan tarihi yok — OLCULEMEDI")
        continue
    # Olcut: BEYAN EDILEN gun ile kod reposunun EN YENI commit gunu.
    #
    # Iki olcut denendi ve ikisi de kor testte elendi:
    #   "beyan gunu 00:00'dan beri kac commit" -> ayni gun dokuz commit atip
    #     sonunda durumu yazan oturum da kirmizi yandi (yanlis alarm).
    #   "dosyanin son yazilma ani" -> dosyaya dokunmak olcutu sifirliyordu;
    #     beyan 2026-01-01'e cekilse bile kontrol susuyordu (olcmuyordu).
    #
    # Kalan olcut gun karsilastirmasi: kod, durumun BEYAN ETTIGI gunden daha
    # yeni bir gunde ilerlemisse durum geridedir. Ayni gun icindeki sira
    # onemsiz — commit'ten sonra yazan oturum cezalandirilmaz, ertesi gune
    # birakan yakalanir.
    _son_commit = (_git_repo(_repo, ["log", "-1", "--format=%cs"]) or "").strip()
    if not _son_commit:
        olcumler.append(f"kontrol 23 · {_alan}: git okunamadi — OLCULEMEDI")
        continue
    if _son_commit > _tarih:
        _gun = (_git_repo(_repo, ["log", f"--since={_tarih} 23:59",
                                  "--format=%H"]) or "").split()
        sorunlar.append(
            f"[durum geride] {_rel_d}: beyan {_tarih}, kod reposunun son "
            f"commit'i {_son_commit} ({len(_gun)} commit sonrasinda). "
            f"Kod ilerledi, alanin durumu yazilmadi — bayat durum once "
            f"{OZEL['acilis']}'e, oradan her oturuma yayilir")
    else:
        olcumler.append(
            f"kontrol 23 · {_rel_d}: beyan {_tarih} · kod reposunun son "
            f"commit'i {_son_commit} — durum geride degil")



# ---------------------------------------------------------------------------
# 24: yazili desen kodda cignenmis mi
#
# 2026-09-09'da web oturumu kendi kusurunu bildirdi ve bu kontrolun gerekcesi
# oldu: `web-desenler`'e o gun ALTI KEZ yazdi, SIFIR kez karar vermek icin
# okudu. Somut bedeli: "sunucudaki sayinin kopyasi arayuzde tutulmaz" deseni
# yaziliydi ve parola ekraninda tam o kusur yasamaya devam ediyordu — deseni
# okuyarak degil, ucu OLCEREK bulundu.
#
# Ders: **yazili desen okunmuyor, olculen desen calisiyor.** Kontrol 8 desen
# DOSYASININ varligini olcuyordu; bu kontrol dosyanin ICINDEKI kuralin kodda
# tutulup tutulmadigini olcer.
#
# Olcut CIRNIK (ratchet): bugunku borc `tavan` olarak yazilidir, artarsa
# kirmizi yanar. Sifir gostermek yalan olurdu (91 sabit renk var); borcu
# gizlemeden buyumesini engellemenin yolu budur. Borc azalirsa betik tavani
# indirmeni soyler — kendi kendini sikan bir kural.
_D24 = (AYAR.get("desen_ihlalleri") or {}).get("kurallar", [])
for _k in _D24:
    _alan = AYAR["alanlar"].get(_k["alan"], {})
    _repo = _alan.get("kod_repo")
    if not _repo:
        olcumler.append(f"kontrol 24 · {_k['ad']}: alan yapilandirmasi yok — OLCULEMEDI")
        continue
    _kok = VAULT.parent / _repo / (_alan.get("kaynak") or ".")
    if not _kok.exists():
        olcumler.append(
            f"kontrol 24 · {_k['ad']}: kod koku yok ({_kok}) — OLCULEMEDI")
        continue
    # Betik tipi kural: olcum mantigi alanin kendi reposunda yasar, cirnigi
    # denetim uygular. Regex'e sigmayan olcutler icin (ornegin bir sozlugun
    # anahtar kumesinin enum kumesine esit olup olmadigi). Sozlesme tek satir:
    # betigin son satiri `IHLAL=<sayi>`.
    if _k.get("betik"):
        _byol = VAULT.parent / _repo / _k["betik"]
        if not _byol.exists():
            olcumler.append(
                f"kontrol 24 · {_k['ad']}: betik yok ({_byol}) — OLCULEMEDI")
            continue
        try:
            _b24 = subprocess.run([sys.executable, str(_byol)], cwd=str(VAULT.parent),
                                  capture_output=True, text=True, timeout=120)
        except Exception as _e24:
            olcumler.append(f"kontrol 24 · {_k['ad']}: betik kosulamadi ({_e24}) — OLCULEMEDI")
            continue
        _m24 = re.search(r"IHLAL=(\d+)\s*$", _b24.stdout.strip())
        if not _m24:
            olcumler.append(
                f"kontrol 24 · {_k['ad']}: betik IHLAL=<sayi> basmadi "
                f"(cikis {_b24.returncode}) — OLCULEMEDI")
            continue
        # Betigin kendi bildirdigi atlama/olcememe satirlari GORUNUR kalmali:
        # web oturumu uyardi — openapi.json yoksa betik IHLAL=0 basip cikiyor,
        # yani kural sessizce kapaniyor. Sessiz kapanan kural, olmayan kuraldir.
        for _satir_b in _b24.stdout.split("\n"):
            if re.search(r"atlan|olculem|ölçülem|bulunamad", _satir_b, re.I):
                olcumler.append(f"kontrol 24 · {_k['ad']}: betik diyor ki: {_satir_b.strip()}")
        _sayi24, _ornek24, _tavan24 = int(_m24.group(1)), "betik ciktisi", _k.get("tavan", 0)
        if _sayi24 > _tavan24:
            sorunlar.append(
                f"[desen ihlali] {_k['alan']} · {_k['ad']}: {_sayi24} yer, tavan "
                f"{_tavan24} ({_k['betik']} ciktisi). Yazili kural: {_k['kaynak']}")
        elif _sayi24 < _tavan24:
            olcumler.append(
                f"kontrol 24 · {_k['ad']}: {_sayi24} yer (tavan {_tavan24}) — "
                f"BORC AZALDI, vault.json'da tavani {_sayi24} yap")
        else:
            olcumler.append(
                f"kontrol 24 · {_k['ad']}: {_sayi24} yer, tavanda ({_k['betik']}) "
                f"— buyumesi kirmizi yanar")
        continue

    _desen24 = re.compile(_k["ara"])
    _uz = set(_k.get("uzantilar", []))
    _sayi24, _ornek24 = 0, None
    for _f24 in _kok.rglob("*"):
        if not _f24.is_file() or _f24.suffix not in _uz:
            continue
        _yol24 = _f24.as_posix()
        if any(_x in _yol24 for _x in _k.get("yol_disi", [])):
            continue
        if any(_h in _f24.parts for _h in ("node_modules", "obj", "bin", ".next")):
            continue
        try:
            _icerik24 = _f24.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Yorum satiri ihlal DEGILDIR. 2026-09-09'da backend olctu: 13 sayilan
        # `DateTime`in biri, "burada DateTime.UtcNow cagirma" diye YAZILMIS
        # UYARIYDI. Bir ihlali duzeltip yerine gerekcesini yazan kisi cirnikta
        # geri gitmis gorunuyordu — tesvik edilmek istenen davranis
        # cezalandiriliyordu. Ucunde de sayim sisikti: 13->12, 91->87, 5->1.
        #
        # ⚠️ Ilk surum satir basina bakiyordu ve `*` ile baslayan her satiri
        # yorum sayiyordu. Backend kor noktayi bildirdi: C#'ta bir satir carpma
        # isleminin devami olarak da `*` ile baslayabilir (`* oran`), yani
        # GERCEK bir ihlal sessizce dusebilirdi — yanlis alarmi kapatirken
        # yanlis sessizlik acmak. Bugun oyle bir satir yok (0 olculdu) ama bu
        # olcumdur, garanti degil; biçim degisirse kimse haber vermezdi.
        # Cozum tahmin degil DURUM: blok yorumun icinde miyiz, izleniyor.
        _blok24 = False
        for _no24, _satir24 in enumerate(_icerik24.split("\n"), 1):
            _sade24 = _satir24.strip()
            _yorum24 = _blok24
            if _blok24:
                if "*/" in _sade24:
                    _blok24 = False
                    _yorum24 = _sade24.split("*/", 1)[1].strip().startswith("//")
            elif _sade24.startswith(("//", "#", "<!--")):
                _yorum24 = True
            elif _sade24.startswith("/*"):
                _yorum24 = True
                _blok24 = "*/" not in _sade24
            if _yorum24:
                continue
            if _desen24.search(_satir24):
                _sayi24 += 1
                if _ornek24 is None:
                    _ornek24 = f"{_f24.relative_to(VAULT.parent).as_posix()}:{_no24}"
    _tavan24 = _k.get("tavan", 0)
    if _sayi24 > _tavan24:
        sorunlar.append(
            f"[desen ihlali] {_k['alan']} · {_k['ad']}: {_sayi24} yer, tavan "
            f"{_tavan24} (orn. {_ornek24}). Yazili kural: {_k['kaynak']}")
    elif _sayi24 < _tavan24:
        olcumler.append(
            f"kontrol 24 · {_k['ad']}: {_sayi24} yer (tavan {_tavan24}) — "
            f"BORC AZALDI, vault.json'da tavani {_sayi24} yap ki geri yukselmesin")
    else:
        olcumler.append(
            f"kontrol 24 · {_k['ad']}: {_sayi24} yer, tavanda — buyumesi kirmizi yanar")


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
