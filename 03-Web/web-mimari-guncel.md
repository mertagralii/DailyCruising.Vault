---
rol: map
kapsam: web
guncelleme: 2026-09-11
uretici: DailyCruising.Front-End/araclar/mimari-cikar.py
durum: uretilen
---

# Web Mimarisi — Güncel Envanter

> ⚠️ **Bu dosya üretiliyor, elle yazılmaz.** Güncellemek için
> `python3 araclar/mimari-cikar.py` çalıştırın.
>
> Gerekçe, alternatif ve elenme sebebi `web-mimari.md`'de —
> burada yalnız **ne var** yazıyor → [[web-mimari]]

## Sayılar

| Ne | Kaç |
|---|---|
| Rota (`page.tsx`) | 44 |
| Bileşen (`src/components/**/*.tsx`) | 145 |
| Yönetim paneli ekranı | 30 |
| API istemci modülü | 12 |
| Uçtaki yol · işlem | 195 · 248 |

## Rotalar

**`/(kök)`** — 1 rota

- `/`

**`/about`** — 1 rota

- `/about`

**`/account`** — 4 rota

- `/account`
- `/account/close`
- `/account/password`
- `/account/reservations/[code]`

**`/add-boat`** — 1 rota

- `/add-boat`

**`/admin`** — 8 rota

- `/admin`
- `/admin/tekneler`
- `/admin/tekneler/[partnerId]/[boatId]`
- `/admin/tekneler/[partnerId]/[boatId]/belgeler`
- `/admin/tekneler/[partnerId]/[boatId]/detay`
- `/admin/tekneler/[partnerId]/[boatId]/fiyat`
- `/admin/tekneler/[partnerId]/[boatId]/resimler`
- `/admin/tekneler/yeni`

**`/blog`** — 2 rota

- `/blog`
- `/blog/[slug]`

**`/boats`** — 3 rota

- `/boats`
- `/boats/[slug]`
- `/boats/[slug]/reviews`

**`/booking`** — 2 rota

- `/booking`
- `/booking/success`

**`/design-system`** — 2 rota

- `/design-system`
- `/design-system/emails`

**`/forbidden`** — 1 rota

- `/forbidden`

**`/forgot-password`** — 1 rota

- `/forgot-password`

**`/login`** — 1 rota

- `/login`

**`/maintenance`** — 1 rota

- `/maintenance`

**`/messages`** — 1 rota

- `/messages`

**`/odeme`** — 1 rota

- `/odeme`

**`/owner-panel`** — 1 rota

- `/owner-panel`

**`/payment`** — 1 rota

- `/payment/mock`

**`/register`** — 1 rota

- `/register`

**`/reservation-lookup`** — 1 rota

- `/reservation-lookup`

**`/reservations`** — 1 rota

- `/reservations/[code]/voucher`

**`/reset-password`** — 1 rota

- `/reset-password`

**`/review`** — 1 rota

- `/review`

**`/support`** — 3 rota

- `/support`
- `/support/[id]`
- `/support/new`

**`/support-panel`** — 1 rota

- `/support-panel`

**`/tarih-degisikligi`** — 2 rota

- `/tarih-degisikligi`
- `/tarih-degisikligi/tamamlandi`

**`/verify-email`** — 1 rota

- `/verify-email`

## API istemci modülleri

- `src/lib/api/admin-sayfa.ts`
- `src/lib/api/blog.ts`
- `src/lib/api/boat-detail.ts`
- `src/lib/api/browser.ts`
- `src/lib/api/client.ts`
- `src/lib/api/errors.ts`
- `src/lib/api/format.ts`
- `src/lib/api/panel.ts`
- `src/lib/api/platform-boats.ts`
- `src/lib/api/pricing-catalog.ts`
- `src/lib/api/reservations.ts`
- `src/lib/api/search.ts`

## ⚠️ Bu dosyanın ÖLÇMEDİKLERİ

Aşağıdakiler bilerek dışarıda; üretilemez oldukları için
`web-mimari.md`'de elle yazılıyor. Yokluklarının **burada
yazılı olması**, birinin onları burada aramasını engelliyor.

- **Hangi rota korumalı** — koruma tek bir listeden gelmiyor,
  sayfa bazında sunucu çağrısıyla kuruluyor. Dosya içeriğinden
  çıkarım, yanlış işaretlenmiş bir rota üretir ve o yanlış
  hiçbir yerden anlaşılmaz.
- **Rotalar arası akış** — hangi ekran hangisine gidiyor.
- **Hangi bileşen nerede kullanılıyor** — içe alım grafiği.
- **Neden böyle kurulduğu** — gerekçenin yeri `web-mimari.md`.
