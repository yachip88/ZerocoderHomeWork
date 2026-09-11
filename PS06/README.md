# PS06 — те же светильники, сохранение в CSV

Тот же парсинг категории [Освещение](https://www.divan.ru/category/svet), что и в PS05: **название, цена, ссылка**. Результат пишется в `lighting.csv` через `csv.writer` (pipeline).

Можно и FEED-экспортом:

```bash
python -m scrapy crawl divannewpars -O lighting.csv
```

## Запуск

```bash
pip install -r requirements.txt
cd divanpars
python -m scrapy crawl divannewpars
```

Файл появится в папке `PS06/lighting.csv` (utf-8-sig, удобно открывать в Excel).

## Файлы

- `divanpars/` — Scrapy-проект (паук `divannewpars`)
- `divanpars/divanpars/pipelines.py` — `LightingCsvPipeline` на `csv.writer`
- `lighting.csv` — выборка реальных товаров с divan.ru
