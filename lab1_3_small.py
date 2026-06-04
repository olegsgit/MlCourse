import os
import sys
import random
import shutil

# Папка с исходными данными (после распаковки notMNIST_small.tar.gz)
DATA_DIR = "notMNIST_small"

if not os.path.isdir(DATA_DIR):
    print(f"Папка '{DATA_DIR}' не найдена. Сначала распакуйте архив.", file=sys.stderr)
    sys.exit(1)

# Получаем список классов (подпапки A–J)
classes = [d for d in os.listdir(DATA_DIR)
           if os.path.isdir(os.path.join(DATA_DIR, d))]
if not classes:
    print(f"Папка '{DATA_DIR}' не содержит подпапок с классами.", file=sys.stderr)
    sys.exit(1)
print("Классы:", classes)

# Создаём пустую структуру папок для выборок
for subset in ["train", "val", "test"]:
    os.makedirs(subset, exist_ok=True)
    for cls in classes:
        os.makedirs(os.path.join(subset, cls), exist_ok=True)

# Собираем все файлы с изображениями по классам
all_files = []

for cls in classes:
    folder = os.path.join(DATA_DIR, cls)
    files = os.listdir(folder)
    for fname in files:
        if fname.lower().endswith(".png"):
            full_path = os.path.join(folder, fname)
            if os.path.isfile(full_path):
                all_files.append((full_path, cls))

if not all_files:
    print("Не найдено ни одного изображения.", file=sys.stderr)
    sys.exit(1)

print(f"Всего найдено изображений: {len(all_files)}")

# Перемешиваем, чтобы выборки были случайными
random.shuffle(all_files)

# Делим на части: 80% train, 10% val, 10% test
n = len(all_files)
n_train = int(n * 0.8)
n_val = int(n * 0.1)

train_files = all_files[:n_train]
val_files = all_files[n_train:n_train + n_val]
test_files = all_files[n_train + n_val:]

print(f"План разделения: train={len(train_files)}, val={len(val_files)}, test={len(test_files)}")


# Функция копирования пар (путь, класс) в нужную выборку
def copy_pairs(pairs, subset):
    """Копирует список файлов pairs в папку subset."""
    copied = 0
    errors = []
    for src, cls in pairs:
        dst = os.path.join(subset, cls, os.path.basename(src))
        try:
            shutil.copy(src, dst)
            copied += 1
        except OSError as e:
            errors.append((src, e))
        if copied % 1000 == 0 and copied > 0:
            print(f"[{subset}] скопировано {copied} файлов...")
    print(f"[{subset}] готово: {copied} файлов.")
    if errors:
        print(
            f"[{subset}] не удалось скопировать {len(errors)} файлов:",
            file=sys.stderr,
        )
        for path, err in errors[:5]:
            print(f"  {path}: {err}", file=sys.stderr)


# Копируем
copy_pairs(train_files, "train")
copy_pairs(val_files, "val")
copy_pairs(test_files, "test")

print("Разделение завершено.")
