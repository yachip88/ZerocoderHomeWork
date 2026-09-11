"""
PS04 — консольный поиск по русской Википедии (Selenium 4).

Как в уроке: открываем ru.wikipedia.org, находим поисковую строку,
вводим запрос и нажимаем Keys.ENTER. Дальше меню из трёх действий:
листать параграфы, перейти на связанную статью, выйти.
"""

from __future__ import annotations

import argparse
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WIKI_HOME = "https://ru.wikipedia.org/wiki/Заглавная_страница"
SKIP_TITLE_PREFIXES = (
    "Файл:",
    "File:",
    "Категория:",
    "Category:",
    "Служебная:",
    "Special:",
    "Википедия:",
    "Wikipedia:",
    "Шаблон:",
    "Template:",
    "Справка:",
    "Help:",
    "Портал:",
    "Portal:",
    "MediaWiki:",
    "Обсуждение:",
    "Talk:",
    "Участник:",
    "User:",
)


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass


def make_browser(headless: bool) -> webdriver.Chrome:
    """Selenium 4: ChromeDriver подтягивает Selenium Manager."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--lang=ru")
    options.add_argument("--disable-search-engine-choice-screen")
    return webdriver.Chrome(options=options)


def open_wikipedia_search(browser: webdriver.Chrome, query: str) -> None:
    browser.get(WIKI_HOME)
    wait = WebDriverWait(browser, 15)
    search_box = None
    locators = [
        (By.ID, "searchInput"),
        (By.NAME, "search"),
        (By.CSS_SELECTOR, "input[type='search']"),
    ]
    for how, value in locators:
        try:
            search_box = wait.until(EC.presence_of_element_located((how, value)))
            if search_box.is_displayed() and search_box.is_enabled():
                break
        except TimeoutException:
            search_box = None
    if search_box is None or not search_box.is_displayed():
        try:
            toggle = browser.find_element(By.CSS_SELECTOR, "#p-search a, .search-toggle, .cdx-search-input")
            toggle.click()
            time.sleep(0.4)
            search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search")))
        except (NoSuchElementException, TimeoutException) as exc:
            raise RuntimeError("Не удалось найти поисковую строку Википедии") from exc

    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1.5)
    _open_first_search_result_if_needed(browser)


def _open_first_search_result_if_needed(browser: webdriver.Chrome) -> None:
    """Если Википедия показала выдачу, а не статью — открываем первый результат."""
    results = browser.find_elements(By.CSS_SELECTOR, ".mw-search-result-heading a, .mw-search-results a")
    if results:
        href = results[0].get_attribute("href")
        if href:
            browser.get(href)
            time.sleep(1)


def article_title(browser: webdriver.Chrome) -> str:
    try:
        return browser.find_element(By.ID, "firstHeading").text.strip()
    except NoSuchElementException:
        return browser.title


def list_paragraphs(browser: webdriver.Chrome, smoke: bool = False) -> None:
    paragraphs = browser.find_elements(By.CSS_SELECTOR, "#mw-content-text p")
    texts = [p.text.strip() for p in paragraphs if p.text and p.text.strip()]
    if not texts:
        print("На этой странице нет текстовых параграфов.")
        return

    print(f"\nСтатья: {article_title(browser)}")
    print(f"Параграфов: {len(texts)}\n")
    for index, text in enumerate(texts, start=1):
        print(f"--- параграф {index}/{len(texts)} ---")
        print(text)
        print()
        if smoke:
            break
        answer = input("Enter — следующий параграф, m — в меню: ").strip().lower()
        if answer in {"m", "q", "меню", "menu"}:
            break


def collect_related_links(browser: webdriver.Chrome) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(title: str, href: str) -> None:
        title = (title or "").strip()
        href = (href or "").split("#", 1)[0]
        if not title or not href:
            return
        if not href.startswith("https://ru.wikipedia.org/wiki/"):
            return
        if any(title.startswith(prefix) for prefix in SKIP_TITLE_PREFIXES):
            return
        if href in seen:
            return
        seen.add(href)
        links.append((title, href))

    for element in browser.find_elements(By.CSS_SELECTOR, "div.hatnote a, div.dablink a"):
        add(element.text, element.get_attribute("href"))

    for element in browser.find_elements(By.CSS_SELECTOR, "#mw-content-text p a[href^='/wiki/']"):
        add(element.text, element.get_attribute("href"))
        if len(links) >= 25:
            break

    return links


def go_related(browser: webdriver.Chrome, smoke: bool = False) -> None:
    links = collect_related_links(browser)
    if not links:
        print("Связанных внутренних ссылок не нашлось.")
        return

    print(f"\nСвязанные страницы для «{article_title(browser)}»:\n")
    for index, (title, _href) in enumerate(links, start=1):
        print(f"{index}. {title}")

    if smoke:
        print(f"\n[smoke] переходим по первой ссылке: {links[0][0]}")
        browser.get(links[0][1])
        time.sleep(1)
        print(f"Открыта статья: {article_title(browser)}")
        return

    raw = input("\nНомер статьи (или Enter — отмена): ").strip()
    if not raw:
        return
    try:
        choice = int(raw)
    except ValueError:
        print("Нужно целое число.")
        return
    if not 1 <= choice <= len(links):
        print("Нет такого номера.")
        return

    title, href = links[choice - 1]
    print(f"Переходим: {title}")
    browser.get(href)
    time.sleep(1)
    print(f"Открыта статья: {article_title(browser)}")


def print_menu(title: str) -> None:
    print("\n" + "=" * 50)
    print(f"Текущая статья: {title}")
    print("1 — листать параграфы текущей статьи")
    print("2 — перейти на связанную (внутреннюю) страницу")
    print("3 — выйти из программы")
    print("=" * 50)


def run_interactive(browser: webdriver.Chrome) -> None:
    while True:
        print_menu(article_title(browser))
        choice = input("Выберите действие (1/2/3): ").strip()
        if choice == "1":
            list_paragraphs(browser)
        elif choice == "2":
            go_related(browser)
        elif choice == "3":
            print("Выход.")
            break
        else:
            print("Введите 1, 2 или 3.")


def run_smoke(browser: webdriver.Chrome) -> None:
    print(f"[smoke] статья: {article_title(browser)}")
    list_paragraphs(browser, smoke=True)
    go_related(browser, smoke=True)
    print("[smoke] ок")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Поиск по русской Википедии через Selenium")
    parser.add_argument("--query", help="Поисковый запрос (если не задан — спросим в консоли)")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Фоновый Chrome (для проверки). По умолчанию окно браузера видимо, как в уроке.",
    )
    parser.add_argument("--smoke", action="store_true", help="Короткий автопрогон без меню")
    return parser.parse_args()


def main() -> int:
    configure_stdout()
    args = parse_args()
    query = (args.query or input("Введите поисковый запрос: ")).strip()
    if not query:
        print("Пустой запрос, выход.")
        return 1

    try:
        browser = make_browser(headless=args.headless)
    except WebDriverException as exc:
        print("Не удалось запустить Chrome через Selenium Manager.")
        print(exc)
        return 1

    try:
        open_wikipedia_search(browser, query)
        print(f"Открыта страница: {article_title(browser)}")
        if args.smoke:
            run_smoke(browser)
        else:
            run_interactive(browser)
    finally:
        browser.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
