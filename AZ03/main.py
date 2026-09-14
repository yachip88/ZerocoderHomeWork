from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

BASE = Path(__file__).resolve().parent

mean = 0
std_dev = 1
num_samples = 1000
data = np.random.normal(mean, std_dev, num_samples)

plt.figure()
plt.hist(data, bins=30)
plt.title("Гистограмма нормального распределения")
plt.xlabel("Значение")
plt.ylabel("Частота")
plt.tight_layout()
plt.savefig(BASE / "hist_normal.png", dpi=120)
plt.close()

x = np.random.rand(50)
y = np.random.rand(50)
plt.figure()
plt.scatter(x, y)
plt.title("Диаграмма рассеяния")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.savefig(BASE / "scatter.png", dpi=120)
plt.close()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
response = requests.get("https://www.divan.ru/category/divany-i-kresla", headers=headers, timeout=30)
response.raise_for_status()

import json
import re

prices = []
for match in re.finditer(
    r'<script type="application/ld\+json">(.*?)</script>',
    response.text,
    flags=re.S,
):
    raw = match.group(1)
    if "ItemList" not in raw:
        continue
    data_json = json.loads(raw)
    for element in data_json.get("itemListElement") or []:
        product = element.get("item") or {}
        offer = product.get("offers") or {}
        price = offer.get("price")
        name = product.get("name")
        if name and price is not None:
            prices.append({"название": name, "цена": int(float(price))})

if not prices:
    raise SystemExit("Не удалось спарсить цены диванов")

df = pd.DataFrame(prices)
df.to_csv(BASE / "divans.csv", index=False, encoding="utf-8-sig")
avg = df["цена"].mean()
print(f"Диванов: {len(df)}")
print(f"Средняя цена: {avg:.0f}")

plt.figure()
plt.hist(df["цена"], bins=15)
plt.title("Цены на диваны divan.ru")
plt.xlabel("Цена, руб.")
plt.ylabel("Количество")
plt.tight_layout()
plt.savefig(BASE / "divans_hist.png", dpi=120)
plt.close()
