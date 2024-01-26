# Web Scraping Pada Detik.com

Project ini merupakan aplikasi web scraping menggunakan Python. Project ini menggunakan Flask, Playwright, Beautifulsoup, dan Pandas.

## Tujuan

Tujuan dari project ini adalah untuk mempelajari cara melakukan web scraping menggunakan Python.

## Data

Data yang digunakan dalam project ini adalah data produk dari web https://www.detik.com/terpopuler/news.

## Output

Output dari project ini adalah data produk dalam bentuk CSV.

## Cara menggunakan

Untuk menggunakan project ini, ikuti langkah-langkah berikut:

1. Instal dependencies:
```python
pip install -r requirements.txt
```
2. Jalankan server:
```python
flask run
```
3. Buka browser dan akses URL berikut:
```python
http://127.0.0.1:5000
```
4. Klik button New untuk menambahkan artikel terbaru saat ini dari Detik.com.
5. Klik button Export untuk export artikel ke dalam bentuk csv.

## Kesimpulan

Project ini telah berhasil melakukan scraping data produk dari web https://www.detik.com/terpopuler/news. Data produk yang diperoleh disimpan dalam folder output dengan nama file data.csv.
