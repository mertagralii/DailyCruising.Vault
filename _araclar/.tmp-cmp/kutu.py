#!/usr/bin/env python3
"""Kutu (zemin, kenarlik, kose, golge) karsilastirmasi — metni olmayan farklar icin."""
import json, sys

def load(p):
    with open(p) as f: return json.load(f)

def sig(b): return (b["x"], b["y"], b["w"], b["h"])

def main(dp, ap):
    D, A = load(dp)["boxes"], load(ap)["boxes"]
    used = set()
    print(f"kutu: tasarim {len(D)}  uygulama {len(A)}")
    difs = 0
    for d in sorted(D, key=lambda b: (b["y"], b["x"])):
        # ayni konum/olcude eslesen kutuyu bul (2px tolerans)
        best, bi = None, None
        for i, a in enumerate(A):
            if i in used: continue
            if abs(a["x"]-d["x"])<=2 and abs(a["y"]-d["y"])<=3 and abs(a["w"]-d["w"])<=2 and abs(a["h"]-d["h"])<=3:
                best, bi = a, i; break
        if best is None:
            print(f"  YOK   y={d['y']:<6} x={d['x']:<5} {d['w']}x{d['h']}  bg={d['bg']} bd={d['bd']} br={d['br']} bi={d['bi'][:40]}")
            difs += 1; continue
        used.add(bi)
        diff = []
        for k, lbl in (("bg","zemin"),("bd","kenar"),("br","kose"),("bi","gradyan"),("pad","dolgu"),("sh","golge")):
            if d[k] != best[k]: diff.append(f"{lbl} {d[k]!r}→{best[k]!r}")
        if diff:
            print(f"  FARK  y={d['y']:<6} x={d['x']:<5} {d['w']}x{d['h']}  " + " · ".join(diff))
            difs += 1
    for i, a in enumerate(A):
        if i not in used:
            print(f"  FAZLA y={a['y']:<6} x={a['x']:<5} {a['w']}x{a['h']}  bg={a['bg']} bd={a['bd']} br={a['br']}")
            difs += 1
    print(f"  toplam {difs}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
