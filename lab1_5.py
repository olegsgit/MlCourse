import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from utils import load_image_data

# Загружаем данные
x_train, y_train = load_image_data("train")
x_val, y_val = load_image_data("val")
x_test, y_test = load_image_data("test")

print("Размеры выборок:")
print("Train:", x_train.shape, "Val:", x_val.shape, "Test:", x_test.shape)

# Проверяем точность при разных размерах обучающей выборки
sizes = [50, 100, 1000, 50000]
accuracies = []

for n in sizes:
    idx = np.random.choice(len(x_train), n, replace=False)
    x_sub, y_sub = x_train[idx], y_train[idx]

    if len(set(y_sub)) < 2:
        print(f"⚠️ В выборке {n} примеров оказался только один класс, пропускаем.")
        continue

    clf = LogisticRegression(max_iter=50000)
    clf.fit(x_sub, y_sub)

    y_pred = clf.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    accuracies.append(acc)
    print(f"Размер {n}: точность = {acc:.4f}")

# Строим график
plt.plot(sizes, accuracies, marker="o")
plt.xlabel("Размер обучающей выборки")
plt.ylabel("Точность на тесте")
plt.title("Зависимость точности классификатора от размера обучающей выборки")
plt.grid(True)
plt.show()
