import hashlib
import sys
import urllib.request

url = "https://commondatastorage.googleapis.com/books1000/notMNIST_small.tar.gz"
filename = "notMNIST_small.tar.gz"

# Expected SHA-256 checksum for integrity verification
EXPECTED_SHA256 = None  # Set after first verified download, e.g. "abcdef1234..."

print("Скачиваю файл...")
urllib.request.urlretrieve(url, filename)

# Verify file integrity after download
sha256 = hashlib.sha256()
with open(filename, "rb") as f:
    for chunk in iter(lambda: f.read(8192), b""):
        sha256.update(chunk)
actual_hash = sha256.hexdigest()

if EXPECTED_SHA256 is not None and actual_hash != EXPECTED_SHA256:
    print(f"ОШИБКА: контрольная сумма не совпадает!")
    print(f"  Ожидалось: {EXPECTED_SHA256}")
    print(f"  Получено:  {actual_hash}")
    sys.exit(1)

print(f"Готово: {filename} (SHA-256: {actual_hash})")