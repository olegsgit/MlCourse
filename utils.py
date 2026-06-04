"""Shared utilities for the notMNIST lab exercises."""

import hashlib
import os
import random
import shutil

import matplotlib.pyplot as plt
from PIL import Image


def list_classes(data_dir):
    """Return sorted list of class subdirectories (e.g. A-J) in *data_dir*."""
    return sorted(
        d for d in os.listdir(data_dir)
        if os.path.isdir(os.path.join(data_dir, d))
    )


def iter_image_files(data_dir, extensions=(".png",)):
    """Yield ``(full_path, class_name)`` for every image file in *data_dir*.

    Only regular files whose extension (case-insensitive) is in *extensions*
    are included.
    """
    for cls in list_classes(data_dir):
        folder = os.path.join(data_dir, cls)
        for fname in os.listdir(folder):
            if fname.lower().endswith(extensions):
                full_path = os.path.join(folder, fname)
                if os.path.isfile(full_path):
                    yield full_path, cls


def show_random_samples(data_dir, n=5):
    """Display *n* random images from *data_dir* using matplotlib."""
    classes = list_classes(data_dir)
    print("Классы:", classes)

    for _ in range(n):
        cls = random.choice(classes)
        folder = os.path.join(data_dir, cls)
        fname = random.choice(os.listdir(folder))
        img = Image.open(os.path.join(folder, fname))

        plt.imshow(img, cmap="gray")
        plt.title(f"Класс: {cls}")
        plt.axis("off")
        plt.show()


def count_images_per_class(data_dir, extensions=(".png", ".jpg")):
    """Return a dict ``{class_name: file_count}`` for *data_dir*."""
    counts = {}
    for cls in list_classes(data_dir):
        folder = os.path.join(data_dir, cls)
        counts[cls] = sum(
            1 for f in os.listdir(folder)
            if f.lower().endswith(extensions) and os.path.isfile(os.path.join(folder, f))
        )
    return counts


def print_class_counts(data_dir, extensions=(".png", ".jpg")):
    """Print per-class image counts for *data_dir*."""
    classes = list_classes(data_dir)
    print("Классы:", classes)
    for cls, count in count_images_per_class(data_dir, extensions).items():
        print(f"Класс {cls}: {count} изображений")


def create_split_dirs(subsets, classes):
    """Create ``subset/class`` directory trees for each subset."""
    for subset in subsets:
        os.makedirs(subset, exist_ok=True)
        for cls in classes:
            os.makedirs(os.path.join(subset, cls), exist_ok=True)


def copy_file_pairs(pairs, subset_dir, verbose=False):
    """Copy ``(source_path, class_name)`` pairs into *subset_dir/class_name/*.

    When *verbose* is True a progress line is printed every 1000 files.
    """
    copied = 0
    for src, cls in pairs:
        dst = os.path.join(subset_dir, cls, os.path.basename(src))
        shutil.copy(src, dst)
        copied += 1
        if verbose and copied % 1000 == 0:
            print(f"[{subset_dir}] скопировано {copied} файлов...")
    if verbose:
        print(f"[{subset_dir}] готово: {copied} файлов.")


def file_hash(path):
    """Return the MD5 hex-digest of the file at *path*."""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def collect_hashes(root):
    """Return a set of MD5 hashes for every file under *root/class/*."""
    hashes = set()
    for path, _ in iter_image_files(root, extensions=(".png", ".jpg", ".jpeg")):
        hashes.add(file_hash(path))
    return hashes


def find_duplicates(root, reference_hashes):
    """Return list of file paths in *root* whose hash is in *reference_hashes*."""
    duplicates = []
    for path, _ in iter_image_files(root, extensions=(".png", ".jpg", ".jpeg")):
        if file_hash(path) in reference_hashes:
            duplicates.append(path)
    return duplicates


def load_image_data(root):
    """Load images from *root/class/* as flattened grayscale numpy arrays.

    Returns ``(X, y)`` where X is a 2-D array of shape ``(n_samples, n_pixels)``
    and y is a 1-D array of class-name strings.
    """
    import numpy as np

    x, y = [], []
    for path, cls in iter_image_files(root, extensions=(".png", ".jpg", ".jpeg")):
        try:
            img = Image.open(path).convert("L")
            x.append(np.array(img).flatten())
            y.append(cls)
        except Exception:
            pass
    return np.array(x), np.array(y)
