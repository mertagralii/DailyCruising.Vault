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
| `DailyCruising.Domain` | **hiçbiri** | 11 klasör, **74 entity** |
| `DailyCruising.Application` | Domain | kimlik doğrulama senaryoları, yetki anahtarları, arayüzler |
| `DailyCruising.Infrastructure` | Application | EF Core, 12 yapılandırma, **8 migration**, JWT ve parola özeti |
| `DailyCruising.Api` | Application + Infrastructure | health + kimlik doğrulama uçları, yetki politikaları |

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

| POST | `/api/auth/register` | erişim + yenileme jetonu |
| POST | `/api/auth/login` | erişim + yenileme jetonu |
| POST | `/api/auth/refresh` | jeton döndürme (eski iptal edilir) |
| POST | `/api/auth/logout` | yenileme jetonunu iptal eder |
| GET | `/api/auth/me` | kimlik + kapsam + yetkiler |

**İş uç noktası hâlâ yok** — tekne, rezervasyon, fiyat uçları yazılmadı → [[durum]]

## Şema

Veritabanı şeması ayrı dosyada, sekiz bölüm halinde çıkarılıyor → [[api-sema]]

İlgili: [[api-kararlar]] · [[proje]] · [[00-Index]]
