import random

from utils import (
    copy_file_pairs,
    create_split_dirs,
    iter_image_files,
    list_classes,
)

DATA_DIR = "notMNIST_small"

classes = list_classes(DATA_DIR)
print("Классы:", classes)

create_split_dirs(["train", "val", "test"], classes)

# Собираем все изображения
all_files = list(iter_image_files(DATA_DIR))
print(f"Всего найдено изображений: {len(all_files)}")

random.shuffle(all_files)

# Делим: 80% train, 10% val, 10% test
n = len(all_files)
n_train = int(n * 0.8)
n_val = int(n * 0.1)

train_files = all_files[:n_train]
val_files = all_files[n_train:n_train + n_val]
test_files = all_files[n_train + n_val:]

print(f"План разделения: train={len(train_files)}, val={len(val_files)}, test={len(test_files)}")

copy_file_pairs(train_files, "train", verbose=True)
copy_file_pairs(val_files, "val", verbose=True)
copy_file_pairs(test_files, "test", verbose=True)

print("Разделение завершено.")
