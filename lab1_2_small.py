import os
import sys

DATA_DIR = "notMNIST_small"

if not os.path.isdir(DATA_DIR):
    print(f"Папка '{DATA_DIR}' не найдена. Сначала распакуйте архив.", file=sys.stderr)
    sys.exit(1)

# список классов (подпапки A–J)
classes = [d for d in os.listdir(DATA_DIR)
           if os.path.isdir(os.path.join(DATA_DIR, d))]
if not classes:
    print(f"Папка '{DATA_DIR}' не содержит подпапок с классами.", file=sys.stderr)
    sys.exit(1)
print("Классы:", classes)

# считаем количество файлов в каждой папке
for cls in classes:
    folder = os.path.join(DATA_DIR, cls)
    files = [f for f in os.listdir(folder)
             if f.lower().endswith((".png", ".jpg"))]
    count = len(files)
    print(f"Класс {cls}: {count} изображений")
