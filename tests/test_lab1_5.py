"""Unit tests for lab1_5.py — image loading utility for ML classification."""

import os
import sys

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import extract_functions

MODULE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lab1_5.py"
)

_ns = extract_functions(MODULE_PATH)
load_data = _ns["load_data"]


@pytest.fixture
def image_dataset(tmp_path):
    """Create a small synthetic image dataset (28x28 grayscale PNGs)."""
    classes = ["A", "B", "C"]
    images_per_class = 4

    for cls in classes:
        cls_dir = tmp_path / cls
        cls_dir.mkdir()
        for i in range(images_per_class):
            img = Image.fromarray(
                np.random.randint(0, 255, (28, 28), dtype=np.uint8), mode="L"
            )
            img.save(str(cls_dir / f"img_{i}.png"))

    return str(tmp_path), classes, images_per_class


class TestLoadData:
    def test_returns_correct_number_of_samples(self, image_dataset):
        root, classes, per_class = image_dataset
        x, y = load_data(root)
        expected_total = len(classes) * per_class
        assert len(x) == expected_total
        assert len(y) == expected_total

    def test_returns_numpy_arrays(self, image_dataset):
        root, _, _ = image_dataset
        x, y = load_data(root)
        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)

    def test_flattened_image_shape(self, image_dataset):
        root, _, _ = image_dataset
        x, y = load_data(root)
        # 28×28 images flattened to 784-element vectors
        assert x.shape[1] == 784

    def test_labels_match_class_names(self, image_dataset):
        root, classes, _ = image_dataset
        x, y = load_data(root)
        unique_labels = set(y)
        assert unique_labels == set(classes)

    def test_pixel_values_in_valid_range(self, image_dataset):
        root, _, _ = image_dataset
        x, y = load_data(root)
        assert x.min() >= 0
        assert x.max() <= 255

    def test_handles_corrupt_files_gracefully(self, tmp_path):
        cls_dir = tmp_path / "A"
        cls_dir.mkdir()
        img = Image.fromarray(np.zeros((28, 28), dtype=np.uint8), mode="L")
        img.save(str(cls_dir / "valid.png"))
        (cls_dir / "corrupt.png").write_bytes(b"not an image at all")

        x, y = load_data(str(tmp_path))
        assert len(x) == 1
        assert y[0] == "A"

    def test_empty_class_directory(self, tmp_path):
        (tmp_path / "A").mkdir()
        x, y = load_data(str(tmp_path))
        assert len(x) == 0
        assert len(y) == 0

    def test_skips_non_directory_entries(self, tmp_path):
        cls_dir = tmp_path / "A"
        cls_dir.mkdir()
        img = Image.fromarray(np.zeros((28, 28), dtype=np.uint8), mode="L")
        img.save(str(cls_dir / "valid.png"))
        # Create a file at root level (not a class dir)
        (tmp_path / "readme.txt").write_text("info")

        x, y = load_data(str(tmp_path))
        # Should only load from the "A" subdirectory
        assert len(x) >= 1

    def test_single_class_single_image(self, tmp_path):
        cls_dir = tmp_path / "Z"
        cls_dir.mkdir()
        img = Image.fromarray(
            np.ones((28, 28), dtype=np.uint8) * 128, mode="L"
        )
        img.save(str(cls_dir / "solo.png"))

        x, y = load_data(str(tmp_path))
        assert len(x) == 1
        assert y[0] == "Z"
        assert x[0].shape == (784,)
