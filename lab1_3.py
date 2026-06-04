import os
import random
import shutil

# Указываем папки с данными 
DATA_LARGE = "notMNIST_large"   # большой набор (train + validation)
DATA_SMALL = "notMNIST_small"   # маленький набор (test)

# Создаём папки для выборок 
# В них будут храниться разделённые данные
for subset in ["train", "val", "test"]:
    os.makedirs(subset, exist_ok=True)

# Получаем список классов (A–J) 
classes = os.listdir(DATA_LARGE)
print("Классы:", classes)

# В каждой выборке создаём подпапки для классов
for subset in ["train", "val", "test"]:
    for cls in classes:
        os.makedirs(os.path.join(subset, cls), exist_ok=True)

# Собираем все файлы из большого набора 
all_files = []
for cls in classes:
    folder = os.path.join(DATA_LARGE, cls)
    files = os.listdir(folder)
    for fname in files:
        if fname.lower().endswith(".png"):   # берём только картинки
            full_path = os.path.join(folder, fname)
            all_files.append((full_path, cls))  # сохраняем путь и класс

print(f"Всего изображений в large: {len(all_files)}")

# Перемешиваем список, чтобы выборка была случайной 
random.shuffle(all_files)

# Делим на train и val 
train_files = all_files[:200000]       # первые 200k → обучающая выборка
val_files   = all_files[200000:210000] # следующие 10k → валидация

# Собираем test из small 
test_files = []
for cls in os.listdir(DATA_SMALL):
    folder = os.path.join(DATA_SMALL, cls)
    files = os.listdir(folder)
    for fname in files:
        if fname.lower().endswith(".png"):
            full_path = os.path.join(folder, fname)
            test_files.append((full_path, cls))

print(f"Train={len(train_files)}, Val={len(val_files)}, Test={len(test_files)}")

# Функция копирования файлов 
def copy_pairs(pairs, subset):
    """Копирует список файлов pairs в папку subset"""
    subset_abs = os.path.abspath(subset)
    for src, cls in pairs:
        basename = os.path.basename(src)
        dst = os.path.join(subset_abs, cls, basename)
        # Защита от path traversal: убеждаемся, что путь остаётся внутри целевой папки
        if not os.path.abspath(dst).startswith(subset_abs + os.sep):
            print(f"⚠️ Пропуск подозрительного имени файла: {basename}")
            continue
        shutil.copy(src, dst)

# Копируем файлы в новые папки 
copy_pairs(train_files, "train")
copy_pairs(val_files, "val")
copy_pairs(test_files, "test")

print("Разделение завершено.")