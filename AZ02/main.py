import pandas as pd

df = pd.DataFrame(
    {
        "Имя": [
            "Анна",
            "Борис",
            "Вика",
            "Глеб",
            "Даша",
            "Егор",
            "Ира",
            "Кирилл",
            "Лена",
            "Миша",
        ],
        "Математика": [5, 4, 3, 5, 4, 2, 5, 4, 3, 5],
        "Русский": [4, 5, 5, 3, 4, 4, 5, 3, 4, 5],
        "История": [3, 4, 5, 4, 5, 3, 4, 5, 4, 3],
        "Физика": [5, 3, 4, 5, 2, 4, 3, 5, 4, 4],
        "Английский": [4, 5, 4, 4, 5, 3, 5, 4, 5, 3],
    }
)

print("Первые строки:")
print(df.head())
print("\nСредняя оценка по предметам:")
print(df.mean(numeric_only=True))
print("\nМедианная оценка по предметам:")
print(df.median(numeric_only=True))

q1_math = df["Математика"].quantile(0.25)
q3_math = df["Математика"].quantile(0.75)
print(f"\nQ1 по математике: {q1_math}")
print(f"Q3 по математике: {q3_math}")
print(f"IQR по математике: {q3_math - q1_math}")
print("\nСтандартное отклонение:")
print(df.std(numeric_only=True))
