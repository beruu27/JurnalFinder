import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, urljoin

# untuk menyimpan hasil donlot sesuaian aja yee mau disimpan di path mana
if "ANDROID_STORAGE" in os.environ:
    DOWNLOAD_DIR = "/storage/emulated/0/Download/"
else:
    DOWNLOAD_DIR = os.path.join(Path.home(), "Downloads")
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/91.0 Safari/537.36"
}

def is_direct_pdf(url):
    return ".pdf" in url.lower()

def download_file(url, filename):
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("application/pdf"):
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"[✗] Error download file: {e}")
    return False

def find_pdf_link_in_page(page_url):
    try:
        response = requests.get(page_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if ".pdf" in href.lower():
                return urljoin(page_url, href)
    except Exception as e:
        print(f"[✗] Gagal parsing halaman: {e}")
    return None

def unduh_jurnal_pdf(jurnal_list, format_file="PDF"):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    saved_count = 0
    referensi_file = os.path.join(DOWNLOAD_DIR, "referensi_jurnal.txt")

    with open(referensi_file, "w") as ref_file:
        for i, jurnal in enumerate(jurnal_list, 1):
            url = jurnal.get("link", "").strip()
            judul = jurnal.get("judul", f"Jurnal_{i}")

            if not url:
                continue

            print(f"\n[🔍] Memproses: {judul}")

            # ni fungsi donlot file pdf
            if is_direct_pdf(url):
                filename = os.path.basename(urlparse(url).path)
                if not filename.endswith(".pdf"):
                    filename += ".pdf"
                filepath = os.path.join(DOWNLOAD_DIR, filename)

                if download_file(url, filepath):
                    saved_count += 1
                    print(f"[✓] Berhasil download langsung: {filename}")
                    continue

            # kalo bukan langsung pdf, cari link pdf di halaman
            print(f"[🕵️] Mencoba cari PDF di halaman...")
            found_pdf = find_pdf_link_in_page(url)
            if found_pdf:
                filename = os.path.basename(urlparse(found_pdf).path)
                if not filename.endswith(".pdf"):
                    filename = f"jurnal_{i}.pdf"
                filepath = os.path.join(DOWNLOAD_DIR, filename)

                if download_file(found_pdf, filepath):
                    saved_count += 1
                    print(f"[✓] PDF ditemukan & berhasil diunduh: {filename}")
                    continue
                else:
                    print(f"[✗] Gagal mengunduh PDF yang ditemukan.")

            # fallback ke referensi
            print(f"[→] Disimpan sebagai referensi.")
            ref_file.write(f"[{i}] {judul}\n{url}\n\n")

    print(f"\n[📁] {saved_count} file PDF berhasil disimpan ke {DOWNLOAD_DIR}")
    print(f"[📝] Sisanya dicatat di: referensi_jurnal.txt")

