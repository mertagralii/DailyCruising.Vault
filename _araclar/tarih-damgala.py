#!/usr/bin/env python3
"""Bu oturumda DEGISTIRDIGIN dosyalarin `guncelleme` beyanini bugune ceker.

Neden var
---------
2026-09-11/12'de kontrol 19 (`beyan geride`) **bes kez** kirmizi yandi ve
besinde de sapma GERCEKTI: dosya yazildi, frontmatter'daki tarih dunde kaldi.
Uc oturum da ayni surtunmeyi yasadi; ikisi "gurultu" dedi, biri (vault oturumu)
itiraz etti ve sonra ayni tuzaga iki kez dustu.

⚠️ Itirazin sebebi duruyor ve bu betik onu BOZMUYOR: `guncelleme` alani
**beyandir** ve dort kontrolun olcutudur (4 bayatlik · 15 mimari · 23 alan
durumu · 25 uretilen dosya). Hepsi *"beyan edilen tarih"* ile *"kodun gercegi"*ni
karsilastirir — "dosyaya dokunmak onu dogru yapmaz" kurali oradan cikti.
Otomatik damga (her yazmada, hook ile) bu dordunu sessizce mtime tabanli yapardi.

Bu betik farkli: **elle cagrilir** ve yalnizca git'e gore DEGISMIS dosyalara
dokunur. Beyan kasitli kalir, yalniz tekrar eden el isi kalkar. Temiz dosyaya
dokunmaz — vault'u toplu damgalayamaz.

⚠️ Bu tasarim bir kotu kullanimi da KENDILIGINDEN engelliyor: kontrol 23
(alan durumu kod commit'lerinin gerisinde) temiz bir dosyada kirmizi yanar —
betik temiz dosyaya dokunmadigi icin o kirmiziyi susturamaz. Susturmanin tek
yolu durumu GERCEKTEN yazmaktir, ki kontrolun amaci da odur.

Kullanim: python3 _araclar/tarih-damgala.py [--kuru]
  --kuru : yazmaz, ne degisecegini basar
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
KURU = "--kuru" in sys.argv
BUGUN = date.today().isoformat()


def degisen_dosyalar():
    """git'e gore degismis .md dosyalari (calisma agaci + index)."""
    r = subprocess.run(["git", "-C", str(VAULT), "status", "--porcelain"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("HATA: git calismadi — vault bir git reposu degil mi?")
    yollar = []
    for satir in r.stdout.split("\n"):
        if not satir.strip():
            continue
        yol = satir[3:].strip().strip('"')
        if " -> " in yol:              # yeniden adlandirma: hedefi al
            yol = yol.split(" -> ")[-1]
        if yol.endswith(".md"):
            yollar.append(VAULT / yol)
    return [y for y in yollar if y.exists()]


def main():
    dosyalar = degisen_dosyalar()
    if not dosyalar:
        # "Degismis dosya yok" ile "goremedim" ayri seyler: git calisti ve bos
        # dondu, bu bir SONUCTUR. Ariza olsaydi yukarida sys.exit ederdi.
        print("Degismis .md dosyasi yok — damgalanacak bir sey de yok.")
        return 0

    damgalanan, atlanan = [], []
    for yol in dosyalar:
        metin = yol.read_text(encoding="utf-8")
        m = re.search(r"^guncelleme: (\S+)\s*$", metin, re.M)
        if not m:
            atlanan.append((yol, "frontmatter'da `guncelleme` yok"))
            continue
        if m.group(1) == BUGUN:
            continue
        yeni = re.sub(r"^guncelleme: .*$", f"guncelleme: {BUGUN}",
                      metin, count=1, flags=re.M)
        damgalanan.append((yol, m.group(1)))
        if not KURU:
            yol.write_text(yeni, encoding="utf-8")

    for yol, sebep in atlanan:
        print(f"ATLANDI · {yol.relative_to(VAULT)} — {sebep}")
    for yol, eski in damgalanan:
        print(f"  {yol.relative_to(VAULT)}: {eski} -> {BUGUN}")

    if not damgalanan:
        print(f"{len(dosyalar)} degismis dosyanin hepsi zaten {BUGUN} diyor.")
        return 0
    print(f"{len(damgalanan)}/{len(dosyalar)} dosyanin beyani guncellendi"
          + (" (--kuru: yazilmadi)" if KURU else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
