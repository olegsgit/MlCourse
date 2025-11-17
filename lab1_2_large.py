import os   # работа с папками и файлами

DATA_DIR = "notMNIST_large"  

# список классов (подпапки A–J)
classes = os.listdir(DATA_DIR)
print("Классы:", classes)

# считаем количество файлов в каждой папке
for cls in classes:
    folder = os.path.join(DATA_DIR, cls)      # путь к папке класса
    files = [f for f in os.listdir(folder)    # берём только файлы-изображения
             if f.lower().endswith((".png", ".jpg"))]
    count = len(files)                         # количество изображений
    print(f"Класс {cls}: {count} изображений")