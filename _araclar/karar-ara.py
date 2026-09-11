#!/usr/bin/env python3
"""Karar dosyalarinda arar — 355 KB'lik dosyayi acmadan.

Neden var
---------
`*-kararlar.md` dosyalari toplam 250+ giris tasiyor; en buyugu tek basina
355 KB. Tetikleyici zaten var ("neden boyle yapmisiz" -> ilgili kararlar
dosyasi) ama 2026-09-11'de backend oturumu bildirdi: **hic okumuyorum.**
O gun bir sorunun cevabini vault'tan degil kodun icindeki yorumdan aldi.

Sebep tetikleyicinin yanlisligi degil, ACILAN SEYIN buyuklugu: 355 KB bir
dosyayi acmak, cevabi olmayan bir maliyet. Envanter/gerekce ayriminin ayni
mantigi: buyuk dosya kalir, ERISIM uretilir.

Ne yapar
--------
Verilen kelimeyi butun `*-kararlar.md` dosyalarinda arar ve eslesen KARAR
GIRISLERINI (## basligindan bir sonraki ## basligina kadar) ozetler: dosya,
satir, baslik ve eslesen satirin kendisi. `-t` ile giris govdesini de basar.

Kullanim:
    python3 _araclar/karar-ara.py kupon
    python3 _araclar/karar-ara.py "iade orani" -t      # tam govde
    python3 _araclar/karar-ara.py --alan 02-API rol    # tek alanda ara
"""
import json
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
_yol = Path(__file__).resolve().parent / "vault.json"
try:
    AYAR = json.loads(_yol.read_text(encoding="utf-8"))
except FileNotFoundError:
    sys.exit(f"HATA: yapilandirma dosyasi yok: {_yol}")
except json.JSONDecodeError as _hata:
    sys.exit(f"HATA: {_yol} gecerli JSON degil.\n"
             f"  Satir {_hata.lineno}, kolon {_hata.colno}: {_hata.msg}")


def girisler(yol):
    """Bir kararlar dosyasini (baslik, govde, satir_no) uclulerine ayirir."""
    satirlar = yol.read_text(encoding="utf-8").split("\n")
    baslik_yerleri = [i for i, s in enumerate(satirlar) if s.startswith("## ")]
    for n, i in enumerate(baslik_yerleri):
        son = baslik_yerleri[n + 1] if n + 1 < len(baslik_yerleri) else len(satirlar)
        yield satirlar[i][3:].strip(), "\n".join(satirlar[i:son]), i + 1


def main():
    arg = list(sys.argv[1:])
    tam = "-t" in arg
    if tam:
        arg.remove("-t")
    alan_suzgec = None
    if "--alan" in arg:
        i = arg.index("--alan")
        if i + 1 >= len(arg):
            sys.exit("--alan bir alan adi bekler, ornegin: --alan 02-API")
        alan_suzgec = arg[i + 1]
        del arg[i:i + 2]
    if not arg:
        sys.exit("Kullanim: python3 _araclar/karar-ara.py <kelime> [-t] "
                 "[--alan <alan>]")
    kelime = " ".join(arg)
    desen = re.compile(re.escape(kelime), re.I)

    dosyalar = [VAULT / a / f"{v['onek']}-kararlar.md"
                for a, v in AYAR["alanlar"].items()
                if alan_suzgec is None or a == alan_suzgec]
    dosyalar = [d for d in dosyalar if d.exists()]
    if not dosyalar:
        sys.exit(f"Kararlar dosyasi bulunamadi (alan suzgeci: {alan_suzgec})")

    toplam_giris = bulunan = 0
    for yol in sorted(dosyalar):
        rel = yol.relative_to(VAULT).as_posix()
        for baslik, govde, satir_no in girisler(yol):
            toplam_giris += 1
            if not desen.search(govde):
                continue
            bulunan += 1
            print(f"\n── {rel}:{satir_no}")
            print(f"   {baslik}")
            if tam:
                print()
                for s in govde.split("\n")[1:]:
                    print("   " + s)
            else:
                # Eslesen satirin KENDISI basilir: baslik tek basina yaniltir,
                # cunku bir karar baska bir kararin gerekcesinde de anilabilir.
                for s in govde.split("\n"):
                    if desen.search(s):
                        print(f"   … {s.strip()[:160]}")
                        break

    print(f"\n{bulunan}/{toplam_giris} karar eslesti · aranan: {kelime!r}")
    if not bulunan:
        # Bos sonuc BILGIDIR: "karar alinmadi" ile "yanlis kelime aradim"
        # ayri seylerdir ve betik ikisini ayirt edemez. Soylemesi gerekiyor.
        print("Eslesme yok. Bu, kararin ALINMADIGI anlamina gelmez — baska bir")
        print("kelimeyle yazilmis olabilir. Once es anlamlisini dene.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
