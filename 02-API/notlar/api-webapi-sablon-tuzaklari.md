---
rol: not
kapsam: api
guncelleme: 2026-08-21
durum: guncel
---

# `dotnet new webapi` şablon tuzakları

## Varsayılan Minimal API'dir

`dotnet new webapi` controller **üretmez**; Minimal API iskeleti kurar.
Controller isteniyorsa `--use-controllers` bayrağı şart. Bu bayrak unutulursa
`Controllers/` klasörü hiç oluşmaz ve fark edilmesi zaman alır.

Bizim kullandığımız tam komut:

```
dotnet new webapi -n DailyCruising.Api -o src/DailyCruising.Api -f net10.0 --use-controllers
```

## Şablon çöpü

Şablon `WeatherForecast.cs` + `WeatherForecastController.cs` bırakıyor; `classlib`
şablonu da `Class1.cs`. İkisi de silindi → [[durum]] delete-zone.

## HTTPS yönlendirmesi

`Program.cs` içinde `UseHttpsRedirection()` var ve `http` profili 5163'te dinliyor.
Bizim testimizde `curl http://localhost:5163/api/health` sorunsuz cevap verdi —
yani http profilinde yönlendirme sorun çıkarmadı. Ama frontend'den çağrı yaparken
beklenmedik 307 görülürse ilk bakılacak yer burasıdır.

## Zincirli komutlarda çıktı yutulması

Dört projeyi `&&` ile zincirleyip her birine `| tail -2` uyguladığımda yalnızca ilk
komutun çıktısı göründü; projelerin oluştuğunu ayrıca `ls` ile doğrulamak gerekti.
Toplu kurulumda **çıktıya değil, dosya sistemine bak**.

İlgili: [[api-notlar]] · [[api-kararlar]] · [[api-slnx-formati]]
