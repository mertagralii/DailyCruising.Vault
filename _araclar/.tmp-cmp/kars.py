#!/usr/bin/env python3
"""Tasarim ile uygulamanin metin/kutu parmak izlerini karsilastirir."""
import json, sys, re, unicodedata

def load(p):
    with open(p) as f: return json.load(f)

BRAND = [("Rıhtım", "Daily Cruising"), ("Rihtim", "Daily Cruising")]

def nt(t):
    for a, b in BRAND: t = t.replace(a, b)
    t = t.replace(" ", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t.casefold().replace("i̇", "i")

def key(o): return nt(o["t"])

def main(d_path, a_path):
    D, A = load(d_path), load(a_path)
    print(f"viewport  tasarim {D['vw']}x{D['vh']}   uygulama {A['vw']}x{A['vh']}")
    print(f"sayfa yuk tasarim {D['pageH']}          uygulama {A['pageH']}   fark {A['pageH']-D['pageH']:+}")
    print(f"metin dugumu  tasarim {len(D['texts'])}  uygulama {len(A['texts'])}")
    print(f"kutu          tasarim {len(D['boxes'])}  uygulama {len(A['boxes'])}")

    # metinleri grupla
    from collections import defaultdict
    dg, ag = defaultdict(list), defaultdict(list)
    for o in D["texts"]: dg[key(o)].append(o)
    for o in A["texts"]: ag[key(o)].append(o)

    only_d = sorted(k for k in dg if k not in ag)
    only_a = sorted(k for k in ag if k not in dg)
    print(f"\n=== TASARIMDA VAR, UYGULAMADA YOK ({len(only_d)}) ===")
    for k in only_d:
        o = dg[k][0]
        print(f"  y={o['y']:<6} {o['t'][:70]!r}")
    print(f"\n=== UYGULAMADA VAR, TASARIMDA YOK ({len(only_a)}) ===")
    for k in only_a:
        o = ag[k][0]
        print(f"  y={o['y']:<6} {o['t'][:70]!r}")

    # ortak metinlerde stil/konum farki
    print(f"\n=== ORTAK METINLERDE FARK ===")
    n = 0
    for k in sorted(dg, key=lambda k: dg[k][0]["y"]):
        if k not in ag: continue
        if len(dg[k]) != len(ag[k]):
            print(f"  ADET  {dg[k][0]['t'][:40]!r}  tasarim {len(dg[k])}x  uygulama {len(ag[k])}x"); n += 1
            continue
        for d, a in zip(sorted(dg[k], key=lambda o: (o["y"], o["x"])), sorted(ag[k], key=lambda o: (o["y"], o["x"]))):
            diff = []
            if d["fs"] != a["fs"]: diff.append(f"fs {d['fs']}→{a['fs']}")
            if d["fw"] != a["fw"]: diff.append(f"fw {d['fw']}→{a['fw']}")
            if d["c"] != a["c"]: diff.append(f"renk {d['c']}→{a['c']}")
            if d["lh"] != a["lh"]: diff.append(f"lh {d['lh']}→{a['lh']}")
            if d["ls"] != a["ls"]: diff.append(f"ls {d['ls']}→{a['ls']}")
            if d["tt"] != a["tt"]: diff.append(f"tt {d['tt']}→{a['tt']}")
            if abs(d["x"] - a["x"]) > 2: diff.append(f"x {d['x']}→{a['x']}")
            if abs(d["y"] - a["y"]) > 4: diff.append(f"y {d['y']}→{a['y']}")
            if abs(d["w"] - a["w"]) > 3: diff.append(f"w {d['w']}→{a['w']}")
            if diff:
                print(f"  y={d['y']:<6} {d['t'][:44]!r}  " + " · ".join(diff)); n += 1
    print(f"  toplam {n}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
