"""Unit tests for lab1_4.py — duplicate detection and image counting utilities."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import extract_functions

MODULE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lab1_4.py"
)

_ns = extract_functions(MODULE_PATH)
file_hash = _ns["file_hash"]
collect_hashes = _ns["collect_hashes"]
find_duplicates = _ns["find_duplicates"]
count_images = _ns["count_images"]


@pytest.fixture
def sample_tree(tmp_path):
    """Create a temporary directory tree simulating train/val/test splits."""
    for subset in ("train", "val", "test"):
        for cls in ("A", "B"):
            (tmp_path / subset / cls).mkdir(parents=True)

    # Populate train with unique files
    (tmp_path / "train" / "A" / "img1.png").write_bytes(b"content_a1")
    (tmp_path / "train" / "A" / "img2.png").write_bytes(b"content_a2")
    (tmp_path / "train" / "B" / "img3.png").write_bytes(b"content_b1")

    # val — img4 is a duplicate of train/A/img1 (same content)
    (tmp_path / "val" / "A" / "img4.png").write_bytes(b"content_a1")
    (tmp_path / "val" / "B" / "img5.png").write_bytes(b"unique_val")

    # test — img6 is a duplicate of train/B/img3
    (tmp_path / "test" / "A" / "img6.png").write_bytes(b"content_b1")
    (tmp_path / "test" / "B" / "img7.png").write_bytes(b"unique_test")

    return tmp_path


class TestFileHash:
    def test_same_content_same_hash(self, tmp_path):
        f1 = tmp_path / "a.bin"
        f2 = tmp_path / "b.bin"
        f1.write_bytes(b"hello world")
        f2.write_bytes(b"hello world")
        assert file_hash(str(f1)) == file_hash(str(f2))

    def test_different_content_different_hash(self, tmp_path):
        f1 = tmp_path / "a.bin"
        f2 = tmp_path / "b.bin"
        f1.write_bytes(b"hello")
        f2.write_bytes(b"world")
        assert file_hash(str(f1)) != file_hash(str(f2))

    def test_returns_32_char_hex_string(self, tmp_path):
        f = tmp_path / "x.bin"
        f.write_bytes(b"data")
        result = file_hash(str(f))
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 hex digest length

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.bin"
        f.write_bytes(b"")
        result = file_hash(str(f))
        assert isinstance(result, str)
        assert len(result) == 32

    def test_deterministic(self, tmp_path):
        f = tmp_path / "det.bin"
        f.write_bytes(b"deterministic content")
        assert file_hash(str(f)) == file_hash(str(f))


class TestCollectHashes:
    def test_collects_all_file_hashes(self, sample_tree):
        hashes = collect_hashes(str(sample_tree / "train"))
        assert len(hashes) == 3

    def test_returns_set(self, sample_tree):
        hashes = collect_hashes(str(sample_tree / "train"))
        assert isinstance(hashes, set)

    def test_empty_class_directories(self, tmp_path):
        root = tmp_path / "empty"
        (root / "A").mkdir(parents=True)
        hashes = collect_hashes(str(root))
        assert hashes == set()

    def test_ignores_non_directory_entries(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (root / "stray_file.txt").write_text("not a class dir")
        cls_dir = root / "A"
        cls_dir.mkdir()
        (cls_dir / "img.png").write_bytes(b"data")
        hashes = collect_hashes(str(root))
        assert len(hashes) == 1

    def test_deduplicates_identical_files(self, tmp_path):
        root = tmp_path / "dedup"
        cls_dir = root / "A"
        cls_dir.mkdir(parents=True)
        (cls_dir / "f1.png").write_bytes(b"same")
        (cls_dir / "f2.png").write_bytes(b"same")
        hashes = collect_hashes(str(root))
        assert len(hashes) == 1  # same content → same hash


class TestFindDuplicates:
    def test_finds_duplicates_in_val(self, sample_tree):
        train_hashes = collect_hashes(str(sample_tree / "train"))
        duplicates = find_duplicates(str(sample_tree / "val"), train_hashes)
        assert len(duplicates) == 1
        assert "img4.png" in duplicates[0]

    def test_finds_duplicates_in_test(self, sample_tree):
        train_hashes = collect_hashes(str(sample_tree / "train"))
        duplicates = find_duplicates(str(sample_tree / "test"), train_hashes)
        assert len(duplicates) == 1
        assert "img6.png" in duplicates[0]

    def test_no_duplicates_when_all_unique(self, tmp_path):
        ref_dir = tmp_path / "ref" / "A"
        ref_dir.mkdir(parents=True)
        (ref_dir / "r1.png").write_bytes(b"ref_only")
        ref_hashes = collect_hashes(str(tmp_path / "ref"))

        check_dir = tmp_path / "check" / "A"
        check_dir.mkdir(parents=True)
        (check_dir / "c1.png").write_bytes(b"unique_content")

        duplicates = find_duplicates(str(tmp_path / "check"), ref_hashes)
        assert duplicates == []

    def test_empty_reference_set(self, sample_tree):
        duplicates = find_duplicates(str(sample_tree / "val"), set())
        assert duplicates == []

    def test_returns_full_paths(self, sample_tree):
        train_hashes = collect_hashes(str(sample_tree / "train"))
        duplicates = find_duplicates(str(sample_tree / "val"), train_hashes)
        for dup in duplicates:
            assert os.path.isabs(dup) or os.path.exists(dup)


class TestCountImages:
    def test_counts_files_correctly(self, sample_tree):
        counts = count_images(str(sample_tree / "train"))
        assert counts["A"] == 2
        assert counts["B"] == 1

    def test_returns_dict(self, sample_tree):
        counts = count_images(str(sample_tree / "train"))
        assert isinstance(counts, dict)

    def test_empty_classes(self, tmp_path):
        root = tmp_path / "empty_classes"
        (root / "A").mkdir(parents=True)
        (root / "B").mkdir(parents=True)
        counts = count_images(str(root))
        assert counts["A"] == 0
        assert counts["B"] == 0

    def test_ignores_subdirectories_in_class_folder(self, tmp_path):
        root = tmp_path / "mixed"
        cls_a = root / "A"
        cls_a.mkdir(parents=True)
        (cls_a / "img.png").write_bytes(b"data")
        (cls_a / "subdir").mkdir()
        counts = count_images(str(root))
        assert counts["A"] == 1

    def test_multiple_classes(self, tmp_path):
        root = tmp_path / "multi"
        for cls in ("A", "B", "C"):
            d = root / cls
            d.mkdir(parents=True)
            for i in range(cls == "A" and 3 or cls == "B" and 2 or 1):
                (d / f"f{i}.png").write_bytes(f"c{i}".encode())
        counts = count_images(str(root))
        assert counts["A"] == 3
        assert counts["B"] == 2
        assert counts["C"] == 1
