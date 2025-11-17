import os
import random
import matplotlib.pyplot as plt
from PIL import Image

# Папка с данными (после распаковки архива)
DATA_DIR = "notMNIST_small"    

# Список классов (подпапки A–J)
classes = os.listdir(DATA_DIR)
print("Классы:", classes)

# Покажем 5 случайных картинок
for i in range(5):
    # Выбираем случайную папку 
    cls = random.choice(classes)
    folder = os.path.join(DATA_DIR, cls)

    # Берём случайный файл из этой папки
    file = random.choice(os.listdir(folder))
    img_path = os.path.join(folder, file)

    # Открываем картинку  
    img = Image.open(img_path) 

    # Показываем картинку
    plt.imshow(img, cmap="gray")
    plt.title(f"Класс: {cls}")
    plt.axis("off")
    plt.show()
  