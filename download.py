import urllib.request

url = "https://commondatastorage.googleapis.com/books1000/notMNIST_small.tar.gz"
filename = "notMNIST_small.tar.gz"

print("Скачиваю файл...")
urllib.request.urlretrieve(url, filename)
print("Готово:", filename)