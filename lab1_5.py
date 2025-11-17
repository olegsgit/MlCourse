import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from PIL import Image

# Функция загрузки изображений из папки
def load_data(root):
    x, y = [], []
    classes = os.listdir(root)
    for cls in classes:
        folder = os.path.join(root, cls)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            try:
                img = Image.open(path).convert("L")   # переводим в градации серого
                arr = np.array(img).flatten()        # превращаем картинку в вектор
                x.append(arr)
                y.append(cls)                        # метка = имя папки (A–J)
            except:
                pass
    return np.array(x), np.array(y)

# Загружаем данные 
x_train, y_train = load_data("train")
x_val, y_val     = load_data("val")
x_test, y_test   = load_data("test")

print("Размеры выборок:")
print("Train:", x_train.shape, "Val:", x_val.shape, "Test:", x_test.shape)

# Проверяем точность при разных размерах обучающей выборки 
sizes = [50, 100, 1000, 50000]
accuracies = []

for n in sizes:
    # берём случайные n примеров из train
    idx = np.random.choice(len(x_train), n, replace=False)
    x_sub, y_sub = x_train[idx], y_train[idx]

    # проверяем, что есть хотя бы 2 класса
    if len(set(y_sub)) < 2:
        print(f"⚠️ В выборке {n} примеров оказался только один класс, пропускаем.")
        continue

    # обучаем классификатор
    clf = LogisticRegression(max_iter=50000)
    clf.fit(x_sub, y_sub)

    # точность на тесте
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