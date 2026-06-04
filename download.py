import sys
import urllib.request
import urllib.error

url = "https://commondatastorage.googleapis.com/books1000/notMNIST_small.tar.gz"
filename = "notMNIST_small.tar.gz"

print("Скачиваю файл...")
try:
    urllib.request.urlretrieve(url, filename)
except urllib.error.URLError as e:
    print(f"Ошибка сети при скачивании: {e}", file=sys.stderr)
    sys.exit(1)
except OSError as e:
    print(f"Ошибка записи файла: {e}", file=sys.stderr)
    sys.exit(1)
print("Готово:", filename)
