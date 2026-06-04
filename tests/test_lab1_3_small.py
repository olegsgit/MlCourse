"""Unit tests for lab1_3_small.py — dataset splitting with progress reporting."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import extract_functions

MODULE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lab1_3_small.py"
)

_ns = extract_functions(MODULE_PATH)
copy_pairs = _ns["copy_pairs"]


@pytest.fixture
def source_files(tmp_path):
    """Create source image files and return (pairs_list, tmp_path)."""
    src_dir = tmp_path / "source"
    src_dir.mkdir()

    files = []
    for cls in ("A", "B"):
        cls_dir = src_dir / cls
        cls_dir.mkdir()
        for i in range(5):
            f = cls_dir / f"img_{cls}_{i}.png"
            f.write_bytes(f"data_{cls}_{i}".encode())
            files.append((str(f), cls))

    return files, tmp_path


class TestCopyPairsSmall:
    def test_copies_all_files(self, source_files):
        pairs, tmp_path = source_files
        dest = str(tmp_path / "output")
        for cls in ("A", "B"):
            os.makedirs(os.path.join(dest, cls), exist_ok=True)

        copy_pairs(pairs, dest)

        total_copied = 0
        for cls in ("A", "B"):
            total_copied += len(os.listdir(os.path.join(dest, cls)))
        assert total_copied == 10

    def test_preserves_file_content(self, source_files):
        pairs, tmp_path = source_files
        dest = str(tmp_path / "output")
        for cls in ("A", "B"):
            os.makedirs(os.path.join(dest, cls), exist_ok=True)

        copy_pairs(pairs, dest)

        for src_path, cls in pairs:
            dst_path = os.path.join(dest, cls, os.path.basename(src_path))
            with open(src_path, "rb") as sf:
                src_data = sf.read()
            with open(dst_path, "rb") as df:
                dst_data = df.read()
            assert src_data == dst_data

    def test_empty_list(self, tmp_path):
        dest = str(tmp_path / "output")
        os.makedirs(os.path.join(dest, "A"), exist_ok=True)
        copy_pairs([], dest)
        assert os.listdir(os.path.join(dest, "A")) == []

    def test_correct_class_placement(self, source_files):
        pairs, tmp_path = source_files
        dest = str(tmp_path / "output")
        for cls in ("A", "B"):
            os.makedirs(os.path.join(dest, cls), exist_ok=True)

        copy_pairs(pairs, dest)

        for cls in ("A", "B"):
            cls_dir = os.path.join(dest, cls)
            files = os.listdir(cls_dir)
            assert len(files) == 5
            for f in files:
                assert f"_{cls}_" in f

    def test_single_pair(self, tmp_path):
        src = tmp_path / "src" / "X"
        src.mkdir(parents=True)
        f = src / "one.png"
        f.write_bytes(b"single")

        dest = str(tmp_path / "out")
        os.makedirs(os.path.join(dest, "X"), exist_ok=True)

        copy_pairs([(str(f), "X")], dest)

        out_files = os.listdir(os.path.join(dest, "X"))
        assert out_files == ["one.png"]
