import os
import sys
import random
import matplotlib.pyplot as plt
from PIL import Image, UnidentifiedImageError

# Папка с данными (после распаковки архива)
DATA_DIR = "notMNIST_small"

if not os.path.isdir(DATA_DIR):
    print(f"Папка '{DATA_DIR}' не найдена. Сначала распакуйте архив.", file=sys.stderr)
    sys.exit(1)

# Список классов (подпапки A–J)
classes = [d for d in os.listdir(DATA_DIR)
           if os.path.isdir(os.path.join(DATA_DIR, d))]
if not classes:
    print(f"Папка '{DATA_DIR}' не содержит подпапок с классами.", file=sys.stderr)
    sys.exit(1)
print("Классы:", classes)

# Покажем 5 случайных картинок
shown = 0
attempts = 0
max_attempts = 50

while shown < 5 and attempts < max_attempts:
    attempts += 1
    # Выбираем случайную папку
    cls = random.choice(classes)
    folder = os.path.join(DATA_DIR, cls)

    files = os.listdir(folder)
    if not files:
        continue

    # Берём случайный файл из этой папки
    file = random.choice(files)
    img_path = os.path.join(folder, file)

    # Открываем картинку
    try:
        img = Image.open(img_path)
    except (UnidentifiedImageError, OSError) as e:
        print(f"Не удалось открыть '{img_path}': {e}", file=sys.stderr)
        continue

    # Показываем картинку
    plt.imshow(img, cmap="gray")
    plt.title(f"Класс: {cls}")
    plt.axis("off")
    plt.show()
    shown += 1

if shown < 5:
    print(f"Удалось показать только {shown} из 5 изображений.", file=sys.stderr)
