"""Запуск паука освещения и запись PS06/lighting.csv."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "divanpars"))
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "divanpars.settings")

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main() -> None:
    process = CrawlerProcess(get_project_settings())
    process.crawl("divannewpars")
    process.start()
    csv_path = ROOT / "lighting.csv"
    print(f"Готово: {csv_path} exists={csv_path.exists()}")


if __name__ == "__main__":
    main()
