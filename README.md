# 🛰️ JurnalFinder v1.0 (Beta)

**JurnalFinder** merupakan tools sederhana untuk mencari jurnal akademik.  
Tentunya masih versi **beta** atau **dalam tahap pengembangan**, jadi jangan kaget kalau ada bug kecil yang bikin kamu ngelus dada.

---

## 🧩 Fitur Utama

- 🔍 **Pencarian Jurnal Nasional (GARUDA / SINTA ≥ 3)**  
  Mengambil data langsung dari [garuda.kemdikbud.go.id](https://garuda.kemdikbud.go.id) berdasarkan judul dan bidang studi yang kamu masukkan.

- 🌐 **Pencarian Jurnal Internasional (Semantic Scholar & Crossref)**  
  Menggunakan API publik untuk menampilkan hasil jurnal luar negeri lengkap dengan tahun, penulis, dan DOI (jika tersedia).

- 📥 **Fitur Download Otomatis (PDF)**  
  Jika file PDF tersedia langsung, tool akan mengunduhnya ke folder default:
  - Android → `/storage/emulated/0/Download/`
  - Linux/Windows → `~/Downloads`

- 📝 **Fallback Referensi Otomatis**  
  Jika file tidak dapat diunduh, tautan sumber jurnal tetap disimpan dalam `referensi_jurnal.txt`.

- 💬 **UI Terminal Interaktif (questionary + rich)**  
  Input dan tampilan dibuat interaktif

---

## ⚙️ Persiapan & Instalasi

Pastikan kamu sudah punya **Python 3.9+** dan `pip`.  
Kemudian install semua dependensi berikut:

```
pip install requests rich questionary beautifulsoup4
git clone https://github.com/beruu27/JurnalFinder.git
cd JurnalFinder
python main.py
```


## 🔧 Catatan Teknis

Untuk jurnal nasional, data diambil langsung dari endpoint JSON GARUDA.
Untuk jurnal internasional, tool menggunakan dua API publik:
Semantic Scholar Graph API dan
Crossref REST API

## 🧠 Rencana Pengembangan (Next Update)
Integrasi SerpAPI / Google Scholar untuk hasil lebih luas

Filter tambahan berdasarkan publisher atau keyword

Dukungan pencarian multi-bidang sekaligus
