# PS05 — Scrapy: источники освещения на divan.ru

Проект `divanpars` как в уроке (`scrapy startproject divanpars`, паук `divannewpars`), но парсим **освещение**, не диваны.

## Данные

Для каждого товара: **название, цена, ссылка**.

- Старт: `https://www.divan.ru/category/svet`
- `allowed_domains = ["divan.ru"]` — без `https://` (иначе Scrapy не ходит по сайту)
- Пагинация: `/category/svet/page-2`, `page-3` (кнопка «Показать ещё»)

Селектор диванов из урока `div._Ud0k` на текущей вёрстке **не работает**. Актуальные:

| Поле | Селектор |
|------|----------|
| карточка | `[data-testid="product-card"]` |
| название | `.ProductName` |
| цена | `[data-testid="price"]` |
| ссылка | `a[href*="/product/"]` |

## Запуск

```bash
pip install -r requirements.txt
cd divanpars
python -m scrapy crawl divannewpars
```

Печать в CSV (это уже PS06):

```bash
python -m scrapy crawl divannewpars -O lighting.csv
```

## Структура

```
PS05/
├── README.md
├── requirements.txt
└── divanpars/
    ├── scrapy.cfg
    └── divanpars/
        ├── settings.py
        ├── items.py
        └── spiders/divannewpars.py
```
