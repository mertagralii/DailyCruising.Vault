#!/usr/bin/env python3
"""Sekmeli ekranlarda her sekmeyi ayri ayri karsilastirir."""
import json, sys, os, importlib.util
spec = importlib.util.spec_from_file_location("kars", os.path.join(os.path.dirname(__file__), "kars.py"))
kars = importlib.util.module_from_spec(spec); spec.loader.exec_module(kars)

D = json.load(open(sys.argv[1])); A = json.load(open(sys.argv[2]))
for k in D:
    if k not in A:
        print(f"\n##### {k}: uygulamada yok"); continue
    d, a = D[k], A[k]
    print(f"\n##### {k}   yukseklik {d['pageH']} / {a['pageH']}  ({a['pageH']-d['pageH']:+})  metin {len(d['texts'])}/{len(a['texts'])}")
    json.dump(d, open('/tmp/_d.json','w')); json.dump(a, open('/tmp/_a.json','w'))
    kars.main('/tmp/_d.json', '/tmp/_a.json')
