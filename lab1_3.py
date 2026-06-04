import os
import sys
import random
import shutil

# Указываем папки с данными
DATA_LARGE = "notMNIST_large"   # большой набор (train + validation)
DATA_SMALL = "notMNIST_small"   # маленький набор (test)

for data_dir in [DATA_LARGE, DATA_SMALL]:
    if not os.path.isdir(data_dir):
        print(f"Папка '{data_dir}' не найдена. Сначала распакуйте архив.", file=sys.stderr)
        sys.exit(1)

# Создаём папки для выборок
for subset in ["train", "val", "test"]:
    os.makedirs(subset, exist_ok=True)

# Получаем список классов (A–J)
classes = [d for d in os.listdir(DATA_LARGE)
           if os.path.isdir(os.path.join(DATA_LARGE, d))]
if not classes:
    print(f"Папка '{DATA_LARGE}' не содержит подпапок с классами.", file=sys.stderr)
    sys.exit(1)
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
        if fname.lower().endswith(".png"):
            full_path = os.path.join(folder, fname)
            all_files.append((full_path, cls))

print(f"Всего изображений в large: {len(all_files)}")

if len(all_files) < 210000:
    print(
        f"Недостаточно изображений для разделения: найдено {len(all_files)}, "
        f"нужно минимум 210000.",
        file=sys.stderr,
    )
    sys.exit(1)

# Перемешиваем список, чтобы выборка была случайной
random.shuffle(all_files)

# Делим на train и val
train_files = all_files[:200000]
val_files = all_files[200000:210000]

# Собираем test из small
test_files = []
for cls in os.listdir(DATA_SMALL):
    folder = os.path.join(DATA_SMALL, cls)
    if not os.path.isdir(folder):
        continue
    files = os.listdir(folder)
    for fname in files:
        if fname.lower().endswith(".png"):
            full_path = os.path.join(folder, fname)
            test_files.append((full_path, cls))

print(f"Train={len(train_files)}, Val={len(val_files)}, Test={len(test_files)}")


# Функция копирования файлов
def copy_pairs(pairs, subset):
    """Копирует список файлов pairs в папку subset."""
    errors = []
    for src, cls in pairs:
        dst = os.path.join(subset, cls, os.path.basename(src))
        try:
            shutil.copy(src, dst)
        except OSError as e:
            errors.append((src, e))
    if errors:
        print(
            f"Ошибки при копировании в '{subset}': {len(errors)} файлов не скопировано.",
            file=sys.stderr,
        )
        for path, err in errors[:5]:
            print(f"  {path}: {err}", file=sys.stderr)


# Копируем файлы в новые папки
copy_pairs(train_files, "train")
copy_pairs(val_files, "val")
copy_pairs(test_files, "test")

print("Разделение завершено.")
