# PS04 — поиск по Википедии (Selenium)

Консольная программа на Python + Selenium 4: запрос → русская Википедия → меню из трёх действий.

## Что делает

1. Спрашивает поисковый запрос.
2. Открывает [ru.wikipedia.org](https://ru.wikipedia.org/), находит поле поиска (`#searchInput` / `name="search"`), вводит запрос и нажимает `Keys.ENTER` — как в уроке.
3. Дальше в цикле предлагает:
   - **1** — листать параграфы текущей статьи (`#mw-content-text p`, по одному);
   - **2** — список связанных страниц (hatnote + внутренние ссылки), переход по номеру; после перехода снова то же меню;
   - **3** — выход.

Браузер **видимый**: `webdriver.Chrome()` (Selenium Manager сам подберёт ChromeDriver).

## Запуск

```bash
pip install -r requirements.txt
python wiki_search.py
```

Проверка без окна браузера:

```bash
python wiki_search.py --query "Selenium" --headless --smoke
```

## Файлы

- `wiki_search.py` — программа
- `requirements.txt` — `selenium>=4`
