import os
import hashlib

# Функция для подсчёта хэша файла 
# Если два файла одинаковые, их хэши совпадут
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# Функция для сбора хэшей из папки выборки 
def collect_hashes(root):
    hashes = set()
    for cls in os.listdir(root):                  # идём по классам (A–J)
        folder = os.path.join(root, cls)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):          # идём по файлам
            path = os.path.join(folder, fname)
            if os.path.isfile(path):
                hashes.add(file_hash(path))       # добавляем хэш файла
    return hashes

# Считаем хэши для train 
train_hashes = collect_hashes("train")

# Проверяем val и test на пересечения с train 
def find_duplicates(root, reference_hashes):
    duplicates = []
    for cls in os.listdir(root):
        folder = os.path.join(root, cls)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            if os.path.isfile(path):
                if file_hash(path) in reference_hashes:
                    duplicates.append(path)       # нашли дубликат
    return duplicates

val_duplicates = find_duplicates("val", train_hashes)
test_duplicates = find_duplicates("test", train_hashes)

print(f"Дубликаты в val: {len(val_duplicates)}")
print(f"Дубликаты в test: {len(test_duplicates)}")

# удаляем дубликаты 
for path in val_duplicates + test_duplicates:
     os.remove(path)
print("Дубликаты удалены.")

# Подсчёт количества изображений после очистки 
def count_images(root):
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



