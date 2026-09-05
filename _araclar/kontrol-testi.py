#!/usr/bin/env python3
"""
dogrula.py'nin KENDISINI olcer: her kontrolu bilerek bozar ve kirmiziya
dondugunu gorur.

Neden var
---------
2026-09-05, Y-14: backend `ForcePathStyle` satirini degistirdi, "600 test
yesil" dedi. Sonra olctu: degistirdigi satir hicbir testte KOSMUYORDU. Ayni
gun vault'a desen olarak yazildi — *"testler yesil demeden once degistirdigin
satirin kostugunu olc"* -> [[genel-desenler]].

O kural `dogrula.py`'ye hic uygulanmamisti. Ve tam bu korlugun iki ornegi
zaten yasanmisti:
  * kontrol 15, `if kirli: continue` muafiyeti yuzunden DOKUZ GUN boyunca
    tam da izledigi dosyalarda kor kaldi;
  * kontrol 17 yalniz maddelere bakip bolum yapisina bakmadigi icin bos
    yinelenen basligi gormedi.
Ikisi de "TEMIZ" yazarken kordu. **Susan denetim, dogru calistigi icin mi
susuyor yoksa bozuk oldugu icin mi — olcmeden ayirt edilemez.**

Nasil calisir
-------------
1. Vault, kod repolarinin YANINA kopyalanir (`../.vault-kontrol-testi`).
   Konum onemli: kontrol 15 ve 21 `VAULT.parent` altindaki kod repolarina
   bakar; baska bir yere kopyalanirsa ikisi sessizce atlanir — yani olcumu
   olcerken ayni korluge dusmus olurduk.
2. Once mutasyonsuz calistirilir: taban etiket sayimi alinir.
3. Her senaryo icin: kopya HEAD'e sifirlanir, tek bir bozma uygulanir,
   `dogrula.py` calistirilir, beklenen etiketin sayisi ARTMIS mi bakilir.
4. Artmadiysa o kontrol SESSIZ kalmistir: yazili ama olcmuyor.

Cikis kodu: 0 hepsi kirmiziya dondu, 1 en az bir kontrol sessiz kaldi.
Kullanim: python3 _araclar/kontrol-testi.py [--tut]   (--tut: kopyayi silme)
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
KOPYA = VAULT.parent / ".vault-kontrol-testi"
KOD_REPOLARI = ("DailyCruising.Back-End", "DailyCruising.Front-End")


# --- yardimcilar -----------------------------------------------------------

def oku(k, rel):
    return (k / rel).read_text(encoding="utf-8")


def yaz(k, rel, metin):
    (k / rel).write_text(metin, encoding="utf-8")


def ekle(k, rel, metin):
    yaz(k, rel, oku(k, rel) + metin)


def basliktan_sonra(k, rel, baslik, govde):
    metin = oku(k, rel)
    i = metin.index(baslik) + len(baslik)
    yaz(k, rel, metin[:i] + "\n" + govde + metin[i:])


def not_yaz(k, rel, govde):
    (k / rel).parent.mkdir(parents=True, exist_ok=True)
    yaz(k, rel, "---\nrol: not\nkapsam: genel\nguncelleme: 2026-09-05\n"
                "durum: guncel\n---\n\n# Deneme\n\n" + govde + "\n")


def git(k, *args, **kw):
    return subprocess.run(["git", "-C", str(k)] + list(args),
                          capture_output=True, text=True, **kw)


# --- bozma senaryolari -----------------------------------------------------
# Her biri GERCEK bir kusuru taklit eder; uydurma bir bicim hatasi degil.

def m_frontmatter(k):
    r = "01-Genel/genel-desenler.md"
    yaz(k, r, re.sub(r"^---\n.*?\n---\n", "", oku(k, r), flags=re.S))


def m_dogrulanmali(k):
    r = "02-API/api-mimari.md"
    yaz(k, r, oku(k, r).replace("durum: guncel", "durum: dogrulanmali", 1))


def m_bayat(k):
    for p in sorted(k.rglob("*.md")):
        if ".git" in p.parts:
            continue
        t = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        if m and re.search(r"^rol: (map|status|not)$", m.group(1), re.M):
            p.write_text(re.sub(r"^guncelleme: .*$", "guncelleme: 2026-01-01",
                                t, count=1, flags=re.M), encoding="utf-8")
            return


def m_belirsiz_ad(k):
    shutil.copy(k / "01-Genel/durum.md", k / "02-API/durum.md")


def m_kirik_link(k):
    ekle(k, "01-Genel/genel-notlar.md", "\n- [[olmayan-hedef-9999]]\n")


def m_yetim(k):
    not_yaz(k, "01-Genel/genel-deneme-yetim.md", "Kimse buna link vermiyor. [[durum]]")


def m_gerekcesiz_karar(k):
    ekle(k, "02-API/api-kararlar.md",
         "\n## 2099-01-01 — gerekcesiz deneme karari\n\nGerekce yazilmadi.\n")


def m_not_adi(k):
    not_yaz(k, "01-Genel/notlar/yanlis-onek-deneme.md", "[[durum]]")
    ekle(k, "01-Genel/genel-notlar.md", "\n- [[yanlis-onek-deneme]]\n")


def m_baglanmamis_not(k):
    not_yaz(k, "01-Genel/notlar/genel-deneme-hubsuz.md", "[[durum]]")


def m_yalitilmis_not(k):
    not_yaz(k, "01-Genel/notlar/genel-deneme-yalitilmis.md", "Hicbir yere link yok.")
    ekle(k, "01-Genel/genel-notlar.md", "\n- [[genel-deneme-yalitilmis]]\n")


def m_bolme_yok(k):
    (k / "02-API/api-araclar.md").unlink()


def m_gorev_kimligi(k):
    kimlik = re.search(r"\*\*(A-\d+)\*\*", oku(k, "02-API/api-gorevler.md")).group(1)
    basliktan_sonra(k, "03-Web/web-gorevler.md", "## 🟢 Tamamlandı",
                    f"\n- [x] **{kimlik}** deneme cakismasi\n      Kanıt: deneme\n")


def m_odak(k):
    satirlar = "".join(f"\n- [~] **Z-{i}** deneme · başlangıç: 2026-09-05\n"
                       for i in range(1, 5))
    basliktan_sonra(k, "01-Genel/genel-gorevler.md", "## 🟡 Yapılıyor", satirlar)


def m_kanitsiz_gorev(k):
    basliktan_sonra(k, "01-Genel/genel-gorevler.md", "## 🟢 Tamamlandı",
                    "\n- [x] **Z-90** kanitsiz deneme · bitti: 2026-09-05\n")


def m_acilis_sisti(k):
    ekle(k, "01-Genel/acilis.md", "\n" + ("dolgu " * 700))


def m_durum_bayat(k):
    r = "01-Genel/durum.md"
    yaz(k, r, re.sub(r"^guncelleme: .*$", "guncelleme: 2026-01-01",
                     oku(k, r), count=1, flags=re.M))


def m_gerekcesiz_arac(k):
    ekle(k, "01-Genel/genel-araclar.md", "\n| deneme tetikleyici | `deneme-arac` |  |\n")


def m_dayanak_tek_yonlu(k):
    ekle(k, "01-Genel/genel-desenler.md",
         "\n**Dayanak:** [[durum]] icindeki blocker tablosu\n")


def m_gorev_kimligi_kayboldu(k):
    r = "02-API/api-gorevler.md"
    metin = oku(k, r)
    kimlik = re.search(r"\*\*(A-\d+)\*\*", metin).group(1)
    yaz(k, r, "\n".join(s for s in metin.splitlines() if f"**{kimlik}**" not in s))


def m_mimari_bayat(k):
    r = "02-API/api-mimari.md"
    ekle(k, r, "\n<!-- deneme -->\n")          # kirli yap -> olcut mtime olur
    os.utime(k / r, (1751328000, 1751328000))  # 2025-07-01


def m_acilis_geride(k):
    for i in range(3):
        ekle(k, "01-Genel/durum.md", f"\n<!-- deneme {i} -->\n")
        git(k, "add", "01-Genel/durum.md")
        git(k, "-c", "user.email=d@d", "-c", "user.name=d",
            "commit", "-q", "-m", f"deneme {i}")


def m_pano_kaymasi(k):
    basliktan_sonra(k, "01-Genel/genel-gorevler.md", "## 🔵 Yapılacak",
                    "\n- [x] **Z-91** tasinmamis deneme · bitti: 2026-09-05\n")


def m_yinelenen_baslik(k):
    ekle(k, "01-Genel/genel-gorevler.md", "\n## 🔵 Yapılacak\n")


def m_beyan_geride(k):
    r = "01-Genel/genel-desenler.md"
    metin = re.sub(r"^guncelleme: .*$", "guncelleme: 2026-08-01",
                   oku(k, r), count=1, flags=re.M)
    yaz(k, r, metin + "\n<!-- beyan guncellenmeden icerik degisti -->\n")


def m_tetikleyicisiz(k):
    not_yaz(k, "01-Genel/genel-deneme-cok-atifli.md", "[[durum]]")
    ekle(k, "01-Genel/genel-notlar.md",
         "\n" + "- [[genel-deneme-cok-atifli]]\n" * 12)


def m_olu_atif(k):
    """Kodun atif verdigi bir vault dosyasinin adini degistir."""
    hedefler = {p.stem for p in k.rglob("*.md") if ".git" not in p.parts}
    for repo in KOD_REPOLARI:
        kok = k.parent / repo / "src"
        if not kok.exists():
            continue
        for f in kok.rglob("*"):
            if not f.is_file() or f.suffix not in (".cs", ".ts", ".tsx", ".md"):
                continue
            if any(h in f.parts for h in ("obj", "bin", "node_modules", ".next")):
                continue
            for ad in re.findall(r"\[\[([^\]|#\n]{2,60})\]\]",
                                 f.read_text(encoding="utf-8", errors="ignore")):
                ad = ad.strip()
                if ad in hedefler:
                    p = next(q for q in k.rglob(f"{ad}.md") if ".git" not in q.parts)
                    p.rename(p.with_name(f"{ad}-adi-degisti.md"))
                    return True
    return False


SENARYOLAR = [
    (1,  "frontmatter silindi",              "frontmatter",             m_frontmatter),
    (1,  "durum: dogrulanmali",              "dogrulanmali",            m_dogrulanmali),
    (4,  "mutable not 8 ay bayat",           "bayat",                   m_bayat),
    (2,  "ayni adli iki dosya",              "belirsiz ad",             m_belirsiz_ad),
    (3,  "olmayan hedefe link",              "kirik link",              m_kirik_link),
    (5,  "hicbir yerden linksiz not",        "yetim",                   m_yetim),
    (6,  "gerekcesiz karar girisi",          "gerekcesiz karar",        m_gerekcesiz_karar),
    (7,  "notlar/ altinda yanlis onek",      "not adi",                 m_not_adi),
    (7,  "hub'dan linklenmemis not",         "baglanmamis not",         m_baglanmamis_not),
    (7,  "cikan linki olmayan not",          "yalitilmis not",          m_yalitilmis_not),
    (8,  "bolme dosyasi silindi",            "bolme yok",               m_bolme_yok),
    (9,  "ayni gorev kimligi iki panoda",    "gorev kimligi",           m_gorev_kimligi),
    (9,  "Yapiliyor'da 4 gorev",             "odak",                    m_odak),
    (9,  "Tamamlandi'da Kanit yok",          "kanitsiz gorev",          m_kanitsiz_gorev),
    (10, "acilis.md tavani asti",            "acilis sisti",            m_acilis_sisti),
    (11, "durum.md 8 ay bayat",              "durum bayat",             m_durum_bayat),
    (12, "arac satirinda Neden bos",         "gerekcesiz arac",         m_gerekcesiz_arac),
    (13, "Dayanak tek yonlu",                "dayanak tek yonlu",       m_dayanak_tek_yonlu),
    (14, "panodan gorev satiri silindi",     "gorev kimligi kayboldu",  m_gorev_kimligi_kayboldu),
    (15, "mimari dosyasi kod gerisinde",     "mimari bayat",            m_mimari_bayat),
    (16, "durum 3 kez degisti acilis durdu", "acilis geride",           m_acilis_geride),
    (17, "bitmis gorev Yapilacak'ta",        "pano kaymasi",            m_pano_kaymasi),
    (18, "ayni bolum basligi iki kez",       "yinelenen baslik",        m_yinelenen_baslik),
    (19, "icerik degisti beyan degismedi",   "beyan geride",            m_beyan_geride),
    (20, "cok linkli dosyanin tetikleyicisi yok", "tetikleyicisiz",     m_tetikleyicisiz),
    (21, "kodun atif verdigi dosya adi degisti", "olu atif",            m_olu_atif),
]


# --- kosum -----------------------------------------------------------------

def dogrula_calistir(k):
    r = subprocess.run([sys.executable, str(k / "_araclar" / "dogrula.py")],
                       capture_output=True, text=True, timeout=600)
    return r.stdout + r.stderr


def etiket_sayimi(cikti):
    sayim = {}
    for satir in cikti.splitlines():
        m = re.match(r"\s+\[([a-z ]+)\]", satir)
        if m:
            sayim[m.group(1)] = sayim.get(m.group(1), 0) + 1
    return sayim


def main():
    tut = "--tut" in sys.argv
    eksik_repo = [r for r in KOD_REPOLARI if not (VAULT.parent / r).exists()]

    if KOPYA.exists():
        shutil.rmtree(KOPYA)
    shutil.copytree(VAULT, KOPYA, symlinks=True)
    bas = git(KOPYA, "rev-parse", "HEAD").stdout.strip()
    if shutil.which("rsync") is None:
        sys.exit("rsync yok — sifirlama bu araca bagli, kosum durduruldu")

    def sifirla():
        # git reset DEGIL rsync: reset kopyayi HEAD'e dondurur ve o zaman
        # olculen sey, calisma agacindaki dogrula.py degil COMMIT'LENMIS
        # surumu olur. Ilk surum tam bunu yapiyordu ve meta-testte yakalandi:
        # kontrol 18 bilerek kor edildi, arac yine "KIRMIZI" dedi cunku kor
        # surumu hic calistirmamisti. Aracin kendisi de olculmezse yalan soyler.
        subprocess.run(["rsync", "-a", "--delete", "--exclude", ".git",
                        str(VAULT) + "/", str(KOPYA) + "/"], check=True)
        git(KOPYA, "reset", "-q", bas)   # index'i geri al, calisma agacina dokunma

    taban = etiket_sayimi(dogrula_calistir(KOPYA))

    print(f"Kaynak : {VAULT}")
    print(f"Kopya  : {KOPYA}  (kod repolarinin yaninda — 15 ve 21 icin sart)")
    if eksik_repo:
        print(f"UYARI  : kod reposu yok: {', '.join(eksik_repo)} — "
              f"kontrol 15/21 olculemez")
    if taban:
        print(f"UYARI  : taban TEMIZ degil, mevcut etiketler: {sorted(taban)}")
        print("         olcut yine de dogru: etiket SAYISI artti mi bakilir.")
    print()

    sonuc = []
    for no, ad, etiket, fn in SENARYOLAR:
        sifirla()
        try:
            if fn(KOPYA) is False:
                sonuc.append((no, ad, etiket, "OLCULEMEDI",
                              "bozulacak hedef bulunamadi"))
                continue
        except Exception as e:
            sonuc.append((no, ad, etiket, "OLCULEMEDI", f"bozma hatasi: {e}"))
            continue
        sayim = etiket_sayimi(dogrula_calistir(KOPYA))
        arttimi = sayim.get(etiket, 0) > taban.get(etiket, 0)
        sonuc.append((no, ad, etiket, "KIRMIZI" if arttimi else "SESSIZ", ""))

    sifirla()
    if not tut:
        shutil.rmtree(KOPYA)

    genislik = max(len(a) for _, a, _, _, _ in sonuc)
    print("kontrol · senaryo".ljust(genislik + 12) + "beklenen etiket        sonuc")
    print("-" * (genislik + 50))
    sessiz = 0
    for no, ad, etiket, durum, aciklama in sonuc:
        if durum != "KIRMIZI":
            sessiz += 1
        print(f"{no:>7} · {ad.ljust(genislik)}  [{etiket}]".ljust(genislik + 35)
              + f" {durum} {aciklama}")

    print()
    kapsanan = sorted({no for no, *_ in SENARYOLAR})
    print(f"{len(SENARYOLAR)} senaryo · {len(kapsanan)} kontrol kapsandi: {kapsanan}")
    if sessiz:
        print(f"\n{sessiz} kontrol KIRMIZIYA DONMEDI — yazili ama olcmuyor.")
        sys.exit(1)
    print("\nHEPSI KIRMIZIYA DONDU — her kontrol gercekten olcuyor.")
    sys.exit(0)


if __name__ == "__main__":
    main()
