#!/usr/bin/env python3
"""
Vault notlarinin gercekten ACILIP acilmadigini olcer.

Neden var
---------
Vault'ta 82 not var ve hepsinin YAZILDIGINI biliyoruz — git bunu soyluyor.
Hicbirinin OKUNDUGUNU bilmiyoruz. Yazilip okunmayan not bedava degildir:
yer kaplar, bakim ister, arama sonuclarini kirletir ve en kotusu, "vault'ta
var" hissi verdigi icin ayni bilgiyi ikinci kez uretmeyi engeller —
bayat oldugunda ise tam da bu yuzden yaniltir.

Bu, sablonlastirmanin (`G-15`) on kosulu: yeni bir projeye 82 not
kopyalanmamali, yalnizca karsiligini odeyenler. Bugun hangisinin odedigini
soyleyemiyoruz.

Ne olculur
----------
Kaynak: `~/.claude/projects/<vault.json: oturum_kayit_deseni>/*.jsonl`.
  * OKUNDU   — Read araci, ya da okuma bicimli bir Bash komutu (cat/grep/sed)
  * YAZILDI  — Edit/Write araci, ya da yonlendirmeli Bash komutu (`> dosya`)
  * DISARIDAN-OKUMA — notu YAZAN oturumlarin disinda kac oturumda okundu.
               **Asil olcut budur:** kendi yazildigi oturumda gorunmek, bir
               notun ise yaradigini gostermez.
  * ATIF     — asistan metninde `[[ad]]` gecti ama dosya ACILMADI

⚠️ **Ne olculmez — bilerek yaziliyor:**
  * Acilan dosyanin okunup ANLASILDIGI olculmez, yalnizca acildigi.
  * `acilis.md` her oturuma hook ile OTOMATIK yuklenir; secilerek acilmaz.
    Ayri isaretlenir, yoksa en cok okunan dosya gibi gorunur.
  * Yalniz DISKTE DURAN oturum kayitlari taranir. Silinen oturumlarda
    okunmus bir not burada "hic okunmamis" gorunur — sayilar bir ALT SINIRDIR.
  * Bir notu okumak icin baska bir dosyanin icinden gecmek (hub) sayilmaz.

Kullanim: python3 _araclar/okunma.py [--tam]   (--tam: butun notlari listele)
"""
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import json

VAULT = Path(__file__).resolve().parent.parent
KAYITLAR = Path.home() / ".claude" / "projects"
AYAR = json.loads((Path(__file__).resolve().parent / "vault.json")
                  .read_text(encoding="utf-8"))
KAYIT_DESENI = AYAR["oturum_kayit_deseni"]
OTOMATIK = set(AYAR["otomatik_yuklenen"])   # hook yukluyor, secilerek acilmiyor
OKUMA_ARAC = {"Read", "NotebookRead"}
YAZMA_ARAC = {"Edit", "Write", "NotebookEdit"}
# Bash icin arac adi yetmez: `cat x.md` okur, `cat > x.md` yazar. Ilk surum
# ikisini de "acilma" sayiyordu ve bu, notu YAZAN oturumu da okuyucu gosterip
# sonucu 77/83 gibi sahte bir iyilige cikariyordu.
OKUMA_KOMUT = re.compile(r"\b(cat|bat|head|tail|sed|awk|grep|rg|less|more|wc|diff|open)\b")
YAZMA_KOMUT = re.compile(r"(>>?\s*\S*%s|\btee\b|write_text|\bmv\b|\bcp\b)")


def notlar():
    return {p.stem: p.relative_to(VAULT).as_posix()
            for p in VAULT.rglob("*.md") if ".git" not in p.parts}


def dosya_adaylari(girdi, arac):
    """Bir tool_use girdisinden vault dosya adlarini cikar."""
    parcalar = []
    for anahtar in ("file_path", "path", "notebook_path"):
        v = girdi.get(anahtar)
        if isinstance(v, str):
            parcalar.append(v)
    if arac in ("Bash", "BashOutput"):
        v = girdi.get("command")
        if isinstance(v, str):
            parcalar.append(v)
    if arac in ("Grep", "Glob"):
        for anahtar in ("pattern", "glob"):
            v = girdi.get(anahtar)
            if isinstance(v, str):
                parcalar.append(v)
    return parcalar


def main():
    tam = "--tam" in sys.argv
    ad_yol = notlar()
    # `durum` gibi kisa adlar metinde tesadufen gecebilir; yalniz `<ad>.md`
    # bicimi sayilir — dosyaya isaret ettigi kesin olan tek bicim budur.
    # ⚠️ Ilk surumde onunde-yasak sinifi `/` iceriyordu ve bu, TAM DA olcmek
    # istedigim bicimi — `01-Genel/durum.md` gibi yollari — eliyordu. Arac
    # "4 oturum" dedi, bagimsiz `grep -l` 73 dosya buldu. Ayni dersin ucuncu
    # tekrari: yesil bir cikti, dogru olcugunun kaniti degil.
    desen = re.compile(r"(?<![\w.-])(" + "|".join(
        re.escape(a) for a in sorted(ad_yol, key=len, reverse=True)) + r")\.md\b")
    wikilink = re.compile(r"\[\[([^\]|#\n]{2,60})\]\]")

    okuyan = defaultdict(set)    # ad -> {oturum}  (yalniz okuma)
    yazan = defaultdict(set)     # ad -> {oturum}  (yazma)
    atif = defaultdict(set)
    cagri = defaultdict(int)     # ad -> toplam dokunma sayisi
    belirsiz = defaultdict(int)  # okuma mi yazma mi ayirt edilemeyen Bash dokunusu
    son = {}
    dosyalar = sorted(KAYITLAR.glob(f"{KAYIT_DESENI}/*.jsonl"))
    satir_sayisi = 0

    for f in dosyalar:
        oturum = f.stem
        with f.open(encoding="utf-8", errors="ignore") as fh:
            for ham in fh:
                if '"tool_use"' not in ham and "[[" not in ham:
                    continue
                satir_sayisi += 1
                try:
                    kayit = json.loads(ham)
                except Exception:
                    continue
                if kayit.get("type") != "assistant":
                    continue
                tarih = (kayit.get("timestamp") or "")[:10]
                icerik = (kayit.get("message") or {}).get("content") or []
                if not isinstance(icerik, list):
                    continue
                for blok in icerik:
                    if not isinstance(blok, dict):
                        continue
                    if blok.get("type") == "tool_use":
                        arac = blok.get("name", "")
                        girdi = blok.get("input") or {}
                        if not isinstance(girdi, dict):
                            continue
                        for metin in dosya_adaylari(girdi, arac):
                            for ad in set(desen.findall(metin)):
                                cagri[ad] += 1
                                if tarih > son.get(ad, ""):
                                    son[ad] = tarih
                                if arac in YAZMA_ARAC:
                                    yazan[ad].add(oturum)
                                elif arac in OKUMA_ARAC:
                                    okuyan[ad].add(oturum)
                                elif arac in ("Bash", "BashOutput"):
                                    yazma_d = re.compile(
                                        r"(>>?\s*[^\s|;&]*" + re.escape(ad) +
                                        r"\.md|\btee\b[^\n]*" + re.escape(ad) + r"\.md)")
                                    if yazma_d.search(metin):
                                        yazan[ad].add(oturum)
                                    elif re.search(r"write_text|open\([^)]*['\"]w", metin):
                                        yazan[ad].add(oturum)
                                    elif OKUMA_KOMUT.search(metin):
                                        okuyan[ad].add(oturum)
                                    else:
                                        belirsiz[ad] += 1   # susmasin diye sayilir
                                else:
                                    okuyan[ad].add(oturum)
                    elif blok.get("type") == "text":
                        for ad in wikilink.findall(blok.get("text") or ""):
                            ad = ad.strip()
                            if ad in ad_yol:
                                atif[ad].add(oturum)

    # ASIL OLCUT: notu YAZAN oturumlarin disinda kac oturumda okundu.
    # Kendi yazildigi oturumda goriunmek, o notun ise yaradigini gostermez.
    satirlar = []
    for ad, yol in ad_yol.items():
        disaridan = okuyan[ad] - yazan[ad]
        satirlar.append((len(disaridan), len(okuyan[ad]), len(yazan[ad]),
                         len(atif[ad]), son.get(ad, "-"), yol, ad))
    satirlar.sort()

    hic = [s for s in satirlar if s[0] == 0]
    yalniz_atif = [s for s in hic if s[3] > 0]

    print(f"Vault : {VAULT}")
    print(f"Kaynak: {len(dosyalar)} oturum kaydi, {satir_sayisi} ilgili satir")
    print(f"Not   : {len(ad_yol)}")
    print()
    print("⚠️  ACILMA olculur, OKUNUP ANLASILMA degil. Sayilar bir ALT SINIRDIR:")
    print("    yalniz diskte duran oturum kayitlari taraniyor.")
    print()

    def yaz(baslik, kume):
        print(f"── {baslik} ({len(kume)})")
        for d, o, y, at, s, yol, ad in kume:
            im = " [otomatik yuklenir]" if ad in OTOMATIK else ""
            print(f"   disaridan-okuma {d:>3} · okuma {o:>3} · yazma {y:>3} · "
                  f"atif {at:>3} · son {s} · {yol}{im}")
        print()

    yaz("YAZILDIGI OTURUM DISINDA HIC OKUNMAMIS", hic)
    if yalniz_atif:
        print("   ⚠️ Bunlarin " + str(len(yalniz_atif)) +
              " tanesine ATIF verilmis ama dosya hic acilmamis:")
        for _, _, _, at, _, yol, _ in yalniz_atif:
            print(f"      {at} atif · {yol}")
        print("   Okunmadan verilen atif, belgesiz koddan kotudur -> [[genel-desenler]]")
        print()

    if tam:
        yaz("TAMAMI — az acilandan cok acilana", satirlar)
    else:
        yaz("EN COK ACILAN 12", satirlar[-12:][::-1])

    disaridan_okunan = sum(1 for s in satirlar if s[0] > 0)
    print(f"OZET: {disaridan_okunan}/{len(satirlar)} not, yazildigi oturum "
          f"DISINDA en az bir kez okundu · {len(hic)} not okunmadi")
    print(f"      siniflandirilamayan Bash dokunusu: {sum(belirsiz.values())} "
          f"({len([a for a in belirsiz if belirsiz[a]])} dosyada) — okuma da olabilir "
          f"yazma da; sayilar bu kadar belirsizlik payi tasir")


if __name__ == "__main__":
    main()
