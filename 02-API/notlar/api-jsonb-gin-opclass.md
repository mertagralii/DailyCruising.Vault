---
rol: note
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# `EventLogs.Payload` üzerindeki GIN indeksi `->>` sorgularını hızlandırmaz

`IX_EventLogs_Payload_Gin` var ve doğru kurulmuş. Ama varsayılan opclass
(`jsonb_ops`) yalnız şu operatörleri destekler: `@>` · `?` · `?|` · `?&`.

**Metin çıkarıp karşılaştırma GIN'i hiç kullanmıyor:**

```sql
-- indeks KULLANILMIYOR, payload filtre olarak taranıyor
WHERE "Payload"->>'departureDate' = '2026-09-15'

-- indeksin desteklediği biçim
WHERE "Payload" @> '{"departureDate":"2026-09-15"}'::jsonb
```

`EXPLAIN` çıktısında birincisi `Filter: (("Payload" ->> 'departureDate') = ...)`
olarak görünüyor — yani plan `EventType,OccurredAt` btree'sinden geçip payload'ı
satır satır süzüyor.

⚠️ Küçük veride ikinci biçim de `Seq Scan` seçebilir. Bu **indeksin bozuk olduğu
anlamına gelmez**, planlayıcı tablo küçükken tarama daha ucuz olduğu için öyle
karar veriyor; hacim büyüdükçe `Bitmap Index Scan`'e geçer. Yani "indeks
çalışmıyor" diye erken hüküm verme.

## Sonuç

- Analitik sorgular **`@>` biçiminde** yazılacak.
- `->>` biçiminde yazılması zorunlu bir sorgu çıkarsa GIN yetmez, o alan için
  ayrı bir **ifade btree indeksi** gerekir: `CREATE INDEX ... ((Payload->>'code'))`.
- Hangi alanların gerçekten sorgulanacağı netleşmeden ifade indeksi eklemek erken;
  `A-21` ve AI raporları netleştiğinde bakılacak.

İlgili: [[api-notlar]] · [[api-sema]] · [[api-olay-gunlugu-iptal-jetonu]]
