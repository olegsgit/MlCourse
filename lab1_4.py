import os

from utils import collect_hashes, count_images_per_class, find_duplicates

# Считаем хэши для train
train_hashes = collect_hashes("train")

# Проверяем val и test на пересечения с train
val_duplicates = find_duplicates("val", train_hashes)
test_duplicates = find_duplicates("test", train_hashes)

print(f"Дубликаты в val: {len(val_duplicates)}")
print(f"Дубликаты в test: {len(test_duplicates)}")

# Удаляем дубликаты
for path in val_duplicates + test_duplicates:
    os.remove(path)
print("Дубликаты удалены.")

# Подсчёт количества изображений после очистки
print("\nКоличество изображений после удаления дубликатов:")
for subset in ["train", "val", "test"]:
    counts = count_images_per_class(subset)
    total = sum(counts.values())
    print(f"{subset}: всего {total} изображений")
    for cls, num in counts.items():
        print(f"  {cls}: {num}")
