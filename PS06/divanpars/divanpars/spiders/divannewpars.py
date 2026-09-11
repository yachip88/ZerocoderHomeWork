import scrapy


class DivannewparsSpider(scrapy.Spider):
    """Паук категории «Освещение» на divan.ru (аналог divannewpars из урока)."""

    name = "divannewpars"
    # В уроке часто пишут https://divan.ru — так allowed_domains ломается.
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()

    def parse(self, response):
        cards = response.css('[data-testid="product-card"]')
        yielded = 0

        for card in cards:
            name = self._first_text(card.css(".ProductName::text").getall())
            price = self._first_text(card.css('[data-testid="price"]::text').getall())
            href = card.css('a[href*="/product/"]::attr(href)').get()
            if not name or not href:
                continue
            url = response.urljoin(href)
            if url in self.seen_urls:
                continue
            self.seen_urls.add(url)
            yielded += 1
            yield {
                "название": name,
                "цена": price,
                "ссылка": url,
            }

        if yielded == 0:
            self.logger.warning("CSS-карточки не найдены, пробуем JSON-LD: %s", response.url)

        for item in self._parse_jsonld(response):
            yielded += 1
            yield item

        self.logger.info("Страница %s: товаров %s", response.url, yielded)

        next_pages = response.xpath(
            '//a[.//button[@data-testid="show-more-button"]]/@href'
        ).getall()
        next_pages.extend(response.css('a[href*="/category/svet/page-"]::attr(href)').getall())
        for href in dict.fromkeys(next_pages):
            yield response.follow(href, callback=self.parse)

    @staticmethod
    def _first_text(parts):
        for part in parts:
            text = (part or "").strip()
            if text:
                return text
        return ""

    def _parse_jsonld(self, response):
        import json

        for raw in response.css('script[type="application/ld+json"]::text').getall():
            raw = (raw or "").strip()
            if '"ItemList"' not in raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            for element in data.get("itemListElement") or []:
                product = element.get("item") or {}
                name = (product.get("name") or "").strip()
                url = product.get("url")
                price = (product.get("offers") or {}).get("price")
                if name and url and url not in self.seen_urls:
                    self.seen_urls.add(url)
                    yield {
                        "название": name,
                        "цена": str(price) if price is not None else "",
                        "ссылка": url,
                    }
            return
