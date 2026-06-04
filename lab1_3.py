import random

from utils import (
    copy_file_pairs,
    create_split_dirs,
    iter_image_files,
    list_classes,
)

DATA_LARGE = "notMNIST_large"
DATA_SMALL = "notMNIST_small"

classes = list_classes(DATA_LARGE)
print("Классы:", classes)

create_split_dirs(["train", "val", "test"], classes)

# Собираем все изображения из большого набора
all_files = list(iter_image_files(DATA_LARGE))
print(f"Всего изображений в large: {len(all_files)}")

random.shuffle(all_files)

train_files = all_files[:200000]
val_files = all_files[200000:210000]

# Собираем test из small
test_files = list(iter_image_files(DATA_SMALL))

print(f"Train={len(train_files)}, Val={len(val_files)}, Test={len(test_files)}")

copy_file_pairs(train_files, "train")
copy_file_pairs(val_files, "val")
copy_file_pairs(test_files, "test")

print("Разделение завершено.")
