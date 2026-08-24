---
rol: map
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# API Mimarisi

`DailyCruising.Back-End/` → repo `mertagralii/DailyCruising.API`

## Katmanlar

Clean Architecture, dört proje. Bağımlılık **tek yönlü, içe doğru**:

```
Domain  ←  Application  ←  Infrastructure  ←  Api
  (bağımsız)                                   ↑
                                        Api ayrıca Application'a da bağlı
```

| Proje | Bağımlılıkları | Durum |
|---|---|---|
| `DailyCruising.Domain` | **hiçbiri** | boş — domain tanımlı değil |
| `DailyCruising.Application` | Domain | boş |
| `DailyCruising.Infrastructure` | Application | boş |
| `DailyCruising.Api` | Application + Infrastructure | health endpoint |

**Değişmez kural:** Domain hiçbir projeye referans vermez. Bu yön bozulursa Clean
Architecture'ın anlamı kalmaz.

Solution dosyası `DailyCruising.slnx` — .NET 10'un yeni XML formatı, eski `.sln` değil.

## Yapılandırma

CORS izinli origin'ler koda gömülü **değil**, `appsettings.json` →
`Cors:AllowedOrigins` dizisinden okunuyor. Yeni bir frontend adresi eklenecekse
kod değil yapılandırma değişir.

OpenAPI yalnızca Development ortamında açık (`/openapi/v1.json`).

## Uç noktalar

| Metot | Yol | Döner |
|---|---|---|
| GET | `/api/health` | `{"status":"healthy"}` |

İş uç noktası yok — domain bekleniyor → [[durum]]

## Şema

Veritabanı şeması ayrı dosyada, sekiz bölüm halinde çıkarılıyor → [[api-sema]]

İlgili: [[api-kararlar]] · [[proje]] · [[00-Index]]
