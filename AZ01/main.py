from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent

print("=== 1. Датасет с Kaggle: World Happiness Report 2024 ===")
happiness = pd.read_csv(BASE / "World-happiness-report-2024.csv")
print(happiness.head())
print()
happiness.info()
print()
print(happiness.describe())

print("\n=== 2. Средняя зарплата по городу (dz.csv) ===")
salary = pd.read_csv(BASE / "dz.csv")
print(salary)
print()
mean_salary = salary.groupby("City", dropna=True)["Salary"].mean()
print(mean_salary)
