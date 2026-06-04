import os
import sys
import hashlib


# Функция для подсчёта хэша файла
def file_hash(path):
    """Возвращает MD5-хэш содержимого файла или None при ошибке чтения."""
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except OSError as e:
        print(f"Не удалось прочитать '{path}': {e}", file=sys.stderr)
        return None


# Функция для сбора хэшей из папки выборки
def collect_hashes(root):
    """Возвращает множество хэшей всех файлов в папках классов."""
    if not os.path.isdir(root):
        print(f"Папка '{root}' не найдена.", file=sys.stderr)
        sys.exit(1)
    hashes = set()
    for cls in os.listdir(root):
        folder = os.path.join(root, cls)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            if os.path.isfile(path):
                h = file_hash(path)
                if h is not None:
                    hashes.add(h)
    return hashes


# Считаем хэши для train
train_hashes = collect_hashes("train")


# Проверяем val и test на пересечения с train
def find_duplicates(root, reference_hashes):
    """Находит файлы в root, чьи хэши совпадают с reference_hashes."""
    if not os.path.isdir(root):
        print(f"Папка '{root}' не найдена.", file=sys.stderr)
        sys.exit(1)
    duplicates = []
    for cls in os.listdir(root):
        folder = os.path.join(root, cls)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            if os.path.isfile(path):
                h = file_hash(path)
                if h is not None and h in reference_hashes:
                    duplicates.append(path)
    return duplicates


val_duplicates = find_duplicates("val", train_hashes)
test_duplicates = find_duplicates("test", train_hashes)

print(f"Дубликаты в val: {len(val_duplicates)}")
print(f"Дубликаты в test: {len(test_duplicates)}")

# удаляем дубликаты
remove_errors = []
for path in val_duplicates + test_duplicates:
    try:
        os.remove(path)
    except OSError as e:
        remove_errors.append((path, e))

if remove_errors:
    print(
        f"Не удалось удалить {len(remove_errors)} файлов:",
        file=sys.stderr,
    )
    for path, err in remove_errors[:5]:
        print(f"  {path}: {err}", file=sys.stderr)
else:
    print("Дубликаты удалены.")


# Подсчёт количества изображений после очистки
def count_images(root):
    """Возвращает словарь {класс: количество файлов}."""
    if not os.path.isdir(root):
        print(f"Папка '{root}' не найдена.", file=sys.stderr)
        return {}
    counts = {}
    for cls in os.listdir(root):
        folder = os.path.join(root, cls)
        if os.path.isdir(folder):
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            counts[cls] = len(files)
    return counts


print("\nКоличество изображений после удаления дубликатов:")
for subset in ["train", "val", "test"]:
    counts = count_images(subset)
    total = sum(counts.values())
    print(f"{subset}: всего {total} изображений")
    for cls, num in counts.items():
        print(f"  {cls}: {num}")
