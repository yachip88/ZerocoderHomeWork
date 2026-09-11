# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from pathlib import Path

from itemadapter import ItemAdapter


class LightingCsvPipeline:
    """Пишет название, цену и ссылку в lighting.csv через csv.writer."""

    def open_spider(self, spider):
        self.path = Path(__file__).resolve().parents[2] / "lighting.csv"
        self.file = self.path.open("w", encoding="utf-8-sig", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["название", "цена", "ссылка"])

    def close_spider(self, spider):
        self.file.close()
        spider.logger.info("CSV сохранён: %s (%s)", self.path, self.path.exists())

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.writer.writerow(
            [
                data.get("название", ""),
                data.get("цена", ""),
                data.get("ссылка", ""),
            ]
        )
        return item
