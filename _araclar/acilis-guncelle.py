#!/usr/bin/env python3
"""acilis.md'deki sayilari URETIR — elle yazilmaz.

Neden var
---------
acilis.md her oturuma otomatik yuklenir. 2026-09-09'da AYNI GUN IKI KEZ bayatladi:
sabah dort sayisi da yanlisti (pano 3/93 -> 6/153, 571 -> 706 test, 25 -> 41 rota),
duzeltildi; birkac saat sonra `A-152` bitti ve iki tanesi yine kaydi.

Ders `api-sema`'da odenmisti: **her degisiklikte elle dokunulacak bir belge, ilk
yogun gunde atlanir** — ve atlandigi fark edilmez, cunku belge hala dogru gorunur.
Kontrol 22 sapmayi yakaliyor ama yakalamak duzeltmek degil; bu betik sapmanin
dogmasini engeller.

Ne yapar
--------
`vault.json: acilis_sayilari` yapilandirmasini okur ve acilis.md icindeki
sayilari kaynaklarindan yeniden uretir:
  * pano sayimlari -> panolarin kendi sayimi
  * birim iddialari (test, rota, not, kontrol) -> `cikar` alaninin gosterdigi
    otorite dosya ve desen

Cikaramadigi degeri **yazmaz**: OLCULEMEDI der ve metne dokunmaz. Uydurma sayi,
bayat sayidan kotudur — bayat olan en azindan bir zaman dogruydu.

Kullanim: python3 _araclar/acilis-guncelle.py [--kuru]
  --kuru : dosyaya yazmaz, ne degisecegini basar.
           Cikis kodu 0 = acilis guncel, 1 = uretilen deger metinden farkli.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
_ayar_yolu = (VAULT / "_araclar" / "vault.json")
try:
    AYAR = json.loads(_ayar_yolu.read_text(encoding="utf-8"))
except FileNotFoundError:
    sys.exit(f"HATA: yapilandirma dosyasi yok: {_ayar_yolu}")
except json.JSONDecodeError as _hata:
    sys.exit(f"HATA: {_ayar_yolu} gecerli JSON degil.\n"
             f"  Satir {_hata.lineno}, kolon {_hata.colno}: {_hata.msg}\n"
             f"  Duzeltip tekrar calistir; betik yapilandirmasiz calismaz.")
A = AYAR.get("acilis_sayilari") or {}
PANO = AYAR["pano"]
ACILIS = VAULT / AYAR["ozel"]["acilis"]
KURU = "--kuru" in sys.argv


def pano_sayimi(alan, onek):
    """Panonun gercek sayimi: (acik, bitmis)."""
    yol = VAULT / alan / f"{onek}-gorevler.md"
    if not yol.exists():
        return None
    acik = bitmis = 0
    for blok in re.split(r"^## ", yol.read_text(encoding="utf-8"), flags=re.M):
        bas = blok.lstrip()
        satirlar = [x for x in blok.split("\n") if re.match(r"^- \[[ x~]\] \*\*", x)]
        if bas.startswith((PANO["yapilacak_isareti"], PANO["yapilacak"])):
            acik = len(satirlar)
        elif PANO["tamamlandi"] in bas.split("\n")[0]:
            bitmis = len(satirlar)
    return acik, bitmis


def vault_md_sayisi():
    """dogrula.py'nin saydigi kume: denetim disi dosyalar haric."""
    disi = set(AYAR.get("denetim_disi", []))
    return sum(1 for p in VAULT.rglob("*.md")
               if ".git" not in p.parts and p.name not in disi)


def dogrula_kontrol_sayisi():
    """dogrula.py'nin bas yorumundaki numarali kontrol listesi."""
    metin = (VAULT / "_araclar" / "dogrula.py").read_text(encoding="utf-8")
    bas = metin.split('"""')[1] if '"""' in metin else ""
    return len(re.findall(r"^\s*\d+\.\s", bas, re.M))


def birim_degeri(b):
    """Bir birimin otorite degeri. Bulamazsa None — asla tahmin etmez."""
    c = b.get("cikar") or {}
    if c.get("sayim") == "vault_md":
        return vault_md_sayisi()
    if c.get("sayim") == "dogrula_kontrol":
        return dogrula_kontrol_sayisi()
    if not c.get("dosya"):
        return None
    yol = VAULT / c["dosya"]
    if not yol.exists():
        return None
    bulunan = re.findall(c["desen"], yol.read_text(encoding="utf-8"))
    if not bulunan:
        return None
    return int(bulunan[-1] if c.get("sec") == "son" else bulunan[0])


def bloklar(metin):
    """acilis'in '- **Etiket:**' madde bloklari: (baslangic, bitis) indeksleri."""
    yerler = [m.start() for m in re.finditer(r"^- \*\*", metin, re.M)]
    for i, b in enumerate(yerler):
        yield b, (yerler[i + 1] if i + 1 < len(yerler) else len(metin))


def main():
    if not A:
        sys.exit("vault.json'da acilis_sayilari yok — betik yapilandirmasiz calismaz")
    if not ACILIS.exists():
        sys.exit(f"{ACILIS} yok")

    metin = ACILIS.read_text(encoding="utf-8")
    yeni = metin
    degisenler, olculemeyenler, kor = [], [], []

    # 1) pano sayimlari — her alanin kendi madde blogunda
    for alan, etiket in A.get("alan_etiketleri", {}).items():
        onek = AYAR["alanlar"].get(alan, {}).get("onek")
        sayim = pano_sayimi(alan, onek) if onek else None
        if not sayim:
            olculemeyenler.append(f"{alan}: pano okunamadi")
            continue
        acik, bitmis = sayim
        for b, s in bloklar(yeni):
            blok = yeni[b:s]
            if etiket not in blok.split("\n")[0]:
                continue
            for desen in A.get("pano_desenleri", []):
                def _degistir(m, acik=acik, bitmis=bitmis, alan=alan):
                    eski = m.group(0)
                    yenisi = eski.replace(m.group(1), str(acik), 1)
                    i = yenisi.rindex(m.group(2))          # ikinci sayi
                    yenisi = yenisi[:i] + str(bitmis) + yenisi[i + len(m.group(2)):]
                    if eski != yenisi:
                        degisenler.append(
                            f"{alan} pano: {eski.strip()} -> {yenisi.strip()}")
                    return yenisi
                blok = re.sub(desen, _degistir, blok, flags=re.I)
            yeni = yeni[:b] + blok + yeni[s:]
            break

    # 2) birim iddialari — otorite dosyasindan
    for birim in A.get("birimler", []):
        deger = birim_degeri(birim)
        if deger is None:
            olculemeyenler.append(f"birim '{birim['kelime']}': deger cikarilamadi")
            continue

        def _birim(m, deger=deger, kelime=birim["kelime"]):
            eski = m.group(0)
            yenisi = eski.replace(m.group(1), str(deger), 1)
            if eski != yenisi:
                degisenler.append(f"{kelime}: {eski.strip()} -> {yenisi.strip()}")
            return yenisi
        if not re.search(birim["desen"], yeni):
            kor.append(f"birim '{birim['kelime']}'")
        yeni = re.sub(birim["desen"], _birim, yeni)

    _pano_toplam = sum(len(re.findall(d, metin, re.I))
                       for d in A.get("pano_desenleri", []))
    if A.get("pano_desenleri") and not _pano_toplam:
        # Alan bazinda olculmez: bir alanin maddesinde pano sayisi bulunmamasi
        # MESRU (01-Genel boyle). Hicbir yerde bulunmamasi ariza.
        kor.append("pano (hicbir alanda)")

    for o in olculemeyenler:
        print(f"OLCULEMEDI · {o} — metne dokunulmadi")

    # SESSIZ KORLUK: bir desen acilis'te HIC eslesmezse, "degisiklik yok" ile
    # "goremiyorum" ayni cikti uretir — ve ikincisi felakettir, cunku betik
    # "zaten guncel" der. 2026-09-11'de olculdu: acilis'in bicimi bozulunca
    # betik tam bunu dedi ve cikis kodu 0 verdi.
    # Web oturumunun kendi betiklerinde kapattigi sinifin aynisi: desen hic
    # eslesmiyorsa sayi degil ARIZA bildirilir.
    if kor:
        for k in kor:
            print(f"BOZUK · {k} deseni acilis.md'de HIC eslesmedi — "
                  f"dosyanin bicimi mi degisti, desen mi eski?")
        print("Uretici olcemedigi icin durdu; 'guncel' demiyor.")
        return 2

    if yeni == metin:
        print("acilis.md zaten guncel — degisiklik yok")
        return 0

    for d in degisenler:
        print("  " + d)
    if KURU:
        # Cikis kodu ANLAMLI: 1 = "uretilen deger metinden farkli".
        # dogrula.py kontrol 22 bunu kullaniyor — boylece uretilen ama hicbir
        # kaynak dosyada gecmeyen sayilar (not, kontrol) da denetlenebiliyor.
        print("(--kuru: dosya yazilmadi)")
        return 1

    # Icerik degisti: beyan da degismeli, yoksa kontrol 19 hakli olarak bagirir.
    yeni = re.sub(r"^guncelleme: .*$", f"guncelleme: {date.today().isoformat()}",
                  yeni, count=1, flags=re.M)
    ACILIS.write_text(yeni, encoding="utf-8")
    print(f"acilis.md guncellendi ({len(degisenler)} sayi)")

    tavan = AYAR["esikler"]["acilis_tavan_karakter"]
    if len(yeni) > tavan:
        print(f"UYARI: {len(yeni)} karakter, tavan {tavan} — budanmali")
    return 0


if __name__ == "__main__":
    sys.exit(main())
